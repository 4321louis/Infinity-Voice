from datetime import datetime
from discord import VoiceChannel

# prints argument and current date and time
def print_timed(s: str) -> None:
    print("[" + str(datetime.now()) + "]" + s)


class ChannelOverride():
    """
    docstring
    """
    def __init__(self):
        """
        docstring
        """
        self.name_format = None
        self.limit = None
        self.overwrites = None
        self.position = 1
        self.category = None
        self.editing = False

