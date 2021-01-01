from utils import print_timed,ChannelOverride
from main import bot
import json
from typing import Dict
from functools import reduce

global infinityVoices
#guild id to infity voice
infinityVoices = Dict()[int,InfinityVoice]

class InfinityVoice:    
    def __init__(self, guild: Guild, name_format: str, user_limit: int):
        self.guild = guild
        self.active_channels = []
        self.overrides = defaultdict()[int,ChannelOverride]

    #called to update the infinity voice 
    async def update_channels(self):
        #delete excess channels
        found_empty= False
        i=0
        while i < len(self.active_channels):
            if self.active_channels[i].members == []:
                if found_empty == True:
                    await (self.active_channels.pop(i)).delete(reason = "Clearing Empty voice channels")
                    continue
                found_empty = True
            i+=1
        #create empty channel
        if found_empty==False:
            number = len(self.active_channels)
            self.active_channels.append(await self.guild.create_voice_channel(
                self.overrides.get(number).name_format.format(number+1),
                user_limit=self.overrides.get(number).user_limit,
                overwrites=self.overrides.get(number).overwrites,
                category=self.overrides.get(None).category,
                position=self.overrides.get(None).position + len(active_channels) - 1))
        #rename channels
        for i in range(len(self.active_channels)):
            if self.overrides.get(i).name_format.format(i+1) != self.active_channels[i].name
                    await self.active_channels[i].edit(name =  self.overrides.get(i).name_format.format(i+1))


    #updates the references for the channels in the infinity voice 'infinity_voice'
    async def reload(self) -> None:
        print_timed("Reloading " + self.name_format.format(0))
        for i in range(len(self.active_channels)):
            infinity_voice.active_channels[i] = await bot.fetch_channel(self.active_channels[i].id)    
        print_timed("Reload Finished " + self.name_format)




#updates the infinity voice containing the channel 'channel'
async def update_inifity_voices(channel: VoiceChannel):
    for i in infinityVoices[channel.guild.id]:
        for j in i.active_channels:
            if channel == j:
                await i.update_channels()

        
def saveInfinity():
    f = open("InfinityVoiceSaves.txt","w+")
    dump=json.dumps(infinityVoices,default=json_encoder)
    print_timed("Saving:"+ dump)
    f.write(dump)
    f.close()
