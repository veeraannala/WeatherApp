import json
import os
from datetime import datetime
import discord
import requests
from dotenv import load_dotenv
import aiohttp
import io

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def get_current(city):
  apikey = os.getenv("APIKEY")
  url = "http://api.weatherapi.com/v1/current.json?"
  url += "key=" + (apikey if apikey is not None else "")
  url += "&q=" + city
  url += "&aqi=no&lang=fi"
  response = requests.get(url)
  json_data = json.loads(response.text)
  current = [json_data['current']['temp_c'], 
            json_data['current']['condition']['text'],
            json_data['current']['wind_kph'],
            json_data['current']['wind_dir'],
            json_data['current']['condition']['icon']
  ]
  return current

def get_forecast_tomorrow(city):
  apikey = os.getenv("APIKEY")
  url = "http://api.weatherapi.com/v1/forecast.json?"
  url += "key=" + (apikey if apikey is not None else "")
  url += "&q=" + city
  url += "&days=2"
  url += "&aqi=no&lang=fi"
  response = requests.get(url)
  json_data = json.loads(response.text)
  forecast = [json_data['forecast']['forecastday'][1]['date_epoch'],
              json_data['forecast']['forecastday'][1]['day']['maxtemp_c'],
              json_data['forecast']['forecastday'][1]['day']['mintemp_c'],
              json_data['forecast']['forecastday'][1]['day']['condition']['text'],
              json_data['forecast']['forecastday'][1]['day']['maxwind_kph']]
  return forecast

def get_forecast_today(city):
  now = datetime.now()
  current_time = now.strftime("%H")
  hour = int(current_time)
  apikey = os.getenv("APIKEY")
  url = "http://api.weatherapi.com/v1/forecast.json?"
  url += "key=" + (apikey if apikey is not None else "")
  url += "&q=" + city
  url += "&days=2"
  url += "&aqi=no&lang=fi"
  response = requests.get(url)
  json_data = json.loads(response.text)
  forecast = [json_data['forecast']['forecastday'][0]['date_epoch'],
              json_data['forecast']['forecastday'][0]['hour'],
              ]
  return forecast

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
      
    if message.content.startswith('$nyt'):
      city = message.content.split('-')[1]
      current = get_current(city)
      weather = city.capitalize() + ':'
      weather += '\nLämpötila ' + str(current[0]) + '°C'
      weather += '\nTuulen nopeus ' + str(round(current[2]/3.6,1)) + 'm/s'
      weather += '\nTuulen suunta ' + str(current[3])
      weather += '\n' + str(current[1]) + '\n'
      url = "http:" + str(current[4])

      async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = io.BytesIO(await resp.read())
            await message.channel.send(weather, file=discord.File(data, 'current.png'))

    if message.content.startswith('$tänään'):
      city = message.content.split('-')[1]
      forecast = get_forecast_today(city)
      date = datetime.fromtimestamp(forecast[0])
      header = '__' + city.capitalize() + ' ' + date.strftime("%d.%m.%Y") + ':__\n'
      now = datetime.now()
      current_time = now.strftime("%H")
      hour = int(current_time)
      await message.channel.send(header)
      while hour < 24 :
        date = datetime.fromtimestamp(forecast[1][hour]['time_epoch'])
        weather = '\n' + date.strftime("%H:%M")
        weather += '\n    Lämpötila ' + str(forecast[1][hour]['temp_c'])  + '°C'
        weather += '\n    Tuntuu kuin ' + str(forecast[1][hour]['feelslike_c'])  + '°C'
        weather += '\n    Tuulen nopeus ' + str(round(forecast[1][hour]['wind_kph']/3.6,1)) + 'm/s'
        weather += '\n    Tuulen suunta ' + str(forecast[1][hour]['wind_dir'])
        weather += '\n    Sateen todennäköisyys ' + str(forecast[1][hour]['chance_of_rain']) + '%' 
        weather += '\n    ' + str(forecast[1][hour]['condition']['text']) + '\n'
        hour += 3
        
        await message.channel.send(weather)

    if message.content.startswith('$huomenna'):
      city = message.content.split('-')[1]
      forecast = get_forecast_tomorrow(city)
      date = datetime.fromtimestamp(forecast[0])
      weather = '__' + city.capitalize() + ' ' + date.strftime("%d.%m.%Y") + ':__'
      weather += '\nKorkein lämpötila ' + str(forecast[1]) + '°C'
      weather += '\nMatalin lämpötila ' + str(forecast[2]) + '°C'
      weather += '\nKorkein tuulen nopeus ' + str(round(forecast[4]/3.6,1)) + 'm/s'
      weather += '\n' + str(forecast[3])
      await message.channel.send(weather)

    if message.content.startswith('$help'):
      await message.channel.send('$sää-<kaupunki> palauttaa kaupungin lämpötilan ja tuulen nopeuden')
      await message.channel.send('$ennuste-<kaupunki>  palauttaa kaupungin seuraavan päivän sääennusteen')
      await message.channel.send('$help palauttaa tämän tekstin')

token = os.getenv('TOKEN')
client.run(token)