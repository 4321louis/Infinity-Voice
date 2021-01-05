from datetime import datetime

# prints argument and current date and time
def print_timed(s: str) -> None:
    print("[" + str(datetime.now()) + "]" + s)

def get_infinity_voice(ctx:commands.Context) -> InfinityVoice:
    for infinity_voice in infinityVoices[ctx.guild.id]:
        for active_channel in infinity_voice.active_channels:
            if active_channel==ctx.author.voice.channel:
                return infinity_voice
    ctx.send("Please join an Infinity Voice")
    return None

class ChannelOverride():
    """
    docstring
    """
    def __init__(self,name_format,limit,overwrites,position):
        """
        docstring
        """
        self.name_format = name_format
        self.limit = limit
        self.overwrites = overwrites
        self.position = position
        self.editing = False

