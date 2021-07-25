import json
from ChannelSettings import ChannelSettings

class TextJsonBackup(GeneralBackup):
    SAVE_LOCATION = "../data/InfinityVoiceSaves.txt"
    def __init__(self, *args):
        super(TextJsonBackup, self).__init__(*args))

    def saveAll(self, guild_map) -> None:
        f = open(SAVE_LOCATION,"w+")
        dump = json.dumps(infinityVoices,default=json_encoder)
        f.write(dump)
        f.close()
    
    def loadAll(self):
        f = open(SAVE_LOCATION,"r")
        out = json_decoder(f.read())
        f.close()
        return out

    def json_encoder(self,obj: object) -> Union[int, dict]:
        # encode guilds and voice channels as their id
        if isinstance(obj,Guild) or isinstance(obj,VoiceChannel):
            return obj.id
        # encode InfinityVoice or ChannelSettings's symbol table
        if isinstance(obj,InfinityVoice) or isinstance(obj,ChannelSettings):
            return obj.__dict__
    
    def json_decoder(self,str:str) -> dict:
        loaded = json.loads(str)
        final = {}
        for str_guild_id,infinity_voice_ids in loaded.items():
            guild_id = int(str_guild_id)
            final[guild_id] = []
            for infinity_voice_dict in infinity_voice_ids:
                final[guild_id].append(InfinityVoice(bot.get_guild(infinity_voice_dict["guild"]),infinity_voice_dict["name_format"],infinity_voice_dict["user_limit"]))
                for channel_id in infinity_voice_dict["active_channels"]:
                    final[guild_id][-1].active_channels.append(bot.get_channel(channel_id))
                default_dict = infinity_voice_dict["overrides"]["null"]
                # TODO:kwargs please probs
                default = ChannelSettings(name_format = default_dict["name_format"]
                    ,limit = default_dict["limit"]
                    ,overwrites = default_dict["overwrites"]
                    ,category = bot.fetch_channel(default_dict["category"])
                    ,position = default_dict["position"])
                final[guild_id][-1].overrides = defaultdict(default)
                for number in infinity_voice_dict["overrides"]:
                    if number == "null": continue
                    override_dict = infinity_voice_dict["overrides"][number]
                    # TODO:kwargs please probs
                    override = ChannelSettings(
                        ,name_format = override_dict["name_format"]
                        ,limit = override_dict["limit"]
                        ,overwrites = override_dict["overwrites"]
                        # TODO: bot singleton
                        ,category = bot.fetch_channel(override_dict["category"])
                        ,position = override_dict["position"])
                    final[guild_id][-1].overrides[int(number)] = override
        return final
