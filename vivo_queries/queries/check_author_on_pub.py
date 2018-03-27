from vivo_queries.vdos.article import Article
from vivo_queries.vdos.author import Author

def get_params(connection):
    article = Article(connection)
    author = Author(connection)
    params = {'Article': article, 'Author': author}
    return params

def fill_params(connection, **params):
    params['author_url'] = connection.vivo_url + params['Author'].n_number
    params['article_url'] = connection.vivo_url + params['Article'].n_number

    return params

def get_query(**params):
    query = """SELECT ?relation WHERE{{ ?relation <http://vivoweb.org/ontology/core#relates> <{}> . ?relation <http://vivoweb.org/ontology/core#relates> <{}> . }}""".format(params['author_url'], params['article_url'])

    return query

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(**params)
   
    print('=' * 20 + "\nChecking for author\n" + '=' * 20)
    response = connection.run_query(q)

    n_check = response.json()
    try: 
        if n_check['results']['bindings'][0]['relation']:
            return True
    except IndexError as e:
        if str(e) != "list index out of range":
            raise
        else:
            return False
