import discord
import asyncio
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

id_mj = 1359560536760516841


bot_status = {"buffer_chan": None, "awake" : True, "passing" : True}

## Defining events and bot's behaviour

#Ready event, for debuging only
@bot.event
async def on_ready():
    #J'ai envie d'initialiser buffer ici, et de le passer en arg à on_message
    bot_status["buffer_chan"] = bot.get_channel(id_buffer)
    print("I'm ready")



#On message event, that's the fun part
@bot.event
async def on_message(message):
    buffer = bot_status["buffer_chan"]
    
    #Rétablit l'utilisation des commandes si l'auteur est un MJ
    if sum([role.id == id_mj for role in message.author.roles]):
        await(bot.process_commands(message))

    if message.author == bot.user or not(bot_status["awake"]):
        return

    if type(message.channel) is discord.TextChannel:
        #Voir si le message vient de chan morts ou vivants
        from_v = message.channel.id == id_chan_v
        from_m = message.channel.id == id_chan_m
        if from_v or from_m:
            if from_v:
                prov, dest = "**Vivants :** {}", bot.get_channel(id_chan_m)
            if from_m:
                prov, dest = "**Morts :** {}", bot.get_channel(id_chan_v)

            #L'envoyer dans buffer puis attendre  
            await(buffer.send(prov.format(message.content)))
            await(asyncio.sleep(10)) #Délai entre l'envoi du message et sa réception par l'autre groupe

            #L'envoyer dans l'autre chan
            if bot_status["awake"]:
                await(dest.send(message.content))
    pass


@bot.command()
async def ping(ctx):
    #Envoie un message à la main
    await(ctx.send("pong"))

@bot.command()
async def send(ctx):
    #Envoie un message à la main
    pass

@bot.command()
async def stop(ctx):
    #Empêche un message d'être envoyé
    bot_status["awake"] = False
    pass

@bot.command()
async def go(ctx):
    #Relance l'envoi des messages
    bot_status["awake"] = True
    pass

@bot.command()
async def set_timer(ctx):
    #Choisi la valeur du timer d'obfuscation
    pass


bot.run(TOKEN)
