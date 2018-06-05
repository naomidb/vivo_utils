from jinja2 import Environment
import requests
import subprocess
import time

class WOSnnection(object):
    def __init__(self, credentials):
        self.token = None
        self.credentials = credentials
        self.search_url = 'http://search.webofknowledge.com/esti/wokmws/ws/WokSearchLite'
        self.params = {}
        self.params['databaseId'] = 'WOS'
        self.params['collection'] = 'WOS'
        self.params['queryLanguage'] = 'en'
        self.params['firstRecord'] = '1'
        self.params['count'] = '100'

        self.get_token()

    def get_token(self):
        response = subprocess.check_output('curl -H "Authorization: Basic {}" -d "@wos/msg.xml" -X POST "http://search.webofknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate"'.format(self.credentials), shell=True)
        res = str(response)
        print("Response: ", res)
        try:
            result = res[res.index("<return>")+len("<return>"):res.index("</return>")]
            print(result)
            self.token = result
        except ValueError as e:
            #wait for throttling to end
            print("Waiting 60 seconds for api")
            time.sleep(60)
            self.get_token()

    def run_query(self, **kwargs):
        headers = {'Cookie': 'SID=' + self.token}
        self.params['userQuery'] = kwargs['query']
        try:
            self.params['start'] = kwargs['start']
            self.params['end'] = kwargs['end']
        except KeyError as e:
            self.params['start'] = ''
            self.params['end'] = ''


        q = Environment().from_string("""\
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:woksearchlite="http://woksearchlite.v3.wokmws.thomsonreuters.com">
            <soapenv:Header/>
            <soapenv:Body>
            <woksearchlite:search>
                <queryParameters>
                  <databaseId>{{databaseId}}</databaseId>
                  <userQuery>{{userQuery}}</userQuery>
                   <editions>
                    <collection>{{collection}}</collection>
                    <edition>SCI</edition>
                   </editions>
                   <editions>
                    <collection>{{collection}}</collection>
                    <edition>SSCI</edition>
                   </editions>
                   <editions>
                    <collection>{{collection}}</collection>
                    <edition>AHCI</edition>
                   </editions>
                   <editions>
                    <collection>{{collection}}</collection>
                    <edition>ESCI</edition>
                   </editions>
                {%- if start %}
                   <timeSpan>
                        <begin>{{start}}</begin>
                        <end>{{end}}</end>
                    </timeSpan>
                {%- endif -%}
                  <queryLanguage>{{queryLanguage}}</queryLanguage>
                </queryParameters>
                <retrieveParameters>
                  <firstRecord>{{firstRecord}}</firstRecord>
                   <count>{{count}}</count>
                </retrieveParameters>
              </woksearchlite:search>
            </soapenv:Body>
        </soapenv:Envelope>
        """)

        finished = False
        results = []
        while not finished:
            data = q.render(**self.params)
            result = self.do_search(data, headers)
            results.append(result)
            try:
                totalRecords = result[result.index("<recordsFound>")+len("<recordsFound>"):result.index("</recordsFound>")]
                print(totalRecords)
                if (int(self.params['firstRecord']) + 99) < int(totalRecords):
                    self.params['firstRecord'] = str(int(self.params['firstRecord']) + 100)
                else:
                    finished = True
            except ValueError as e:
                print(result)
                print(e)
                exit()

        self.params['firstRecord'] = 1
        return results

    def do_search(self, query, headers):
        print(query)
        response = requests.post(self.search_url, data=query, headers=headers)
        result = response.text

        #check if query was successful
        if '<faultcode>' in result:
            fault = result[result.index("<faultstring>")+len("<faultstring>"):result.index("</faultstring>")]
            if "There is a problem with your session identifier (SID)" in fault:
                wosnnection.get_token()
                result = self.do_search(wosnnection, query, **params)

        return result