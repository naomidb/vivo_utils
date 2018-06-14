from collections import OrderedDict

from vivo_utils.vdos.journal import Journal
from vivo_utils.vdos.publisher import Publisher
from vivo_utils.queries import make_publisher

def get_params(connection):
    journal = Journal(connection)
    publisher = Publisher(connection)
    params = {'Journal': journal, 'Publisher': publisher}
    return params

def fill_params(connection, **params):
    if not params['Publisher'].n_number:
        make_publisher.run(connection, **params)
    params['publisher_url'] = connection.namespace + params['Publisher'].n_number
    params['journal_url'] = connection.namespace + params['Journal'].n_number

    return params

def get_triples(api, **params):
    triples = """
<{PUBLISHER}> <http://vivoweb.org/ontology/core#publisherOf> <{JOURNAL}> .
<{JOURNAL}> <http://vivoweb.org/ontology/core#publisher> <{PUBLISHER}> .
    """.format(PUBLISHER = params['publisher_url'], JOURNAL = params['journal_url'])

    if api:
        api_trip = """\
        INSERT DATA {{
            GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2>
            {{
              {TRIPS}
            }}
        }}
            """.format(TRIPS=triples)

        return api_trip

    else:
        return triples

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_triples(True, **params)

    print('=' * 20 + "\nAssociating author with pub\n" + '=' * 20)
    response = connection.run_update(q)
    return response

def write_rdf():
    params = fill_params(connection, **params)
    rdf = get_triples(False, **params)

    return rdf