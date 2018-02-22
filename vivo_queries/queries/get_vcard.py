from author import Author

def get_params(connection):
    author = Author(connection)
    params = {'Author': author,}
    return params

def fill_params(connection, **params):
    params['subj'] = connection.vivo_url + params['Author'].n_number

def get_query(**params):
    query = """ SELECT ?vcard WHERE {{<{}> <http://purl.obolibrary.org/obo/ARG_2000028> ?vcard .}} LIMIT 1 """.format(params['subj'])

    return query

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(**params)

    print('=' * 20 + '\nFinding vcard\n' + '=' * 20)
    response = connection.run_query(q)
    print(response)

    #Navigate json
    finding = response.json()
    vcard = finding['results']['bindings'][0]['vcard']['value']

    return vcard