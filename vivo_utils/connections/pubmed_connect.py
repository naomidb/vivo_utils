from Bio import Entrez
from Bio import Medline

class PUBnnection(object):
    def __init__(self, email):
        self.email = email
        self.retmax = 100000
        self.retstart = 0
        self.count_up = 0

    def get_id_list(self, term):
        Entrez.email = self.email
        res = Entrez.esearch(term=term,
                             db='pubmed',
                             retmax=100000,
                             retstart=self.retstart)
        result = Entrez.read(res)
        id_list = result['IdList'] #pull relavent IDs from query
        total = result['Count']

        self.count_up += 100000
        if self.count_up < int(total): #if the number of results exceeds 100,000, you will need to run the query again
            self.retstart += 100000
            id_list += self.get_id_list(term)

        return id_list

    def get_details(self, id_list):
        ids = ','.join(id_list)
        Entrez.email = self.email
        handle = Entrez.efetch(db='pubmed',
                               retmode='xml',
                               id=ids)
        results = Entrez.read(handle)

        return results
