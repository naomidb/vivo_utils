def get_params(connection):
    params = {}
    return params

def get_query(**params):
    query = """ SELECT ?label ?u WHERE { ?u <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ontology/bibo/Journal> . ?u <http://www.w3.org/2000/01/rdf-schema#label> ?label . } """

    return query

def run(connection, **params):
    q = get_query(**params)

    print('=' * 20 + '\nGenerating journal list\n' + '=' * 20)
    response = connection.run_query(q)
    print(response)

    journal_dump = response.json()
    all_journals = {}
    for listing in journal_dump['results']['bindings']:
        j_name = parse_json(listing, 'label')
        j_url = parse_json(listing, 'u')
        j_n = j_url.rsplit('/', 1)[-1]
        all_journals[j_n] = j_name       

    return all_journals

def parse_json(data, search):
    try:
        value = data[search]['value']
    except KeyError as e:
        value = ''

    return value