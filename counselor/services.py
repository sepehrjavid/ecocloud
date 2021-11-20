class Spec(object):

    def __init__(self, **kwargs):
        self.provider = kwargs.get('provider')
        self.nodes = int(kwargs.get('nodes'))
        self.storage = int(kwargs.get('storage'))
        self.memory = int(kwargs.get('memory'))
        self.stats = {}
