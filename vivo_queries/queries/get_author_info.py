from author import Author
from queries import get_vcard

def get_params(connection):
    author = Author(connection)
    params = {'Author': author}
    return params

def fill_params(connection, **params):
    params['subj'] = connection.vivo_url + params['Author'].n_number
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

    full_name = parse_json(finding, 'fullname')
    given_name = parse_json(finding, 'given')
    middle_name = parse_json(finding, 'middle')
    last_name = parse_json(finding, 'last')
    phone = parse_json(finding, 'phone')
    email = parse_json(finding, 'email')
    title = parse_json(finding, 'title')
    overview = parse_json(finding, 'overview')
    geofocus = parse_json(finding, 'geofocus')

    info = {'full name': full_name, 'given name': given_name, 'middle name': middle_name, 'last name': last_name, 'phone': phone, 'email': email, 'title': title, 'overview': overview, 'geographic focus': geofocus}
    return info

def parse_json(finding, search):
    try:
        value = finding['results']['bindings'][0][search]['value']
    except KeyError as e:
        value = ''

    return value