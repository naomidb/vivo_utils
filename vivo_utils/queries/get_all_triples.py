from vivo_utils.vdos.thing import Thing
from vivo_utils.queries import get_all_with_x_as_obj
from vivo_utils.queries import get_all_with_x_as_subj

def get_params(connection):
    thing = Thing(connection)
    params = {'Thing': thing,}
    return params

def run(connection, **params):
    triples = get_all_with_x_as_subj.run(connection, **params)
    obj_trip = get_all_with_x_as_obj.run(connection, **params)

    for item in obj_trip:
        triples.append(item)

    return triples
