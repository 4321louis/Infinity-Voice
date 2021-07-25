

class ChannelSettings():
    def __init__(self,**kwargs):
        self.name_format = kwargs.get('name_format',None)
        self.limit = kwargs.get('limit',None)
        self.overwrites = kwargs.get('overwrites',None)
        self.position = kwargs.get('position',1)
        self.category = kwargs.get('category',None)  