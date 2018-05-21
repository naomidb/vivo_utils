def get_params(connection):
    params = {}
    return params


def run(connection, **params):
    q = """ select ?label ?u where { ?u <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#Department> . ?u <http://www.w3.org/2000/01/rdf-schema#label> ?label . } """

    print('=' * 20 + '\nGenerating journal list\n' + '=' * 20)
    response = connection.run_query(q)
    print(response)

    department_dump = response.json()
    all_departments = {}
    for listing in department_dump['results']['bindings']:
        d_name = listing['label']['value']
        d_url = listing['u']['value']
        d_n = d_url.rsplit('/', 1)[-1]
        all_departments[d_n] = d_name
    return all_departments
