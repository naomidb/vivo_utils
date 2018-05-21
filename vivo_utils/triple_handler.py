import sys

class TripleHandler(object):
    def __init__(self, api, connection, log_file=None):
        self.api = api
        self.connection = connection
        self.triples = []
        self.log_file = log_file

    def search_for_label(self, label):
        for trip in self.triples:
            if label in trip:
                uri = trip.split('>', 1)[0]
                number = uri.rsplit('/', 1)[-1]
                return number
        return None

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
        result = query.run(self.connection, **params)
        print(result)

    def add_trips(self, query, **params):
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