from utils import *
from InfinityVoice import *

from discord import *
from discord.ext import commands

import asyncio


def json_encoder(obj: Object):
    if isinstance(obj,Guild) or isinstance(obj,VoiceChannel):
        return obj.id
    if isinstance(obj,InfinityVoice):
        return obj.__dict__

def json_decoder(str:str) -> dict:
    loaded = json.loads(str)
    final = []
    for i in loaded:
        final.append(InfinityVoice(bot.get_guild(i["guild"]),i["name_format"],i["user_limit"]))
        for j in i["channels"]:
            final[-1].active_channels.append(bot.get_channel(j))
    return final

def get_InfinityVoice(ctx:Context) ->InfinityVoice:
    for i in infinityVoices[ctx.guild.id]:
        for j in i:
            if j==ctx.author.voice.channel:
                return i
    ctx.send("Please join an Infinity Voice")
    return None

def channelToChannelOverride

#create bot instance
bot = commands.Bot('!v',commands.HelpCommand())

#################### Events ####################

@bot.event
async def on_ready():
    print_timed("")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    global infinityVoices
    f = open("infinityVoiceSaves.txt","r")
    infinityVoices = json_decoder(f.read())
    f.close()
    
@bot.event
async def on_disconnect():
    print_timed("Disconnected")
    saveInfinity()
    
@bot.event
async def on_voice_state_update(member:Member, before, after):
    #update the infinity voice that was affected
    if (before.channel != None):
        await update_inifity_voices(before.channel)
    if (after.channel != None):
        await update_inifity_voices(after.channel)

@bot.event
async def on_guild_channel_update(before, after):
    #TODO:fix this logic
    #when an infinity voice channel is edited (but not by the bot) updates the references for channels in that infinity voice
    if before.name == after.name:
        for i in infinityVoices[before.guild.id]:
            for j in i.active_channels:
                if before.id == j.id:
                    await i.reload()
                    return

@bot.event
async def on_guild_join(guild):
    infinityVoices[guild.id] = []

@bot.event
async def on_guild_remove(guild):
    infinityVoices.pop(guild.id)

#################### Commands ####################

#TODO:HELP? look into the help command in the library
# @bot.command()
# async def help(ctx,command)
#     pass

#TODO:think about what name_format is for the end user
@bot.command()
async def create(ctx,name_format,user_limit = 0):
    if ctx.message.author.guild_permissions.administrator:
        new = InfinityVoice(ctx.guild,name_format,int(user_limit))
        infinityVoices[ctx.guild.id].append(new)
        await new.update_channels()

@bot.command()
async def edit(ctx, number = "0"):
    iv = get_InfinityVoice(ctx)
    if iv == None: return
    if number == "list":
        await ctx.send(iv.overrides.toString())
    elif number.isnumeric():
        if (int(number) in iv.overrides or number =="0"):
            iv[int(number)].editing = True


@bot.command()
async def save(ctx, number = "0"):
    iv = get_InfinityVoice(ctx)
    if iv == None: return
    if number == "all":
        for i in iv.overrides.keys().append(0): 
            iv.overrides[i].editing = False
    if (int(number) in iv.overrides or number == "0"):
        if iv.overrides(int(number)).editing:
            iv.overrides[int[number]].editing = False
            if number == "0":
                ctx.send("Saved default channel")
            else:
                ctx.send("Saved channel " + str(number))
        else:
            ctx.send("That channel is not currently being edited")
            return







@bot.command()
#4321louis' panic button
async def bleh(ctx):
    if ctx.message.author.id == 184599719060832257:
        global infinityVoices
        infinityVoices = {}
      
@bot.command()
#4321louis' other panic button
async def saveAll(ctx):
    if ctx.message.author.id == 184599719060832257:
        saveInfinity()



bot.run('NzQwOTg3ODQ3NzU0MTIxMzc5.XyxAtQ.aHNDmsoAWWwzPq6bP_JaXIsaYBg')
saveInfinity()