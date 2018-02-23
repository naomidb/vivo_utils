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
    This function will fill in the extra information needed for the query. This is especially relevant for updates which will be making new n numbers.
    Objects have a create_n() function to create an n number. For other necessary n numbers (like the relationships between articles and authors), you can use the gen_n() function on the connection object.
    '''

    return params

def get_triples(api, **params):
    '''
    WRITE YOUR TRIPLES HERE
    This function will place the information from the params into the triples and then return those completed triples.
    '''

    #Write your triples between the triple quotes. Map the variables in the format function.
    triples = ("""""").format()

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
    #You will call this function when using the API.
    params = fill_params(connection, **params)
    q = get_triples(True, **params)

    #Write what your update is doing between the new line characters below
    print('=' * 20 + "\n\n" + '=' * 20)

    response = connection.run_update(q)

    #Return the response code to be sure the update has gone through.
    return response

def write_rdf(connection, **params):
    '''
    This function will return the triples without the surrounding insert statement. Use this to create files that can be manually uploaded.
    '''

    params = fill_params(connection, **params)
    rdf = get_triples(False, **params)

    return rdf
