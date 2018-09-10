class Grantication(object):
    def __init__(self):
        self.title = None
        self.total_award = 0
        self.direct_costs = 0
        self.sponsor_award_id = None
        self.ps_contract_num = None
        self.start_date = None
        self.end_date = None
        self.award_dept = None
        self.subcontract = None
        self.admin = None
        self.pi = None

    def check_dates(self, start, end):
        if start < self.start_date:
            self.start_date = start
        if end > self.end_date:
            self.end_date = end