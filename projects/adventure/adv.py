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


# Set up queue to use:
class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1] 

# Do dijkstra's (returning path) over the mapped rooms, looking for closest '?'
## Something going wrong in this search, not sure, but I suspect it has to do
## with finding the '?' in a room's values.

'''def dijkstra_search(mapped, start_room, dest):
    queue = PriorityQueue()
    queue.put(start_room, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start_room] = None
    cost_so_far[start_room] = 0

    while not queue.empty():
        cur_room = queue.get()
        
        if dest in mapped[cur_room].values():
            break

        for neighbor in mapped[cur_room].values():
            new_cost = cost_so_far[cur_room] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost
                queue.put(neighbor, priority)
                came_from[neighbor] = cur_room
    dest = [k for k in cost_so_far.keys()][-1]
    return came_from, dest

def rebuild_path(came_from, start_room, dest):
    cur_room = dest
    path = []
    while cur_room != start_room:
        path.append(cur_room)
        cur_room = came_from[cur_room]
    path.append(start_room)
    path.reverse()
    return path'''
   

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
    # first time we've been in this room
    if cur_room not in mapped_rooms:
        mapped_rooms[player.current_room.id] = {key: '?' for key in player.current_room.get_exits()}

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
                    # append new room player is in to stack
                    stack.append(new_room)
                    break
                else:
                    pass

        # means we should be done with this room
        else:
            # find next path
            if cur_room != player.current_room.id:
                print(f'ERROR CHECK THIS ROOM: {cur_room}, {player.current_room.id}')
            path = bfs(cur_room, '?')
            # came_from, dest = dijkstra_search(mapped_rooms, cur_room, '?')
            # path = rebuild_path(came_from, cur_room, dest)

            if path is not None:
                # translate path to movements:
                for node in path[1:]:
                    # k = direction, v = node.id
                    try:
                        for k, v in mapped_rooms[cur_room].items():
                            if v == node:
                                player.travel(k)
                                traversal_path.append(k)
                                cur_room = player.current_room.id
                    except KeyError:
                        print(f'{traversal_path}')
                        print(f'pathlen: {len(traversal_path)}, dictlen{len(mapped_rooms)}')
                        print(mapped_rooms)
                        print('KEYERROR')
                if cur_room not in stack:            
                    stack.append(cur_room)
            
            else:
                # Search can't find any other '?'s
                print(f'traversal path: {traversal_path}\n length: {len(traversal_path)}')
                break    


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
