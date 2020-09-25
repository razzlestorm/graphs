from room import Room
from player import Player
from world import World

import heapq
from collections import deque
import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# create dictionary of mapped rooms/vertices
mapped_rooms = {}
# create initial key/value (unknown edges) of room

'''
# Set up queue to use:
class PriorityQueue:
    def __init__(self):
        self.elements: Array[T] = []
    
    def empty(self) -> bool:
        return len(self.elements) == 0
    
    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self) -> T:
        return heapq.heappop(self.elements)[1] 

# Do A* (returning path) over the mapped rooms, looking for closest '?'
def heuristic(a: source_coords, b: dest_coords) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(map, cur_room, goal: ???):
    frontier = PriorityQueue()
    frontier.put(cur_room.get_coords())
    came_from = {}
    cost_so_far = {}
    came_from[cur_room] = None
    cost_so_far[cur_room] = 0    

    while not frontier.empty():
        current = frontier.get()
    
        if current == goal:
            break'''
   

# function to search for path to nearest '?'
def bfs(cur_room, dest):
    q = deque()
    visited = set()
    q.appendleft([cur_room]) # list of room ids

    while len(q) > 0:
        cur_path = q.pop()
        cur_node = cur_path[-1] # room id

        # checking if ? in values of cur_node's dict
        if dest in mapped_rooms[cur_node].values():
            return cur_path
        
        if cur_node not in visited:
            visited.add(cur_node)

            # get confirmed neighbors and add to q
            for neighbor in mapped_rooms[cur_node].values():
                n_path = cur_path.copy()
                n_path.append(neighbor)
                q.appendleft(n_path)
    return None
    

def get_opposite(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    else:
        return 'e'

# add starting room to stack
stack = deque([player.current_room.id])

while len(stack) > 0:
    cur_room = stack.pop()
    breakpoint()
    
    if cur_room in mapped_rooms:
        # as we move into '?' room:
        if '?' in mapped_rooms[cur_room].values():
            # note done, check all values
            for k, v in mapped_rooms[cur_room].items():
                if v == '?':
                    player.travel(k)
                    traversal_path.append(k)
                    new_room = player.current_room.id
                    ## create key of new room's id, with values of new room's directions = '?'
                    if new_room not in mapped_rooms:
                        mapped_rooms[new_room] = {key: '?' for key in player.current_room.get_exits()}
                    ## update the values of direction_to and direction_from in both new/old room keys
                    mapped_rooms[cur_room][k] = new_room
                    mapped_rooms[new_room][get_opposite(k)] = cur_room
                    # means we aren't done with prev node
                    if '?' in mapped_rooms[cur_room].values():
                        stack.append(cur_room)
                    stack.append(new_room)
                    break
                else:
                    pass

        # means we should be done with this room
        else:
            # find next path
            path = bfs(cur_room, '?')

            if path is not None:
                # translate path to movements:
                for node in path[1:]:
                    # k = direction, v = node.id
                    for k, v in mapped_rooms[cur_room].items():
                        if v == node:
                            player.travel(k)
                            traversal_path.append(k)
                            cur_room = player.current_room.id
                if cur_room not in stack:            
                    stack.append(cur_room)
            
            else:
                print(f'traversal path: {traversal_path}')
                break   

    # first time we've been in this room
    elif cur_room not in mapped_rooms:
        mapped_rooms[player.current_room.id] = {key: '?' for key in player.current_room.get_exits()}
        stack.append(cur_room)
                

        


## update cost of moving from one room to this new room/update cost to all '?'s?




# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
