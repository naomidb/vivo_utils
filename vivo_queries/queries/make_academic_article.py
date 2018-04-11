from jinja2 import Environment

from vivo_queries.vdos.article import Article
from vivo_queries.vdos.author import Author
from vivo_queries.vdos.journal import Journal


def get_params(connection):
    author = Author(connection)
    article = Article(connection)
    journal = Journal(connection)
    params = {'Author': author, 'Article': article, 'Journal': journal}
    return params


def fill_params(connection, **params):
    params['Article'].create_n()
    relationship_id = connection.gen_n()
    params['relationship'] = relationship_id
    params['upload_url'] = connection.vivo_url

    year_id = None
    if params['Article'].publication_year:
        year_id = connection.gen_n()
        params['Article'].final_check(year_id)
        params['year'] = year_id

    # make sure none of the n numbers generated before inserting triples have repeating n numbers
    params['Article'].final_check(relationship_id)
    if params['Journal'] is not None:
        params['Journal'].final_check(relationship_id)
        params['Article'].final_check(params['Journal'].n_number)

    return params


def get_triples(api):
    triples = """\
<{{upload_url}}{{ Article.n_number }}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ontology/bibo/AcademicArticle>  .
<{{upload_url}}{{ Article.n_number }}> <http://www.w3.org/2000/01/rdf-schema#label> "{{ Article.name }}"^^<http://www.w3.org/2001/XMLSchema#string> .

{%- if Article.volume %}
<{{upload_url}}{{ Article.n_number }}> <http://purl.org/ontology/bibo/volume> "{{ Article.volume }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Article.issue %}
<{{upload_url}}{{ Article.n_number }}> <http://purl.org/ontology/bibo/issue> "{{ Article.issue }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Article.start_page %}
<{{upload_url}}{{ Article.n_number }}> <http://purl.org/ontology/bibo/pageStart> "{{ Article.start_page }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Article.end_page %}
<{{upload_url}}{{ Article.n_number }}> <http://purl.org/ontology/bibo/pageEnd> "{{ Article.end_page }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Article.publication_year %}
<{{upload_url}}{{ Article.n_number }}> <http://vivoweb.org/ontology/core#dateTimeValue> <{{upload_url}}{{ year }}> .
<{{upload_url}}{{ year }}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#DateTimeValue> .
<{{upload_url}}{{ year }}> <http://vivoweb.org/ontology/core#dateTime> "{{ Article.publication_year }}-01-01T00:00:00"^^<http://www.w3.org/2001/XMLSchema#string> .
<{{upload_url}}{{ year }}> <http://vivoweb.org/ontology/core#dateTimePrecision> <http://vivoweb.org/ontology/core#yearPrecision> .
{%- endif -%}

{%- if Article.doi %}
<{{upload_url}}{{Article.n_number}}> <http://purl.org/ontology/bibo/doi> "{{ Article.doi }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Article.pmid %}
<{{upload_url}}{{Article.n_number}}> <http://purl.org/ontology/bibo/pmid> "{{ Article.pmid }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Author.n_number %}
<{{upload_url}}{{ relationship }}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#Authorship>  .
<{{upload_url}}{{ relationship }}> <http://vivoweb.org/ontology/core#relates> <{{upload_url}}{{ Article.n_number }}> .
<{{upload_url}}{{ relationship }}> <http://vivoweb.org/ontology/core#relates> <{{upload_url}}{{ Author.n_number }}> .
<{{upload_url}}{{ Article.n_number }}> <http://vivoweb.org/ontology/core#relatedBy> <{{upload_url}}{{ relationship }}> .
{%- endif -%}

{%- if Journal.n_number %}
<{{upload_url}}{{ Article.n_number }}> <http://vivoweb.org/ontology/core#hasPublicationVenue> <{{upload_url}}{{ Journal.n_number }}> .
<{{upload_url}}{{ Journal.n_number }}> <http://vivoweb.org/ontology/core#publicationVenueFor> <{{upload_url}}{{ Article.n_number }}> .
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

    print('=' * 20 + "\nAdding article\n" + '=' * 20)
    response = connection.run_update(q.render(**params))
    return response


def write_rdf(connection, **params):
    params = fill_params(connection, **params)
    q = get_triples(False)

    rdf = q.render(**params)
    return rdf
