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
    gtirb_url = f'http://{gi.IP_HOST_GTIRB}/simple'.encode("utf8").strip()

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

    # index_files = 0
    # for filename in gi.current_tasks[uploads_id].keys():
    #     if filename != "JobInfo":
    #         # print(filename)
    #         files[index_files] = open(os.path.join(user_space, filename), 'rb')
    #         index_files += 1
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


def gen_filename(original_bin: str, transforms:str):

    file_extensions = {
        "ddisasm": ".d",
        "to-static": ".ts",
        "reachable-reduce": ".rr",
        "shuffle": ".sf",
        "retpoline": ".rp",
        "stack-stamp": ".ss",
        "pretty-print": ".asm",
        "binary-print": ".bp",
        "static-binary-print": ".sbp"
    }
    transform_to_int = {
        "ddisasm": 1,
        "to-static": 2,
        "reachable-reduce": 3,
        "shuffle": 4,
        "retpoline": 5,
        "stack-stamp": 6,
        "pretty-print": 7,
        "binary-print": 8,
        "static-binary-print": 9
    }
    # Use file_to_int values as keys
    int_to_transform = {value: key for key, value in transform_to_int.items()}

    # split string of transforms into list
    str_transforms_list = transforms.split(",")

    # Convert each string to an integer using transform to int for sorting
    int_transform_list = []
    for transform in str_transforms_list:
        int_transform_list.append(transform_to_int[transform])

    # Convert
    extension_list = []
    for integer in int_transform_list:
        extension_list.append(file_extensions[int_to_transform[integer]])
    file_extension = "".join(extension_list)

    transform_bin_name = original_bin + file_extension
    return transform_bin_name

def gtirb_run_transform_set(uploads_id: str):
    """
    Generalized GTIRB Server transform
    uploads_id (str): provide the upload id of the set of files to run the transforms on

    returns:
        status (str): The HTTP status code returned by the GTIRB Server
        message (str): Human Readable Server Response depends on status
        original_bin (str): The filename of the original binary. Found by searching data structure
        transformed_bin (str): The filename of the transformed original binary
        transformed_bin_type (str): 3 Potential returns; 1. binary,
                                                         2. gtirb,
                                                         3. asm
    """


    url_gtirb = f"https://{gi.IP_HOST_GTIRB}/simple"
    user_space = os.path.join('uploads', str(uploads_id))
    files = []
    # print(gi.current_tasks)
    original_bin = ""
    for filename in gi.current_tasks[uploads_id].keys():
        if filename != "JobInfo":
            lib_or_bin = gi.current_tasks[uploads_id][filename][0]
            files.append((lib_or_bin, (filename, open(os.path.join(user_space, filename), "rb"))))
            if lib_or_bin == "binary":
                original_bin = filename

    if original_bin == "":
        status = "400"
        message = "[ERROR] Binary file not detected in upload.  Please check that you have selected uploaded and " \
                  "labeled your binary file for transformation "
        transformed_bin = ""
        transformed_bin_type = ""
        return status, message, original_bin, transformed_bin, transformed_bin_type

    job_transforms = gi.current_tasks[id]["JobInfo"][0]

    response = re.post(url_gtirb,
                        files=files,
                        data={"transform": f"{job_transforms}"},
                        stream=True)

    status = response[0].status_code
    transformed_bin = ""
    # Write output of response body to the desired output location
    if str(status) == "200":
        total_byte = 0
        transformed_bin = gen_filename(original_bin, transforms=job_transforms)
        output_location = os.path.join(os.path.join("uploads", uploads_id), response[1])
        with open(output_location, "wb") as ol:
            print("writing to output_bin...")
            for chunk in response[0].iter_content(chunk_size=1024):
                if chunk:
                    total_byte += 1024
                    print(total_byte)
                    ol.write(chunk)
            message = "finished writing to output_bin"
    elif str(status) == "400":
        try:
            raise SyntaxError
        except SyntaxError:
            message = "Error encountered by server.  Syntax given was invalid"
    elif str(status) == "500":
        try:
            raise SystemError
        except SystemError:
            message = "Error encountered by server.\nError information stored in 'ErrorLog.txt'"
            with open("ErrorLog.txt", "w") as EL:
                EL.write(response[0].text)
    else:
        # TODO: Add contact information for developers
        message = f"Return status: {status} not explicitly handled by this server.  Please report this error to development"
    return status, message, original_bin, transformed_bin  # TODO:, transformed_bin_type; Using Name Gen Technique

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


# gi.current_tasks = {'1': {'ld-linux-x86-64.so.2': ['library', 'Not Specified', 'fine'], 'JobInfo': ['Not Specified', 'None To Report'], 'libc.so.6': ['library', 'Not Specified', 'fine'], 'libdl.so.2': ['library', 'Not Specified', 'fine'], 'libpcre2-8.so.0': ['library', 'Not Specified', 'fine'], 'libpthread.so.0': ['library', 'Not Specified', 'fine'], 'libselinux.so.1': ['library', 'Not Specified', 'fine'], 'ls': ['binary', 'Not Specified', 'fine']}}
# gtirb_run_transform_set('1')

print(gen_filename("ls", "ddisasm,stack-stamp,binary-print"))