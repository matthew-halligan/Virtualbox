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
    uploads_id:

    """
    user_space = os.path.join('uploads', str(uploads_id))
    gtirb_url = "gtirb/simple"
    # files = {}
    # for filename in task_map.keys():
    #     files[filename] = open(os.path.join(user_space, filename), 'rb')
    # file = {filename: open(os.path.join(user_space, filename), 'rb')}
    raise NotImplementedError
