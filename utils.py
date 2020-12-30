from discord import *
from datetime import datetime,timedelta
import json
from InfinityVoice import InfinityVoice
from main import bot

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

def print_timed(s: str) -> None:
    print("[" + str(datetime.now()) + "]" + s)   