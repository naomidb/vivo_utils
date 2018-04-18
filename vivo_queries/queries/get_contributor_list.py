def get_params(connection):
    params = {}
    return params


def get_triples():
    q = """ SELECT ?label ?u
        WHERE { ?u <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Organization> . ?u <http://www.w3.org/2000/01/rdf-schema#label> ?label . }
        """
    return q


def run(connection, **params):
    q = get_triples()
    print('=' * 20 + '\nGenerating organization list\n' + '=' * 20)
    response = connection.run_query(q)
    print(response)

    org_dump = response.json()

    all_orgs = {}
    for listing in org_dump['results']['bindings']:
        o_name = listing['label']['value']
        o_url = listing['u']['value']
        o_n = o_url.rsplit('/', 1)[-1]
        all_orgs[o_n] = o_name
    return all_orgs
