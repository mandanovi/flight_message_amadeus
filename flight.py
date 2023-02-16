import requests
import json
import base64
from dotenv import load_dotenv
import os


class Flight:
    def __init__(self):
        load_dotenv()
        client_id = os.environ.get("client_id")
        client_secret = os.environ.get("client_secret")
        message = f"{client_id}:{client_secret}".encode('ascii')
        self.b64auth = base64.b64encode(message).decode('ascii')
        url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
        # Set the authentication headers
        self.headers = {
            'Authorization': f'Basic {self.b64auth}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        # Set the request parameters
        data = {
            'grant_type': 'client_credentials'
        }
        # Make the API request
        response = requests.post(url, headers=self.headers, data=data)
        # Parse the access token from the response
        access_token = json.loads(response.text)['access_token']
        # Use the access token in your API requests
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        print("flight.py init is called")

    def get_flight_price(self, origin, destination, date):
        url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
        params = {
            'originLocationCode': origin,
            'destinationLocationCode': destination,
            'departureDate': date,
            'adults': 1,
            'currencyCode':'USD'
        }
        response = requests.get(url, headers=self.headers, params=params)
        data = response.text
        response_json = json.loads(data)
        print("get_flight_price from flight.py is called")
        return response_json

    def airport_prediction(self, origin, date):
        url = 'https://test.api.amadeus.com/v1/airport/predictions/on-time'
        params = {
            'airportCode': origin,
            'date': date,
        }
        response = requests.get(url, headers=self.headers, params=params)
        print("flight.py airport prediction is called")
        if response.status_code == 200:
            data = response.text
            response_json = json.loads(data)
            print("airport_prediction from flight.py is called")
            return response_json
        else:
            print('Error writing:', response.status_code, response.text)