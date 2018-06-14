from vivo_utils.vdos.author import Author
from vivo_utils.queries import get_vcard

def get_params(connection):
    author = Author(connection)
    params = {'Author': author}
    return params

def fill_params(connection, **params):
    params['subj'] = connection.namespace + params['Author'].n_number
    params['vcard'] = get_vcard.run(connection, **params)

    return params

def get_query(**params):
    query = """ SELECT ?fullname ?given ?middle ?last ?phone ?email ?title ?overview ?geofocus
            WHERE {{
                OPTIONAL {{ <{subj}> <http://www.w3.org/2000/01/rdf-schema#label> ?fullname . }}
                OPTIONAL {{ <{vcard}> <http://www.w3.org/2006/vcard/ns#givenName> ?given . }}
                OPTIONAL {{ <{vcard}> <http://www.w3.org/2006/vcard/ns#middleName> ?middle . }}
                OPTIONAL {{ <{vcard}> <http://www.w3.org/2006/vcard/ns#lastName> ?last . }}
                OPTIONAL {{ <{vcard}> <http://www.w3.org/2006/vcard/ns#hasTelephone> ?puri . ?puri <http://www.w3.org/2006/vcard/ns#telephone> ?phone . }}
                OPTIONAL {{ <{vcard}> <http://www.w3.org/2006/vcard/ns#hasEmail> ?euri . ?euri <http://www.w3.org/2006/vcard/ns#email> ?email . }}
                OPTIONAL {{ <{vcard}> <http://www.w3.org/2006/vcard/ns#hasTitle> ?turi . ?turi <http://www.w3.org/2006/vcard/ns#title> ?title . }}
                OPTIONAL {{ <{subj}> <http://vivoweb.org/ontology/core#overview> ?overview . }}
                OPTIONAL {{ <{subj}> <http://vivoweb.org/ontology/core#geographicFocus> ?geofocus . }}                
            }}""".format(subj = params['subj'], vcard = params['vcard'])

    return query

def run(connection, **params):
    params = fill_params(connection, **params)
    q = get_query(**params)

    response = connection.run_query(q)
    print(response)
    finding = response.json()

    info = {}
    for listing in finding['results']['bindings']:
        for key in listing.keys():
            if key not in info:
                info[key] = []
            value = parse_json(listing, key)
            info[key].append(value)

    return info

def parse_json(listing, search):
    try:
        value = listing[search]['value']
    except KeyError as e:
        value = ''

    return value