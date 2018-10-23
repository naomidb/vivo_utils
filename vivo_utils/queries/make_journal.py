from jinja2 import Environment

from vivo_utils.vdos.journal import Journal
from vivo_utils.vdos.publisher import Publisher

def get_params(connection):
    journal = Journal(connection)
    publisher = Publisher(connection)
    params = {'Journal': journal, 'Publisher': publisher}
    return params

def fill_params(connection, **params):
    journal = params.get('Journal')
    params['namespace'] = connection.namespace

    journal.create_n()
    if params['Publisher'].name:
        params['Publisher'].create_n()
        journal.final_check(params['Publisher'].n_number) 
    
    return params

def get_triples(api):
    triples = """\
<{{namespace}}{{Journal.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ontology/bibo/Journal> .
<{{namespace}}{{Journal.n_number}}> <http://www.w3.org/2000/01/rdf-schema#label> "{{Journal.name}}"^^<http://www.w3.org/2001/XMLSchema#string> .

{%- if Journal.issn %}
<{{namespace}}{{Journal.n_number}}> <http://purl.org/ontology/bibo/issn> "{{Journal.issn}}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Publisher.name %}
<{{namespace}}{{Publisher.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Thing> .
<{{namespace}}{{Publisher.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#Publisher> .
{%- endif -%}

{%- if Publisher.n_number %}
<{{namespace}}{{Publisher.n_number}}> <http://vivoweb.org/ontology/core#publisherOf> <{{namespace}}{{Journal.n_number}}> .
<{{namespace}}{{Journal.n_number}}> <http://vivoweb.org/ontology/core#publisher> <{{namespace}}{{Publisher.n_number}}> .
{%- endif -%}

{%- if source %}
<{{namespace}}{{Journal.n_number}}> <http://vivo.ufl.edu/ontology/vivo-ufl/harvestedBy> "{{ source }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if harvest_date %}
<{{namespace}}{{Journal.n_number}}> <http://vivo.ufl.edu/ontology/vivo-ufl/dateHarvested>  "{{ harvest_date }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif %}
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