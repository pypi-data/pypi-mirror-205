import requests


class PublicApiResponse(object):
    def __init__(self):
        self.TOKEN = ""
        self.CATALOG = 0
        self.MENU = 0


class PublicApi(object):
    def __init__(self, api_key: str, secret_key: str, public_api_url: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.public_api_url = public_api_url

    def fetch(self) -> PublicApiResponse | None:

        url = f"{self.public_api_url}/publicapi/auth/login"
        body = {
            "apikey": self.api_key,
            "secretkey": self.secret_key,
        }

        print(url)
        print(body)
        response = requests.post(url, json=body)
        if response.status_code == 200:
            response = response.json()
            response_obj = PublicApiResponse()
            response_obj.TOKEN = response.get("access_token", "")
            response_obj.CATALOG = response.get("catalog", 0)
            response_obj.MENU = response.get("menu", 0)
            return response_obj
        else:
            return None
