class VivoDomainObject(object):
    def __init__(self):
        return

    def get_details(self):
        return self.details

    def create_n(self):
        self.n_number = self.connection.gen_n()

    def final_check(self, other_n):
        if self.n_number == other_n:
            self.n_number = self.connection.gen_n()
        return self.n_number