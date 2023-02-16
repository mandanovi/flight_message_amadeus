import requests
from dotenv import load_dotenv
import os


class Sheety:
    def __init__(self):
        load_dotenv()
        self.SHEETY_URL = "https://api.sheety.co/f23e01c6269912b80714f7f1d400ec9d/flightMessage/sheet1"
        self.SHEETY_KEY = os.environ.get("SHEETY_KEY")
        self.headers = {
            "Authorization": self.SHEETY_KEY,
            'Content-Type': 'application/json'
        }
        self.result = {}
        print("sheety init is called")

    def write_to_sheety(self, column, value, row):
        put_url = f'https://api.sheety.co/f23e01c6269912b80714f7f1d400ec9d/flightMessage/sheet1/{row}'
        data = {
            'sheet1': {
                column: value,
            }
        }
        response = requests.put(put_url, headers=self.headers, json=data)
        if response.status_code == 200:
            print("write sheety is working")
            self.result = response.json()
            return self.result
        else:
            print('Error writing:', response.status_code, response.text)

    def read_sheety(self):
        response = requests.get(url=self.SHEETY_URL, headers=self.headers)
        if response.status_code == 200:
            print("read sheety is working")
            self.result = response.json()
            return self.result
        else:
            print('Error reading:', response.status_code, response.text)
