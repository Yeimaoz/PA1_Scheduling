from node import Node
from graph import Graph
from tool import type_itos, type_stoi

class Scheduler:
    def __init__(self):
        # 0: adder, 1: multiplier
        self.resource_types = 2
        self.resources = [0, 0]
        self.delay_unit = [1, 2]
        self.G = None

    def load_graph(self, filename):
        print("Loading %s ..." % filename)
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
            self.resources[0] = int(lines[0])
            self.resources[1] = int(lines[1])
            G = Graph([None for i in range(2+int(lines[2]))])
            # create nodes
            for nnt in lines[4:4+len(G)-2]:
                id, type_ = nnt.split(' ')
                id = int(id)
                G[id] = Node(id, type_stoi[type_])
                if type_ == 'i':
                    G.PIs.append(G[id])
                elif type_ == 'o':
                    G.POs.append(G[id])
            
            # start nop, end nop
            G[0] = Node(0, 4)
            G[-1] = Node(-1, 4)
            
            # construct connections
            for edge in lines[4+len(G)-2:]:
                source, sink = edge.split(' ') 
                G.connect_from_source_to_sink(int(source), int(sink))
            
            # connect nops
            for PI in G.PIs:
                G.connect_from_source_to_sink(0, PI.id)
            for PO in G.POs:
                G.connect_from_source_to_sink(PO.id, -1)
            f.close()
        self.G = G

    def evaluate_level(self):
        def backtrack_evaluate_level(cur):
            if cur.level != -1:
                return cur.level
            cur.level = 1 + max([backtrack_evaluate_level(fanin) for fanin in cur.fanins])
            return cur.level
        print("Evaluating level ...")
        self.G[0].level = 0
        backtrack_evaluate_level(self.G[-1])
        self.G.information() 
    
    def information(self):
        print("Adders: %d" % self.resources[0])
        print("Multiplier: %d" % self.resources[1])
        self.G.information()
