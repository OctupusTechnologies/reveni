import requests
import json


class ReveniApi(object):

    def __init__(self, IrConfigParams:object):
        self.store_id = IrConfigParams.get_param('reveni.store_id') if not IrConfigParams.get_param('reveni.debug') else IrConfigParams.get_param('reveni.sandbox_store_id')
        self.api_key = IrConfigParams.get_param('reveni.api_key') if not IrConfigParams.get_param('reveni.debug') else IrConfigParams.get_param('reveni.sandbox_api_key')
        self.debug = IrConfigParams.get_param('reveni.debug')
        self.base_url = 'https://api.reveni.io/merchants/v0/stores/' if not self.debug else 'https://api.sandbox.reveni.io/merchants/v0/stores/'

    def request_reveni(self, endpoint, method='GET', data=None):
        url = '{}{}/{}'.format(self.base_url, self.store_id, endpoint)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_key,
            'Accept': 'application/json'
        }
        try:
            response = requests.request(method, url, headers=headers, data=json.dumps(data))
        except ConnectionError as error:
            return error
        return response.json() if response.status_code in [200, 201] else False
