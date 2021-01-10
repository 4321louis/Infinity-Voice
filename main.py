import utils
from InfinityVoice import InfinityVoice,save_infinities,get_infinity_voice
from discord import Member,VoiceChannel
import discord.ext.commands as dcec

import json
import asyncio
from collections import defaultdict

# ONLY USE THIS TO GET THE 'infinityVoices' "global" variable
import InfinityVoice as IV

def json_decoder(str:str) -> list:
    loaded = json.loads(str)
    final = []
    for i in loaded:
        final.append(InfinityVoice(bot.get_guild(i["guild"]),i["name_format"],i["user_limit"]))
        for j in i["channels"]:
            final[-1].active_channels.append(bot.get_channel(j))
    return final

#TODO:pass xd
def voice_channel_to_channel_override(channel:VoiceChannel)->utils.ChannelOverride:
    pass

#create bot instance
bot = dcec.Bot('v!',dcec.HelpCommand())

#################### Events ####################

@bot.event
async def on_ready():
    utils.print_timed("")
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")

    f = open("infinityVoiceSaves.txt","r")
    IV.infinityVoices = json_decoder(f.read())
    print(IV.infinityVoices)
    f.close()

@bot.event
async def on_disconnect():
    utils.print_timed("Disconnected")
    save_infinities()

@bot.event
async def on_voice_state_update(member:Member, before, after):
    #update the infinity voice that was affected
    if (before.channel != None):
        await get_infinity_voice(before.channel).update_channels()
    if (after.channel != None):
        await get_infinity_voice(after.channel).update_channels()

@bot.event
async def on_guild_channel_update(before, after):
    #TODO:fix this if statements logic
    #when an infinity voice channel is edited (but not by the bot) updates the references for channels in that infinity voice
    if before.name == after.name:
        await get_infinity_voice(before).reload()

@bot.event
async def on_guild_join(guild):
    IV.infinityVoices[guild.id] = []

@bot.event
async def on_guild_remove(guild):
    IV.infinityVoices.pop(guild.id)

#################### Commands ####################

#TODO:HELP? look into the help command in the library
# @bot.command()
# async def help(ctx,command)
#     pass

#TODO:think about what name_format is for the end user
##i.e. "Gaming {}" where {} is the number? how about special chars instead? which?
@bot.command()
async def create(ctx,name_format,user_limit = 0):
    if ctx.message.author.guild_permissions.administrator:
        new = InfinityVoice(ctx.guild,name_format,int(user_limit))
        IV.infinityVoices[ctx.guild.id].append(new)
        await new.update_channels()

@bot.command()
async def edit(ctx, number = "0"):
    iv = get_infinity_voice(ctx.author.voice.channel)
    if iv == None: 
        ctx.send("Please join an Infinity Voice")
        return
    if number == "list":
        await ctx.send(iv.overrides.toString())
    elif number.isnumeric():
        if not (int(number) in iv.overrides or number == "0"):
            iv.overrides[int(number)] = utils.ChannelOverride()
        iv.overrides[int(number)].editing = True

@bot.command()
async def save(ctx, number = "0"):
    iv = get_infinity_voice(ctx.author.voice.channel)
    if iv == None: 
        ctx.send("Please join an Infinity Voice")
        return
    if number == "all":
        for i in iv.overrides.keys().append("0"): 
            iv.overrides[i].editing = False
    if (int(number) in iv.overrides or number == "0"):
        if iv.overrides(int(number)).editing:
            iv.overrides[int(number)].editing = False
            if number == "0":
                ctx.send("Saved default channel")
            else:
                ctx.send("Saved channel " + str(number))
        else:
            ctx.send("That channel is not currently being edited")





@bot.command()
#4321louis' panic button
async def bleh(ctx):
    if ctx.message.author.id == 184599719060832257:
        IV.infinityVoices = {}

@bot.command()
#4321louis' other panic button
async def saveall(ctx):
    if ctx.message.author.id == 184599719060832257:
        save_infinities()


f = open("token.txt","r")
bot.run(f.read())
save_infinities()
