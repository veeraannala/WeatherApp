# weather_formatter.py
from datetime import datetime

def format_current(data):
	# Nykyisen säädatan muotoilu

	weather = str(data[0]).capitalize() + ':'
	weather += '\nLämpötila ' + str(data[1]) + '°C'
	weather += '\nTuulen nopeus ' + str(round(data[3]/3.6,1)) + 'm/s'
	weather += '\nTuulen suunta ' + str(data[4])
	weather += '\n' + str(data[2 ]) + '\n'
	weatherUrl = "http:" + str(data[5])
	return [weather, weatherUrl]

def format_forecast_tomorrow(data):
	date = datetime.fromtimestamp(data[1])
	weather = '__' + data[0].capitalize() + ' ' + date.strftime("%d.%m.%Y") + ':__'
	weather += '\nKorkein lämpötila ' + str(data[2]) + '°C'
	weather += '\nMatalin lämpötila ' + str(data[3]) + '°C'
	weather += '\nKorkein tuulen nopeus ' + str(round(data[5]/3.6,1)) + 'm/s'
	weather += '\n' + str(data[4])
	return weather

def format_forecast_today(data):
	# Tänään säädatan muotoilu
	pass
