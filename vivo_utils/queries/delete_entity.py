import re

from vivo_utils.vdos.thing import Thing
from vivo_utils.queries import get_label
from vivo_utils.queries import get_all_triples

def get_params(connection):
    thing = Thing(connection)
    params = {'Thing': thing,}
    return params

def fill_params(connection, **params):
    params['triples'] = get_all_triples.run(connection, **params)
    params['label'] = get_label.run(connection, **params)

    return params

def get_triples(api, **params):
    format_triples = ""
    for trip in params['triples']:
        format_triples = format_triples + trip + " . \n"

    #Fix label
    format_triples = format_triples.encode('utf-8')
    format_triples = str.replace(format_triples, "<" + params['label'] + ">", "\"" + params['label'] + "\"")

    if api:
        api_trip = """\
        DELETE DATA {{
            GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2> {{
                {}
            }}
        }}
            """.format(format_triples)

        return api_trip

    else:
        return format_triples

def fix_strings(triples):
    clean_triples = []
    for trip in triples:
        sub, pred, obj = re.findall("<.*?>", trip)[:]
        #If the object is not a uri, change the angular brackets into quotation marks 
        if 'http://' not in obj and 'https://' not in obj:
            bare_obj = obj[1:-1]
            quoted_obj = '"' + bare_obj + '"'
            trip = sub + ' ' + pred + ' ' + quoted_obj
        clean_triples.append(trip)

    return clean_triples

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_triples(True, **params)

    print('=' * 20 + "\nDeleting\n" + '=' * 20)
    response = connection.run_update(q)
    return response

def write_rdf(connection, **params):
    params = fill_params(connection, **params)
    rdf = get_triples(False, **params)

    return rdf