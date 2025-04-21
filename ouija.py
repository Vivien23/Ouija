import discord
from asyncio import sleep 
from discord.ext import commands

## Get the bot's token from file token_list.txt


TOKEN = None #Put your own bot token here if you have one

#And ignore this part
token_file = open("../token_list.txt", 'r')
while TOKEN == None:
    try:
        name, TOKEN = token_file.readline().split()
        if name != 'ouija':
            TOKEN = None
    except:
        raise "Token can't be found"
token_file.close()


## Declaring intents
bot_intents = discord.Intents.default()
bot_intents.message_content = True
bot = commands.Bot("!", intents=bot_intents)

## Declaring channel ids and other constants
id_chan_v = 1359543316235944282
id_chan_m = 1359543772928540923

id_buffer = 1363906704810578253
buffer = None

## Defining events and bot's behaviour

#Ready event, for debuging only
@bot.event
async def on_ready():
    #J'ai envie d'initialiser buffer ici, et de le passer en arg à on_message
    print("I'm ready")
    pass


#On message event, that's the fun part
@bot.event
async def on_message(message):
    buffer = bot.get_channel(id_buffer)

    if message.author == bot.user:
        return
    if type(message.channel) is discord.TextChannel:
    
        #Voir si le message vient de chan morts ou vivants
        from_v = message.channel.id == id_chan_v
        from_m = message.channel.id == id_chan_m
        if from_v:
            prov, dest = "**Vivants :** {}", bot.get_channel(id_chan_m)
        if from_m:
            prov, dest = "**Morts :** {}", bot.get_channel(id_chan_v)
        if not(from_v or from_m):
            #Rétablit l'utilisation des commandes si on est dans un channel sans joueur
            await(bot.process_commands(message))
            return

        #L'envoyer dans buffer puis attendre  
        await(buffer.send(prov.format(message.content)))
        await(sleep(5)) #Délai entre l'envoi du message et sa réception par l'autre groupe
        #L'envoyer dans l'autre chan
        await(dest.send(message.content))

@bot.command()
async def ping(ctx):
    await ctx.send("pong")




bot.run(TOKEN)
