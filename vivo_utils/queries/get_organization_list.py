def get_params(connection):
    params = {}
    return params

def get_query(**params):
    query = """ SELECT ?label ?u ?sub_type
            WHERE { 
            ?u <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Organization> .
            ?u <http://vitro.mannlib.cornell.edu/ns/vitro/0.7#mostSpecificType> ?sub_type .
            ?u <http://www.w3.org/2000/01/rdf-schema#label> ?label . } """

    return query

def run(connection, **params):
    q = get_query(**params)

    print('=' * 20 + '\nGenerating organization list\n' + '=' * 20)
    response = connection.run_query(q)
    print(response)

    org_dump = response.json()
    all_orgs = {}
    for listing in org_dump['results']['bindings']:
        name = parse_json(listing, 'label')
        uri = parse_json(listing, 'u')
        n_num = uri.rsplit('/', 1)[-1]
        
        sub_type = parse_json(listing, 'sub_type')
        if sub_type == 'http://vivoweb.org/ontology/core#Department':
            kind = 'department'
        else:
            kind = 'organization'

        all_orgs[n_num] = (name, kind)

    return all_orgs

def parse_json(data, search):
    try:
        value = data[search]['value']
    except KeyError as e:
        value = ''

    return value