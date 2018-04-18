from vivo_queries.vdos.thing import Thing

def get_params(connection):
    thing = Thing (connection)
    params = {'Thing': thing,}
    return params

def fill_params(connection, **params):
    params['identity'] = ""
    if params['Thing'].type == 'academic_article':
        params['identity'] = 'http://purl.org/ontology/bibo/AcademicArticle'
    elif params['Thing'].type == 'letter':
        params['identity'] = 'http://purl.org/ontology/bibo/Letter'
    elif params['Thing'].type == 'editorial':
        params['identity'] = 'http://vivoweb.org/ontology/core#EditorialArticle'
    elif params['Thing'].type == 'journal':
        params['identity'] = 'http://purl.org/ontology/bibo/Journal'
    elif params['Thing'].type == 'person':
        params['identity'] = 'http://xmlns.com/foaf/0.1/Person'
    elif params['Thing'].type == 'publisher':
        params['identity'] = 'http://vivoweb.org/ontology/core#Publisher'
    elif params['Thing'].type == 'grant':
        params['identity'] = 'http://vivoweb.org/ontology/core#Grant'
    elif params['Thing'].type == 'department':
        params['identity'] = 'http://vivoweb.org/ontology/core#Department'
    elif params['Thing'].type == 'contributor_copi':
        params['identity'] = 'http://vivoweb.org/ontology/core#CoPrincipalInvestigatorRole'
    elif params['Thing'].type == 'contributor_pi':
        params['identity'] = 'http://vivoweb.org/ontology/core#PrincipalInvestigatorRole'
    elif params['Thing'].type == 'organization':
        params['identity'] = 'http://xmlns.com/foaf/0.1/Organization'
    else:
        params['identity'] = 'http://www.w3.org/2002/07/owl#Thing'


    #Escape special characters
    params['Thing'].extra = params['Thing'].extra.replace('(', '\\\(')
    params['Thing'].extra = params['Thing'].extra.replace(')', '\\\)')
    params['Thing'].extra = params['Thing'].extra.replace('[', '\\\[')
    params['Thing'].extra = params['Thing'].extra.replace('+', '\\\+')
    
    #Workaround for escaping parentheses
    # params['Thing'].extra = params['Thing'].extra.replace('(', '[(]')
    # params['Thing'].extra = params['Thing'].extra.replace(')', '[)]')

    return params

def get_query(**params):
    try:
        query = """SELECT ?uri ?label WHERE {{?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{}> . ?uri <http://www.w3.org/2000/01/rdf-schema#label> ?label . FILTER (regex (?label, "{}", "i")) }}""".format(params['identity'], params['Thing'].extra)
    except UnicodeEncodeError as e:
        print(e)
        print('Error in: ')
        print(params['Thing'].extra)
        exit()

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
