from jinja2 import Environment

from vivo_utils.vdos.article import Article
from vivo_utils.vdos.contributor import Contributor
from vivo_utils.vdos.grant import Grant
from vivo_utils.vdos.organization import Organization


def get_params(connection):
    """
    Initializes the Grant object with the params as per the structure of the Grant. For structure of Grants,
    visit https://github.com/roukna/owl-post/blob/develop/documents/Grant%20structure.pdf.
    :param connection:
    :return:
    """
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
    """
    Prepares the template for the query to load first half of the data. If we tried loading the entire data at once
    as a part of a single query, it was throwing HTTP error. Breaking it into two parts did the work.
    :return:
    """
    triples = """\
        <{{namespace}}{{Grant.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#Grant> .
        <{{namespace}}{{Grant.n_number}}> <http://www.w3.org/2000/01/rdf-schema#label> "{{Grant.name}}" .

        {%- if Grant.abstract %}
              <{{namespace}}{{Grant.n_number}}> <http://purl.org/ontology/bibo/abstract> "{{Grant.abstract}}" .
        {%- endif -%}

        {%- if Grant.end_date %}
            <{{namespace}}{{end_date_id}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#DateTimeValue> .
            <{{namespace}}{{end_date_id}}> <http://vivoweb.org/ontology/core#dateTime> "{{Grant.end_date}}" .
            <{{namespace}}{{end_date_id}}> <http://vivoweb.org/ontology/core#dateTimePrecision> <http://vivoweb.org/ontology/core#yearMonthDayPrecision> .
            <{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#dateTimeInterval> <{{namespace}}{{date_time_interval_id}}> .
            <{{namespace}}{{date_time_interval_id}}> <http://vivoweb.org/ontology/core#end> <{{namespace}}{{end_date_id}}> .
            <{{namespace}}{{date_time_interval_id}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#DateTimeInterval> .
        {%- endif -%}

        {%- if Grant.start_date %}
            <{{namespace}}{{start_date_id}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#DateTimeValue> .
            <{{namespace}}{{start_date_id}}> <http://vivoweb.org/ontology/core#dateTime> "{{Grant.start_date}}" .
            <{{namespace}}{{start_date_id}}> <http://vivoweb.org/ontology/core#dateTimePrecision> <http://vivoweb.org/ontology/core#yearMonthDayPrecision> .
            <{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#dateTimeInterval> <{{namespace}}{{date_time_interval_id}}> .
            <{{namespace}}{{date_time_interval_id}}> <http://vivoweb.org/ontology/core#start> <{{namespace}}{{start_date_id}}> .
            <{{namespace}}{{date_time_interval_id}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#DateTimeInterval> .
        {%- endif -%}

        {%- if AwardingDepartment.name %}
            <{{namespace}}{{AwardingDepartment.n_number}}> <http://vivoweb.org/ontology/core#assigns> <{{namespace}}{{Grant.n_number}}> .
        {%- endif -%}

        {%- if SubContractedThrough.name %}
            <{{namespace}}{{Grant.n_number}}>	<http://vivoweb.org/ontology/core#grantSubcontractedThrough> <{{namespace}}{{SubContractedThrough.n_number}}> .
            <{{namespace}}{{SubContractedThrough.n_number}}> <http://vivoweb.org/ontology/core#subcontractsGrant> <{{namespace}}{{Grant.n_number}}> .
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
    """
    Prepares the template for the query to load second half of the data.
    :return:
    """
    triples = """\
        {%- if AdministeredBy.name %}
            <{{namespace}}{{AdministeredBy.role}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#AdministratorRole> .
            <{{namespace}}{{AdministeredBy.role}}> <http://purl.obolibrary.org/obo/RO_0000052> <{{namespace}}{{AdministeredBy.n_number}}> .
            <{{namespace}}{{AdministeredBy.n_number}}> <http://purl.obolibrary.org/obo/RO_0000053>	<{{namespace}}{{AdministeredBy.role}}> .
            <{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#relates> <{{namespace}}{{AdministeredBy.n_number}}> .
            <{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#relates> <{{namespace}}{{AdministeredBy.role}}> .
            <{{namespace}}{{AdministeredBy.n_number}}>	<http://vivoweb.org/ontology/core#relatedBy> <{{namespace}}{{Grant.n_number}}> .
            <{{namespace}}{{AdministeredBy.role}}> <http://vivoweb.org/ontology/core#relatedBy> <{{namespace}}{{Grant.n_number}}> .

        {%- endif -%}

        {%- if Grant.sub_grant_of %}

            {%- if Grant.sub_grant_not_exists %}
                <{{Grant.sub_grant_id}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#Grant> .
                <{{Grant.sub_grant_id}}> <http://www.w3.org/2000/01/rdf-schema#label> "{{Grant.sub_grant_of}}" .
            {%- endif -%}

            <{{namespace}}{{Grant.n_number}}> <http://purl.obolibrary.org/obo/BFO_0000051> <{{Grant.sub_grant_id}}> .
            <{{Grant.sub_grant_id}}> <http://purl.obolibrary.org/obo/BFO_0000050> <{{namespace}}{{Grant.n_number}}> .

        {%- endif -%}

        {%- if Grant.total_award_amount %}
              <{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#totalAwardAmount> "{{Grant.total_award_amount}}" .
        {%- endif -%}

        {%- if Grant.direct_costs %}
              <{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#grantDirectCosts> "{{Grant.direct_costs}}" .
        {%- endif -%}

        {%- if Grant.sponsor_award_id %}
              <{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#sponsorAwardId> "{{Grant.sponsor_award_id}}" .
        {%- endif -%}

        {%- if Grant.direct_award_id %}
              <{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#localAwardId> "{{Grant.direct_award_id}}" .
        {%- endif -%}

        {%- if Contributor_PI.name %}
            <{{namespace}}{{Contributor_PI.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{{Contributor_PI.type}}> .
            <{{namespace}}{{Contributor_PI.n_number}}> <http://purl.obolibrary.org/obo/RO_0000052> <{{namespace}}{{Contributor_PI.person_id}}> .
            <{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#relates> <{{namespace}}{{Contributor_PI.person_id}}> .
            <{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#relates> <{{namespace}}{{Contributor_PI.n_number}}> .
            <{{namespace}}{{Contributor_PI.n_number}}> <http://vivoweb.org/ontology/core#relatedBy> <{{namespace}}{{Grant.n_number}}> .
        {%- endif -%}

        {%- if Contributor_CoPI.name %}
            <{{namespace}}{{Contributor_CoPI.n_number}}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{{Contributor_CoPI.type}}> .
            <{{namespace}}{{Contributor_CoPI.n_number}}> <http://purl.obolibrary.org/obo/RO_0000052> <{{namespace}}{{Contributor_CoPI.person_id}}> .
            <{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#relates> <{{namespace}}{{Contributor_CoPI.person_id}}> .
            <{{namespace}}{{Grant.n_number}}> <http://vivoweb.org/ontology/core#relates> <{{namespace}}{{Contributor_CoPI.n_number}}> .
            <{{namespace}}{{Contributor_CoPI.n_number}}> <http://vivoweb.org/ontology/core#relatedBy> <{{namespace}}{{Grant.n_number}}> .
        {%- endif -%}

        {%- if SupportedWork.name %}
            <{{namespace}}{{Grant.n_number}}>	<http://vivoweb.org/ontology/core#supportedInformationResource> <{{namespace}}{{SupportedWork.n_number}}> .
            <{{namespace}}{{SupportedWork.n_number}}> <http://vivoweb.org/ontology/core#informationResourceSupportedBy> <{{namespace}}{{Grant.n_number}}> .

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
    params['namespace'] = connection.namespace

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
            params['Grant'].sub_grant_id = connection.namespace + connection.gen_n()
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
