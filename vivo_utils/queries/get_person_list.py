def get_params(connection):
    params = {}
    return params

def get_query(**params):
    query = """ SELECT ?label ?first ?middle ?last ?u 
                WHERE { 
                    ?u <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> . 
                    ?u <http://www.w3.org/2000/01/rdf-schema#label> ?label . 
                    ?u <http://purl.obolibrary.org/obo/ARG_2000028> ?vcard . 
                    OPTIONAL { ?vcard <http://www.w3.org/2006/vcard/ns#givenName> ?first .}
                    OPTIONAL { ?vcard <http://www.w3.org/2006/vcard/ns#middleName> ?middle .}
                    OPTIONAL { ?vcard <http://www.w3.org/2006/vcard/ns#lastName> ?last .}
                } """

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
        first = parse_json(listing, 'first')
        middle = parse_json(listing, 'middle')
        last = parse_json(listing, 'last')
        if not last:
            try:
                last, rest = a_name.split(', ')
                try:
                    first, middle = rest.split(" ", 1)
                except ValueError as e:
                    first = rest
            except ValueError as e:
                last = a_name

        all_authors[a_n] = (last, first, middle, a_name)

    return all_authors

def parse_json(data, search):
    try:
        value = data[search]['value']
    except KeyError as e:
        value = ''

    return value