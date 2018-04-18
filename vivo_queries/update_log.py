import json

class UpdateLog(object):
    def __init__(self):
        self.articles = []
        self.authors = []
        self.journals = []
        self.publishers = []
        self.skips = {}
        self.ambiguities = {}

    def add_to_log(self, collection, label, uri):
        getattr(self, collection).append((label, uri))

    def track_ambiguities(self, label, ids):
        if label not in self.ambiguities.keys():
            self.ambiguities[label] = ids

    def add_n_to_ambiguities(self, label, number):
        if label in self.ambiguities.keys():
            self.ambiguities[label].append(number)

    def track_skips(self, pub_id, pub_type, **params):     
        if pub_id not in self.skips.keys():
            self.skips[pub_id] = {'pubmed type': pub_type,
                                            'doi': params['Article'].doi,
                                            'title': params['Article'].name,
                                            'volume': params['Article'].volume,
                                            'issue': params['Article'].issue,
                                            'start': params['Article'].start_page,
                                            'end': params['Article'].end_page,
                                            'journal': params['Journal'].n_number,
                                            'authors': []}

    def add_author_to_skips(self, pub_id, author):
        if author not in self.skips[pub_id]['authors']:
            self.skips[pub_id]['authors'].append(author)

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
                msg.write('New publications: ' + str(len(articles)) + '\n')
                if self.articles:
                    for pub in self.articles:
                        msg.write(pub[0] + '   ---   ' + pub[1] + '\n')

                if self.publishers:
                    msg.write('\n\nNew publishers: ' + str(len(publishers)) + '\n')
                    for publisher in self.publishers:
                        msg.write(publisher[0] + '   ---   ' + publisher[1] + '\n')

                if self.journals:
                    msg.write('\n\nNew journals: ' + str(len(journals)) + '\n')
                    for journal in self.journals:
                        msg.write(journal[0] + '   ---   ' + journal[1] + '\n')

                if self.authors:
                    msg.write('\n\nNew people: ' + str(len(authors)) + '\n')
                    for person in self.authors:
                        msg.write(person[0] + '   ---   ' + person[1] + '\n')

        return created
