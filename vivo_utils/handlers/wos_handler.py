from bibtexparser import loads
import xml.etree.ElementTree as ET

from vivo_utils.name_cleaner import clean_name
from vivo_utils.publication import Publication
from vivo_utils.connections.wos_connect import WOSnnection

class WHandler(object):
    def __init__(self, credentials, connect=True):
        if connect:
            self.wosnnection = WOSnnection(credentials)

    def bib2csv(self, bib_file):
        bib_str = ""
        with open(bib_file, 'r') as bib:
            for line in bib:
                bib_str += line

        bib_data = loads(bib_str)
        csv_data = {}
        row = 0
        col_names = set(y for x in bib_data.entries for y in x.keys())

        for x in bib_data.entries:
            row += 1
            csv_data[row] = {}

            for col_name in col_names:
                v = x.get(col_name, '')
                v = v.replace('\n', ' ')
                v = v.replace('\r', ' ')
                v = v.replace('\t', ' ')
                csv_data[row][col_name] = v
        return csv_data

    def parse_csv(self, info):
        publications = []

        for number, data in info.items():
            publication = Publication()

            author_str = data['author']
            publication.authors = author_str.split(" and ")

            publication.volume = self.find_values(data, 'volume')
            publication.issue = self.find_values(data, 'issue')
            publication.wosid = self.find_values(data, 'unique-id').replace('ISI', 'WOS')
            publication.doi = self.find_values(data, 'doi')
            publication.title = clean_name(self.find_values(data, 'title'))
            publication.year = self.find_values(data, 'year')
            pages = self.find_values(data, 'pages')
            publication.issn = self.find_values(data, 'issn')
            journal = clean_name(self.find_values(data, 'journal').replace('&amp;', '&'))
            publication.journal = journal.title()
            publisher = clean_name(self.find_values(data, 'publisher'))
            publication.publisher = publisher.title()
            try:
                start, end = pages.split('-')
            except ValueError as e:
                start = pages
                end = ''
            publication.start_page = start
            publication.end_page = end
            publication.number = self.find_values(data, 'number')
            publication.type = self.find_values(data, 'type')

            publications.append(publication)

        return publications

    def find_values(self, data, search):
        try:
            value = data[search]
        except KeyError as e:
            value = ''
        return value

    def get_data(self, query, start, end):
        kwargs = {'query': query, 'start': start, 'end': end}
        results = self.wosnnection.run_query(**kwargs)
        return results

    def parse_api(self, results):
        pubs = []
        pub_auth = {}
        authors = []
        journals = {}
        pub_journ = {}

        for result in results:
            root = ET.fromstring(result)
            for record in root.iter('records'):
                doi = issn = jname = year = volume = issue = start = end = ''

                titag = record.find('title')
                title = clean_name(titag.find('value').text)

                tytag = record.find('doctype')
                doctype = tytag.find('value').text

                wosid = record.find('uid').text

                try:
                    autag = record.find('authors')
                    people = autag.findall('value')
                    crowd = [person.text for person in people]
                except AttributeError as e:
                    crowd = []
                    print('No Authors:', title, wosid)

                #DOI, ISSN
                others = record.findall('other')
                for other in others:
                    if other.find('label').text == 'Identifier.Doi':
                        doi = other.find('value').text
                    if other.find('label').text == 'Identifier.Issn':
                        issn = other.find('value').text

                #Pub year, Journal
                sources = record.findall('source')
                for source in sources:
                    if source.find('label').text == 'Published.BiblioYear':
                        year = source.find('value').text
                    if source.find('label').text == 'SourceTitle':
                        journal = source.find('value').text.replace('&amp;', '&')
                        journal = journal.title()
                    if source.find('label').text == 'Volume':
                        volume = source.find('value').text
                    if source.find('label').text == 'Issue':
                        issue = source.find('value').text
                    if source.find('label').text == 'Pages':
                        pages = source.find('value').text
                        try:
                            start, end = pages.split('-')
                        except ValueError as e:
                            start = pages
                        except AttributeError as e:
                            pass

                pubs.append({'doi': doi, 'title': title, 'year': year,
                    'volume': volume, 'issue': issue, 'start': start,
                    'end': end, 'type': doctype, 'wosid': wosid})
                pub_auth[wosid] = crowd
                for author in crowd:
                    if author not in authors:
                        authors.append(author)
                if issn not in journals.keys():
                    journals[issn] = journal
                pub_journ[wosid] = issn

        return (pubs, pub_auth, authors, journals, pub_journ)
