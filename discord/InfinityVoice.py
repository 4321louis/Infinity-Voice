from utils.Utils import print_timed
from ChannelSettings import ChannelSettings
import json
from typing import Dict
from functools import reduce
from collections import defaultdict
from discord import Guild,VoiceChannel

# array of voice channels
class InfinityVoice:    
    def __init__(self, guild: Guild, name_format: str, user_limit: int = -1):
        # server the bot is in
        self.guild = guild
        # current voice channels in infinityvoice
        self.active_channels = []
        # controls the state of the voice
        self.inEditMode = false
        #position in the server
        self.position = 1
        #category of the voice channel
        self.category = None  

        # name format of voice channels
        name_format
        # max users of voice channels
        user_limit
        # where shit is actually stored
        default = ChannelSettings(name_format = name_format,user_limit = user_limit)

        # settings is a dictionary containing a number then the channel
        # lambda ensures all future keys get auto assigned default as their value
        self.settings = defaultdict(lambda:default)#[int,ChannelSettings]

    async def on_voice_state_update(self,member:Member, before, after):
        if not self.inEditMode:
            await self.on_size_change()
        
    # called to update the infinity voice 
    async def on_size_change(self):
        # delete excess channels
        found_empty:bool = False
        i:int=0
        # loop over all voice channels in infinityvoice
        while i < len(self.active_channels):
            # this deletes the next empty channel after an empty channel is found
            if self.active_channels[i].members == []:
                if found_empty == True:
                    await (self.active_channels.pop(i)).delete(reason = "Clearing Empty voice channels")
                    continue
                found_empty = True
            i+=1

        # no empty channels found, create empty channel
        if found_empty == False:
            number:int = len(self.active_channels)
            self.active_channels.append(await self.guild.create_voice_channel(
                # locates the most recent channel and changes the name format to be the same but with number incremented
                # name_format needs to be channelName {number}
                name = self.settings[number].name_format.format(number + 1),
                # gets user_limit and overwrites from the last channel
                user_limit = self.settings[number].user_limit,
                overwrites = self.settings[number].overwrites,
                category   = self.settings[None].category,
                # puts new channel below
                position   = self.settings[None].position + len(self.active_channels) - 1))
    
        # rename channels
        for i in range(len(self.active_channels)):
            if self.settings[i].name_format.format(i+1) != self.active_channels[i].name:
                await self.active_channels[i].edit(name =  self.settings[i].name_format.format(i+1))


    # updates the references for the channels in the infinity voice 'infinity_voice'
    async def reload_references(self,bot) -> None:
        print_timed("Reloading " + self.name_format.format(0))
        for i in range(len(self.active_channels)):
            infinity_voice.active_channels[i] = await bot.fetch_channel(self.active_channels[i].id)    
        print_timed("Reload Finished " + self.name_format)
