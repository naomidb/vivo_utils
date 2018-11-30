from vivo_utils.vdos.VDO import VivoDomainObject

class DateTime(VivoDomainObject):
    def __init__(self, connection):
        self.connection = connection
        self.type = "dateTime"
        self.category = "dateTime"
        
        self.n_number = None
        self.year = None
        self.month = None
        self.day = None
        self.precision = None
        self.date = None
        self.interval = None
        self.details = ['year', 'month', 'day']

    def get_precision(self):
        if self.year:
            if self.month:
                if self.day:
                    self.precision = 'http://vivoweb.org/ontology/core#yearMonthDayPrecision'
                else:
                    self.precision = 'http://vivoweb.org/ontology/core#yearMonthPrecision'
            else:
                self.precision = 'http://vivoweb.org/ontology/core#yearPrecision'

    def get_printable_date(self):
        if self.month:
            month = self.month
        else:
            month = '01'

        if self.day:
            day = self.day
        else:
            day = '01'

        self.date = self.year + '-' + month + '-' + day + 'T00:00:00'