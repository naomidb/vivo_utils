import json

class UpdateLog(object):
    def __init__(self):
        self.articles = []
        self.authors = []
        self.journals = []
        self.publishers = []
        self.skips = {}

    def add_to_log(self, collection, label, uri):
        getattr(self, collection).append((label, uri))

    def track_skips(self, pm_type, **params):
        if params['Article'].pmid not in self.skips.keys():
            self.skips[params['Article'].pmid] = {'pubmed type': pm_type,
                                            'doi': params['Article'].doi,
                                            'title': params['Article'].name,
                                            'volume': params['Article'].volume,
                                            'issue': params['Article'].issue,
                                            'start': params['Article'].start_page,
                                            'end': params['Article'].end_page,
                                            'journal': params['Journal'].n_number,
                                            'authors': []}

    def add_author_to_skips(self, pmid, author):
        if author not in self.skips[pmid]['authors']:
            self.skips[pmid]['authors'].append(author)

    def write_skips(self, filepath):
        with open(filepath, 'w') as skipfile:
            json.dump(self.skips, skipfile)

    def create_file(self, filepath):
        with open(filepath, 'w') as msg:
            msg.write('New publications: \n')
            for pub in self.articles:
                msg.write(pub[0] + '   ---   ' + pub[1] + '\n')
            msg.write('\n\nNew publishers: \n')
            for publisher in self.publishers:
                msg.write(publisher[0] + '   ---   ' + publisher[1] + '\n')
            msg.write('\n\nNew journals: \n')
            for journal in self.journals:
                msg.write(journal[0] + '   ---   ' + journal[1] + '\n')
            msg.write('\n\nNew people: \n')
            for person in self.authors:
                msg.write(person[0] + '   ---   ' + person[1] + '\n')