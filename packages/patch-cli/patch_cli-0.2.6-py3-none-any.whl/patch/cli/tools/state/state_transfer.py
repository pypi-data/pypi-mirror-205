import requests


class StateTransfer:

    def __init__(self, base_url, path):
        self.base_url = base_url
        self.path = path
        self._response = None

    def call_for_state_transfer(self, payload):
        headers = {"Content-Type": "application/json"}
        url = self.base_url + self.path
        response = requests.get(url, params=payload, headers=headers, allow_redirects=True)
        response.raise_for_status()
        self._response = response.json()

    def get_redirect_url(self):
        if self._response:
            return self.base_url + self._response.get('redirect-path')
