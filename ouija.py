import discord
from discord.ext import commands

## Get the bot's token from file token_list.txt


TOKEN = None #Put your own bot token here if you have one

#And ignore this part
token_file = open("token_list.txt", 'r')
while TOKEN == None:
    try:
        name, TOKEN = token_file.readline().split()
        if name != 'ouija':
            TOKEN = None
    except:
        raise "Token can't be found"
token_file.close()



bot_intents = discord.Intents.default()
bot_intents.message_content = True
bot = commands.Bot("!", intents=bot_intents)


@bot.event
async def on_ready():
    print("I'm ready")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if type(message.channel) is discord.TextChannel:
        await message.channel.send(content="Bouh")

bot.run(TOKEN)
