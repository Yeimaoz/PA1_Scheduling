from argparse import ArgumentParser
from node import Node
from graph import Graph
from scheduler import Scheduler

def getopt():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', dest='input', type=str, required=True, 
            help="mode, 1) input file for test")
    args = parser.parse_args()
    return args

if __name__ == '__main__':   
    args = getopt()
    test = Scheduler()
    test.load_graph(args.input)
