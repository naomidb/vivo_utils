from vivo_utils.vdos.article import Article

def get_params(connection):
    article = Article(connection)
    params = {'Article': article}
    return params

def fill_params(connection, **params):
    params['article_url'] = connection.namespace + params['Article'].n_number
    
    return params

def get_query(**params):
    query = """SELECT ?j ?label WHERE{{?j <http://vivoweb.org/ontology/core#publicationVenueFor> <{}> . <{}> <http://vivoweb.org/ontology/core#hasPublicationVenue> ?j . ?j <http://www.w3.org/2000/01/rdf-schema#label> ?label . }}""".format(params['article_url'], params['article_url'])

    return query

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(**params)
    
    print('=' * 20 + "\nChecking for journal\n" + '=' * 20)
    response = connection.run_query(q)

    j_check = response.json()
    for listing in j_check['results']['bindings']:
        try:
            j_name = parse_json(listing, 'label')
            j_url = parse_json(listing, 'j')
            j_n = j_url.rsplit('/', 1)[-1]
            pubs_journal = (j_n, j_name)
            return pubs_journal 
        except KeyError as e:
            return None

def parse_json(data, search):
    try:
        value = data[search]['value']
    except KeyError as e:
        value = ''

    return value