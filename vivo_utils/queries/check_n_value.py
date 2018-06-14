from vivo_utils.vdos.thing import Thing

def get_params(connection):
    thing = Thing(connection)
    params = {'Thing': thing,}
    return params

def fill_params(connection, **params):
    params['uri'] = connection.namespace + params['Thing'].n_number
    
    return params

def get_query(**params):
    query = """
            SELECT (COUNT(?o) as ?count)
            WHERE{{<{}> ?p ?o}}""".format(params['uri'])
    return query

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(**params)

    print('=' * 20 + "\nRunning n check\n" + '=' * 20)
    response = connection.run_query(q)

    n_check = response.json()
    exists = True
    if int(n_check['results']['bindings'][0]['count']['value'])>0:
        exists = True
    else:
        exists = False

    return exists
