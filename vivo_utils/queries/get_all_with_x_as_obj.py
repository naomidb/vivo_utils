from vivo_utils.vdos.thing import Thing

def get_params(connection):
    thing = Thing(connection)
    params = {'Thing': thing,}
    return params

def fill_params(connection, **params):
    params['obj'] = connection.namespace + params['Thing'].n_number

    return params

def get_query(**params):
    query = """ SELECT ?s ?p ?o WHERE{{?s ?p <{}> .}} """.format(params['obj'])

    return query

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(**params)

    print('=' * 20 + '\nGenerating triples\n' + '=' * 20)
    response = connection.run_query(q)
    print(response)

    #Navigate json
    triple_dump = response.json()
    triples = []
    for listing in triple_dump['results']['bindings']:
        subj = listing['s']['value']
        pred = listing['p']['value']
        trip = "<" + subj + "> <" + pred + "> <" + params['obj'] + ">"
        triples.append(trip)

    return triples