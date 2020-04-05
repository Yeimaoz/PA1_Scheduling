from tool import type_itos

class Node:
    def __init__(self, id, type_):
        self.id = id
        self.type = type_
        self.fanins = []
        self.fanouts = []
        self.level = -1
    
    def __str__(self):
        return str(self.id)

    def information(self):
        print('[ Node: %d ]' % self.id)
        print(' - Type: %s' % type_itos[self.type])
        print(' - Fanins: %s' % ', '.join([str(fanin) for fanin in self.fanins]))
        print(' - Fanouts: %s' % ', '.join([str(fanout) for fanout in self.fanouts]))

