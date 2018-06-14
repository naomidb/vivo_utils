from vivo_utils.vdos.thing import Thing

def get_params(connection):
    thing = Thing(connection)
    params = {'Thing': thing,}
    return params

def fill_params(connection, **params):
    params['subj'] = connection.namespace + params['Thing'].n_number

    return params

def get_query(**params):
    query = """ SELECT ?label WHERE {{<{}> <http://www.w3.org/2000/01/rdf-schema#label> ?label .}} """.format(params['subj'])

    return query

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(**params)

    print('=' * 20 + '\nFinding label\n' + '=' * 20)
    response = connection.run_query(q)
    print(response)

    #Navigate json
    finding = response.json()
    label = finding['results']['bindings'][0]['label']['value']

    return label