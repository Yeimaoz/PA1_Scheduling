import collections
from node import Node

class Graph(list):
    def __init__(self, *args):
        list.__init__(self, *args)
        self.PIs = []
        self.POs = []

    def __getitem__(self, index):
        return super(Graph, self).__getitem__(index)
    
    def __setitem__(self, index, value):
        super(Graph, self).__setitem__(index, value)

    def connect_from_source_to_sink(self, source, sink):
        self[source].fanouts.append(self[sink])
        self[sink].fanins.append(self[source])

    def information(self):
        for node in self:
            node.information()
