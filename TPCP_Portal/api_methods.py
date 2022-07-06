import requests
import requests as re
import global_items as gi
import os


def get_counter():
    # gi.counter, gi.current_tasks
    gi.counter += 1
    return str(gi.counter) + str(gi.current_tasks)

    # Task Map Structure is as follows
    # { id:{filename: [filetype, transform, status]}, ...,
    #   id+n:{filename: [filetype, transform, status]} }
def gtirb_ddisasm(uploads_id):
    """
    Highly specific to sort-8.16 test case
    uploads_id:

    """
    # gtirb_url = "gtirb/simple"
    gtirb_url = 'http://172.20.0.6/simple'.encode("utf8").strip()
    # binary = 'sort-8.16'
    # output = binary + ".gtirb"
    user_space = os.path.join('uploads', str(uploads_id))
    files = {open("uploads/1/sort-8.16", "rb"),
             open("/lib/x86_64-linux-gnu/libpthread.so.0", "rb"),
             open("/lib/x86_64-linux-gnu/libc.so.6", "rb"),
             open("/lib64/ld-linux-x86-64.so.2", "rb")
             }
    # for filename in gi.current_tasks[uploads_id].keys():
    #     if filename != "JobInfo":
    #         # print(filename)
    #         files[filename] = open(os.path.join(user_space, filename), 'rb')
    # file = {filename: open(os.path.join(user_space, filename), 'rb')}
    # print(file)

    options = {
        "transform": "ddisasm",
        "output": "sort-8.16.gtirb"
    }
    # print(files)
    # print(requests.Request("POST", gtirb_url, data=files).prepare().body.decode('utf8'))
    response = requests.post(gtirb_url, data=options)
    status = response.status_code
    print(response.text)
    print(status)
    # raise NotImplementedError
gi.current_tasks = {'1': {'JobInfo': ['Not Specified', 'Must Pipe Output'], 'sort-8.16': ['c/c++ binary', 'Not Specified', '']}}
gtirb_ddisasm('1')

options = {
        "transform": "ddisasm",
        "binary": "sort-8.16",#open("uploads/1/sort-8.16", "rb"),
        "library": (
            "libpthread.so.0",
            "libc.so.6",
            "ld-linux-x86-64.so.2"
        ),
        "output": "sort-8.16.gtirb"
    }