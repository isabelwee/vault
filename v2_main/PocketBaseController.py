from pocketbase import PocketBase
import requests

class PocketBaseController:

    def __init__(self):
        self.baseUrl = "http://127.0.0.1:8090"

    def createRecord(self, collection, data):
        response = requests.post(f"{self.baseUrl}/api/collections/{collection}/records", json=data)
        if response.status_code != 200:
            print(f"Failed to create record. Status code: {response.status_code}")

    def getUserRecord(self, username):
        params = { "filter": f"username='{username}'" }
        response = requests.get(f"{self.baseUrl}/api/collections/users/records", params=params)

        try:
            data = response.json()
            items = data['items'][0]
        except requests.JSONDecodeError:
            data = None

        return items
    
