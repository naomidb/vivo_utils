from vivo_utils.queries import get_author_journals
from vivo_utils.queries import get_author_coauthors

class Auth_Match(object):
    def __init__(self, connection):
        self.connection = connection

        self.n_number = None
        self.journals = {}
        self.journal_match = False
        self.coauthors = {}
        self.coauthor_matches = []
        self.coauthor_ratio = 0
        self.points = 0

    def get_journals(self):
        #get journals
        params = get_author_journals.get_params(self.connection)
        params['Author'].n_number = self.n_number
        journal_results = get_author_journals.run(self.connection, **params)
        self.journals = journal_results

    def get_coauthors(self):
        #get co-authors
        params = get_author_coauthors.get_params(self.connection)
        params['Author'].n_number = self.n_number
        coauthor_results = get_author_coauthors.run(self.connection, **params)
        self.coauthors = coauthor_results

    def get_points(self, total):
        overlap = 0
        if journal_match:
            overlap = 1
        overlap = overlap + len(coauthor_matches)
        self.points = overlap/(total + 1)