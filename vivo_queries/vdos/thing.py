from vivo_queries.vdos.VDO import VivoDomainObject

class Thing(VivoDomainObject):
    def __init__(self, connection):
        #might have to swap type and category
        self.connection = connection
        self.category = "thing"

        self.n_number = None
        self.name = None
        self.type = None
        self.extra = None

        self.details = ['extra']