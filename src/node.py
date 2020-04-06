from tool import type_itos

class Node:
    def __init__(self, id, type_):
        self.id = id
        self.type = type_
        self.fanins = []
        self.operations = []
        self.fanouts = []
        self.level = -1
        # -1: unscheduled, 0: running, 1: scheduled
        self.status = -1 
        self.remaining_time = 0

    def __str__(self):
        return str(self.id)

    def ready(self):
        for fanin in self.fanins:
            if fanin.status != 1:
                return False
        return True

    def unscheduled(self):
        return True if self.status == -1 else False

    def finished(self):
        return True if self.status == 1 else False 

    def information(self):
        print('[ Node: %d ]' % self.id)
        print(' - Type: %s' % type_itos[self.type])
        print(' - Level: %d' % self.level)
        print(' - Fanins: %s' % ', '.join([str(fanin) for fanin in self.fanins]))
        print(' - Fanouts: %s' % ', '.join([str(fanout) for fanout in self.fanouts]))

