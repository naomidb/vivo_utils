from jinja2 import Environment

from vivo_queries.vdos.journal import Journal
from vivo_queries.vdos.publisher import Publisher

def get_params(connection):
    journal = Journal(connection)
    publisher = Publisher(connection)
    params = {'Journal': journal, 'Publisher': publisher}
    return params

def fill_params(connection, **params):
    journal = params.get('Journal')
    params['upload_url'] = connection.vivo_url

    journal.create_n()
    if params['Publisher'].name:
        params['Publisher'].create_n()
        journal.final_check(params['Publisher'].n_number) 
    
    return params

def get_triples(api):
    triples = """\
<{{upload_url}}{{Journal.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ontology/bibo/Journal> .
<{{upload_url}}{{Journal.n_number}}> <http://www.w3.org/2000/01/rdf-schema#label> "{{Journal.name}}"^^<http://www.w3.org/2001/XMLSchema#string> .

{%- if Journal.issn %}
<{{upload_url}}{{Journal.n_number}}> <http://purl.org/ontology/bibo/issn> "{{Journal.issn}}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Publisher.name %}
<{{upload_url}}{{Publisher.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Thing> .
<{{upload_url}}{{Publisher.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#Publisher> .
{%- endif -%}

{%- if Publisher.n_number %}
<{{upload_url}}{{Publisher.n_number}}> <http://vivoweb.org/ontology/core#publisherOf> <{{upload_url}}{{Journal.n_number}}> .
<{{upload_url}}{{Journal.n_number}}> <http://vivoweb.org/ontology/core#publisher> <{{upload_url}}{{Publisher.n_number}}> .
{%- endif -%}         
    """

    if api:
        api_trip = """\
        INSERT DATA {{
            GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2>
            {{
              {TRIPS}
            }}
        }}
            """.format(TRIPS=triples)

        jinj_trip = Environment().from_string(api_trip)
        return jinj_trip

    else:
        trips = Environment().from_string(triples)
        return trips

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_triples(True)

    print('=' * 20 + "\nCreating new journal\n" + '=' * 20)
    response = connection.run_update(q.render(**params))
    return response

def write_rdf(connection, **params):
    params = fill_params(connection, **params)
    q = get_triples(False)

    rdf = q.render(**params)
    return rdf