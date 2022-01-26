import os
import discord
my_secret = os.environ['Token']

client = discord.Client()

#The bot is connecting to the server
@client.event
async def on_ready():
  print('{0.user} has connected.'.format(client))

#When there is a message
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')


#Run the bot
client.run(my_secret)