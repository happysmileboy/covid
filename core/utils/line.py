import requests
import random
import string
import time
from core.utils.hashing import get_signature

class LineManager:
    cashew = 'test-api.blockchain.line.me'
    daphne = 'api.blockchain.line.me'
    service_api_key = 'c0102049-3a5c-43f8-86ae-05c63cf615b9'
    api_secret = 'baf5ce54-f8da-488d-b8e9-48092208e3e7'
    wallet_address = 'tlink1kszytuezy0gndtjr6fcdgjwp6v3z028sw23ptl'
    wallet_secret = 'GKzXIJ093O+D6dYYIEuy3yWAo7lurzr8Q7sim9n6qlY='

    url = f'https://{cashew}'

    def post_memo(self, memo, wallet_address, wallet_secret):
        path = '/v1/memos'

        request_body = {
            'walletAddress': wallet_address,
            'walletSecret': wallet_secret,
            'memo': memo
        }

        headers = self.headers()
        signature = get_signature('POST', path, headers['nonce'], headers['timestamp'], self.api_secret, request_body)
        headers['signature'] = signature

        res = requests.post(self.url + path, headers=headers, json=request_body)
        return res.json()

    def retrieve_memo(self, txHash):
        path = f'/v1/memos/{txHash}'
        headers = self.headers()
        signature = get_signature('GET', path, headers['nonce'], headers['timestamp'], self.api_secret)
        headers['signature'] = signature
        res = requests.get(self.url + path, headers=headers)
        return res.json()

    def nonce(self):
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))

    def timestamp(self):
        return int(round(time.time() * 1000))

    def headers(self):
        return {
            'service-api-key': self.service_api_key,
            'nonce': self.nonce(),
            'timestamp': str(self.timestamp()),
            'Content-Type': 'application/json'
        }