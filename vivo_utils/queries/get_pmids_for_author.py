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
    query = """
SELECT ?pmid
WHERE {{
    <{}> <http://vivoweb.org/ontology/core#relatedBy> ?relation .
    ?relation <http://vivoweb.org/ontology/core#relates> ?article .
    ?article <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ontology/bibo/AcademicArticle> .
    ?article <http://purl.org/ontology/bibo/pmid> ?pmid .
}} """.format(params['author_url'])

    return query

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(**params)

    print('=' * 20 + "\nGenerating Associated PMIDs for Author\n" + '=' * 20)
    response = connection.run_query(q)
    print(response)

    pmid_dump = response.json()
    pmid_list = []
    for listing in pmid_dump['results']['bindings']:
        pmid = parse_json(listing, 'pmid')
        pmid_list.append(pmid)

    return pmid_list

def parse_json(data, search):
    try:
        value = data[search]['value']
    except KeyError as e:
        value = ''

    return value