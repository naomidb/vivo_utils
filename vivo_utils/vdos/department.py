from vivo_utils.vdos.VDO import VivoDomainObject


class Department(VivoDomainObject):
    def __init__(self, connection):
        self.connection = connection
        self.type = "department"
        self.category = "department"

        self.n_number = None
        self.name = None
        self.dep_type = None
        self.name_details = ['name']
        self.more_details = ['dep_type']
