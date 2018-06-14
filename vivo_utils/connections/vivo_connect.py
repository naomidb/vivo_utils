import random
import requests

from vivo_utils.queries import check_n_value
from vivo_utils.vdos.thing import Thing

class Connection(object):
    def __init__(self, namespace, user, password, u_endpoint, q_endpoint):
        self.user = user
        self.password = password
        self.update_endpoint = u_endpoint
        self.query_endpoint = q_endpoint
        self.namespace = namespace
        self.n_list = []

    def check_n(self, n):
        #create a Thing to test n number
        thing_check = Thing(self)
        thing_check.n_number = n
        thing_check.type = 'thing'
        params = {'Thing': thing_check}
        #use query to check if n number exists
        response = check_n_value.run(self, **params)
        if not response:
            if n in self.n_list:
                response = True
            else:
                self.n_list.append(n) #n is probably being used, so add to n_list to prevent duplicate n
        return response

    def gen_n(self):
        bad_n = True
        while bad_n:
            # get an n
            n = "n" + str(random.randint(1,9999999999))
            # check if n is taken
            bad_n = self.check_n(n)
        return n

    def run_update(self, template):
        print("Query:\n" + template)
        payload = {
            'email': self.user,
            'password': self.password,
            'update': template
        }
        url = self.update_endpoint
        response = requests.post(url, params=payload, verify=False)
        return response

    def run_query(self, template):
        print("Query:\n" + template)
        payload = {
            'email': self.user,
            'password': self.password,
            'query': template
        }
        url = self.query_endpoint
        headers = {'Accept': 'application/sparql-results+json'}
        try:
            response = requests.get(url, params=payload, headers=headers, verify=False)
        except requests.exceptions.ConnectionError as e:
            print("Error with this query.")
            response = None
        return response
