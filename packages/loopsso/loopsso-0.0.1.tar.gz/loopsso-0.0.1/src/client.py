import requests


class LoopsClient(object):

    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key
        self.base_url = base_url or 'https://app.loops.so/api/v1'

    @property
    def headers(self):
        return {
            'Accept': 'application/json',
            'Authorization': 'Bearer %s' % self.api_key
        }

    def create(self, email, first_name, last_name, source, **kwargs):
        url = '%s/contacts/create' % self.base_url
        data = {
            'email': email,
            'firstName': first_name,
            'lastName': last_name,
            'source': source
        }
        data =  data.update(kwargs)
        response = requests.post(url, data=data, headers=self.headers)
        return response

    def update(self, email, first_name, last_name, source, **kwargs):
        url = '%s/contacts/update' % self.base_url
        data = {
            'email': email,
            'firstName': first_name,
            'lastName': last_name,
            'source': source
        }
        data =  data.update(kwargs)
        response = requests.put(url, data=data, headers=self.headers)
        return response

    def status(self):
        url = '%s/api-key' % self.base_url
        return requests.get(url, headers=self.headers)

    def find(self, email=None, user_id=None):
        if not email or not user_id:
            return 
        if email:
            params={'email': email}
        if user_id:
            params={'userId': user_id}
        url = '%s/contacts/find' % self.base_url
        return requests.get(url, params)

    def delete(self, email):
        url = '%s/contacts/delete' % self.base_url
        return requests.delete(url, data={'email': email})

    def send(self, email, event_name):
        url = '%s/events/send' % self.base_url
        data = {
            'email': email,
            'eventName': event_name
        }
        response = requests.post(url, data=data, headers=self.headers)
        return response
