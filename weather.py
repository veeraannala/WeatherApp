# weather.py
import os
import requests
import json
from datetime import datetime

def get_url(data, city):
	apikey = os.getenv("APIKEY")
	url = "http://api.weatherapi.com/v1/" + data + ".json?"
	url += "key=" + (apikey if apikey is not None else "")
	url += "&q=" + city
	if data == 'forecast':
		url += "&days=2"
	url += "&aqi=no&lang=fi"
	return url

def get_current(city):
	url = get_url('current', city)
	response = requests.get(url)
	json_data = json.loads(response.text)
	current = [ city,
	    	    json_data['current']['temp_c'], 
		    	json_data['current']['condition']['text'],
	        	json_data['current']['wind_kph'],
		    	json_data['current']['wind_dir'],
		    	json_data['current']['condition']['icon']
	]
	return current

def get_forecast_tomorrow(city):
	url = get_url('forecast', city)
	response = requests.get(url)
	json_data = json.loads(response.text)
	forecast = [city,
    			json_data['forecast']['forecastday'][1]['date_epoch'],
	    		json_data['forecast']['forecastday'][1]['day']['maxtemp_c'],
		    	json_data['forecast']['forecastday'][1]['day']['mintemp_c'],
			    json_data['forecast']['forecastday'][1]['day']['condition']['text'],
			    json_data['forecast']['forecastday'][1]['day']['maxwind_kph']]
	return forecast   

def get_forecast_today(city):
	
	now = datetime.now()
	current_time = now.strftime("%H")
	hour = int(current_time)
	url = get_url('forecast')
	url += "&q=" + city
	url += "&days=2"
	url += "&aqi=no&lang=fi"
	response = requests.get(url)
	json_data = json.loads(response.text)
	forecast = [json_data['forecast']['forecastday'][0]['date_epoch'],
				json_data['forecast']['forecastday'][0]['hour'],
				]
	return forecast
