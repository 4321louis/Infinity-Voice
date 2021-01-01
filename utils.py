def print_timed(s: str) -> None:
    print("[" + str(datetime.now()) + "]" + s)   

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

