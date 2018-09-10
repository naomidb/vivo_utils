from jinja2 import Environment

from vivo_utils.queries import make_dateTimeInterval
from vivo_utils.vdos.author import Author
from vivo_utils.vdos.article import Article
from vivo_utils.vdos.grant import Grant
from vivo_utils.vdos.organization import Organization


def get_params(connection):
    grant = Grant(connection)
    award_by = Organization(connection)
    sub_through = Organization(connection)
    admin = Organization(connection)
    sup_grant = Grant(connection)
    pi = Author(connection)
    co_pi = Author(connection)
    article = Article(connection)

    params = {'Grant': grant, 'AwardedBy': award_by, 'SubcontractedThrough': sub_through, 'AdministeredBy': admin, 'SubgrantOf': sup_grant, 'PI': pi, 'CoPI': co_pi, 'SupportedWork': article}
    return params

def fill_params(connection, **params):
    params['Grant'].create_n()
    params['namespace'] = connection.namespace

    # grantload reuses dateTimeIntervals
    if not params['Grant'].interval_n and params['Grant'].start_year:
        params['Grant'].get_interval_n()

    if params['AdministeredBy'].n_number:
        params['admin_ship'] = connection.gen_n()

    if params['PI'].n_number:
        params['PI_ship'] = connection.gen_n()

    if params['CoPI'].n_number:
        params['CoPI_ship'] = connection.gen_n()
    return params

