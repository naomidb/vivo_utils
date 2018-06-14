from jinja2 import Environment

from vivo_utils.vdos.organization import Organization


def get_params(connection):
    organization = Organization(connection)
    params = {'Organization': organization}
    return params


def fill_params(connection, **params):

    params['namespace'] = connection.namespace
    params['Organization'].n_number = connection.gen_n()
    return params


def get_triples():
    triples = """\
        <{{namespace}}{{Organization.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Organization> .
        <{{namespace}}{{Organization.n_number}}> <http://www.w3.org/2000/01/rdf-schema#label> "{{Organization.name}}" .
    """

    api_trip = """\
    INSERT DATA {{

        GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2>
        {{
            {TRIPS}
        }}
    }}
        """.format(TRIPS=triples)
    trips = Environment().from_string(api_trip)
    return trips


def run(connection, **params):

    if params['Organization'].n_number:
        return
    else:
        params = fill_params(connection, **params)

    print(params['namespace'])
    q = get_triples()
    print('=' * 20 + "\nCreating new organization\n" + '=' * 20)
    response = connection.run_update(q.render(**params))
    print(response)
    return response
