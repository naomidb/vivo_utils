from jinja2 import Environment

from vivo_utils.vdos.organization import Organization


def get_params(connection):
    organization = Organization(connection)
    params = {'Organization': organization}
    return params


def fill_params(connection, **params):
    params['Organization'].n_number = connection.gen_n()
    params['org_uri'] = connection.namespace + params['Organization'].n_number

    if params['Organization'].type == 'academic_dept':
        params['Type'] = 'http://vivoweb.org/ontology/core#Department'
        params['Dep_Type'] = 'http://vivoweb.org/ontology/core#AcademicDepartment'
    elif params['Organization'].type == 'organization':
        params['Type'] = 'http://xmlns.com/foaf/0.1/Organization'
        params['Dep_Type'] = None

    return params


def get_triples(api):
    triples = """\
<{{org_uri}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Organization> .
<{{org_uri}}> <http://www.w3.org/2000/01/rdf-schema#label> "{{Organization.name}}" .
<{{org_uri}}> <http://vitro.mannlib.cornell.edu/ns/vitro/0.7#mostSpecificType> <{{Type}}> .

{%- if Dep_Type %}
<{{org_uri}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{{Dep_Type}}>
{%- endif -%}

{%- if source %}
<{{namespace}}{{org_uri}}> <http://vivo.ufl.edu/ontology/vivo-ufl/harvestedBy> "{{ source }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if harvest_date %}
<{{namespace}}{{org_uri.n_number}}> <http://vivo.ufl.edu/ontology/vivo-ufl/dateHarvested>  "{{ harvest_date }}"^^<http://www.w3.org/2001/XMLSchema#string> .
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

    print('=' * 20 + "\nCreating new organization\n" + '=' * 20)
    response = connection.run_update(q.render(**params))
    return response

def write_rdf(connection, **params):
    params = fill_params(connection, **params)
    q = get_triples(False)

    rdf = q.render(**params)
    return rdf
