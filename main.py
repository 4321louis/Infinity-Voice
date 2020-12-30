from discord import *
from discord.ext import commands
import asyncio
from datetime import datetime,timedelta
import json

# ----------------------------------------------------------

def print_timed(s: str) -> None:
    print("[" + str(datetime.now()) + "]" + s)   
       

#updates the references for the channels in the infinity voice 'infinity_voice'
async def reload(infinity_voice:InfinityVoice) -> None:
    print_timed("Reloading " + infinity_voice.name_format.format(0))
    for i in range(len(infinity_voice.channels)):
        infinity_voice.channels[i] = await bot.fetch_channel(infinity_voice.channels[i].id)    
    print_timed("Reload Finished " + infinity_voice.name_format)

#updates the infinity voice containing the channel 'channel'
async def update_inifity_voices(channel:VoiceChannel):
    for i in infinityVoices[channel.guild.id]:
        for j in i.channels:
            if channel == j:
                await i.update_channels()



class InfinityVoice:    
    def __init__(self, guild: Guild, name_format: str, user_limit: int):
        self.guild = guild
        self.name_format = name_format
        self.channels = []
        self.user_limit = user_limit
        self.custom_names = {}

    async def update_channels(self):
        print_timed("updating the voice channels")
        
        #check for one empty channel
        found_empty = False
        i = 0
        while i < len(self.channels):
            if self.channels[i].members == []:
                if found_empty == True:
                    await (self.channels.pop(i)).delete(reason = "Clearing Empty voice channels")
                    i-=1
                found_empty = True
            i+=1
        
        if found_empty==False:
            if self.channels != []:
                self.channels.append(await self.guild.create_voice_channel(self.name_format.format(len(self.channels)+1),user_limit=self.user_limit,overwrites=self.channels[-1].overwrites ,category=self.channels[-1].category,position=self.channels[-1].position))
            else:
                self.channels.append(await self.guild.create_voice_channel(self.name_format.format(len(self.channels)+1),user_limit=self.user_limit))
        
        #rename channels
        for i in range(len(self.channels)):
            if i in self.custom_names:
                if self.channels[i].name != self.custom_names(i):
                    await self.channels[i].edit(name =  self.custom_names(i))
            elif self.channels[i].name != self.name_format.format(i+1):
                await self.channels[i].edit(name =  self.name_format.format(i+1))
        



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
            final[-1].channels.append(bot.get_channel(j))
    return final
        
def saveInfinity():
    f = open("infinityVoiceSaves.txt","w+")
    dump=json.dumps(infinityVoices,default=json_encoder)
    print_timed("Saving:"+ dump)
    f.write(dump)
    f.close()


#----------------------------------------------------------

#create bot instance
bot = commands.Bot(command_prefix='?')

global infinityVoices
infinityVoices = {}



#----------------------------------------------------------




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
    #when an infinity voice channel is edited (but not by the bot) updates the references for channels in that infinity voice
    if before.name == after.name:
        for i in infinityVoices[before.guild.id]:
            for j in i.channels:
                if before.id == j.id:
                    await reload(i)
                    return

@bot.event
async def on_guild_join(guild):
    infinityVoices[guild.id] = []

@bot.event
async def on_guild_remove(guild):
    infinityVoices.pop(guild.id)

@bot.command()
async def rename(ctx,name,index):
    if ctx.author.voice == null:
        pass

    for i in infinityVoices[ctx.guild]:
        for j in i:
            if j==ctx.author.voice.channel:
                pass




@bot.command()
async def create(ctx,name_format,user_limit = 0):
    if ctx.message.author.guild_permissions.administrator:
        new = InfinityVoice(ctx.guild,name_format,int(user_limit))
        infinityVoices[ctx.guild.id].append(new)
        await new.update_channels()
        
@bot.command()
async def bleh(ctx):
    #4321louis' panic button
    if ctx.message.author.id == 184599719060832257:
        global infinityVoices
        infinityVoices = {}


        
@bot.command()
async def save(ctx):
    #4321louis' other panic button
    if ctx.message.author.id == 184599719060832257:
        saveInfinity()



bot.run('NzQwOTg3ODQ3NzU0MTIxMzc5.XyxAtQ.aHNDmsoAWWwzPq6bP_JaXIsaYBg')
saveInfinity()