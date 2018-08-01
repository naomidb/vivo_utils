import mysql.connector
from time import localtime, strftime

from vivo_utils.connections.pubmed_connect import PUBnnection
from vivo_utils.name_cleaner import clean_name
from vivo_utils.publication import Publication

class Citation(object):
    def __init__(self, data):
        self.data = data

    def check_key(self, paths, data=None):
        if not data:
            data = self.data
        if paths[0] in data:
            trail = data[paths[0]]
            if len(paths) > 1:
                trail = self.check_key(paths[1:], trail)
            return trail
        else:
            return ""

class PHandler(object):
    def __init__(self, email):
        self.pubnnection = PUBnnection(email)

    def get_data(self, query_info, log_file=None):
        if isinstance(query_info, str):
            id_list = self.pubnnection.get_id_list(query_info)
        elif isinstance(query_info, list):
            id_list = query_info
        else:
            raise Exception('Error running pubmed query: check input')

        if log_file:
            with open(log_file, 'a+') as log:
                log.write("\n" + '=' * 10 + "Articles found: " + str(len(id_list)) + '\n')
        results = self.pubnnection.get_details(id_list)
        return results

    def parse_api(self, pm_dump):
        publications = []

        for citing in pm_dump['PubmedArticle']:
            publication = Publication()
            citation = Citation(citing['MedlineCitation'])
            
            publication.title = clean_name(citation.check_key(['Article', 'ArticleTitle'])).title()
            publication.year = str(citation.check_key(['Article', 'Journal', 'JournalIssue', 'PubDate', 'Year']))
            publication.volume = str(citation.check_key(['Article', 'Journal', 'JournalIssue', 'Volume']))
            publication.issue = str(citation.check_key(['Article', 'Journal', 'JournalIssue', 'Issue']))
            publication.pmid = str(citation.check_key(['PMID']))
            publication.journal = clean_name(citation.check_key(['Article', 'Journal', 'Title'])).title()

            try:
                count = 0
                proto_doi = citation.check_key(['Article', 'ELocationID'])[count]
                while proto_doi.attributes['EIdType'] != 'doi':
                    count += 1
                    proto_doi = citation.check_key(['Article', 'ELocationID'])[count]
                publication.doi = str(proto_doi)
            except IndexError as e:
                publication.doi = ''
            
            pages = str(citation.check_key(['Article', 'Pagination', 'MedlinePgn']))
            try:
                start, end = pages.split('-')
            except ValueError as e:
                start = pages
                end = ''
            publication.start_page = start
            publication.end_page = end

            proto_types = citation.check_key(['Article', 'PublicationTypeList'])
            for cat in proto_types:
                publication.types.append(str(cat))

            proto_issn = citation.check_key(['Article', 'Journal', 'ISSN'])
            if proto_issn.attributes['IssnType'] == 'Electronic':
                publication.eissn = str(proto_issn)
            else:
                publication.issn = str(proto_issn)
            
            author_dump = citation.check_key(['Article', 'AuthorList'])
            for person in author_dump:
                lname = fname = ''
                author = Citation(person)
                lname = clean_name(author.check_key(['LastName']))
                fname = clean_name(author.check_key(['ForeName']))
                if lname and fname:
                    name = lname + ', ' + fname
                elif lname:
                    name = lname
                try:
                    count = 0
                    proto_orcid = author.check_key(['Identifier'])[count]
                    while proto_orcid.attributes['Source'] != 'ORCID':
                        count += 1
                        proto_orcid = author.check_key(['Identifier'])[count]
                    orcid = str(proto_orcid).split('/')[-1]
                except IndexError as e:
                    orcid = ''

                publication.authors[name] = orcid

            publications.append(publication)

        return publications

    def prepare_tables(self, c):
        print("Making tables")
        c.execute('''create table if not exists pubmed_pubs
                        (doi text, title text, year text, volume text, issue text, pages text, type text, pmid varchar(15) unique, created_dt text not null, modified_dt text not null, written_by text not null)''')

        c.execute('''create table if not exists pubmed_authors
                        (author varchar(40) unique)''')

        c.execute('''create table if not exists pubmed_journals
                        (issn varchar(30) unique, title text, created_dt text not null, modified_dt text not null, written_by text not null)''')

        c.execute('''create table if not exists pubmed_pub_auth
                        (pmid varchar(15), auth varchar(40), unique (pmid, auth))''')

        c.execute('''create table if not exists pubmed_pub_journ
                        (pmid varchar(15), issn varchar(30), unique (pmid, issn))''')

    def local_add_pubs(self, c, pubs, source):
        print("Adding publications")
        timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
        for pub in pubs:
            pmid = pub[7]
            c.execute('SELECT * FROM pubmed_pubs WHERE pmid=%s', (pmid,))
            rows = c.fetchall()

            if len(rows)==0:
                dataset = (pub + (timestamp, timestamp, source))
                #import pdb
                #pdb.set_trace()
                c.execute('INSERT INTO pubmed_pubs VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', dataset)
            else:
                for row in rows:
                    if row[0:8] != pub:
                        with open('log.txt', 'a+') as log:
                            log.write(timestamp + ' -- ' + 'pubmed_pubs' + '\n' + str(row) + '\n')
                        sql = '''UPDATE pubmed_pubs
                                    SET doi = %s ,
                                        title = %s ,
                                        year = %s ,
                                        volume = %s ,
                                        issue = %s ,
                                        pages = %s ,
                                        type = %s ,
                                        modified_dt = %s ,
                                        written_by = %s
                                    WHERE pmid = %s'''
                        c.execute(sql, (pub[0:7] + (timestamp, source, pub[7])))

    def local_add_authors(self, c, authors):
        print("Adding authors")
        for auth in authors:
            try:
                c.execute('INSERT INTO pubmed_authors VALUES(%s)', (auth,))
            except mysql.connector.errors.IntegrityError as e:
                pass

    def local_add_journals(self, c, journals, source):
        print("Adding journals")
        timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
        for issn, title in journals.items():
            c.execute('SELECT * FROM pubmed_journals WHERE issn=%s', (issn,))
            rows = c.fetchall()

            if len(rows)==0:
                c.execute('INSERT INTO pubmed_journals VALUES (%s, %s, %s, %s, %s)', (issn, title, timestamp, timestamp, source))
            else:
                for row in rows:
                    if row[0:2] != (issn, title):
                        with open('log.txt', 'a+') as log:
                            log.write(timestamp + ' -- ' + 'pubmed_journals' + '\n' + str(row) + '\n')
                        sql = '''UPDATE wos_journals
                                SET title = %s ,
                                    modified_dt = %s ,
                                    written_by = %s
                                WHERE issn = %s'''
                        c.execute(sql, (title, timestamp, source, issn))

    def local_add_pub_auth(self, c, pub_auth):
        print("Adding publication-author linkages")
        for pmid, auth_list in pub_auth.items():
            for auth in auth_list:
                try:
                    c.execute('INSERT INTO pubmed_pub_auth VALUES(%s, %s)', (pmid, auth))
                except mysql.connector.errors.IntegrityError as e:
                    pass

    def local_add_pub_journ(self, c, pub_journ):
        print("Adding publication-journal linkages")
        for pmid, issn in pub_journ.items():
            try:
                c.execute('INSERT INTO pubmed_pub_journ VALUES(%s, %s)', (pmid, issn))
            except mysql.connector.errors.IntegrityError as e:
                pass
