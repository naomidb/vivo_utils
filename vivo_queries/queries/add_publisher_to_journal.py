from vivo_queries.vdos.article import Article
from vivo_queries.vdos.author import Author
from vivo_queries.queries import make_publisher

def get_params(connection):
    article = Article(connection)
    author = Author(connection)
    params = {'Article': article, 'Author': author}
    return params

def fill_params(connection, **params):
    if not params['Publisher'].n_number:
        make_publisher.run(connection, **params)
    publisher_url = connection.vivo_url + params['Publisher'].n_number
    journal_url = connection.vivo_url + params['Journal'].n_number

    return params

def get_triples(api, **params):
    triples = """
        INSERT DATA {{
            GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2>
            {{
                <{PUBLISHER}> <http://vivoweb.org/ontology/core#publisherOf> <{JOURNAL}> .
                <{JOURNAL}> <http://vivoweb.org/ontology/core#publisher> <{PUBLISHER}> .
            }}
        }}
    """.format(PUBLISHER = publisher_url, JOURNAL = journal_url)

    if api:
        api_trip = """\
        INSERT DATA {{
            GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2>
            {{
              {TRIPS}
            }}
        }}
            """.format(TRIPS=triples)

        return api_trip

    else:
        return triples

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_triples(True, **params)

    print('=' * 20 + "\nAssociating author with pub\n" + '=' * 20)
    response = connection.run_update(q)
    return response

def write_rdf():
    params = fill_params(connection, **params)
    rdf = get_triples(False, **params)

    return rdf