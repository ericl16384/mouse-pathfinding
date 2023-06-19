import random, time
import pygame

# waypoints = []

width = 35
height = 20

# start = (random.randint(0, width-1), random.randint(0, height-1))
# target = (random.randint(0, width-1), random.randint(0, height-1))
start = (1, 1)
target = (width-2, height-2)

density = 0.5

wall_destroying_cost = 100

autoplay_interval = 0.2

EMPTY = 0
WALL = 1
EDGE = WALL#"XX"
START = EMPTY#"@@"
END = EMPTY#"()"
DESTROYED = 2

def create_map():
    global map_contents
    map_contents = []
    for x in range(width):
        map_contents.append([])
        for y in range(height):
            if x == start[0] and y == start[1]:
                content = START
            elif x == target[0] and y == target[1]:
                content = END

            elif x == 0 or y == 0 or x == width-1 or y == height-1:
                content = WALL
            

            elif random.random() < density:
                content = WALL
            else:
                content = EMPTY

            map_contents[x].append(content)

def text_map():
    map = ""
    map += EDGE * (width + 2) + "\n"
    for y in range(height-1, -1, -1):
        map += EDGE
        for x in range(width):
            map += str(map_contents[x][y])
        map += "XX\n"
    map += EDGE * (width + 2) + "\n"
    return map

def print_map():
    print(text_map())

create_map()
# print_map()





class Pathfinder:
    class Node:
        def __init__(self, pos, parent, g, h):
            self.pos = pos
            self.parent = parent
            self.f = g + h
            self.g = g
            self.h = h
        
        def path_to_head(self):
            if self.parent:
                path = self.parent.path_to_head()
                path.append(self.pos)
                return path
            else:
                return [self]
        
        def path_from_head(self):
            path = self.path_to_head()
            path.reverse()
            return path
    
    class NoPathFound(Exception):
        "Raised when pathfinding search fails, either from an impossible map or from a max depth escape"
        pass

    def __init__(self, target, position, map_data=None):
        self.target = target
        self.position = position
        self.map_data = {}
        if map_data:
            self.add_map_data(map_data)

        self.path_stack = []
        self.recalculate_path()

        # self.last_pos = self.position

    def do_action(self):
        if len(self.path_stack) > 0:
            # self.last_pos = self.position
            next_pos = self.path_stack[-1]
            next_tile = None
            if next_pos in self.map_data:
                next_tile = self.map_data[next_pos]

            # break
            if next_tile == WALL:
                del self.map_data[next_pos]
                return ("break", next_pos)
            
            # move
            else:
                # self.position = next_pos.pos
                self.path_stack.pop()
                return ("move", next_pos)
            
        else:
            return ()
    
    # def move(self):
    #     self.last_pos = self.position
    #     if len(self.path_stack) > 0:
    #         self.position = self.path_stack.pop().pos
    #         return True
    #     else:
    #         return False
    
    # def apply_collision(self):
    #     self.position = self.last_pos
    #     self.path_stack = []

    def add_map_data(self, data):
        for location in data:
            self.map_data[location] = data[location]
    
    def recalculate_path(self, max_depth=1000):
        if self.position == self.target:
            self.path_stack = []
            return

        # (x, y) : Node
        closed_locations = {}
        open_locations = {}

        open_locations[self.position] = self.Node(self.position, None, 0, self.calculate_h_cost(self.position))

        depth = 1
        while depth < max_depth:
            if len(open_locations) == 0:
                raise Pathfinder.NoPathFound

            # find cheapest node
            best_location = None
            best_cost = 10**100
            best_node = None
            for location, node in open_locations.items():
                # # g = abs(pos[0] - self.position[0]) + abs(pos[1] - self.position[1])
                # h = abs(pos[0] - self.target[0]) + abs(pos[1] - self.target[1])
                # open_locations[location] = (g, h)
                # g, h = open_locations[location]

                if node.f < best_cost:
                    best_cost = node.f
                    best_location = location
                    best_node = node

            # bookkeeping
            closed_locations[best_location] = open_locations[best_location]
            del open_locations[best_location]

            # add more locations
            for location in self.get_possible_moves(best_location):
                g = best_node.g

                if location in self.map_data and self.map_data[location] == WALL:
                    g += wall_destroying_cost
                else:
                    g += 1


                if location in closed_locations:
                    continue
                    


                if location in open_locations:
                    existing_node = open_locations[location]
                    if g < existing_node.g:
                        existing_node.parent = best_node
                
                else:
                    node = self.Node(location, best_node, g, self.calculate_h_cost(location))
                    open_locations[location] = node
                    depth += 1

                    # print(self.map_data[location])
                
                    if location == self.target:
                        # target found!
                        self.path_stack = node.path_from_head()
                        self.path_stack.pop()
                        return


            # print(open_locations)
            # print(closed_locations)
            # return
    
        raise self.NoPathFound



    def calculate_h_cost(self, location):
        return abs(location[0] - self.target[0]) + abs(location[1] - self.target[1])

    def get_possible_moves(self, position):
        x, y = position
        return (
            (x + 1, y),
            (x, y + 1),
            (x - 1, y),
            (x, y - 1)
        )