def get_triples(api, part):
    if part==1:
        triples = """\
<{{namespace}}{{Grant.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#Grant> .
<{{namespace}}{{Grant.n_number}}> <http://www.w3.org/2000/01/rdf-schema#label> "{{Grant.name}}"^^<http://www.w3.org/2001/XMLSchema#string> .

{%- if Grant.abstract %}
<{{namespace}}{{Grant.n_number}}> <http://purl.org/ontology/bibo/abstract> "{{Grant.abstract}}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Grant.interval_n %}
<{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#dateTimeInterval> <{{namespace}}{{Grant.interval_n}}> .
{%- endif -%}

{%- if Grant.ps_contract_num %}
<{{namespace}}{{Grant.n_number}}> <http://vivo.ufl.edu/ontology/vivo-ufl/psContractNumber> "{{Grant.ps_contract_num}}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif %}

{%- if Grant.sponsor_award_id %}
<{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#sponsorAwardId> "{{Grant.sponsor_award_id}}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if AwardedBy.n_number %}
<{{namespace}}{{AwardedBy.n_number}}> <http://vivoweb.org/ontology/core#assigns> <{{namespace}}{{Grant.n_number}}> .
<{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#assignedBy> <{{namespace}}{{AwardedBy.n_number}}> .
{%- endif -%}

{%- if SubcontractedThrough.n_number %}
<{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#grantSubcontractedThrough> <{{namespace}}{{SubcontractedThrough.n_number}}> .
<{{namespace}}{{SubcontractedThrough.n_number}}> <http://vivoweb.org/ontology/core#subcontractsGrant> <{{namespace}}{{Grant.n_number}}> .
{%- endif -%}"""

    if part==2:
        triples = """\
{%- if AdministeredBy.n_number %}
<{{namespace}}{{admin_ship}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#AdministratorRole> .
<{{namespace}}{{admin_ship}}> <http://purl.obolibrary.org/obo/RO_0000052> <{{namespace}}{{AdministeredBy.n_number}}> .
<{{namespace}}{{AdministeredBy.n_number}}> <http://purl.obolibrary.org/obo/RO_0000053> <{{namespace}}{{admin_ship}}> .
<{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#relates> <{{namespace}}{{admin_ship}}> .
<{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#relates> <{{namespace}}{{AdministeredBy.n_number}}> .
<{{namespace}}{{AdministeredBy.n_number}}> <http://vivoweb.org/ontology/core#relatedBy> <{{namespace}}{{Grant.n_number}}> .
<{{namespace}}{{AdministeredBy.n_number}}> <http://purl.obolibrary.org/obo/RO_0000053> <{{namespace}}{{admin_ship}}> .
{%- endif -%}

{%- if SubgrantOf.n_number %}
<{{namespace}}{{Grant.n_number}}> <http://purl.obolibrary.org/obo/BFO_0000050> <{{namespace}}{{SubgrantOf.n_number}}> .
<{{namespace}}{{SubgrantOf.n_number}}> <http://purl.obolibrary.org/obo/BFO_0000051> <{{namespace}}{{Grant.n_number}}> .
{%- endif -%}

{%- if SupportedWork.n_number %}
<{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#supportedInformationResource> <{{namespace}}{{SupportedWork.n_number}}> .
<{{namespace}}{{SupportedWork.n_number}}> <http://vivoweb.org/ontology/core#informationResourceSupportedBy> <{{namespace}}{{Grant.n_number}}> .
{%- endif -%}"""

    if part==3:
        triples = """\
{%- if PI.n_number %}
<{{namespace}}{{PI_ship}}> <http://purl.obolibrary.org/obo/RO_0000052> <{{namespace}}{{PI.n_number}}> .
<{{namespace}}{{PI.n_number}}> <http://purl.obolibrary.org/obo/RO_0000053> <{{namespace}}{{PI_ship}}> .
<{{namespace}}{{PI_ship}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#InvestigatorRole> .
<{{namespace}}{{PI_ship}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#ResearcherRole> .
<{{namespace}}{{PI_ship}}> <http://vitro.mannlib.cornell.edu/ns/vitro/0.7#mostSpecificType> <http://vivoweb.org/ontology/core#PrincipalInvestigatorRole> .
<{{namespace}}{{PI_ship}}> <http://vivoweb.org/ontology/core#relatedBy> <{{namespace}}{{Grant.n_number}}> .
<{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#relates> <{{namespace}}{{PI_ship}}> .
{%- endif -%}

{%- if CoPI.n_number %}
<{{namespace}}{{CoPI_ship}}> <http://purl.obolibrary.org/obo/RO_0000052> <{{namespace}}><{{CoPI.n_number}}> .
<{{namespace}}{{CoPI.n_number}}> <http://purl.obolibrary.org/obo/RO_0000053> <{{namespace}}{{CoPI_ship}}> .
<{{namespace}}{{CoPI_ship}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#InvestigatorRole> .
<{{namespace}}{{CoPI_ship}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#ResearcherRole> .
<{{namespace}}{{CoPI_ship}}> <http://vitro.mannlib.cornell.edu/ns/vitro/0.7#mostSpecificType> <http://vivoweb.org/ontology/core#CoPrincipalInvestigatorRole> .
<{{namespace}}{{CoPI_ship}}> <http://vivoweb.org/ontology/core#relatedBy> <{{namespace}}{{Grant.n_number}}> .
<{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#relates> <{{namespace}}{{CoPI_ship}}> .
{%- endif -%}

{%- if source %}
<{{namespace}}{{Grant.n_number}}> <http://vivo.ufl.edu/ontology/vivo-ufl/harvestedBy> "{{ source }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if harvest_date %}
<{{namespace}}{{Grant.n_number}}> <http://vivo.ufl.edu/ontology/vivo-ufl/dateHarvested>  "{{ harvest_date }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif %}"""

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
    q = get_triples(True, 1)

    print('=' * 20 + "\nAdding grant\n" + '=' * 20)
    res = connection.run_update(q.render(**params))

    q2 = get_triples(True, 2)
    res2 = connection.run_update(q.render(**params))

    q3 = get_triples(True, 3)
    res3 = connection.run_update(q.render(**params))

    return (res, res2, res3)

def write_rdf(connection, **params):
    params = fill_params(connection, **params)
    q = get_triples(False, 1)
    q2 = get_triples(False, 2)
    q3 = get_triples(False, 3)

    rdf = (q.render(**params) + q2.render(**params) + q3.render(**params))
    return rdf