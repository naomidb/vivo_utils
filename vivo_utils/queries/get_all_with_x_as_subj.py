from vivo_utils.vdos.thing import Thing

def get_params(connection):
    thing = Thing(connection)
    params = {'Thing': thing,}
    return params

def fill_params(connection, **params):
    params['subj'] = connection.namespace + params['Thing'].n_number

    return params

def get_query(**params):
    query = """ SELECT ?s ?p ?o WHERE{{<{}> ?p ?o .}} """.format(params['subj'])

    return query

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(**params)

    print('=' * 20 + '\nGenerating triples\n' + '=' * 20)
    response = connection.run_query(q)
    print(response)

    #Navigate json
    triple_dump = response.json()
    string_tag = 'http://www.w3.org/2001/XMLSchema#string'
    lang_tag = 'en-US'
    date_tag = 'http://www.w3.org/2001/XMLSchema#dateTime'
    triples = []
    for listing in triple_dump['results']['bindings']:
        pred = listing['p']['value']
        obj = listing['o']['value']
        try:
            obj_type = listing['o']['datatype']
        except KeyError as e:
            try:
                obj_type = listing['o']['xml:lang']
            except KeyError as e:
                obj_type = ''
        
        if 'http://' not in obj and 'https://' not in obj:
            trip = '<' + params['subj'] + '> <' + pred + '> "' + obj + '"'
            if obj_type == string_tag:
                trip += '^^<' + string_tag + '>'
            elif obj_type == lang_tag:
                trip += '@' + lang_tag
            elif obj_type == date_tag:
                trip += '^^<' + date_tag + '>'

        else:
            trip = '<' + params['subj'] + '> <' + pred + '> <' + obj + '>'
        triples.append(trip)

    return triples