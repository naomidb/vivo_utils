from vivo_utils.vdos.author import Author

def get_params(connection):
    author = Author(connection)
    params = {'Author': author}
    return params

def fill_params(connection, **params):
    namespace = connection.namespace
    params['author_url'] = namespace + params['Author'].n_number

    return params

def get_query(**params):
    query = """ SELECT ?label ?article WHERE {{<{}> <http://vivoweb.org/ontology/core#relatedBy> ?relation . ?relation <http://vivoweb.org/ontology/core#relates> ?article . ?article <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ontology/bibo/AcademicArticle> . ?article <http://www.w3.org/2000/01/rdf-schema#label> ?label . }} """.format(params['author_url'])

    return query

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(**params)

    print('=' * 20 + "\nGenerating Author's Article List\n" + '=' * 20)
    response = connection.run_query(q)
    print(response)

    article_dump = response.json()
    all_articles = {}
    for listing in article_dump['results']['bindings']:
        a_name = parse_json(listing, 'label')
        a_url = parse_json(listing, 'article')
        a_n = a_url.rsplit('/', 1)[-1]
        all_articles[a_n] = a_name

    return all_articles

def parse_json(data, search):
    try:
        value = data[search]['value']
    except KeyError as e:
        value = ''

    return value