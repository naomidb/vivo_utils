def get_params(connection):
    params = {}
    return params


def run(connection, **params):
    q = """ select ?label ?u where { ?u <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#Grant> . ?u <http://www.w3.org/2000/01/rdf-schema#label> ?label . } """

    print('=' * 20 + '\nGenerating grant list\n' + '=' * 20)
    response = connection.run_query(q)
    print(response)

    grant_dump = response.json()
    all_grants = {}
    for listing in grant_dump['results']['bindings']:
        g_name = listing['label']['value']
        g_url = listing['u']['value']
        g_n = g_url.rsplit('/', 1)[-1]
        all_grants[g_n] = g_name
    return all_grants
