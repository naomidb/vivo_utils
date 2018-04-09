from vivo_queries.vdos.VDO import VivoDomainObject

class Article(VivoDomainObject):
    def __init__(self, connection):
        self.connection = connection
        self.type = "academic_article"
        self.category = "publication"

        self.n_number = None
        self.name = None
        self.volume = None
        self.issue = None
        self.start_page = None
        self.end_page = None
        self.publication_year = None
        self.doi = None
        self.pmid = None
        # self.details = ['volume', 'issue', 'start_page', 'end_page', 'publication_year', 'doi', 'pmid']
        self.details = ['name', 'type', 'volume', 'issue', 'start_page', 'end_page', 'publication_year', 'doi', 'pubmed_id']


    def lookup(self, connection):
        params = {'Article': self}
        info = get_article_info.run(connection, **params)
        self.name = info['title']
        self.volume = info['volume']
        self.issue = info['issue']
        self.start_page = info['start page']
        self.end_page = info['end page']
        self.publication_year = info['year']
        self.doi = info['doi']
        self.pmid = info['pmid']
