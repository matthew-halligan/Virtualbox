import requests as re
import global_items as gi
import os
import textwrap


def get_counter():
    # gi.counter, gi.current_tasks
    gi.counter += 1
    return str(gi.counter) + str(gi.current_tasks)

    # Task Map Structure is as follows
    # { id:{filename: [filetype, transform, status]}, ...,
    #   id+n:{filename: [filetype, transform, status]} }
def gtirb_ddisasm(uploads_id):
    """
    Highly specific to 'ls' test case
    uploads_id:

    """
    gtirb_url = 'http://172.20.0.6/simple'.encode("utf8").strip()

    user_space = os.path.join('uploads', str(uploads_id))
    files = [("binary", ("ls", open("/bin/ls", "rb"))),
             ("library", ("libpthread.so.0", open("/lib/x86_64-linux-gnu/libpthread.so.0", "rb"))),
             ("library", ("libc.so.6", open("/lib/x86_64-linux-gnu/libc.so.6", "rb"))),
             ("library", ("ld-linux-x86-64.so.2", open("/lib64/ld-linux-x86-64.so.2", "rb"))),
             ("library", ("libselinux.so.1", open("/lib/x86_64-linux-gnu/libselinux.so.1", "rb"))),
             ("library", ("libpcre2-8.so.0", open("/lib/x86_64-linux-gnu/libpcre2-8.so.0", "rb"))),
             ("library", ("libdl.so.2", open("/lib/x86_64-linux-gnu/libdl.so.2", "rb")))
             ]
    # for filename in gi.current_tasks[uploads_id].keys():
    #     if filename != "JobInfo":
    #         # print(filename)
    #         files[filename] = open(os.path.join(user_space, filename), 'rb')
    # file = {filename: open(os.path.join(user_space, filename), 'rb')}
    # print(file)


    response = re.post(gtirb_url, files=files, data={"transform": "to-static,stack-stamp,pretty-print"})
    status = response.status_code
    print(response.text)
    print(status)

    # req = requests.Request('POST', gtirb_url, files=files, data={"transform": "ddisasm"})
    # prepared = req.prepare()

    # print(ascii(prepared.body))
    # pretty_print_POST(prepared)

    # Write output of response body to the desired output location
    # with open(output_location, "wb") as ol:
    #     ol.write(res.body)

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    text = '{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    )

    print(textwrap.fill(text, width=80))


gi.current_tasks = {'1': {'JobInfo': ['Not Specified', 'Must Pipe Output'], 'sort-8.16': ['c/c++ binary', 'Not Specified', '']}}
gtirb_ddisasm('1')
