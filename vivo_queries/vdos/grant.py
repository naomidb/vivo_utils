from vivo_queries.vdos.VDO import VivoDomainObject


class Grant(VivoDomainObject):
    def __init__(self, connection):
        self.connection = connection
        self.type = "grant"
        self.category = "grant"

        self.n_number = None
        self.name = None
        self.abstract = None
        self.start_date = None
        self.end_date = None
        self.geographic_focus = None
        self.sub_grant_of = None
        self.provides_funding_for = None
        self.total_award_amount = None
        self.direct_costs = None
        self.sponsor_award_id = None
        self.direct_award_id = None
        self.details = ['name', 'abstract', 'start_date', 'end_date', 'sub_grant_of', 'geographic_focus',
                        'provides_funding_for', 'total_award_amount', 'direct_costs', 'sponsor_award_id',
                        'direct_award_id']
