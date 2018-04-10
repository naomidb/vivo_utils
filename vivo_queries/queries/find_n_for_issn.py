from vivo_queries.vdos.thing import Thing

def get_params(connection):
    thing = Thing (connection)
    params = {'Thing': thing,}
    return params

def fill_params(connection, **params):
    #Escape special characters
    params['Thing'].extra = params['Thing'].extra.replace('(', '\\\(')
    params['Thing'].extra = params['Thing'].extra.replace(')', '\\\)')
    params['Thing'].extra = params['Thing'].extra.replace('[', '\\\[')
    params['Thing'].extra = params['Thing'].extra.replace('+', '\\\+')

    return params

def get_query(**params):    
    query = """SELECT ?uri ?issn WHERE {{?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ontology/bibo/Journal> . ?uri <http://purl.org/ontology/bibo/issn> ?issn . FILTER (regex (?issn, "{}")) }}""".format(params['Thing'].extra)

    return query

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(**params)

    print('=' * 20 + "\nFinding n number\n" + '=' * 20)
    response = connection.run_query(q)

    lookup = response.json()


    matches = {}
    for listing in lookup['results']['bindings']:
        issn = parse_json(listing, 'issn')
        url = parse_json(listing, 'uri')
        url_n = url.rsplit('/', 1)[-1]
        matches[url_n] = issn

    return matches

def parse_json(data, search):
    try:
        value = data[search]['value']
    except KeyError as e:
        value = ''

    return value