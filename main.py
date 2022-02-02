import os
import discord
import requests
import json
import random
from replit import db

my_secret = os.environ['Token']

client = discord.Client()

sadWords = ["sad","depressed", "angry", "help", "depressing"]

starterEnc =[
  "Cheer Up!",
  "You got this",
  "You're doing great"
]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q']+" -" + json_data[0]['a']
  return quote

def updateEnc(encMsg):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.appen(encMsg)
    db["encouragements"] = encouragements
  else:
      db["encouragements"] = [encMsg]

def deleteEnc(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('{0.user} has connected.'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$quote'):
    quote = get_quote()
    await message.channel.send(quote)

    options = starterEnc
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

  if any(word in msg for word in sadWords):
    await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encMsg = msg.split("$new ",1)[1]
    updateEnc(encMsg)
    await message.channel.send("New Encouragement Added.")

  if msg.startswith("$delete"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$delete", 1)[1])
      deleteEnc(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

client.run(my_secret)

