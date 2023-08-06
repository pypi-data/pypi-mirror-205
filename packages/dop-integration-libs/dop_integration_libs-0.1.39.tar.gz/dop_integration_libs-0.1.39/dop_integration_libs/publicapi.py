import requests


class PublicApiResponse(object):
    def __init__(self):
        self.TOKEN = ""
        self.public_api_url = ""
        self.CATALOG = 0
        self.MENU = 0

    def __str__(self):
        return f"TOKEN: {self.TOKEN}, CATALOG: {self.CATALOG}, MENU:\
        {self.MENU} {self.public_api_url}"

    def fetch_orders(self, last_service_id):
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        data = {"last_service_id": last_service_id}
        api_endpoint = f"{self.public_api_url}/publicapi/product/table-orders"
        response = requests.post(api_endpoint, json=data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", [])
        else:
            print(f"Error fetching orders: {response.status_code}")
            return None

    def save_product(self, data: dict) -> bool | None:
        url = f"{self.public_api_url}/publicapi/product"
        headers = {
            "Authorization": f"Bearer {self.TOKEN}"
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return True
        else:
            print(f"Error: {response.text} - {response.status_code}")
            return None


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
        response = requests.post(url, json=body)
        if response.status_code == 200:
            response = response.json()
            response_obj = PublicApiResponse()
            response_obj.TOKEN = response.get("access_token", "")
            response_obj.CATALOG = response.get("catalog", 0)
            response_obj.MENU = response.get("menu", 0)
            response_obj.public_api_url = self.public_api_url
            return response_obj
        else:
            return None
