from jinja2 import Environment

from vivo_utils.vdos.article import Article
from vivo_utils.vdos.author import Author
from vivo_utils.vdos.journal import Journal


def get_params(connection):
    author = Author(connection)
    article = Article(connection)
    article.type = 'editorial'
    journal = Journal(connection)
    params = {'Author': author, 'Article': article, 'Journal': journal}
    
    return params


def fill_params(connection, **params):
    params['Article'].create_n()
    relationship_id = connection.gen_n()
    params['relationship'] = relationship_id
    params['namespace'] = connection.namespace

    year_id = None
    if params['Article'].publication_year:
        year_id = connection.gen_n()
        params['Article'].final_check(year_id)
        params['year'] = year_id

    # make sure none of the n numbers generated before inserting triples have repeating n numbers
    params['Article'].final_check(relationship_id)
    params['Journal'].final_check(relationship_id)
    params['Article'].final_check(params['Journal'].n_number)

    return params


def get_triples(api):
    triples = """\
<{{namespace}}{{ Article.n_number }}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#EditorialArticle>  .
<{{namespace}}{{ Article.n_number }}> <http://www.w3.org/2000/01/rdf-schema#label> "{{ Article.name }}"^^<http://www.w3.org/2001/XMLSchema#string> .

{%- if Article.volume %}
<{{namespace}}{{ Article.n_number }}> <http://purl.org/ontology/bibo/volume> "{{ Article.volume }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Article.issue %}
<{{namespace}}{{ Article.n_number }}> <http://purl.org/ontology/bibo/issue> "{{ Article.issue }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Article.start_page %}
<{{namespace}}{{ Article.n_number }}> <http://purl.org/ontology/bibo/pageStart> "{{ Article.start_page }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Article.end_page %}
<{{namespace}}{{ Article.n_number }}> <http://purl.org/ontology/bibo/pageEnd> "{{ Article.end_page }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Article.publication_year %}
<{{namespace}}{{ Article.n_number }}> <http://vivoweb.org/ontology/core#dateTimeValue> <{{namespace}}{{ year }}> .
<{{namespace}}{{ year }}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#DateTimeValue> .
<{{namespace}}{{ year }}> <http://vivoweb.org/ontology/core#dateTime> "{{ Article.publication_year }}-01-01T00:00:00"^^<http://www.w3.org/2001/XMLSchema#string> .
<{{namespace}}{{ year }}> <http://vivoweb.org/ontology/core#dateTimePrecision> <http://vivoweb.org/ontology/core#yearPrecision> .
{%- endif -%}

{%- if Article.doi %}
<{{namespace}}{{Article.n_number}}> <http://purl.org/ontology/bibo/doi> "{{ Article.doi }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Article.pmid %}
<{{namespace}}{{Article.n_number}}> <http://purl.org/ontology/bibo/pmid> "{{ Article.pmid }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if Author.n_number %}
<{{namespace}}{{ relationship }}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vivoweb.org/ontology/core#Authorship>  .
<{{namespace}}{{ relationship }}> <http://vivoweb.org/ontology/core#relates> <{{namespace}}{{ Article.n_number }}> .
<{{namespace}}{{ relationship }}> <http://vivoweb.org/ontology/core#relates> <{{namespace}}{{ Author.n_number }}> .
<{{namespace}}{{ Article.n_number }}> <http://vivoweb.org/ontology/core#relatedBy> <{{namespace}}{{ relationship }}> .
{%- endif -%}

{%- if Journal.n_number %}
<{{namespace}}{{ Article.n_number }}> <http://vivoweb.org/ontology/core#hasPublicationVenue> <{{namespace}}{{ Journal.n_number }}> .
<{{namespace}}{{ Journal.n_number }}> <http://vivoweb.org/ontology/core#publicationVenueFor> <{{namespace}}{{ Article.n_number }}> .
{%- endif -%}

{%- if source %}
<{{namespace}}{{Article.n_number}}> <http://vivo.ufl.edu/ontology/vivo-ufl/harvestedBy> "{{ source }}"^^<http://www.w3.org/2001/XMLSchema#string> .
{%- endif -%}

{%- if harvest_date %}
<{{namespace}}{{Article.n_number}}> <http://vivo.ufl.edu/ontology/vivo-ufl/dateHarvested>  "{{ harvest_date }}"^^<http://www.w3.org/2001/XMLSchema#string> .
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
