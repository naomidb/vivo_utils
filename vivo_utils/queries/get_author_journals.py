from vivo_utils.vdos.author import Author

def return_type():
    return "query"

def get_params(connection):
    author = Author(connection)
    params = {'Author': author}
    return params

def fill_params(connection, **params):
    namespace = connection.namespace
    params['author_url'] = namespace + params['Author'].n_number

    return params

def get_query(**params):
    query = """
SELECT ?journ_n ?journ_name
WHERE {{<{}> <http://vivoweb.org/ontology/core#relatedBy> ?relation .
        ?relation <http://vivoweb.org/ontology/core#relates> ?article .
        ?article <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ontology/bibo/AcademicArticle> .
        ?article <http://vivoweb.org/ontology/core#hasPublicationVenue> ?journ_n.
        ?journ_n <http://www.w3.org/2000/01/rdf-schema#label> ?journ_name . }}
    """.format(params['author_url'])

    return query

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(**params)

    print('=' * 20 + "\nGetting Journals for Author\n" + '=' * 20)
    response = connection.run_query(q)
    print(response)

    author_journals = response.json()
    journals = {}
    for listing in author_journals['results']['bindings']:
        j_name = parse_json(listing, 'journ_name')
        j_url = parse_json(listing, 'journ_n')
        j_n = j_url.rsplit('/', 1)[-1]
        journals[j_n] = j_name

    return journals

def parse_json(data, search):
    try:
        value = data[search]['value']
    except KeyError as e:
        value = ''

    return value