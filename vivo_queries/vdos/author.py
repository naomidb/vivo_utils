import urllib
from VDO import VivoDomainObject

class Author(VivoDomainObject):
    def __init__(self, connection):
        self.connection = connection
        self.type = "person"
        self.category = "person"

        self.n_number = None
        self.name = None
        self.first = None
        self.middle = None
        self.last = None
        self.email = None
        self.phone = None
        self.title = None
        self.overview = None
        self.geographic_focus = None
        self.details = ['email', 'phone', 'title']
        self.extra = ['overview', 'geographic_focus']

    def lookup(self, connection):
        params = {'Author': self}
        info = get_author_info.run(connection, **params)
        self.name = info['full name']
        self.first = info['given name']
        self.middle = info['middle name']
        self.last = info['last name']
        self.email = info['email']
        self.phone = info['phone']
        self.title = info['title']
        self.overview = info['overview']
        self.geographic_focus = info['geographic focus']