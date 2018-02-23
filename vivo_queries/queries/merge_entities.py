from vivo_queries.vdos.thing import Thing
from vivo_queries.queries import get_label
from vivo_queries.queries import delete_entity
from vivo_queries.queries import get_all_triples

def get_params(connection):
    thing1 = Thing(connection)
    thing2 = Thing(connection)
    params = {'Primary URI': thing1, 'Secondary URI': thing2}
    return params

def fill_params(connection, **params):
    merge_params = {'Thing': params['Secondary URI']}

    params['final_uri'] = params['Primary URI'].n_number
    params['old_uri'] = params['Secondary URI'].n_number

    params['triples'] = get_all_triples.run(connection, **merge_params)
    params['label'] = get_label.run(connection, **merge_params)

    return params

def get_triples(api, **params):
    format_triples = ""
    for trip in params['old_trips']:
        format_triples = format_triples + trip + " . \n"

    format_triples = format_triples.encode('utf-8')
    format_triples = str.replace(format_triples, old_uri + ">", final_uri + ">")
    format_triples = str.replace(format_triples, "<" + params['label'] + ">", "\"" + label + "\"")

    if api:
        api_trip = """\
        INSERT DATA {{
            GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2>
            {{
              {}
            }}
        }}
            """.format(format_triples)

        return api_trip

    else:
        return format_triples

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_triples(True, **params)

    print('=' * 20 + "\nMerging\n" + '=' * 20)
    ins_response = connection.run_update(q)
    print(ins_response)

    #Delete if Insert is successful
    merge_params = {'Thing': params['Secondary URI']}
    if ins_response == 200:
        del_response = delete_entity.run(connection, **merge_params)
        return del_response
    else:
        return ins_response