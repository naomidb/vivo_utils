from vivo_utils.vdos.dateTime import DateTime

def get_params(connection):
    start_date = DateTime(connection)
    end_date = DateTime(connection)
    params = {'start_date': start_date, 'end_date': end_date}
    return params

def fill_params(connection, **params):
    params['start_date'].get_precision()
    params['start_date'].get_printable_date()
    params['start_date'].create_n()
    if params['end_date'].year:
        params['end_date'].get_precision()
        params['end_date'].get_printable_date()
        params['end_date'].create_n()

    params['namespace'] = connection.namespace
    params['start_date'].interval = connection.gen_n()
    return params

def get_triples(api, part, **params):
    if part == 1:
        triples = """\
<{namespace}{interval}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#DateTimeInterval> .
<{namespace}{start_n}> <http://vivoweb.org/ontology/core#dateTime> "{start_date}"^^<http://www.w3.org/2001/XMLSchema#dateTime> .
<{namespace}{start_n}> <http://vivoweb.org/ontology/core#dateTimePrecision> <{start_precision}> .
<{namespace}{start_n}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#DateTimeValue> .
<{namespace}{start_n}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.obolibrary.org/obo/BFO_0000001> .
<{namespace}{start_n}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.obolibrary.org/obo/BFO_0000003> .
<{namespace}{start_n}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.obolibrary.org/obo/BFO_0000008> .
<{namespace}{start_n}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.obolibrary.org/obo/BFO_0000148> .
""".format(namespace=params['namespace'], interval=params['start_date'].interval, start_n=params['start_date'].n_number,
            start_date=params['start_date'].date, start_precision=params['start_date'].precision)

    if part == 2:
        triples = """\
<{namespace}{end_n}> <http://vivoweb.org/ontology/core#dateTime> "{end_date}"^^<http://www.w3.org/2001/XMLSchema#dateTime> .
<{namespace}{end_n}> <http://vivoweb.org/ontology/core#dateTimePrecision> <{end_precision}> .
<{namespace}{end_n}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#DateTimeValue> .
<{namespace}{end_n}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.obolibrary.org/obo/BFO_0000001> .
<{namespace}{end_n}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.obolibrary.org/obo/BFO_0000003> .
<{namespace}{end_n}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.obolibrary.org/obo/BFO_0000008> .
""".format(namespace=params['namespace'], end_n=params['end_date'].n_number,
            end_date=params['end_date'].date, end_precision=params['end_date'].precision)

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
    params = fill_params(connection, **params)
    q = get_triples(True, 1, **params)

    print('=' * 20 + "\nMaking DateTime Interval\n" + '=' * 20)
    response = connection.run_update(q)

    if params['end_date'].n_number:
        q2 = get_triples(True, 2, **params)
        res2 = connection.run_update(q2)
        response = (response, res2)
    return response

def write_rdf(connection, **params):
    params = fill_params(connection, **params)
    q = get_triples(False, 1, **params)

    if params['end_date'].n_number:
        q2 = get_triples(False, 2, **params)

    rdf = q + q2
    return rdf