from sheety import Sheety
from flight import Flight
import smtplib
import os, datetime
from dotenv import load_dotenv


class FlightData:
    def send_email(self, to, subject, content):
        try:
            load_dotenv()
            my_email = os.environ.get("my_email")
            password = os.environ.get("password")
            connection = smtplib.SMTP(host="smtp.gmail.com", port=587)
            connection.starttls()
            connection.login(user=my_email, password=password)
            SUBJECT = subject
            TEXT = content
            message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
            connection.sendmail(from_addr=my_email, to_addrs=to, msg=message)
            return f'Done sending message to {to}.'

        except Exception as e:
            return e

    def get_lowest_price_for_specific_date(self, date, origin):
        DATE_TO_CHECK = date
        ORIGIN = origin
        EMAIL_TO = os.environ.get("EMAIL_TO")

        my_sheet = Sheety()
        my_flight = Flight()
        sheety_read = my_sheet.read_sheety()
        new_prices = []
        the_durations = []
        # checking data in spreadsheet using sheety
        for something in sheety_read['sheet1']:
            city_name = something['city']
            iata = something['iat']
            lowest_price = something['lowestPrice']

            # getting flight data from ORIGIN to the desired city
            data = my_flight.get_flight_price(ORIGIN, iata, DATE_TO_CHECK)

            # saving flight data to lists
            iteneraries = []
            prices = []
            durations = []
            for number in range(0, len(data['data'])):
                iter = data['data'][number]
                price = iter['price']['grandTotal']
                prices.append(float(price))
                for a in iter['itineraries']:
                    iteneraries.append(a)

            number_of_flights = len(iteneraries)

            # getting the flight durations and saving it to the list that has been stated above as empty list
            for f in range(0, number_of_flights):
                flight = iteneraries[f]
                dur = flight['duration']
                duration = dur.replace('PT', '').replace('H', ' hours ').replace('M', ' minutes')
                durations.append(duration)

            # getting the cheapest price flight and it's duration
            cheapest = min(prices)
            min_index = prices.index(min(prices))
            its_duration = durations[min_index]
            print(f"cheapest: {cheapest}, duration {its_duration}")
            new_prices.append(cheapest)
            the_durations.append(its_duration)

            # if the flight ticket found is lower than the lowest price that we define in spreadsheet, then send email.
            if int(lowest_price) > cheapest:
                self.send_email(EMAIL_TO, 'Low Price Alert!', f'Only {cheapest} with {its_duration} flight duration to fly to {city_name} from {ORIGIN}! in {DATE_TO_CHECK}')

        # write the newest price to the "get price" column in spreadsheet
        for i in range(0, len(new_prices)):
            my_sheet.write_to_sheety('getPrice', new_prices[i], i+2)

    def airport_prediction_data(self, origin, date):
        my_flight = Flight()
        return my_flight.airport_prediction(origin, date)