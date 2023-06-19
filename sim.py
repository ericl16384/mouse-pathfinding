import random
import pygame

# waypoints = []

width = 20
height = 20

start = (random.randint(0, width-1), random.randint(0, height-1))
target = (random.randint(0, width-1), random.randint(0, height-1))

EMPTY = "  "
BLOCKED = "[]"
EDGE = "XX"
START = EMPTY#"@@"
END = EMPTY#"()"

def create_map():
    global map_contents
    map_contents = []
    for x in range(width):
        map_contents.append([])
        for y in range(height):
            if random.random() < 0.75:
                content = EMPTY
            else:
                content = BLOCKED
            
            if x == start[0] and y == start[1]:
                content = START
            if x == target[0] and y == target[1]:
                content = END

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
        def __init__(self, location, parent, g, h):
            self.location = location
            self.parent = parent
            self.f = g + h
            self.g = g
            self.h = h

    def __init__(self, target, position, map_data=None):
        self.target = target
        self.position = position
        self.map_data = {}
        if map_data:
            self.add_map_data(map_data)

        self.__planned_path = []
        self.recalculate_path()
    
    def next_move(self):
        pass

    def add_map_data(self, data):
        for location in data:
            self.map_data[location] = data[location]
    
    def recalculate_path(self):
        max_opens = 1000

        # (x, y) : f
        closed_locations = {}

        # (x, y) : (g, h)
        open_locations = {}

        # (x, y) : (x, y)
        connections = {}

        open_locations[self.position] = (0, self.calculate_h_cost(self.position))

        locations_opened = 0
        while locations_opened < max_opens:
            # find cheapest node
            best_location = None
            best_cost = 10**100
            for location in open_locations:
                # # g = abs(pos[0] - self.position[0]) + abs(pos[1] - self.position[1])
                # h = abs(pos[0] - self.target[0]) + abs(pos[1] - self.target[1])
                # open_locations[location] = (g, h)
                g, h = open_locations[location]

                f = g + h
                if f < best_cost:
                    best_cost = f
                    best_location = location
            
            locations_opened += 1

            prev_g = open_locations[best_location][0]

            # bookkeeping
            closed_locations[best_location] = open_locations[best_location]
            del open_locations[best_location]

            # add more locations
            for location in self.get_possible_moves(best_location):
                if location in self.map_data and self.map_data[location] == BLOCKED:
                    continue
                if location in closed_locations:
                    continue
                if location == self.target:
                    assert False # TODO
                
                new_g = prev_g + 1

                if location in open_locations:
                    if new_g < open_locations[location][0]:
                        h = open_locations[location][1]
                        open_locations[location] = (new_g, h)
                else:


            print(open_locations)
            print(closed_locations)
            return



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



pygame.init()
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()

window_valid = True
while window_valid:
    clock.tick(60)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            window_valid = False  # Flag that we are done so we exit this loop


    screen.fill(GREY)

    for x, column in enumerate(map_contents):
        for y, tile in enumerate(column):
            if tile == EMPTY:
                color = WHITE
            elif tile == BLOCKED:
                color = BLACK

            pygame.draw.rect(screen, color, (
                x*tile_display_size, y*tile_display_size,
                tile_display_size, tile_display_size
            ))

    pygame.draw.circle(screen, BLUE, [(i+0.5)*tile_display_size for i in bot.position], 10)

    
    pygame.display.flip()
