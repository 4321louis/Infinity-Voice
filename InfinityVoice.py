from utils import print_timed,ChannelOverride
import json
from typing import Dict,Union
from collections import defaultdict
from discord import Guild,VoiceChannel

class InfinityVoice:    
    def __init__(self: InfinityVoice, guild: Guild, name_format: str, user_limit: int = -1):
        self.guild = guild
        self.active_channels = []
        # every channel that gets created in this infinityvoice will by default have the following
        default = ChannelOverride()
        default.name_format = name_format
        default.user_limit = user_limit
        # dictionary that stores all the potential overrides in: {channelNumber: ChannelOverride}
        self.overrides = defaultdict(lambda:default)
    
    # called to update the infinity voice 
    async def update_channels(self: InfinityVoice) -> None:
        # delete excess channels
        found_empty= False
        i=0
        while i < len(self.active_channels):
            if self.active_channels[i].members == []:
                # this deletes the next empty channel after an empty channel is found
                if found_empty == True:
                    await (self.active_channels.pop(i)).delete(reason = "Clearing Empty voice channels")
                    continue
                found_empty = True
            i+=1

        # no empty channels found, create empty channel
        if found_empty == False:
            number = len(self.active_channels)
            self.active_channels.append(await self.guild.create_voice_channel(
                self.overrides[number].name_format.format(number + 1),
                user_limit = self.overrides[number].user_limit,
                overwrites = self.overrides[number].overwrites,
                category   = self.overrides[None].category,
                position   = self.overrides[None].position + len(self.active_channels) - 1))
    
        # rename channels
        for i in range(len(self.active_channels)):
            if self.overrides[i].name_format.format(i+1) != self.active_channels[i].name:
                await self.active_channels[i].edit(name =  self.overrides[i].name_format.format(i+1))


    # updates the references for the channels in the infinity voice 'infinity_voice'
    async def reload(self: InfinityVoice, bot: Bot) -> None:
        print_timed("Reloading " + self.name_format.format(0))
        for i in range(len(self.active_channels)):
            infinity_voice.active_channels[i] = await bot.fetch_channel(self.active_channels[i].id)    
        print_timed("Reload Finished " + self.name_format)

#TODO:is this even type hinting?
# {guildID: InfinityVoice}
infinityVoices = dict()

def json_encoder(obj: object) -> Union[int, dict]:
    # encode guilds and voice channels as their id
    if isinstance(obj,Guild) or isinstance(obj,VoiceChannel):
        return obj.id
    # encode InfinityVoice or ChannelOverride's symbol table
    if isinstance(obj,InfinityVoice) or isinstance(obj,ChannelOverride):
        return obj.__dict__

# Returns the infinityvoice the given channel is in
def get_infinity_voice(channel: VoiceChannel) -> Union[InfinityVoice, None]:
    for infinity_voice in infinityVoices[channel.guild.id]:
        for active_channel in infinity_voice.active_channels:
            if channel == active_channel:
                return infinity_voice
    return None

def save_infinities() -> None:
    f = open("InfinityVoiceSaves.txt","w+")
    dump=json.dumps(infinityVoices,default=json_encoder)
    print_timed("Saving:"+ dump)
    f.write(dump)
    f.close()
