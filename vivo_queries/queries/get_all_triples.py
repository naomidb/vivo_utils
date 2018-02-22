from queries import get_all_with_x_as_obj
from queries import get_all_with_x_as_subj
from thing import Thing

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
