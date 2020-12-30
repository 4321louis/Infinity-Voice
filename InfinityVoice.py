from utils import print_timed,json_encoder
from main import bot
import json
from typing import Dict

global infinityVoices
infinityVoices = Dict[int,InfinityVoice]

class InfinityVoice:    
    def __init__(self, guild: Guild, name_format: str, user_limit: int):
        self.guild = guild
        self.active_channels = []
        #default channel override is stored in -1
        self.overrides = {}

    #called to update the infinity voice 
    async def update_channels(self):
        #check for one empty channel
        found_empty = False
        i = 0
        while i < len(self.active_channels):
            if self.active_channels[i].members == []:
                if found_empty == True:
                    await (self.active_channels.pop(i)).delete(reason = "Clearing Empty voice channels")
                    i-=1
                found_empty = True
            i+=1
        
        if found_empty==False:
            if self.active_channels != []:
                self.active_channels.append(await self.guild.create_voice_channel(self.name_format.format(len(self.active_channels)+1),user_limit=self.user_limit,overwrites=self.active_channels[-1].overwrites ,category=self.active_channels[-1].category,position=self.active_channels[-1].position))
            else:
                self.active_channels.append(await self.guild.create_voice_channel(self.name_format.format(len(self.active_channels)+1),user_limit=self.user_limit))
        
        #rename channels
        for i in range(len(self.active_channels)):
            if i in self.custom_names:
                if self.active_channels[i].name != self.custom_names(i):
                    await self.active_channels[i].edit(name =  self.custom_names(i))
            elif self.active_channels[i].name != self.name_format.format(i+1):
                await self.active_channels[i].edit(name =  self.name_format.format(i+1))


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
