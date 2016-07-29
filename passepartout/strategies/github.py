import json
from base64 import b64encode
import requests

from passepartout.locking import Locking


class GithubLocking(Locking):
    BASE_URL = 'https://api.github.com'

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token')
        super(GithubLocking, self).__init__(*args, **kwargs)

    @property
    def url(self):
        return '{base}/repos/{owner}/{repo}/contents/{path}'.format(
            base=self.BASE_URL,
            owner=self.owner,
            repo=self.repo,
            path=self.LOCK_PATH)

    def lock(self):
        response = self._get()
        if response:
            return False
        content = b64encode(self.LOCK_CONTENT.encode('utf-8')).decode('utf-8')
        data = {
            'path': self.LOCK_PATH,
            'message': self.LOCK_MESSAGE,
            'content': content,
        }
        response = requests.put(self.url,
                                params={'access_token': self.token},
                                data=json.dumps(data))
        self._log(self.url, data)
        self._log(response.status_code, response.text)
        if response.status_code == 201:
            return response.json()
        return False

    def unlock(self):
        response = self._get()
        if response:
            data = {
                'message': self.UNLOCK_MESSAGE,
                'sha': response['sha'],
            }
            response = requests.delete(self.url,
                                       params={'access_token': self.token},
                                       data=json.dumps(data))
            self._log(self.url, data)
            self._log(response.status_code, response.text)
            if response.status_code == 200:
                return response.json()
        return False

    def is_locked(self):
        return self._get()

    def _get(self):
        response = requests.get(self.url,
                                params={'access_token': self.token})
        self._log(self.url)
        self._log(response.status_code, response.text)
        if response.status_code == 200:
            return response.json()
        return {}
