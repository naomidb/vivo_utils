from vivo_utils.vdos.VDO import VivoDomainObject
from vivo_utils.queries import make_dateTimeInterval

class Grant(VivoDomainObject):
    def __init__(self, connection):
        self.connection = connection
        self.type = "grant"
        self.category = "grant"

        self.n_number = None
        self.name = None
        self.abstract = None
        self.total_award_amount = None
        self.direct_costs = None
        self.sponsor_award_id = None
        self.ps_contract_num = None

        self.interval_n = None

        self.details = ['name', 'abstract', 'total_award_amount', 'direct_costs',
                        'sponsor_award_id', 'ps_contract_num', 'interval_n']