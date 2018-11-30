from vivo_utils.vdos.author import Author
from vivo_utils.queries import get_articles_for_author
from vivo_utils.queries import get_authors_on_pub

def return_type():
    return "query"

def get_params(connection):
    author = Author(connection)
    params = {'Author': author}
    return params

def run(connection, **params):
    coauthors = {}
    # get all articles
    articles = get_articles_for_author.run(connection, **params)
    # get authors for each article
    pub_params = get_authors_on_pub.get_params(connection)
    for article in articles.keys():
        pub_params['Article'].n_number = article
        author_list = get_authors_on_pub.run(connection, **pub_params)
        coauthors.update(author_list)
    try:
        coauthors.pop(params['Author'].n_number)
    except KeyError:
        pass

    return coauthors