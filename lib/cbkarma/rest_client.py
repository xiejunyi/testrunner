import sys
sys.path.append('lib')

import json
import urllib

from membase.api.rest_client import RestConnection

class CbKarmaClient(RestConnection):
    """Performance dashboard (cbkarma) REST API"""

    def __init__(self, hostname, port='80'):
        """Create REST API client.

        Keyword arguments:
        hostname -- dashboard hostname/ip address
        port -- dashboard port
        """

        server_info = {'ip': hostname,
                       'port': port,
                       'username': '',
                       'password': ''}

        super(CbKarmaClient, self).__init__(server_info)

    def init(self):
        """Get initial test id (optional)"""

        api = self.baseUrl + 'init'
        return self._http_request(api, 'GET')

    def update(self, id=None, build='', spec='', description='', phase='',
               status=''):
        """Post test progress updates.

        Keyword arguments:
        id -- unique test id
        biuld -- build version
        spec -- configuration filename
        phase -- phase name
        status -- latest phase status ('started' or 'done')
        description -- optional test description

        Return tuple with status and test id.
        """

        api = self.baseUrl + 'update'

        params = {'phase': phase,
                  'build': build,
                  'spec': spec,
                  'description': description,
                  'status': status}
        if id:
            params['id'] = id

        return self._http_request(api, 'POST', urllib.urlencode(params))

    def histo(self, id=None, description='', attachment=''):
        """Attach latency histogram to the test"""
        api = self.baseUrl + 'histo'

        attachment = json.dumps(attachment)

        params = {'description': description,
                  'attachment': attachment}
        if id:
            params['id'] = id

        return self._http_request(api, 'POST', urllib.urlencode(params))