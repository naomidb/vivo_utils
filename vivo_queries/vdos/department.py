from vivo_queries.vdos.VDO import VivoDomainObject


class Department(VivoDomainObject):
    def __init__(self, connection):
        self.connection = connection
        self.type = "department"
        self.category = "department"

        self.n_number = None
        self.name = None
        self.dep_type = None
        self.details = ['name', 'dep_type']
