from jinja2 import Environment

from vivo_utils.vdos.publisher import Publisher

def get_params(connection):
    publisher = Publisher(connection)
    params = {'Publisher': publisher}
    return params

def fill_params(connection, **params):
    params['Publisher'].create_n()
    params['namespace'] = connection.namespace

    return params

def get_triples(api, **params):
    triples = """\
<{{namespace}}{{Publisher.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Thing> .
<{{namespace}}{{Publisher.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#Publisher> .
<{{namespace}}{{Publisher.n_number}}> <http://www.w3.org/2000/01/rdf-schema#label> "{{Publisher.name}}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if source %}
<{{namespace}}{{Publisher.n_number}}> <http://vivo.ufl.edu/ontology/vivo-ufl/harvestedBy> "{{ source }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if harvest_date %}
<{{namespace}}{{Publisher.n_number}}> <http://vivo.ufl.edu/ontology/vivo-ufl/dateHarvested>  "{{ harvest_date }}"^^<http://www.w3.org/2001/XMLSchema#string> .
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
    q = get_triples(True, **params)

    print('=' * 20 + "\nCreating new publisher\n" + '=' * 20)
    response = connection.run_update(q.render(**params))
    return response

def write_rdf(connection, **params):
    params = fill_params(connection, **params)
    q = get_triples(False)

    rdf = q.render(**params)
    return rdf