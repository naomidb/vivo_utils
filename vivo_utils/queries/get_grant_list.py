def get_params(connection):
    params = {}
    return params


def run(connection, **params):
    q = """ select ?label ?id ?uri ?pi_n ?pi_name ?start ?end
            where { 
            ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#Grant> .
            ?uri <http://www.w3.org/2000/01/rdf-schema#label> ?label .
            OPTIONAL { ?uri <http://vivoweb.org/ontology/core#localAwardId> ?id . }
            OPTIONAL { 
                ?uri <http://vivoweb.org/ontology/core#relates> ?pi_ship .
                ?pi_ship <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#InvestigatorRole> .
                ?pi_ship <http://purl.obolibrary.org/obo/RO_0000052> ?pi_n .
                ?pi_n <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
                ?pi_n <http://www.w3.org/2000/01/rdf-schema#label> ?pi_name . }
            OPTIONAL {
                ?uri <http://vivoweb.org/ontology/core#dateTimeInterval> ?dti .
                ?dti <http://vivoweb.org/ontology/core#start> ?start_uri .
                ?start_uri <http://vivoweb.org/ontology/core#dateTime> ?start .
               OPTIONAL {
                ?dti <http://vivoweb.org/ontology/core#start> ?end_uri .
                ?end_uri <http://vivoweb.org/ontology/core#dateTime> ?end . }
            }
            } """

    print('=' * 20 + '\nGenerating grant list\n' + '=' * 20)
    response = connection.run_query(q)
    print(response)

    grant_dump = response.json()
    all_grants = {}
    for listing in grant_dump['results']['bindings']:
        g_name = parse_json(listing, 'label')
        g_id = parse_json(listing, 'id')
        g_uri = parse_json(listing, 'uri')
        g_n = g_uri.rsplit('/', 1)[-1]
        pi_n = parse_json(listing, 'pi_n')
        pi_name = parse_json(listing, 'pi_name')
        start = parse_json(listing, 'start')
        end = parse_json(listing, 'end')
        all_grants[g_n] = (g_name, g_id, pi_n, pi_name, start, end)
    return all_grants

def parse_json(data, search):
    try:
        value = data[search]['value']
    except KeyError as e:
        value = ''

    return value
