from vivo_queries.vdos.VDO import VivoDomainObject


class Organization(VivoDomainObject):
    def __init__(self, connection):
        self.connection = connection
        self.type = "organization"
        self.category = "organization"

        self.n_number = None
        self.name = None
        self.role = None
        self.details = ['name']
