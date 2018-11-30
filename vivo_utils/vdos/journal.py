from vivo_utils.vdos.VDO import VivoDomainObject

class Journal(VivoDomainObject):
    def __init__(self, connection):
        self.connection = connection
        self.type = "journal"
        self.category = "venue"
        
        self.n_number = None
        self.name = None
        self.issn = None
        self.eissn = None
        self.name_details = ['name']
        self.more_details = ['issn', 'eissn']