#import requests as re
import os.path


def get_counter():
    global counter, current_tasks
    counter += 1
    return str(counter) + str(current_tasks)

 # Task Map Structure is as follows
    # { id:{filename: [filetype, transform, status]}, ...,
    #   id+n:{filename: [filetype, transform, status]} }
def gtirb_ddisasm(uploads_id, task_map, ):
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
