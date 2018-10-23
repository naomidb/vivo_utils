from vivo_utils.vdos.article import Article
from vivo_utils.queries import get_vcard

def get_params(connection):
    article = Article(connection)
    params = {'Article': article}
    return params

def fill_params(connection, **params):
    params['subj'] = connection.namespace + params['Article'].n_number
    return params

def get_query(**params):
    query = """ SELECT ?author_name
            WHERE {{
                <{subj}> <http://vivoweb.org/ontology/core#relatedBy> ?relation .
                ?relation <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#Authorship> .
                ?relation <http://vivoweb.org/ontology/core#relates> ?author.
                ?author <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
                ?author <http://www.w3.org/2000/01/rdf-schema#label> ?author_name .
            }}""".format(subj = params['subj'])

    return query

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(**params)

    response = connection.run_query(q)
    print(response)
    finding = response.json()

    authors = []
    for listing in finding['results']['bindings']:
        try:
            author_name = parse_json(listing, 'author_name')
            if author_name not in authors:
                authors.append(author_name)
        except KeyError as e:
            continue

    return authors

def parse_json(listing, search):
    try:
        value = listing[search]['value']
    except KeyError as e:
        value = ''

    return value