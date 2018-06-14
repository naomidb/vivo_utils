from vivo_utils.vdos.author import Author


def get_params(connection):
    author = Author(connection)
    params = {'Author': author,}
    return params


def fill_params(connection, **params):
    params['subj'] = connection.namespace + params['Author'].vcard

    return params


def get_query(**params):
    print(params['subj'])
    query = """ SELECT ?name_id WHERE {{<{}> <http://www.w3.org/2006/vcard/ns#hasName> ?name_id .}} LIMIT 1 """.format(params['subj'])
    print(query)

    return query


def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(**params)

    print('=' * 20 + '\nFinding name id\n' + '=' * 20)
    response = connection.run_query(q)
    print(response)

    #Navigate json
    finding = response.json()
    name_id = finding['results']['bindings'][0]['name_id']['value'].split("/")[-1]

    return name_id