from node import Node
from graph import Graph
from tool import type_itos, type_stoi, type_itod

class Scheduler:
    def __init__(self):
        # 0: adder, 1: multiplier
        self.resource_types = 2
        self.resources = [0, 0]
        self.available_resources = [0, 0]
        self.G = None

    def load_graph(self, filename):
        #print("Loading %s ..." % filename)
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
            self.resources[0] = int(lines[0])
            self.resources[1] = int(lines[1])
            self.available_resources[0] = int(lines[0])
            self.available_resources[1] = int(lines[1])
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
            
            # construct connections
            for edge in lines[4+len(G)-2:]:
                source, sink = edge.split(' ') 
                G.connect_from_source_to_sink(int(source), int(sink))
            G.add_nop()
            

            f.close()
        self.G = G

    def evaluate_level(self):
        def backtrack_evaluate_level(cur):
            if cur.level != -1:
                return cur.level
            cur.level = 1 + max([backtrack_evaluate_level(fanin) for fanin in cur.fanins])
            return cur.level
        #print("Evaluating level ...")
        for PI in self.G.PIs:
            PI.level = 0

        backtrack_evaluate_level(self.G[-1])
   
    def list_scheduling_algorithm(self):
        #print("Scheduling ...")
        self.G[0].status = 1
        for PI in self.G.PIs:
            PI.status = 1
        remaining_set = set()
        timeline = []
        while not self.G[-1].finished():
            finished_set = set()
            for remaining_operation in remaining_set:
                if remaining_operation.type not in ['i', 'o']:
                    remaining_operation.remaining_time -= 1
                if not remaining_operation.remaining_time:
                    finished_set.add(remaining_operation)
            for remaining_operation in finished_set:
                remaining_operation.status = 1
                remaining_set.remove(remaining_operation)
                if remaining_operation.type not in [2, 3]:
                    self.available_resources[remaining_operation.type] += 1
            ready_set = sorted([node for node in self.G if node.unscheduled() and node.ready()], key=lambda x: x.level, reverse=True)
            unscheduled_set = [node for node in self.G if node.unscheduled() and not node.finished()]
            for node in ready_set:
                if node is self.G[-1]:
                    node.status = 1
                    break
                if type_itos[node.type] == 'o':
                    node.status = 0
                    node.remaining_time = type_itod[node.type]
                    remaining_set.add(node)
                    continue
                if self.available_resources[node.type]:
                    node.status = 0
                    node.remaining_time = type_itod[node.type]
                    remaining_set.add(node)
                    self.available_resources[node.type] -= 1
            track = [remaining_operation for remaining_operation in remaining_set if remaining_operation.type not in [2, 3]]
            if track:
                timeline.append(track)
            unscheduled_set = [node for node in self.G if not node.finished()]
    
        self.timeline = timeline


    def show_timeline(self):
        #print("Showing timeline ...")
        print('%d' % len(self.timeline))
        for i, track in enumerate(self.timeline):
            #print(' - Track %d:' % (i+1), ', '.join([str(operation.id) for operation in track]))
            print(' '.join([str(operation.id) for operation in track]))
        #print(' - Latency: %d' % len(self.timeline))

    def information(self):
        print("Adders: %d" % self.resources[0])
        print("Multiplier: %d" % self.resources[1])
        self.G.information()
