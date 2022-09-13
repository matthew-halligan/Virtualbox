import sys, os, shutil, datetime
import global_items as gi
import json


import api_methods
import client

from flask import Flask, render_template, flash, request, redirect, send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Centralized URL Map
app.add_url_rule('/api/methods/get_counter', methods=['GET'], view_func=api_methods.get_counter)
app.add_url_rule('/api/methods/gtirb_run_transform', methods=['GET'], view_func=api_methods.gtirb_run_transform_set)
app.add_url_rule('/api/methods/logger', methods=['GET'], view_func=api_methods.logger)

# Check that the upload folder exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

@app.route('/logs')
def logger_render():
    # gi.docker_logs = api_methods.logger()
    return render_template("logs.html", piped_logs=gi.docker_logs)

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
    # print(gi.current_tasks)
    counter = 0
    if request.method != 'POST':
        # print("In not post")
        return render_template("gtirb_upload.html",
                               current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                               current_tasks=gi.current_tasks)

    if request.form['HiddenField'] == 'ModifyFile':

        id = request.form['ID']
        filename = request.form['FileName']
        try:
            filetype = request.form['FileType'] if request.form['FileType'] != 'No Change' else get_task_map_id_file_info(id, filename, "filetype")
        except:
            filetype = get_task_map_id_file_info(id, filename, "filetype")
            print(f"[Info] 'FileType' field not detected.  Setting to what is stored in the task map: {filetype}", flush=True)
        try:
            included = True if request.form['Included'] == "True" else False
        except:
            included=False
            print("[INFO] 'Included' field not detected. Setting to False by default.", flush=True)

        dependency_libs = ""

        if filetype[-6:] == "binary":
            dependency_libs = api_methods.get_bin_ldd(id, filename)
        elif filetype in ["Log", "Directory"]:
            r_filename, destination = make_archive(id, filename)
            return send_from_directory(directory=destination, path=r_filename)
        add_to_task_map(id, filename, filetype, included, dependency_libs=dependency_libs)

        modify_job_included(id, filename, included)
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
                file.save(os.path.join(upload_space, filename))
                included = True
                filetype = "library"
                add_to_task_map(id, filename, filetype, included)
                modify_job_included(id, filename, included)

                # TODO: Define Logic to Make JobInfo Included List

        return render_template("gtirb_upload.html", id=id,
                       current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                       current_tasks=gi.current_tasks)

    elif request.form['HiddenField'] == 'RunJob':
        id = request.form['JobID']
        transform = request.form['JobTransform']
        job_status = api_methods.logger()
        metrics_collection = request.form['JobMetrics']
        update_job_info(id, transform, job_status, metrics_collection)

        status, message, original_bin, transformed_bin, transformed_bin_type = api_methods.gtirb_run_transform_set(id)
        update_job_info(id, transform=gi.current_tasks[id]["JobInfo"]["transform"], status=gi.current_tasks[id]["JobInfo"]["status"])
        if status != "200":
            path = os.path.join(app.config["UPLOAD_FOLDER"], id)
            if os.path.exists(os.path.join(path, "ErrorLog.txt")):
                add_to_task_map(id, "ErrorLog.txt", "Log", False)
            return render_template("gtirb_upload.html",
                                   current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                                   current_tasks=gi.current_tasks)
        # Status == "200" and can assume this is true
        add_to_task_map(id, transformed_bin, transformed_bin_type, included=False)
        if transformed_bin_type == "dynamic binary" or transformed_bin_type == "static binary":
            client.send_data_to_GSA_server(id, original_bin, transformed_bin, metrics_collection)
            metrics_dir = f"gsa-metrics-{metrics_collection}-{transformed_bin}"
            add_to_task_map(id, metrics_dir, "Directory", False)
            # TODO: Modify client to collect the name of the stats output dir and add to task map
        return render_template("gtirb_upload.html",
                               current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                               current_tasks=gi.current_tasks)
    elif request.form['HiddenField'] == 'DownloadJob':
        id = request.form['JobID']
        filename, destination = make_archive(id)
        return send_from_directory(directory=destination, path=filename)

