class Auth_Match(object):
    def __init__(self, connection):
        self.connection = connection

        self.n_number = None
        self.journal_match = False
        self.coauthors = []
        self.coauthor_matches = []
        self.points = 0

    def get_journals(self):
        #get journals
        params = queries.get_author_journals.params(self.connection)
        params['Author'].n_number = self.n_number
        journal_results = queries.get_author_journals.run(self.connection, **params)
        self.journals = journal_results

    def get_coauthors(self):
        #get co-authors
        params = queries.get_author_coauthors.params(self.connection)
        params['Author'].n_number = self.n_number
        coauthor_results = queries.get_author_coauthors.run(self.connection, **params)
        self.coauthors = coauthor_results