bot = Pathfinder(target, start)

# for location in bot.get_possible_moves(bot.position):
#     try:
#         bot.add_map_data({location: map_contents[location[0]][location[1]]})
#     except IndexError:
#         pass
bot.add_map_data({bot.position: EMPTY})

bot.recalculate_path()

# for x in range(width):
#     for y in range(height):
#         bot.add_map_data({(x, y): map_contents[x][y]})

# bot.recalculate_path()

# print(bot.map_data)


# Colors
# Grayscale
WHITE  = 255, 255, 255
BLACK  =   0,   0,   0
GREY   = 128, 128, 128
# Primary
RED    = 255,   0,   0
GREEN  =   0, 255,   0
BLUE   =   0,   0, 255
# Secondary
YELLOW = 255, 255,   0
PURPLE = 255,   0, 255
CYAN   =   0, 255, 255



tile_display_size = 25

autoplay = False
last_move_time = time.time()


def handle_action(action):
    if len(action):
        assert len(action) == 2

        success = False

        if action[0] == "move":
            pos = action[1]
            x, y = pos
            if map_contents[x][y] == WALL:
                bot.add_map_data({pos: WALL})
            else:
                bot.position = pos
                success = True
        
        elif action[0] == "break":
            pos = action[1]
            x, y = pos
            if map_contents[x][y] == WALL:
                map_contents[x][y] = DESTROYED
                success = True
        
        if not success:
            bot.recalculate_path()



pygame.init()
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()

window_valid = True
while window_valid:
    clock.tick(60)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            window_valid = False  # Flag that we are done so we exit this loop
            break
        elif event.type == pygame.KEYDOWN:
            if not autoplay:
                handle_action(bot.do_action())
                last_move_time = time.time()

            if event.key == pygame.K_SPACE:
                autoplay = not autoplay

    if autoplay and time.time()-last_move_time >= autoplay_interval:
        handle_action(bot.do_action())
        last_move_time = time.time()
        


    bot.add_map_data({bot.position: map_contents[bot.position[0]][bot.position[1]]})
    if map_contents[bot.position[0]][bot.position[1]] == WALL:
        bot.apply_collision()
        try:
            bot.recalculate_path()
        except Pathfinder.NoPathFound:
            pass



    screen.fill(GREY)

    for location, tile in bot.map_data.items():
        if tile == EMPTY:
            color = WHITE
        elif tile == WALL:
            color = BLACK
        elif tile == DESTROYED:
            color = RED
        else:
            color = PURPLE

        x, y = location
        pygame.draw.rect(screen, color, (
            x*tile_display_size, y*tile_display_size,
            tile_display_size, tile_display_size
        ))
    
    pygame.draw.circle(screen, RED, [(i+0.5)*tile_display_size for i in target], 5)

    pygame.draw.circle(screen, BLUE, [(i+0.5)*tile_display_size for i in bot.position], 10)

    for i in range(len(bot.path_stack)-1):
        pygame.draw.line(screen, GREEN,
            [(j+0.5)*tile_display_size for j in bot.path_stack[i]],
            [(j+0.5)*tile_display_size for j in bot.path_stack[i+1]],
        )

    
    pygame.display.flip()

    

    assert map_contents[bot.position[0]][bot.position[1]] != WALL, map_contents[bot.position[0]][bot.position[1]]
