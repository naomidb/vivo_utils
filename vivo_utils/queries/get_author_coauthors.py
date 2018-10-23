from vivo_utils.vdos.author import Author
from vivo_utils.queries import get_vcard

def get_params(connection):
    author = Author(connection)
    params = {'Author': author}
    return params

def run(connection, **params):
    coauthors = {}
    # get all articles
    # get authors for each article