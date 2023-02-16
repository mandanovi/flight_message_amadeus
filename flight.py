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

    def get_flight_price(self, origin, destination, date):
        url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
        # Set the authentication headers
        headers = {
            'Authorization': f'Basic {self.b64auth}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        # Set the request parameters
        data = {
            'grant_type': 'client_credentials'
        }
        # Make the API request
        response = requests.post(url, headers=headers, data=data)
        # Parse the access token from the response
        access_token = json.loads(response.text)['access_token']
        # Use the access token in your API requests
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
        params = {
            'originLocationCode': origin,
            'destinationLocationCode': destination,
            'departureDate': date,
            'adults': 1,
            'currencyCode':'USD'
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.text
        response_json = json.loads(data)
        return response_json

