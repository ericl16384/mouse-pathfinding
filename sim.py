import random

# waypoints = []

width = 20
height = 20

start = [random.randint(0, width-1), random.randint(0, height-1)]
end = [random.randint(0, width-1), random.randint(0, height-1)]

EMPTY = "  "
BLOCKED = "[]"
EDGE = "XX"
START = "@@"
END = "()"

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
            if x == end[0] and y == end[1]:
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
print_map()
