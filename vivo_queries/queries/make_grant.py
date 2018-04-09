from jinja2 import Environment

from vivo_queries.vdos.article import Article
from vivo_queries.vdos.contributor import Contributor
from vivo_queries.vdos.grant import Grant
from vivo_queries.vdos.organization import Organization


def get_params(connection):
    grant = Grant(connection)
    article = Article(connection)
    pi_contributor = Contributor(connection)
    copi_contributor = Contributor(connection)
    a_department = Organization(connection)
    s_department = Organization(connection)
    organization = Organization(connection)
    params = {'Grant': grant, 'SupportedWork': article, 'Contributor_PI': pi_contributor, 'Contributor_CoPI': copi_contributor, 'AwardingDepartment': a_department,
              'SubContractedThrough': s_department, 'AdministeredBy': organization}
    return params

def q1_get_triples():
    triples = """\
        <{{upload_url}}{{Grant.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#Grant> .
        <{{upload_url}}{{Grant.n_number}}> <http://www.w3.org/2000/01/rdf-schema#label> "{{Grant.name}}" .

        {%- if Grant.abstract %}
              <{{upload_url}}{{Grant.n_number}}> <http://purl.org/ontology/bibo/abstract> "{{Grant.abstract}}" .
        {%- endif -%}

        {%- if Grant.end_date %}
            <{{upload_url}}{{end_date_id}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#DateTimeValue> .
            <{{upload_url}}{{end_date_id}}> <http://vivoweb.org/ontology/core#dateTime> "{{Grant.end_date}}" .
            <{{upload_url}}{{end_date_id}}> <http://vivoweb.org/ontology/core#dateTimePrecision> <http://vivoweb.org/ontology/core#yearMonthDayPrecision> .
            <{{upload_url}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#dateTimeInterval> <{{upload_url}}{{date_time_interval_id}}> .
            <{{upload_url}}{{date_time_interval_id}}> <http://vivoweb.org/ontology/core#end> <{{upload_url}}{{end_date_id}}> .
            <{{upload_url}}{{date_time_interval_id}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#DateTimeInterval> .
        {%- endif -%}

        {%- if Grant.start_date %}
            <{{upload_url}}{{start_date_id}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#DateTimeValue> .
            <{{upload_url}}{{start_date_id}}> <http://vivoweb.org/ontology/core#dateTime> "{{Grant.start_date}}" .
            <{{upload_url}}{{start_date_id}}> <http://vivoweb.org/ontology/core#dateTimePrecision> <http://vivoweb.org/ontology/core#yearMonthDayPrecision> .
            <{{upload_url}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#dateTimeInterval> <{{upload_url}}{{date_time_interval_id}}> .
            <{{upload_url}}{{date_time_interval_id}}> <http://vivoweb.org/ontology/core#start> <{{upload_url}}{{start_date_id}}> .
            <{{upload_url}}{{date_time_interval_id}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#DateTimeInterval> .
        {%- endif -%}

        {%- if AwardingDepartment.name %}
            <{{upload_url}}{{AwardingDepartment.n_number}}> <http://vivoweb.org/ontology/core#assigns> <{{upload_url}}{{Grant.n_number}}> .
        {%- endif -%}

        {%- if SubContractedThrough.name %}
            <{{upload_url}}{{Grant.n_number}}>	<http://vivoweb.org/ontology/core#grantSubcontractedThrough> <{{upload_url}}{{SubContractedThrough.n_number}}> .
            <{{upload_url}}{{SubContractedThrough.n_number}}> <http://vivoweb.org/ontology/core#subcontractsGrant> <{{upload_url}}{{Grant.n_number}}> .
        {%- endif -%}
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

def q2_get_triples():
    triples = """\
        {%- if AdministeredBy.name %}
            <{{upload_url}}{{AdministeredBy.role}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#AdministratorRole> .
            <{{upload_url}}{{AdministeredBy.role}}> <http://purl.obolibrary.org/obo/RO_0000052> <{{upload_url}}{{AdministeredBy.n_number}}> .
            <{{upload_url}}{{AdministeredBy.n_number}}> <http://purl.obolibrary.org/obo/RO_0000053>	<{{upload_url}}{{AdministeredBy.role}}> .
            <{{upload_url}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#relates> <{{upload_url}}{{AdministeredBy.n_number}}> .
            <{{upload_url}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#relates> <{{upload_url}}{{AdministeredBy.role}}> .
            <{{upload_url}}{{AdministeredBy.n_number}}>	<http://vivoweb.org/ontology/core#relatedBy> <{{upload_url}}{{Grant.n_number}}> .
            <{{upload_url}}{{AdministeredBy.role}}> <http://vivoweb.org/ontology/core#relatedBy> <{{upload_url}}{{Grant.n_number}}> .

        {%- endif -%}

        {%- if Grant.sub_grant_of %}

            {%- if Grant.sub_grant_not_exists %}
                <{{Grant.sub_grant_id}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#Grant> .
                <{{Grant.sub_grant_id}}> <http://www.w3.org/2000/01/rdf-schema#label> "{{Grant.sub_grant_of}}" .
            {%- endif -%}

            <{{upload_url}}{{Grant.n_number}}> <http://purl.obolibrary.org/obo/BFO_0000051> <{{Grant.sub_grant_id}}> .
            <{{Grant.sub_grant_id}}> <http://purl.obolibrary.org/obo/BFO_0000050> <{{upload_url}}{{Grant.n_number}}> .

        {%- endif -%}

        {%- if Grant.total_award_amount %}
              <{{upload_url}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#totalAwardAmount> "{{Grant.total_award_amount}}" .
        {%- endif -%}

        {%- if Grant.direct_costs %}
              <{{upload_url}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#grantDirectCosts> "{{Grant.direct_costs}}" .
        {%- endif -%}

        {%- if Grant.sponsor_award_id %}
              <{{upload_url}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#sponsorAwardId> "{{Grant.sponsor_award_id}}" .
        {%- endif -%}

        {%- if Grant.direct_award_id %}
              <{{upload_url}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#localAwardId> "{{Grant.direct_award_id}}" .
        {%- endif -%}

        {%- if Contributor_PI.name %}
            <{{upload_url}}{{Contributor_PI.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{{Contributor_PI.type}}> .
            <{{upload_url}}{{Contributor_PI.n_number}}> <http://purl.obolibrary.org/obo/RO_0000052> <{{upload_url}}{{Contributor_PI.person_id}}> .
            <{{upload_url}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#relates> <{{upload_url}}{{Contributor_PI.person_id}}> .
            <{{upload_url}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#relates> <{{upload_url}}{{Contributor_PI.n_number}}> .
            <{{upload_url}}{{Contributor_PI.n_number}}> <http://vivoweb.org/ontology/core#relatedBy> <{{upload_url}}{{Grant.n_number}}> .
        {%- endif -%}

        {%- if Contributor_CoPI.name %}
            <{{upload_url}}{{Contributor_CoPI.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{{Contributor_CoPI.type}}> .
            <{{upload_url}}{{Contributor_CoPI.n_number}}> <http://purl.obolibrary.org/obo/RO_0000052> <{{upload_url}}{{Contributor_CoPI.person_id}}> .
            <{{upload_url}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#relates> <{{upload_url}}{{Contributor_CoPI.person_id}}> .
            <{{upload_url}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#relates> <{{upload_url}}{{Contributor_CoPI.n_number}}> .
            <{{upload_url}}{{Contributor_CoPI.n_number}}> <http://vivoweb.org/ontology/core#relatedBy> <{{upload_url}}{{Grant.n_number}}> .
        {%- endif -%}

        {%- if SupportedWork.name %}
            <{{upload_url}}{{Grant.n_number}}>	<http://vivoweb.org/ontology/core#supportedInformationResource> <{{SupportedWork.n_number}}> .
            <{{SupportedWork.n_number}}> <http://vivoweb.org/ontology/core#informationResourceSupportedBy> <{{upload_url}}{{Grant.n_number}}> .

        {%- endif -%}
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

def fill_params(connection, **params):

    params['Grant'].create_n()
    params['upload_url'] = connection.vivo_url

    if params['AdministeredBy']:
        params['AdministeredBy'].role = connection.gen_n()

    # Start Date
    if params['Grant'].start_date:
        params['start_date_id'] = connection.gen_n()

    # End Date
    if params['Grant'].end_date:
        params['end_date_id'] = connection.gen_n()

    if params['Grant'].start_date or params['Grant'].end_date:
        params['date_time_interval_id'] = connection.gen_n()

    # Sub Grant
    if params['Grant'].sub_grant_of:

        # Check if department already exists
        query = "SELECT ?n_number WHERE {?n_number <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#Grant> . " + "?n_number <http://www.w3.org/2000/01/rdf-schema#label> \"" + params['Grant'].sub_grant_of + "\"}"
        response = (connection.run_query(query)).json()

        if not response['results']['bindings']:
            params['Grant'].sub_grant_not_exists = True
            params['Grant'].sub_grant_id = connection.vivo_url + connection.gen_n()
        else:
            params['Grant'].sub_grant_not_exists = False
            params['Grant'].sub_grant_id = response['results']['bindings'][0]['n_number']['value']

    return params

def run(connection, **params):

    if params['Grant'].n_number:
        return
    else:
        params = fill_params(connection, **params)
    q1 = q1_get_triples()
    q2 = q2_get_triples()

    print('=' * 20 + "\nCreating new grant\n" + '=' * 20)
    response = connection.run_update(q1.render(**params))
    print(response)
    response = connection.run_update(q2.render(**params))
    print(response)
    return response
