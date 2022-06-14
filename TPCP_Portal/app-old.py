from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
import subprocess
import os
import jinja2
from werkzeug.utils import secure_filename

UPLOAD_FOLDER='/app/uploads'
DOWNLOAD_FOLDER = "candidates"
ALLOWED_EXTENSIONS = {"tar.gz"}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


current_tasks = {}

def allowed_file(filename):
    # Currently accept any file type and try to use it because
    # it requires extra code logic to verify file types like .tar.gz
    # that are not necessary in the initial version
    return '.tar.gz' in filename
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_to_task_map(id, tarball_name, transform, quantity_bins, status):
    # Task Map Structure is as follows
    # { id:[tarball_name, transform, quantity_bins, status], ...,
    #   id+n:[tarball_name, transform, quantity_bins, status] }
    current_tasks[id] = [tarball_name, transform, quantity_bins, status]


def get_task_map_id(id):
    return current_tasks[id]


def update_task_map_transform(id, transform):
    # update the current tasks data structure to enable easier tracking
    # of what transforms are taking place in the background
    current_tasks[id][1] = transform


def untar(session_path, filename):
    # Extract each of the files from the uploaded tarball
    # This function requires that the input have no folders inside
    # of the tarball.  The input should be a series of
    # executable files only
    file = os.path.join(session_path, filename)
    os.mkdir(os.path.join(session_path, DOWNLOAD_FOLDER))
    # TODO: Fix: The server will break and require restart if filetype other than .tar.gz is uploaded

    status = subprocess.check_call(f"tar -xzf {file} -C {os.path.join(session_path, DOWNLOAD_FOLDER)}", shell=True)
    print("Status: ", status)
    files = [f for f in os.listdir(os.path.join(session_path, DOWNLOAD_FOLDER))]
    print(files)

    if status == 0:
        # TODO: This quantity will be inaccurate if a directory is present in the untarred directory.  The directory will be considered as 1 item in the count regardless of quantity of nested directories and files beneath
        identified_bin_quantity = int(subprocess.check_output(f"ls {os.path.join(session_path, DOWNLOAD_FOLDER)} | wc -l", shell=True))
        status = "Fine"

    else:
        identified_bin_quantity = "N/A"
        status = str(subprocess.check_output(f"tar -xzf {file} -C {os.path.join(session_path, DOWNLOAD_FOLDER)}", shell=True))

    return identified_bin_quantity, status

@app.route('/download', methods=["POST", "GET"])
def download_file():
    if request.method=="POST":
        id = request.form["id"]
        session_path = os.path.join(app.config["UPLOAD_FOLDER"], id)
        name = current_tasks[id][0]
        subprocess.call(f"tar -czvf {os.path.join(session_path, 'candidates.tar.gz')} {os.path.join(session_path, DOWNLOAD_FOLDER)}", shell=True)
        return send_from_directory(session_path, "candidates.tar.gz", as_attachment=True)

@app.route('/transform', methods=["POST", "GET"])
def transformation_on_file():
    # TODO: the function works on one file at a time. Create a system for using the correct cmd line arguments
    if request.method=="POST":
        id = request.form["id"]
        transform = request.form["transform"]
        task = get_task_map_id(id)
        update_task_map_transform(id, transform)
        subprocess.call(f"./{transform}.sh {id}", shell=True)
        return return_index(id)

def return_index(id):
    if id != None:
        return render_template("index.html", id=id,
                        current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                        current_tasks=current_tasks)

    return render_template("index.html",
                           current_series_ids=sorted(os.listdir(app.config['UPLOAD_FOLDER'])),
                           current_tasks=current_tasks)


@app.route('/', methods=["POST", "GET"])
def upload_file():
    global current_tasks
    errors = []
    # Ensure the file storage is configured otherwise prepare it.
    try:
        current_series_ids = sorted(os.listdir(app.config['UPLOAD_FOLDER']))
    except:
        os.mkdir(app.config['UPLOAD_FOLDER'])
        current_series_ids = sorted(os.listdir(app.config['UPLOAD_FOLDER']))

    # Ensure that the data structure representing current tasking
    # is reflective of the tasks truly in queue
    current_tasks_temp = {}
    for key in current_tasks.keys():
        if key in current_series_ids:
            current_tasks_temp[key] = current_tasks[key]
    current_tasks = current_tasks_temp

    if request.method == 'POST':
        print("POST")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            print("No file part")
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print("No Filename")
            flash('No selected file')
            return return_index(id=None)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if len(current_series_ids) > 0:
                id = str(int(current_series_ids[-1])+1)
            else:
                id = "1"
            session_path = os.path.join(app.config['UPLOAD_FOLDER'], id)
            os.mkdir(session_path)
            file.save(os.path.join(session_path, filename))
            transform = "None"
            quantity_bins, status = untar(session_path, filename)
            add_to_task_map(id, filename, transform, quantity_bins, status)

            return return_index(id)
    return return_index(id=None)



if __name__ == '__main__':
    app.run()