@app.route('/upload_chisel', methods=['POST', 'GET'])
def upload_chisel():
    global current_tasks
    # print(gi.current_tasks)
    counter = 0
    if request.method != 'POST':
        # print("In not post")
        return render_template("chisel_upload.html",
                               current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                               current_tasks=gi.current_tasks)

    if request.form['HiddenField'] == 'ModifyFile':
        id = request.form['ID']
        filename = request.form['FileName']
        filetype = request.form['FileType'] if request.form['FileType'] != 'No Change' else get_task_map_id_file_info(
            id, filename, "filetype")
        included = True if request.form['Included'] == "True" else False

        # status = ""
        # print(f"id: {id}")
        # print(f"filename: {filename}")
        # print(f"filetype: {filetype}")
        # print(f"transform: {transform}")
        # print(f"included: {included}")

        add_to_task_map(id, filename, filetype, included)

        modify_job_included(id, filename, included)
        print(f"[INFO] Task Map: {gi.current_tasks}", flush=True)
        return render_template("chisel_upload.html",
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
                file.save(os.path.join(upload_space, filename))
                transform = "Not Specified"
                filetype, included = "Not Specified", False
                # TODO: Define Logic to Make JobInfo Included List
                add_to_task_map(id, filename, filetype, included)
        return render_template("chisel_upload.html", id=id,
                               current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                               current_tasks=gi.current_tasks)

    elif request.form['HiddenField'] == 'RunJob':
        id = request.form['JobID']
        transform = request.form['JobTransform']
        job_status = "Must Pipe Output"
        metrics_collection = request.form['JobMetrics']
        update_job_info(id, transform, job_status, metrics_collection)

        status, message, original_bin, transformed_bin, transformed_bin_type = api_methods.gtirb_run_transform_set(id)
        update_job_info(id, transform=gi.current_tasks[id]["JobInfo"]["transform"],
                        status=gi.current_tasks[id]["JobInfo"]["status"])
        if status != "200":
            path = os.path.join(app.config["UPLOAD_FOLDER"], id)
            if os.path.exists(os.path.join(path, "ErrorLog.txt")):
                add_to_task_map(id, "ErrorLog.txt", "Log (Do Not Include)", False)
            return render_template("chisel_upload.html",
                                   current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                                   current_tasks=gi.current_tasks)
        # Status == "200" and can assume this is true
        add_to_task_map(id, transformed_bin, transformed_bin_type, included=False)
        if transformed_bin_type == "dynamic binary" or transformed_bin_type == "static binary":
            client.send_data_to_GSA_server(id, original_bin, transformed_bin, metrics_collection)
            metrics_dir = f"{transformed_bin}-gsa-metrics"
            add_to_task_map(id, metrics_dir, "directory (do not include)", False)
            # TODO: Modify client to collect the name of the stats output dir and add to task map
        return render_template("chisel_upload.html",
                               current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                               current_tasks=gi.current_tasks)
    elif request.form['HiddenField'] == 'DownloadJob':
        id = request.form['JobID']
        filename, destination = make_archive(id)
        return send_from_directory(directory=destination, path=filename)


def update_job_info(id, job_transform, job_status):
    try:
        if job_transform != "No Change":
            gi.current_tasks[id]["JobInfo"]["transform"] = job_transform
        if job_status != "None To Report":
            gi.current_tasks[id]["JobInfo"]["status"] = job_status
    except KeyError as e:
        print(e)


def add_to_task_map(id, filename, filetype, included, metrics="", dependency_libs=""):
    # Task Map Structure is as follows
    # { id:{filename: [filetype, transform, status], "JobInfo": [transform, status]}, ...,
    #   id+n:{filename: [filetype, transform, status], "JobInfo": [transform, status]} }
    try:
        print(f"[INFO] Dynamic Dependencies Received: {type(dependency_libs)}")
        gi.current_tasks[id][filename] = {"filetype": filetype, "included": included,
                                          "dependency_libs": dependency_libs}

    except KeyError:
        gi.current_tasks[id] = {filename: {"filetype": filetype, "included": included, "dependency_libs": dependency_libs},
                                "JobInfo": {"transform": "", "status": "None To Report", "included": [], "metrics": metrics}}


def update_job_info(id, transform="", status="", included="", metrics_collection=""):
    # Update transform
    if transform != "":
        gi.current_tasks[id]["JobInfo"]["transform"] = transform

    # if included != "":
    #     gi.current_tasks[id]["JobInfo"]["included"] = included
    # Update Status
    if status == "":
        return
    if status == "None To Report":
        gi.current_tasks[id]["JobInfo"]["status"] = status
    else:
        gi.current_tasks[id]["JobInfo"]["status"] += status

    if metrics_collection != "":
        gi.current_tasks[id]["JobInfo"]["metrics"] = metrics_collection

def modify_job_included(id, filename, included):
    """
        id (string): id of job to modify
        filename (string): filename that will be added or removed from
                           the included list
        included (bool): the logic control that will enable the addition
                         or removal of filename
    """

    for gi_filename in gi.current_tasks[id]["JobInfo"]["included"]:
        if included and gi_filename == filename:
            #Item already in the included list
            return
        if not included and gi_filename == filename:
            gi.current_tasks[id]["JobInfo"]["included"].remove(gi_filename)
            return
    gi.current_tasks[id]["JobInfo"]["included"].append(filename)


def get_task_map_id(id):
    return gi.current_tasks[id]


def get_task_map_id_file_info(id, filename, index):
    return gi.current_tasks[id][filename][index]


def make_archive(id, directory=""):
    source = os.path.join("uploads", id)
    if directory != "":
        source = os.path.join(os.path.join("uploads", id), directory)

    destination = source
    base_dir = os.path.basename(destination)
    name = base_dir
    file_format = "zip"
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))

    if os.path.exists(os.path.join(destination, f'{name}.{file_format}')):
        os.remove(os.path.join(destination, f'{name}.{file_format}'))

    shutil.make_archive(name, file_format, archive_from, archive_to)
    try:
        shutil.move(f'{name}.{file_format}', destination)
    except shutil.Error:
        os.remove(f'{name}.{file_format}')
    return f'{name}.{file_format}', destination


if __name__ == "__main__":
    print('to upload files navigate to http://10.0.2.15:5000/upload_gtirb')
    app.run(host='10.0.2.15', port=5000, debug=True, threaded=True)
