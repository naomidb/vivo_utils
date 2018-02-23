#import all VDOs you need for your query. The following line is an example, but if you do not need the thing VDO, you may change it.
from vivo_queries.vdos.thing import Thing

#You can also import other queries. If you do this, make sure your params contain information for every query you will be running. Below is an example:
from vivo_queries.queries import make_person

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
    This function will fill in the extra information needed for the query.
    '''

    return params

def get_query(**params):
    '''
    WRITE YOUR QUERY HERE
    This function will place the information from the params into the query and then return the query.
    '''

    #Write your query between the triple quotes. Map the variables in the format function.
    query = (""" SELECT """).format()

    return query

def run(connection, **params):
    #You will call this function when using the API.
    params = fill_params(connection, **params)
    q = get_query(**params)

    #Write what your query is doing between the new line characters below
    print('=' * 20 + "\n\n" + '=' * 20)

    response = connection.run_query(q)

    #You will probably want to parse through the results and return the desired information. Information is returned in json. You can use this line to get the json:
    data = response.json()

def parse_json(data, search):
    '''
    If you are searching for multiple values, it might be easier to use this function to find the actual value. Data is the json and search is the variable you used in your query. If you have the potential to get back multiple results (e.g. finding all articles from a particular journal), you will need to adjust this function.
    '''
    try:
        value = data['results']['bindings'][0][search]['value']
    except KeyError as e:
        value = ''

    # If you have the potential to get back multiple results (e.g. finding all articles from a particular journal), iterate through the lists in bindings and search with this instead:
    try:
        value = data[search]['value']
    except KeyError as e:
        value = ''

    return value

