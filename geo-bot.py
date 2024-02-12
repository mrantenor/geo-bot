import os
import discord
import requests
import json
import pandas as pd
import datetime

url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
response = requests.get(url)
json_data = json.loads(response.text)
data = pd.DataFrame(json_data[1:], columns=json_data[0])


def kp_index(valor):
  if valor < 5:
    return ["", "insignificante"]
  elif 5 <= valor < 6:
    return ["G1", "pequena"]
  elif 6 <= valor < 7:
    return ["G2", "moderada"]
  elif 7 <= valor < 8:
    return ["G3", "forte"]
  elif 8 <= valor < 9:
    return ["G4", "severa"]
  else:
    return ["G5", "extrema"]


periodo = datetime.datetime.strptime(data.iloc[-1]['time_tag'],
                                     "%Y-%m-%d %H:%M:%S.%f")
hoje = datetime.datetime.now().strftime("%d/%m/%Y")
dia = str(periodo.strftime("%d/%m/%Y"))
hora = str(periodo.strftime("%H:%M"))
kp = float(data.iloc[-1]['Kp'])

if hoje == dia:
  compl = 'hoje'
else:
  compl = ''
mensagem = f'De acordo com a última atualização realizada {compl} {dia} as {hora} horas, o índice planetário de distúrbio geomagnético causado por eventos solares é {kp_index(kp)[1]} com valor de {kp} na escala kp (índice global planetário).'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('status'):
    await message.channel.send(mensagem)


try:
  token = os.environ['token']
  if token == "":
    raise Exception("Please add your token to the Secrets pane.")
  client.run(token)

except discord.HTTPException as e:
  if e.status == 429:
    print(
        "The Discord servers denied the connection for making too many requests"
    )
  else:
    raise e
