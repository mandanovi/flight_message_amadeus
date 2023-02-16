data = {'data': {'id': 'CGK20230616', 'probability': '0.928', 'result': '0.72337395', 'subType': 'on-time', 'type': 'prediction'}, 'meta': {'links': {'self': 'https://test.api.amadeus.com/v1/airport/predictions/on-time?airportCode=CGK&date=2023-06-16'}}}

prob = data['data']['probability']
percentage = "{:.1%}".format(float(prob))
print(percentage)