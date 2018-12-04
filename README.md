# vivo_utils
Tools for interacting with VIVO and various data sources

## Purpose
vivo_utils contains a collection of pre-written queries for getting information from your VIVO database or changing the information in your VIVO database without needing to know any SPARQL. Simply fill in the variables specified by the VivoDomainObjects and the query will be written for you (and can be run via the Connection object). By accessing the repo directly, you can also find an added functionality for creating new queries (however, this requires some knowledge of SPARQL).

## Usage
vivo_utils has limited functionality on its own and is meant to be used in conjunction with other programs. [Owls](https://github.com/naomidb/owl-post) is one example, which allows you to manually fill in information for the queries via the command line.

## Connections and Handlers
Connectiors create the connections with various APIs while handlers handle data parsing to prepare data for conforming to VIVO. There are currently three connectors (VIVO, PubMed, Web of Science) and two handlers (PubMed, Web of Science).

## Queries
Queries to insert into or get data from VIVO

### Query Types
Queries have a select set of key words that they start with and use either the query or update API.

| Name   | Type   | Description                                       |
|--------|--------|---------------------------------------------------|
| Add    | Update | Add a relationship between two existing entities. |
| Check  | Query  | Check if something exists. Returns a boolean.     |
| Delete | Update | Remove data from VIVO.                            |
| Get    | Query  | Get data from VIVO.                               |
| Make   | Update | Make a new entity in VIVO.                        |
| Merge  | Update | Merge two entities in VIVO.                       |

## VDOs
VDOs represent the types of Things that exist in VIVO. They hold data to be used in preparing queries and updates to VIVO. VDOs are meant to be as broad as possible and the 'type' attribute can be used to specify. For instance, academic articles, editorial articles, and letters would all be part of the Article VDO. The 'Thing' VDO is technically broad enough to include all types, but is used when many different objects could fill a query. The list of VDOs are:
Article
Author
DateTime
Department
Grant
Journal
Organization
Publisher
Thing

## Matching with vivo_log, input_matcher, and auth_match
When ingests are trying to match new entities to existing ones in VIVO, they can do so through input_matcher and vivo_log. When starting an ingest, use vivo_log to create a temporary database of entities in VIVO (which precludes the timely process of constantly label matching via the API), Input_matcher will then perform matches through that database. Additionally, input_matcher can do more sophisticated matching of authors using auth_matches to calculate points per potential match by comparing coauthors and journals to the coauthors and journals of the incoming author.

The advanced author_matching provides points for every coauthor match and journal match. The best match is then compared to the second-best match. If the best match is x times better than the second-best, it is returned. The default value for x is 2, but this can be changed via giving a different parameter.

## Publication and Grantication
These objects are used to store data in the interim between input and vivo-formatted output.