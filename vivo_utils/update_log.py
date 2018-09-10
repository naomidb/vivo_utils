import json

class UpdateLog(object):
    def __init__(self):
        self.articles = []
        self.authors = []
        self.journals = []
        self.publishers = []
        self.grants = []
        self.organizations = []
        self.citations = {}
        self.skips = {}
        self.ambiguities = {}

    def add_to_log(self, collection, label, uri):
        getattr(self, collection).append((label, uri))

    def add_citation(self, publication, uri):
        citation = ''
        names = []
        for author in publication.authors:
            last = rest = name = ''
            try:
                last, rest = author.split(', ')
                name = last + ', ' + rest[0:1] + '.'
            except ValueError as e:
                name = author
            names.append(name)
        if names:
            name_string = ', '.join(names)
            if not citation.endswith('.'):
                citation += '.'
            name_string += ' '
            citation = name_string

        if publication.year:
            citation += '(' + publication.year + '). '

        citation += publication.title
        if not publication.title.endswith('.'):
            citation += '. '
        else:
            citation += ' '

        if publication.journal:
            citation += publication.journal
            if publication.volume or publication.issue or publication.start_page:
                citation += ', '
                if publication.volume:
                    citation += publication.volume
                if publication.issue:
                    citation += '(' + publication.issue + ')'
                if publication.start_page:
                    if not citation.endswith(', '):
                        citation += ', '
                    citation += publication.start_page
                    if publication.end_page:
                        citation += '-' + publication.end_page
            citation += '.'
        self.citations[uri] = citation

    def track_ambiguities(self, label, ids):
        if label not in self.ambiguities.keys():
            self.ambiguities[label] = ids

    def add_n_to_ambiguities(self, label, number):
        if label in self.ambiguities.keys():
            self.ambiguities[label].append(number)

    def track_skips(self, pub_id, pub_types, **params):     
        if pub_id not in self.skips.keys():
            self.skips[pub_id] = {'type': pub_types,
                                'doi': params['Article'].doi,
                                'title': params['Article'].name,
                                'volume': params['Article'].volume,
                                'issue': params['Article'].issue,
                                'start': params['Article'].start_page,
                                'end': params['Article'].end_page,
                                'journal': params['Journal'].n_number,
                                'authors': {}}

    def add_author_to_skips(self, pub_id, author, orcid):
        if author not in self.skips[pub_id]['authors'].keys():
            self.skips[pub_id]['authors'][author] = orcid

    def write_disam_file(self, filepath):
        if self.ambiguities:
            with open(filepath, 'w') as ambfile:
                json.dump(self.ambiguities, ambfile)

    def write_skips(self, filepath):
        if self.skips:
            with open(filepath, 'w') as skipfile:
                json.dump(self.skips, skipfile)

    def create_file(self, filepath):
        created = False
        if self.articles or self.authors or self.journals or self.publishers:
            created = True
            with open(filepath, 'w') as msg:
                if self.articles:
                    msg.write('New publications: ' + str(len(self.articles)) + '\n')
                    for pub in self.articles:
                        msg.write(pub[0] + '   ---   ' + pub[1] + '\n')

                if self.publishers:
                    msg.write('\n\nNew publishers: ' + str(len(self.publishers)) + '\n')
                    for publisher in self.publishers:
                        msg.write(publisher[0] + '   ---   ' + publisher[1] + '\n')

                if self.journals:
                    msg.write('\n\nNew journals: ' + str(len(self.journals)) + '\n')
                    for journal in self.journals:
                        msg.write(journal[0] + '   ---   ' + journal[1] + '\n')

                if self.authors:
                    msg.write('\n\nNew people: ' + str(len(self.authors)) + '\n')
                    for person in self.authors:
                        msg.write(person[0] + '   ---   ' + person[1] + '\n')

                if self.grants:
                    msg.write('\n\nNew grants: ' + str(len(self.grants)) + '\n')
                    for grant in self.grants:
                        msg.write(grant[0] + '   ---   ' + grant[1] + '\n')

                if self.organizations:
                    msg.write('\n\nNew organizations: ' + str(len(self.organizations)) + '\n')
                    for org in self.organizations:
                        msg.write(org[0] + '   ---   ' + org[1] + '\n')

        if self.articles:
            with open('citations.txt', 'w') as cite:
                json.dump(self.citations, cite)
        return created

    def create_citation_file(self, filepath):
        created = False
        if self.citations:
            created = True
            message = '''\
                        <!DOCTYPE html>\
                        <html>\
                        <head>\
                            <title>VIVO Uploads</title>\
                        </head>\
                        <body>'''
            message += '<h3>' + str(len(self.articles)) + ' new publications</h3>'            
            for uri, cite in self.citations.items():
                message += '<p>' + cite + '</p>'
                message += '<p>(<a href="' + uri + '" target="_blank">VIVO Entry</a>)</p>'
            message += '''\
                        </body>
                        </html>'''
            with open(filepath, 'w') as msg:
                msg.write(message)
        return created