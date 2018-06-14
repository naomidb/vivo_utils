from vivo_utils.vdos.article import Article
from vivo_utils.vdos.journal import Journal
from vivo_utils.queries import make_person

def get_params(connection):
    article = Article(connection)
    journal = Journal(connection)
    params = {'Article': article, 'Journal': journal}
    return params

def fill_params(connection, **params):
    if not params['Journal'].n_number:
        make_publisher.run(connection, **params)
    params['article_url'] = connection.namespace + params['Article'].n_number
    params['journal_url'] = connection.namespace + params['Journal'].n_number

    return params

def get_triples(api, **params):
    triples = """
<{ARTICLE}> <http://vivoweb.org/ontology/core#hasPublicationVenue> <{JOURNAL}> .
<{JOURNAL}> <http://vivoweb.org/ontology/core#publicationVenueFor> <{ARTICLE}> .""".format(ARTICLE = params['article_url'], JOURNAL = params['journal_url'])

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

    print('=' * 20 + "\nAssociating journal with pub\n" + '=' * 20)
    response = connection.run_update(q)
    return response

def write_rdf():
    params = fill_params(connection, **params)
    rdf = get_triples(False, **params)

    return rdf