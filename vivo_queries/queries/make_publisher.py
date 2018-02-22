from publisher import Publisher

def get_params(connection):
    publisher = Publisher(connection)
    params = {'Publisher': publisher}
    return params

def fill_params(connection, **params):
    params['Publisher'].create_n()
    params['publisher_url'] = connection.vivo_url + params['Publisher'].n_number

    return params

def get_triples(**params):
    triples = """\
<{PUBLISHER}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Thing> .
<{PUBLISHER}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#Publisher> .
<{PUBLISHER}> <http://www.w3.org/2000/01/rdf-schema#label> "{NAME}"^^<http://www.w3.org/2001/XMLSchema#string> .      
    """.format(PUBLISHER = params['publisher_url'], NAME = params['Publisher'].name)

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
    q = get_triples(**params)

    print('=' * 20 + "\nCreating new publisher\n" + '=' * 20)
    response = connection.run_update(q)
    return response

def write_rdf(connection, **params):
    params = fill_params(connection, **params)
    rdf = get_triples(**params)

    return rdf