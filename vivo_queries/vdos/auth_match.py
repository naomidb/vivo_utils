class Auth_Match(object):
    def __init__(self):
        self.n_number = None
        self.name = None
        self.pubs = {}
        self.points = 0

    def compare_pubs(self, title):
        for address, pub in self.pubs.items():
            if title.lower() == pub.lower():
                self.points += 1
                return True
        return False