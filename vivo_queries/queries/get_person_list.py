def get_params(connection):
    params = {}
    return params

def get_query(**params):
    query = """ SELECT ?label ?u WHERE { ?u <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> . ?u <http://www.w3.org/2000/01/rdf-schema#label> ?label . } """

    return query

def run(connection, **params):
    q = get_query(**params)

    print('=' * 20 + '\nGenerating author list\n' + '=' * 20)
    response = connection.run_query(q)
    print(response)

    author_dump = response.json()
    all_authors = {}
    for listing in author_dump['results']['bindings']:
        a_name = parse_json(listing, 'label')
        a_url = parse_json(listing, 'u')
        a_n = a_url.rsplit('/', 1)[-1]
        all_authors[a_n] = a_name

    return all_authors

def parse_json(data, search):
    try:
        value = data[search]['value']
    except KeyError as e:
        value = ''

    return value