import requests
from twilio.rest import Client

# OpenWeatherMap API endpoint and your API key
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = "your api key given from openweather"

# Twilio account SID and authentication token
account_sid = 'your sid given from twilio'
auth_token = 'your token given from twilio'

# Parameters for the API request: latitude, longitude, API key, and count of time periods (4 periods = 12 hours of forecast)
params = {
    "lat": 41.0252832,
    "lon": 28.8726498,
    "appid": api_key,
    "cnt": 4  # only request 4 time periods, giving a 12-hour forecast (each period is 3 hours apart)
}

# Make a request to the OpenWeatherMap API
response = requests.get(OWM_Endpoint, params=params)
response.raise_for_status()  # raise an error if the request failed
weather_data = response.json()  # parse the response as JSON

# Check if it will rain in the next 12 hours
will_rain = False
for hour_data in weather_data["list"]:  # iterate over each time period in the forecast
    condition_code = hour_data["weather"][0]['id']  # get the weather condition code
    if int(condition_code) < 700:  # if the condition code is less than 700, it indicates rain or other bad weather
        will_rain = True

# If it will rain, send a notification via Twilio
if will_rain:
    client = Client(account_sid, auth_token)  # initialize the Twilio client
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella ☂️",  # the message to send
        from_='demo number given from twilio',  # your Twilio phone number
        to='your number'  # the recipient's phone number
    )
    print(message.status)  # print the status of the sent message
