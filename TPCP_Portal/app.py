import sys, os
import global_items as gi


import api_methods
import client

from flask import Flask, render_template, flash, request, redirect
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Centralized URL Map
app.add_url_rule('/api/methods/get_counter', methods=['GET'], view_func=api_methods.get_counter)
app.add_url_rule('/api/methods/gtirb_run_transform', methods=['GET'], view_func=api_methods.gtirb_run_transform_set)

# Check that the upload folder exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)



@app.route('/upload_gtirb')
def upload():
    if request.method != 'GET':
        return render_template("gtirb_upload.html",
                           current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                           current_tasks=gi.current_tasks)
    global counter
    gi.counter +=1
    #TODO: Post terminal updates to the template
    return render_template("gtirb_upload.html", counter=gi.counter,
                           current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                           current_tasks=gi.current_tasks)

@app.route('/upload_gtirb', methods=['POST', 'GET'])
def modify_or_upload_files():
    global current_tasks
    print(gi.current_tasks)
    counter = 0
    if request.method != 'POST':
        print("In not post")
        return render_template("gtirb_upload.html",
                               current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                               current_tasks=gi.current_tasks)

    if request.form['HiddenField'] == 'ModifyFile':
        id = request.form['ID']
        filename = request.form['FileName']
        filetype = request.form['FileType'] if request.form['FileType'] != 'No Change' else get_task_map_id_file_info(id, filename, "filetype")
        transform = request.form['Transform'] if request.form['Transform'] != 'No Change' else get_task_map_id_file_info(id, filename, "transform")
        included = True if request.form['Included'] == "True" else False
        job_status = "Must Pipe Output"
        # status = ""
        print(f"id: {id}")
        print(f"filename: {filename}")
        print(f"filetype: {filetype}")
        print(f"transform: {transform}")
        print(f"included: {included}")

        add_to_task_map(id, filename, transform, filetype, included)
        update_job_info(id, transform, job_status)
        print(f"[INFO] Task Map: {gi.current_tasks}", flush=True)
        return render_template("gtirb_upload.html",
                               current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                               current_tasks=gi.current_tasks)
    elif request.form['HiddenField'] == 'UploadFile':
        try:
            current_series_ids = sorted(os.listdir(app.config['UPLOAD_FOLDER']))
        except:
            os.mkdir(app.config['UPLOAD_FOLDER'])
            current_series_ids = sorted(os.listdir(app.config['UPLOAD_FOLDER']))

        if request.form['JobID'] == "New Job" and len(current_series_ids) > 0:
            id = str(int(current_series_ids[-1]) + 1)
        else:
            id = "1"

        upload_space = os.path.join(app.config['UPLOAD_FOLDER'], id)
        if not os.path.isdir(upload_space):
            os.mkdir(upload_space)


        if 'files[]' not in request.files:
            flash('No files found, try again.')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                print(filename)
                file.save(os.path.join(upload_space, filename))
                transform = "Not Specified"
                filetype, included = "Not Specified", False
                # TODO: Define Logic to Make JobInfo Included List
                add_to_task_map(id, filename, transform, filetype, included)
        return render_template("gtirb_upload.html", id=id,
                       current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                       current_tasks=gi.current_tasks)

    elif request.form['HiddenField'] == 'RunJob':
        print("runjob", flush=True)
        status, message, original_bin, transformed_bin, transformed_bin_type = api_methods.gtirb_run_transform_set("1")
        update_job_info("1", transform=gi.current_tasks["1"]["JobInfo"]["transform"], status=gi.current_tasks["1"]["JobInfo"]["status"])
        print(f"current tasks {gi.current_tasks}", flush=True)
        if status != "200":

            return render_template("gtirb_upload.html",
                                   current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                                   current_tasks=gi.current_tasks)
        # Status == "200" and can assume this is true
        add_to_task_map("1", transformed_bin, "Not Specified", transformed_bin_type, included=False)
        if transformed_bin_type == "dynamic binary" or transformed_bin_type == "static binary":
            client.send_data_to_GSA_server("1", original_bin, transformed_bin)

        return render_template("gtirb_upload.html",
                               current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                               current_tasks=gi.current_tasks)

@app.route('/upload_chisel', methods=['POST', 'GET'])
def upload_chisel():
    return render_template("chisel_upload.html",
                           current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                           current_tasks=gi.current_tasks)


def update_job_info(id, job_transform, job_status):
    try:
        if job_transform != "No Change":
            gi.current_tasks[id]["JobInfo"]["transform"] = job_transform
        if job_status != "None To Report":
            gi.current_tasks[id]["JobInfo"]["status"] = job_status
    except KeyError as e:
        print(e)


def add_to_task_map(id, filename, transform, filetype, included):
    # Task Map Structure is as follows
    # { id:{filename: [filetype, transform, status], "JobInfo": [transform, status]}, ...,
    #   id+n:{filename: [filetype, transform, status], "JobInfo": [transform, status]} }
    try:
        gi.current_tasks[id][filename] = {"filetype": filetype, "transform": transform, "included": included}

    except KeyError:
        gi.current_tasks[id] = {filename: {"filetype": filetype, "transform": transform, "included": included},
                                "JobInfo": {"transform": transform, "status": "None To Report"}}

def update_job_info(id, transform="", status="", included=""):
    # Update transform
    if transform != "":
        gi.current_tasks[id]["JobInfo"]["transform"] = transform

    if included != "":
        gi.current_tasks[id]["JobInfo"]["included"] = included
    # Update Status
    if status == "":
        return
    if status == "None To Report":
        gi.current_tasks[id]["JobInfo"]["status"] = status
    else:
        gi.current_tasks[id]["JobInfo"]["status"] += status


def get_task_map_id(id):
    return gi.current_tasks[id]

def get_task_map_id_file_info(id, filename, index):
    return gi.current_tasks[id][filename][index]

if __name__ == "__main__":
    print('to upload files navigate to http://10.0.2.15:5000/upload_gtirb')
    app.run(host='10.0.2.15', port=5000, debug=True, threaded=True)