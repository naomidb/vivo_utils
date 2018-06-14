from vivo_utils.vdos.article import Article

def get_params(connection):
    article = Article(connection)
    params = {'Article': article}
    return params

def fill_params(connection, **params):
    params['subj'] = connection.namespace + params['Article'].n_number

    return params

def get_query(**params):
    query = """ SELECT ?title ?volume ?issue ?start ?finish ?year ?doi ?pmid ?journal ?journal_name ?author
            WHERE {{
                OPTIONAL {{ <{subj}> <http://www.w3.org/2000/01/rdf-schema#label> ?title . }}
                OPTIONAL {{ <{subj}> <http://purl.org/ontology/bibo/volume> ?volume . }}
                OPTIONAL {{ <{subj}> <http://purl.org/ontology/bibo/issue> ?issue . }}
                OPTIONAL {{ <{subj}> <http://purl.org/ontology/bibo/pageStart> ?start . }}
                OPTIONAL {{ <{subj}> <http://purl.org/ontology/bibo/pageEnd> ?finish . }}
                OPTIONAL {{ <{subj}> <http://vivoweb.org/ontology/core#dateTimeValue> ?duri . ?duri <http://vivoweb.org/ontology/core#dateTime> ?year . }}
                OPTIONAL {{ <{subj}> <http://purl.org/ontology/bibo/doi> ?doi . }}
                OPTIONAL {{ <{subj}> <http://purl.org/ontology/bibo/pmid> ?pmid . }}
                OPTIONAL {{ <{subj}>  <http://vivoweb.org/ontology/core#hasPublicationVenue> ?journal . ?journal <http://www.w3.org/2000/01/rdf-schema#label> ?journal_name .}}
            }}""".format(subj = params['subj'])

    return query

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(**params)

    response = connection.run_query(q)
    print(response)
    data = response.json()

    title = parse_json(data, 'title')
    volume = parse_json(data, 'volume')
    issue = parse_json(data, 'issue')
    start = parse_json(data, 'start')
    finish = parse_json(data, 'finish')
    year = parse_json(data, 'year')
    doi = parse_json(data, 'doi')
    pmid = parse_json(data, 'pmid')
    journal_id = parse_json(data, 'journal')
    journal_name = parse_json(data, 'journal_name')

    info = {'title': title, 'volume': volume, 'issue': issue, 'start page': start, 'end page': finish, 'year': year, 'doi': doi, 'pmid': pmid, 'journal': journal_name, 'journal_n': journal_id}
    return info

def parse_json(data, search):
    try:
        value = data['results']['bindings'][0][search]['value']
    except KeyError as e:
        value = ''

    return value
