import requests


class ZoomClient:

    def __init__(self, account_id, client_id, client_secret) -> None:
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.get_access_token()

    def get_access_token(self):
        data = {
            "grant_type": "account_credentials",
            "account_id": self.account_id,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post("https://zoom.us/oauth/token", data=data)
        return response.json()["access_token"]

    def get_recordings(self):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        url = f"https://api.zoom.us/v2/users/me/recordings"

        return requests.get(url, headers=headers).json()

    def get_download_url(self, meeting_id):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        url = f"https://api.zoom.us/v2/meetings/{meeting_id}/recordings"

        r = requests.get(url, headers=headers).json()

        url = [i['download_url'] for i in r['recording_files'] if i['recording_type'] == 'audio_only'][0]
        download_link = f'{url}?access_token={self.access_token}&playback_access_token={r["password"]}'
        return download_link