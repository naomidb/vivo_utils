from vivo_queries.vdos.VDO import VivoDomainObject

class Publisher(VivoDomainObject):
    def __init__(self, connection):
        self.connection = connection
        self.type = "publisher"
        self.category = "publisher"
        
        self.n_number = None
        self.name = None
        self.details = []