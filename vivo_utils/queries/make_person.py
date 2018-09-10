from jinja2 import Environment

from vivo_utils.vdos.author import Author

def get_params(connection):
    author = Author(connection)
    params = {'Author': author}
    return params

def fill_params(connection, **params):
    if params['Author'].orcid:
        if not params['Author'].orcid.startswith('http://orcid.org/'):
            params['Author'].orcid = 'http://orcid.org/' + params['Author'].orcid

    params['Author'].create_n()

    params['namespace'] = connection.namespace

    params['vcard'] = connection.gen_n()

    if params['Author'].name:
        params['name_id'] = connection.gen_n()

    if params['Author'].email:
        params['email_id'] = connection.gen_n()

    if params['Author'].phone:
        params['phone_id'] = connection.gen_n()

    if params['Author'].title:
        params['title_id'] = connection.gen_n()

    params['Author'].vcard = params['vcard']
    params['Author'].name_id = params['name_id']

    return params

def get_triples(api):
  triples = """\
<{{namespace}}{{Author.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
<{{namespace}}{{Author.n_number}}> <http://www.w3.org/2000/01/rdf-schema#label> "{{Author.name}}"^^<http://www.w3.org/2001/XMLSchema#string> .
<{{namespace}}{{Author.n_number}}> <http://purl.obolibrary.org/obo/ARG_2000028> <{{namespace}}{{vcard}}> .
<{{namespace}}{{vcard}}> <http://purl.obolibrary.org/obo/ARG_2000029> <{{namespace}}{{Author.n_number}}> .
<{{namespace}}{{vcard}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2006/vcard/ns#Individual> .

{%- if Author.name %}
<{{namespace}}{{vcard}}> <http://www.w3.org/2006/vcard/ns#hasName> <{{namespace}}{{name_id}}> .
<{{namespace}}{{name_id}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2006/vcard/ns#Name> .
{%- endif -%}

{%- if Author.first %}
<{{namespace}}{{name_id}}> <http://www.w3.org/2006/vcard/ns#givenName> "{{Author.first}}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Author.middle %}
<{{namespace}}{{name_id}}> <http://vivoweb.org/ontology/core#middleName> "{{Author.middle}}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Author.last %}
<{{namespace}}{{name_id}}> <http://www.w3.org/2006/vcard/ns#familyName> "{{Author.last}}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Author.email %}
<{{namespace}}{{vcard}}> <http://www.w3.org/2006/vcard/ns#hasEmail> <{{namespace}}{{email_id}}> .
<{{namespace}}{{email_id}}> <http://www.w3.org/2006/vcard/ns#email> "{{Author.email}}"^^<http://www.w3.org/2001/XMLSchema#string> .
<{{namespace}}{{email_id}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2006/vcard/ns#Email> .
<{{namespace}}{{email_id}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2006/vcard/ns#Work> .
{%- endif -%}

{%- if Author.phone %}
<{{namespace}}{{vcard}}> <http://www.w3.org/2006/vcard/ns#hasTelephone> <{{namespace}}{{phone_id}}> .
<{{namespace}}{{phone_id}}> <http://www.w3.org/2006/vcard/ns#telephone> "{{Author.phone}}"^^<http://www.w3.org/2001/XMLSchema#string> .
<{{namespace}}{{phone_id}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2006/vcard/ns#Telephone> .
{%- endif -%}

{%- if Author.title %}
<{{namespace}}{{vcard}}> <http://www.w3.org/2006/vcard/ns#hasTitle> <{{namespace}}{{title_id}}> .
<{{namespace}}{{title_id}}> <http://www.w3.org/2006/vcard/ns#title> "{{Author.title}}"^^<http://www.w3.org/2001/XMLSchema#string> .
<{{namespace}}{{title_id}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2006/vcard/ns#Title> .
{%- endif -%}

{%- if Author.orcid %}
<{{namespace}}{{Author.n_number}}> <http://vivoweb.org/ontology/core#orcidId> "{{Author.orcid}}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif %}

{%- if Author.ufentity %}
<{{namespace}}{{Author.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivo.ufl.edu/ontology/vivo-ufl/UFEntity> .
{%- endif %}

{%- if Author.ufcurrententity %}
<{{namespace}}{{Author.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivo.ufl.edu/ontology/vivo-ufl/UFCurrentEntity> .
{%- endif -%}

{%- if source %}
<{{namespace}}{{Author.n_number}}> <http://vivo.ufl.edu/ontology/vivo-ufl/harvestedBy> "{{ source }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if harvest_date %}
<{{namespace}}{{Author.n_number}}> <http://vivo.ufl.edu/ontology/vivo-ufl/dateHarvested>  "{{ harvest_date }}"^^<http://www.w3.org/2001/XMLSchema#string> .
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

    print('=' * 20 + "\nCreating new person\n" + '=' * 20)
    response = connection.run_update(q.render(**params))
    return response

def write_rdf(connection, **params):
    params = fill_params(connection, **params)
    q = get_triples(False)

    rdf = q.render(**params)
    return rdf
