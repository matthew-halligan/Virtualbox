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
    gtirb_url = 'http://172.17.0.1/simple'.encode("utf8").strip()

    user_space = os.path.join('uploads', str(uploads_id))
    files = [("binary", ("ls", open("/bin/ls", "rb")))  # ,
             # ("library", ("libpthread.so.0", open("/lib/x86_64-linux-gnu/libpthread.so.0", "rb"))),
             # ("library", ("libc.so.6", open("/lib/x86_64-linux-gnu/libc.so.6", "rb"))),
             # ("library", ("ld-linux-x86-64.so.2", open("/lib64/ld-linux-x86-64.so.2", "rb"))),
             # ("library", ("libselinux.so.1", open("/lib/x86_64-linux-gnu/libselinux.so.1", "rb"))),
             # ("library", ("libpcre2-8.so.0", open("/lib/x86_64-linux-gnu/libpcre2-8.so.0", "rb"))),
             # ("library", ("libdl.so.2", open("/lib/x86_64-linux-gnu/libdl.so.2", "rb")))
             ]

    files_ts = [("binary", ("ls", open("/bin/ls", "rb"))),
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

    # stack-stamp
    ss_response = re.post(gtirb_url,
                          files=files,
                          data={"transform": "ddisasm,stack-stamp,binary-print"},
                          stream=True)

    # to-static
    # t_response = re.post(gtirb_url,
    #                      files=files_ts,
    #                      data={"transform": "to-static,pretty-print"},
    #                      stream=True)

    # to-static, stack-stamp
    tss_response = re.post(gtirb_url,
                           files=files_ts,
                           data={"transform": "to-static,stack-stamp,static-binary-print"},
                           stream=True)

    # to-static, shuffle
    # s_response = re.post(gtirb_url,
    #                      files=files_ts,
    #                      data={"transform": "to-static,shuffle,static-binary-print"},
    #                      stream=True)
    responses = [
        [ss_response, "stack-stamp.ls"],
        # [t_response, "to-static.ls"],
        [tss_response, "t-stack-stamp.ls"],
        # [s_response, "shuffle.ls"]
    ]
    for response in responses:
        status = response[0].status_code

        # Write output of response body to the desired output location
        if str(status) == "200":
            total_byte = 0
            output_location = os.path.join(os.path.join("uploads", uploads_id), response[1])
            with open(output_location, "wb") as ol:
                print("writing to output_bin...")
                for chunk in response[0].iter_content(chunk_size=1024):
                    if chunk:
                        total_byte += 1024
                        print(total_byte)
                        ol.write(chunk)
                print("finished writing to output_bin")
        elif str(status) == "400":
            try:
                raise SyntaxError
            except SyntaxError:
                print("Error encountered by server.  Syntax given was invalid")
        elif str(status) == "500":
            try:
                raise SystemError
            except SystemError:
                print("Error encountered by server.\nError information stored in 'ErrorLog.txt'")
                with open("ErrorLog.txt", "w") as EL:
                    EL.write(response[0].text)


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

# def
# gi.current_tasks = {'1': {'JobInfo': ['Not Specified', 'Must Pipe Output'], 'sort-8.16': ['c/c++ binary', 'Not Specified', '']}}
# gtirb_ddisasm('1')
