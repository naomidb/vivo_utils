from vivo_utils.vdos.VDO import VivoDomainObject


class Organization(VivoDomainObject):
    def __init__(self, connection):
        self.connection = connection
        self.type = "organization"
        self.category = "organization"

        self.n_number = None
        self.name = None
        self.role = None    
        self.name_details = ['name']
        self.more_details = ['role']

        #If type is department
        self.dep_type = None