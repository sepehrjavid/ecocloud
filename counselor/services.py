class Spec(object):

    def __init__(self, **kwargs):
        self.provider = kwargs.get('provider')
        self.nodes = kwargs.get('nodes')
        self.storage = kwargs.get('storage')
        self.memory = kwargs.get('memory')