

class ChannelSettings():
    #TODO:pass xd
    def voice_channel_to_channel_override(channel:VoiceChannel) -> utils.ChannelSettings:
        pass

    def __init__(self,channel = None,**kwargs):
        if (channel != None):
            channelConstructor(channel)
        else:
            self.name_format = kwargs.get('name_format',None)
            self.limit = kwargs.get('limit',None)
            self.overwrites = kwargs.get('overwrites',None)
    
    def channelConstructor(self,channel:VoiceChannel):
            self.name_format = kwargs.get('name_format',channel.name)
            self.limit = kwargs.get('limit',channel.user_limit)
            self.overwrites = kwargs.get('overwrites',channel.overwrites)