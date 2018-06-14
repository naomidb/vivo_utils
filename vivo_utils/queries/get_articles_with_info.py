from vivo_utils.vdos.author import Author

def get_params(connection):
    author = Author(connection)
    params = {'Author': author}
    return params

def fill_params(connection, **params):
    params['namespace'] = connection.namespace

    return params

def get_query(stage, **params):
    if stage == 1:
        query = """ SELECT ?label ?article WHERE {{<{}{}> <http://vivoweb.org/ontology/core#relatedBy> ?relation . ?relation <http://vivoweb.org/ontology/core#relates> ?article . ?article <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ontology/bibo/AcademicArticle> . ?article <http://www.w3.org/2000/01/rdf-schema#label> ?label . }} """.format(params['namespace'], params['Author'].n_number)

    if stage == 2:
        query = """ SELECT ?year WHERE {{<{}{}> <http://vivoweb.org/ontology/core#dateTimeValue> ?duri . ?duri <http://vivoweb.org/ontology/core#dateTime> ?year .}}""".format(params['namespace'], params['pub_n'])

    if stage == 3:
        query = """ SELECT ?label WHERE {{<{}{}> <http://vivoweb.org/ontology/core#hasPublicationVenue> ?puri . ?puri <http://www.w3.org/2000/01/rdf-schema#label> ?label .}}""".format(params['namespace'], params['pub_n'])

    return query

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(1, **params)

    print('=' * 20 + '\nGenerating Article List\n' + '=' * 20)
    response = connection.run_query(q)
    print(response)

    article_dump = response.json()
    all_articles = {}
    for listing in article_dump['results']['bindings']:
        a_name = parse_json(listing, 'label')
        a_url = parse_json(listing, 'article')
        a_n = a_url.rsplit('/', 1)[-1]
        all_articles[a_name] = a_n

    for key, value in all_articles.items():
        params['pub_n'] = value

        q2 = get_query(2, **params)
        viv_res = connection.run_query(q2)
        year_res = viv_res.json()
        if year_res['results']['bindings']:
            pub_year = parse_json(year_res['results']['bindings'][0], 'year')
            pub_year = pub_year[0:4]

        q3 = get_query(3, **params)
        vivRes = connection.run_query(q3)
        pub_res = vivRes.json()
        if pub_res['results']['bindings']:
            publisher = parse_json(pub_res['results']['bindings'][0], 'label')

        with open('log.txt', 'a+') as log:
            log.write("Article: " + key + "\nPublication Year: " + pub_year + "\nPublished in: " + publisher + "\n\n")

    return response

def parse_json(data, search):
    try:
        value = data[search]['value']
    except KeyError as e:
        value = ''

    return value