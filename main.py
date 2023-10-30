# bot.py
import os
import discord
import aiohttp
import io
from dotenv import load_dotenv
from datetime import datetime
from weather import get_current, get_forecast_tomorrow, get_forecast_today
from formatter import format_current, format_forecast_tomorrow, format_forecast_today

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
		print(f'We have logged in as {client.user}')
		channel = client.get_channel(1127892746808602656)
		if channel:
			await channel.send('Hello, this is your favourite ' + client.user.name + '! Type $help to get started!')

@client.event
async def on_message(message):
		if message.author == client.user:
				return

		if message.content.startswith('$hello'):
				await message.channel.send('Hello ' + str(message.author.mention) + '!')
			
		if message.content.startswith('$nyt'):
			weather = format_current(get_current(message.content.split('-')[1]))

			async with aiohttp.ClientSession() as session:
				async with session.get(weather[1]) as resp:
						data = io.BytesIO(await resp.read())
						await message.channel.send(weather[0], file=discord.File(data, 'current.png'))

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
			forecast = format_forecast_tomorrow(get_forecast_tomorrow(message.content.split('-')[1]))
			await message.channel.send(forecast)

		if message.content.startswith('$help'):
			await message.channel.send('$nyt-<kaupunki> palauttaa kaupungin lämpötilan ja tuulen nopeuden')
			await message.channel.send('$tänään-<kaupunki>  palauttaa kaupungin tämän päivän sääennusteen')
			await message.channel.send('$huomenna-<kaupunki>  palauttaa kaupungin seuraavan päivän sääennusteen')
			await message.channel.send('$help palauttaa tämän tekstin')

token = os.getenv('TOKEN')
client.run(token)