def get_params(connection):
    params = {}
    return params

def get_query(**params):
    query = """ SELECT ?label ?doi ?pmid ?type ?u
                WHERE { 
                    ?u <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ontology/bibo/Article> . 
                    ?u <http://www.w3.org/2000/01/rdf-schema#label> ?label . 
                    ?u <http://vitro.mannlib.cornell.edu/ns/vitro/0.7#mostSpecificType> ?type .
                    OPTIONAL {?u <http://purl.org/ontology/bibo/doi> ?doi .}
                    OPTIONAL {?u <http://purl.org/ontology/bibo/pmd> ?pmid .} } """

    return query

def run(connection, **params):
    q = get_query(**params)

    print('=' * 20 + '\nGenerating article list\n' + '=' * 20)
    response = connection.run_query(q)
    print(response)

    article_dump = response.json()
    all_articles = {}
    for listing in article_dump['results']['bindings']:
        a_name = parse_json(listing, 'label')
        a_url = parse_json(listing, 'u')
        a_n = a_url.rsplit('/', 1)[-1]
        doi = parse_json(listing, 'doi')
        pmid = parse_json(listing, 'pmid')
        specific_type = parse_json(listing, 'type')
        all_articles[a_n] = (a_name, doi, pmid, specific_type)

    return all_articles

def parse_json(data, search):
    try:
        value = data[search]['value']
    except KeyError as e:
        value = ''

    return value