#import all VDOs you need for your query. The following line is an example, but if you do not need the thing VDO, you may change it.
from vdos import Thing

def get_params(connection):
    '''
    Create the instances of the objects you will need. Remember that they must all be initialized with connection.
    The params dictionary will be sent back with all of the necessary objects. The key should be the name of the object capitalized.
    example:
    author = Author(connection)
    article = Article(connection)
    params = {'Author': author, 'Article: article}
    '''

    params = {}
    return params

def fill_params(connection, **params):
    '''
    This function will fill in the extra information needed for the query. This is especially relevant for updates which will be making new n numbers.
    Objects have a create_n() function to create an n number. For other necessary n numbers (like the relationships between articles and authors), you can use the gen_n() function on the connection object.
    '''

    return params

def get_triples(connection, **params):
    '''
    WRITE YOUR TRIPLES HERE
    This function will place the information from the params into the triples and then return those completed triples.
    '''

    #Write your triples between the triple quotes. Map the variables in the format function.
    triples = ("""""").format()

    return triples

def run(connection, **params):
    #You will call this function when using the API. It can be used both for queries and updates.
    params = fill_params(connection, **params)
    q = get_triples(connection, **params)

    #Write what your query is doing between the new line characters below
    print('=' * 20 + "\n\n" + '=' * 20)

    #If you are running a query, use this:
    response = connection.run_query(q)
    #If you are running an update, use this:
    response = connection.run_update(q)

    #If you have run a query, you will probably want to parse through the results and return the desired information. Information is returned in json. You can use this line to get the json:
    data = response.json()

    #For updates, you can simply return the response code to be sure the update has gone through.
    return response

def write_rdf(connection, **params):
    '''
    You will only need this function if you are writing an update query. If you will only be querying information from VIVO, you can delete this function.
    '''
    params = fill_params(connection, **params)
    rdf = get_triples(connection, **params)

    return rdf
