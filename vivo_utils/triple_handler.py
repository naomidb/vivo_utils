import sys

class TripleHandler(object):
    def __init__(self, api, connection, meta, log_file=None):
        '''
        api     bool    update vivo through the api(True) or create rdf files(False)
        meta    dict    harvest information ('source' and 'harvest_date')
        '''
        self.api = api
        self.connection = connection
        self.triples = []
        self.meta = meta
        self.log_file = log_file


    def search_for_label(self, label):
        for trip in self.triples:
            if label in trip:
                uri = trip.split('>', 1)[0]
                number = uri.rsplit('/', 1)[-1]
                return number
        return None

    def run_checks(self, query, **params):
        stdout = sys.stdout
        if self.log_file:
            sys.stdout = open(self.log_file, 'a+')
        result = query.run(self.connection, **params)
        sys.stdout = stdout
        return result

    def update(self, query, **params):
        stdout = sys.stdout
        if self.log_file:
            sys.stdout = open(self.log_file, 'a+')
        if self.api:
            result = self.upload(query, **params)
        else:
            result = self.add_trips(query, **params)
        sys.stdout = stdout

    def upload(self, query, **params):
        params.update(self.meta)
        result = query.run(self.connection, **params)
        print(result)

    def add_trips(self, query, **params):
        params.update(self.meta)
        result = query.write_rdf(self.connection, **params)
        self.triples.append(result)

    def print_rdf(self, filepath):
        with open(filepath, 'w') as rdf:
            for triple in self.triples:
                rdf.write(triple + '\n')
        if self.log_file:
            with open(self.log_file, 'a+') as log:
                log.write("=" * 15 + "rdf file saved to: " + filepath)
        else:
            print("rdf file saved to " + filepath)