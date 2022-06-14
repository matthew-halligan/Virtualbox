import sys, os, re, subprocess
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER='uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Check that the upload folder exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

current_tasks = {}

@app.route('/upload')
def upload():
    print(len(current_tasks))
    return render_template("index2.html",
                           current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                           current_tasks=current_tasks)

@app.route('/upload', methods=['POST'])
def modify_or_upload_files():
    global current_tasks

    if request.method != 'POST':
        return render_template("index2.html",
                               current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                               current_tasks=current_tasks)

    if request.form['HiddenField'] == 'ModifyFile':
        id = request.form['ID']
        filename = request.form['FileName']
        filetype = request.form['FileType'] if request.form['FileType'] != 'No Change' else 'Not Specified'
        transform = request.form['Transform'] if request.form['Transform'] != 'No Change' else 'Not Specified'
        status = request.form['Status']

        add_to_task_map(id, filename, transform, filetype, status)

        return render_template("index2.html",
                               current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                               current_tasks=current_tasks)
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
                filetype, status = "Not Specified", 'fine'
                add_to_task_map(id, filename, transform, filetype, status)
        return render_template("index2.html", id=id,
                       current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                       current_tasks=current_tasks)


def add_to_task_map(id, filename, transform, filetype, status):
    # Task Map Structure is as follows
    # { id:[filename, filetype, transform, status], ...,
    #   id+n:[filename, filetype, transform, status] }
    try:
        current_tasks[id][filename] = [filetype, transform, status]
    except KeyError:
        current_tasks[id] = {filename: [filetype, transform, status]}


def get_task_map_id(id):
    return current_tasks[id]

if __name__ == "__main__":
    print('to upload files navigate to http://10.0.2.15:5000/upload')
    app.run(host='10.0.2.15', port=5000, debug=True, threaded=True)