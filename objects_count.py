def objects_counter(objects_dict, object):

    if object not in objects_dict.keys():
        objects_dict.update({f"{object}": 1})
