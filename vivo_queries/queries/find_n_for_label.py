from vivo_queries.vdos.thing import Thing

def get_params(connection):
    thing = Thing (connection)
    params = {'Thing': thing,}
    return params

def fill_params(connection, **params):
    params['identity'] = ""
    if params['Thing'].type == 'academic_article':
        params['identity'] = 'http://purl.org/ontology/bibo/AcademicArticle'
    if params['Thing'].type == 'letter':
        params['identity'] = 'http://purl.org/ontology/bibo/Letter'
    if params['Thing'].type == 'journal':
        params['identity'] = 'http://purl.org/ontology/bibo/Journal'
    if params['Thing'].type == 'person':
        params['identity'] = 'http://xmlns.com/foaf/0.1/Person'
    if params['Thing'].type == 'publisher':
        params['identity'] = 'http://vivoweb.org/ontology/core#Publisher'

    return params

def get_query(**params):
    query = """SELECT ?uri ?label WHERE {{?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{}> . ?uri <http://www.w3.org/2000/01/rdf-schema#label> ?label . FILTER (regex (?label, "{}", "i")) }}""".format(params['identity'], params['thing'].name)

    return query

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(**params)

    print('=' * 20 + "\nFinding n number\n" + '=' * 20)
    response = connection.run_query(q)

    lookup = response.json()
    matches = {}
    for listing in lookup['results']['bindings']:
        name = parse_json(listing, 'label')
        url = parse_json(listing, 'uri')
        url_n = url.rsplit('/', 1)[-1]
        matches[url_n] = name

    return matches

def parse_json(data, search):
    try:
        value = data[search]['value']
    except KeyError as e:
        value = ''

    return value