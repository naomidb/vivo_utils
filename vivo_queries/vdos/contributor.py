from vivo_queries.vdos.VDO import VivoDomainObject


class Contributor(VivoDomainObject):
    def __init__(self, connection):
        self.connection = connection
        self.type = "contributor"
        self.category = "contributor"

        self.n_number = None
        self.person_id = None
        self.details = ['name', 'type']
