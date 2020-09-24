    # Describe problem as graph problem
    # ancestors is list of (parent, child) tuples


    # Build graph or write getNeighbors()

    # Which algorithm to go with?


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)

class Graph():
    def __init__(self):
        self.nodes = {}
    
    def add_node(self, value):
        self.nodes[value] = set()
    
    def add_edge(self, n1, n2):
        self.nodes[n1].add(n2)

    def get_parents(self, node):
        return self.nodes[node]

def earliest_ancestor(ancestors, starting_node):
    # What are nodes? nodes are either parents or children *unpacked tuples
    # What are edges? edges are the tuples (relationship between p & c)
    # Building graph
    g = Graph()
    for parent, child in ancestors:
        if child not in g.nodes:
            g.add_node(child)
        g.add_edge(child, parent)
    print(g.nodes)
    # creates queue, adds starting node to queue
    q = Queue()
    q.enqueue(starting_node)

    # check if visited
    visited = set()
    path = []

    while q.size() > 0:
        current = q.dequeue()
                # if not in visited, add to visited
        if current not in visited:
            visited.add(current)
            path.append(current)
            
            if current in g.nodes:                
                # get current's parents and add to queue
                parents = g.get_parents(current)
                for parent in parents:
                    q.enqueue(parent)
            else:
                # This checks if current is in the dictionary of children
                # if not, it has no parents, and will have been appended to path
                # if the queue is empty, it will be returned, otherwise the remainining parents are followed
                pass
    print(path)
    return path[-1] if len(path) > 1 else -1      

        