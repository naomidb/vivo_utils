def get_params(connection):
    params = {}
    return params

def get_query(**params):
    query = """ SELECT ?label ?u WHERE { ?u <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#Publisher> . ?u <http://www.w3.org/2000/01/rdf-schema#label> ?label . } """

    return query

def run(connection, **params):
    q = get_query(**params)

    print('=' * 20 + '\nGenerating publisher list\n' + '=' * 20)
    response = connection.run_query(q)
    print(response)

    publisher_dump = response.json()
    all_publishers = {}
    for listing in publisher_dump['results']['bindings']:
        p_name = parse_json(listing, 'label')
        p_url = parse_json(listing, 'u')
        p_n = p_url.rsplit('/', 1)[-1]
        all_publishers[p_n] = p_name

    return all_publishers

def parse_json(data, search):
    try:
        value = data[search]['value']
    except KeyError as e:
        value = ''

    return value