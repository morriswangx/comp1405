import pygame
import sys

# Window colors
SCREEN_R = 212
SCREEN_G = 224
SCREEN_B = 236

# refresh frequency
FREQUENCY = 120

# Window
WIDTH, HEIGHT = 1250, 900
TITLE = "Assignment 10 - Text Adventure"
# General setup
pygame.init()
pygame.font.init()
map = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Area colors and initialization information
WHITE = [255,255,255]
GREEN = [0,180,0]
GRAY = [120,120,120]
RED = [255,0,0]
PINK = [120,0,0]
LIGHT = [170, 170, 170]

AREA_BASE_COLOR_R = 25
AREA_BASE_COLOR_G = 25
AREA_BASE_COLOR_B = 25
AREA_BASE_W = 300
AREA_BASE_H = 200
AREA_COLOR_INCREMENTS = 35
AREA_START_X = 18
AREA_START_Y = 174

# Player colors
PLAYER_COLOR_R = 250
PLAYER_COLOR_G = 120
PLAYER_COLOR_B = 60
# Player size
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 12

# dictionary to keep track of the areas already built. It will be populated during startup.
loaded_areas = {}

AREA_DESCRIPTIONS = ["FR: the family room is a private room for the whole family. It has a fireplace.",
                     "DR: the dinning room is usually for dinners. Sometimes we entertain guests there.",
                     "K: the kitchen is where food is made. It could be noisy but this is also where sandwiches are made for you to take.",
                     "GAR: the garage is rarely used for cars. It gets cold in winter.",
                     "GR: the Game room is where magic happens. Whatever happens in the game room stays in the game room.",
                     "L: the library has a lot of interesting books. Hurry to claim your own.",
                     "CR: the computer room is where you can browse the internet of whatever you want. It is a convinient way of getting information quickly.",
                     "RS: the recording studio is where you can record songs and make beats. It needs good sound insulation.",
                     "GM: the gym is where you burn calories and have fun while doing it. You don't need a lot of equipment to have a good workout,",
                     "MT: the movie theatre allows you to watch your favourite movies over and over. It's normally in the basement.",
                     "TC: the tennis court is next to the swimming pool and the lawn. It allows you to play singles or doubles.",
                     "LN: the lawn is gorgeous with a tree in the middle. It's next to the golf course.",
                     "SR: the storage room is where useful tools or instruments are stored. Claim your prize here.",
                     "CB: the chicken barn has lots of chickens. But there is one rooster and it is noisy in the morning.",
                     "HB: the horse barn has horses. They are a graceful animal.",
                     "GD: the garden is where you can grow flowers or vegetables. They need constant care.",
                     "SP: the swimming pool has beautiful blue water. They are perfect for a hot summer day.",
                     "PP: the ping pong room is where you can play ping pong with family or friends. It could get intense.",
                     "GC: the golf course is a full 21-hole-course. It's always packed with players in the summer.",
                     "CF: the corn field produces lots of sweet corn in the summer. They are the best."
                     ]

# Area name list
AREA_FULL_NAMES =["Family Room","Dining Room",          "Kitchen",      "Garage",       "Game Room",        "Library",      "Computer Room",
                  "Recording Studio","Gym",             "Movie Threatre","Tennis Court","Lawn",             "Storage Room", "Chicken Barn",
                  "Horse Barn",      "Garden",          "Swimming Pool", "Ping Pong",   "Golf Course",      "Corn Field"]

# Area name list
AREA_NAMES =     ["FR",         "DR",                   "K",            "GAR",          "GR",               "L",            "CR",
                  "RS",         "GM",                   "MT",           "TC",           "LN",               "SR",           "CB",
                  "HB",         "GD",                   "SP",           "PP",           "GC",               "CF"]

# Adjacency list correlates to the area name list
AREA_ADJ_LIST = [["SP", "DR"],  ["FR", "K", "GAR"],     ["DR", "GR"],   ["DR","CR"],    ["K","L","CR"],     ["GR","GM"],    ["GAR","GR","RS"],
                 ["CR","TC"],   ["L","GD","MT","LN"],   ["GM"],         ["RS","PP"],    ["GM","SR","HB"],   ["LN","CB"],    ["SR"],
                 ["LN","CF"],   ["GC","GM"],            ["FR"],         ["TC"],         ["GD"],             ["HB"]]

# Area exits/entrances directions lists that correlates to the area name list
AREA_EXITS =    [['E','S'],     ['N','E','S'],          ['W','S'],      ['N','E'],      ['N','E','S'],      ['W','E'],      ['W','N','E'],
                 ['W','S'],     ['W','N','S','E'],      ['N'],          ['N','E'],      ['W','S','E'],      ['N','E'],      ['W'],
                 ['W','N'],     ['N','S'],              ['W'],          ['W'],          ['S'],              ['S']]

# Area size (width and height pairs) lists that correlates to the area name list
AREA_SIZES =    [[229, 112],    [180,174],              [202,113],      [217,246],      [131,120],          [152,70],       [166,67],
                 [114,93],      [254,122],              [211,66],       [233,116],      [143,246],          [114,96],       [295,71],
                 [282,112],     [158,94],               [119,82],       [134,46],       [352,202],          [232,376]]

PRIZES_LIST =    [[],         [],              [["Sandwiches"],[3]],    [],             [["Games"],[3]],  [["Books"],[3]],        [],
                  [],         [],              [],                      [],             [],               [["Tennis Rackets", "Pingpong Rackets", "Golf Clubs", "Golf Balls"],[4,4,12,100]], [],
                  [],         [],              [],                      [],             [],               []]

# exit size
EXIT_SIZE = 20

# check if a tuple is inside the rectangle
# sx,sy: tuple;
# rx,ry,rw,rh: rectangle parameters
def isInRect(sx,sy,rx,ry,rw,rh):
   if sx >= rx and sx <= rx + rw and sy >= ry and sy <= ry+rh:
       return True
   return False
def isInAnyRect(sx,sy):
   for key in loaded_areas.keys():
       rect = loaded_areas[key]
       rx = rect[0]
       ry = rect[1]
       rw = rect[2]
       rh = rect[3]
       if isInRect(sx,sy,rx,ry,rw,rh):
           return key
   return None
def updateText(size, text, color, x, y):
    # blit the names
    myfont = pygame.font.SysFont("arial", size, True)
    textSurface = myfont.render(text, True, color)
    TextRect = textSurface.get_rect()
    TextRect.center = [x, y]
    map.blit(textSurface, TextRect)

def loadAreas():
    # The previous adjacent area coorindates and sizes
    cur_x, cur_y, cur_w, cur_h = 0,0,0,0
    prev_x, prev_y, prev_w, prev_h = 0,0,0,0
    cur_exit = ''
    cur_color = [AREA_BASE_COLOR_R , AREA_BASE_COLOR_G, AREA_BASE_COLOR_B]

    # loop through the name list to load areas one by one
    for i in range (len(AREA_NAMES)):
        cur_area_name= AREA_NAMES[i]
        cur_area_description = AREA_DESCRIPTIONS[i]
        cur_area_adjacent_list = AREA_ADJ_LIST[i]
        cur_area_size = AREA_SIZES[i]
        cur_area_exits = AREA_EXITS[i]

        cur_w = cur_area_size[0]
        cur_h = cur_area_size[1]

        # Area colors:
        surface = pygame.Surface([cur_w, cur_h])
        # outdoor spaces in green
        if cur_area_name in ["CF", "GC", "LN", "TC", "GD"]:
            cur_color = GREEN
            surface.fill(cur_color)
            cur_color = [AREA_BASE_COLOR_R, AREA_BASE_COLOR_G, AREA_BASE_COLOR_B]
        # indoor areas with non-green colors
        elif i % 3 == 0:
            cur_color = [cur_color[0]+AREA_COLOR_INCREMENTS,cur_color[1],cur_color[2]]
            surface.fill(cur_color)
        elif i % 3 == 1:
            cur_color = [cur_color[0], cur_color[1]+ AREA_COLOR_INCREMENTS, cur_color[2]]
            surface.fill(cur_color)
        else:
            cur_color = [cur_color[0], cur_color[1], cur_color[2]+AREA_COLOR_INCREMENTS]
            surface.fill(cur_color)

        # load the surface rectangles
        if i == 0:
            # start position
            cur_x = AREA_START_X
            cur_y = AREA_START_Y
        else:
            # get the relative position of the new area
            for j in range(len(cur_area_adjacent_list)):
                if cur_area_adjacent_list[j] in loaded_areas.keys():
                    lval = loaded_areas[cur_area_adjacent_list[j]]
                    prev_x = lval[0]
                    prev_y = lval[1]
                    prev_w = lval[2]
                    prev_h = lval[3]
                    cur_exit = cur_area_exits[j]
            #
            # calculate the top-left coordinate for the current area beyond the very first one
            #
            # Prev area is in the north
            if cur_exit == 'N':
                cur_x = prev_x + prev_w/2 - cur_w/2
                cur_y = prev_y + prev_h
            # Prev area is in the south
            elif cur_exit == 'S':
                cur_x = prev_x + prev_w/2 - cur_w/2
                cur_y = prev_y - cur_h
            # Prev area is in the west
            elif cur_exit == 'W':
                cur_x = prev_x + prev_w
                cur_y = prev_y + prev_h/2 - cur_h/2
            # Prev area is in the east
            elif cur_exit == 'E':
                cur_x = prev_x - cur_w
                cur_y = prev_y + prev_h/2 - cur_h/2

        # remember the current area information to calculate the next one
        loaded_areas[cur_area_name] = [cur_x, cur_y, cur_w, cur_h]

        # load the area
        map.blit(surface, [cur_x, cur_y])

        # blit the full area names
        updateText (12, AREA_FULL_NAMES[AREA_NAMES.index(cur_area_name)], WHITE, cur_x+cur_w/2, cur_y + cur_h/2)

    # blit  all exit markers as a white bar
    for key in loaded_areas.keys():
        lval = loaded_areas[key]
        _x = lval[0]
        _y = lval[1]
        _w = lval[2]
        _h = lval[3]

        ind = AREA_NAMES.index(key)
        cur_exit = AREA_EXITS[ind]

        # drawing the white bar
        for i in range (len(cur_exit)):
            val = cur_exit[i]
            if val == 'N':
                # draw a white line to indicate the exit
                pygame.draw.line(map, WHITE, (_x + _w / 2 - EXIT_SIZE / 2, _y + 1),
                                 (_x + _w / 2 + EXIT_SIZE / 2, _y + 1), 2)
            # Prev area is in the south
            elif val == 'S':
                # draw a white line to indicate the exit
                pygame.draw.line(map, WHITE, (_x + _w / 2 - EXIT_SIZE / 2, _y + _h - 3),
                                 (_x + _w / 2 + EXIT_SIZE / 2, _y + _h - 3), 2)

            # Prev area is in the west
            elif val == 'W':
                # draw a white line to indicate the exit
                pygame.draw.line(map, WHITE, (_x + 1, _y + _h / 2 - EXIT_SIZE / 2),
                                 (_x + 1, _y + _h / 2 + EXIT_SIZE / 2), 2)

            # Prev area is in the east
            elif val == 'E':
                # draw a white line to indicate the exit
                pygame.draw.line(map, WHITE, (_x + _w -3, _y + _h / 2 - EXIT_SIZE / 2),
                                 (_x + _w -3, _y + _h / 2 + EXIT_SIZE / 2), 2)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.x = int(x)
        self.y = int(y)
        self.color = (PLAYER_COLOR_R, PLAYER_COLOR_G, PLAYER_COLOR_B)
        # velocity x or y directions
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 20

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def update_default(self):
        # velocity
        self.velX = 0
        self.velY = 0

        # figure out the movement
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed

        # adjust horizontally so the player square doesn't go out of boundary
        self.x += self.velX
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - PLAYER_WIDTH:
            self.x = WIDTH - PLAYER_WIDTH

        # adjust vertically so the player square doesn't go out of boundary
        self.y += self.velY
        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT - PLAYER_HEIGHT:
            self.y = HEIGHT - PLAYER_HEIGHT

        # update the full description of each area
        global cur_area
        cur_area = isInAnyRect(self.x, self.y)
        if cur_area is None:
            updateText(15, "Out of bound.", RED, WIDTH/2, HEIGHT*0.9)
        else:
            updateText(15, AREA_DESCRIPTIONS[AREA_NAMES.index(cur_area)], GRAY, WIDTH/2, HEIGHT*0.9)
            # update the prizes if any
            prizes = PRIZES_LIST[AREA_NAMES.index(cur_area)]
            if len(prizes) > 0:
                prize_names = prizes[0]
                prize_quantity = prizes[1]
                msg = "Inventory: "
                for i in range (len(prize_names)):
                    msg += str(prize_quantity[i]) + " " + prize_names[i] + " "
                updateText(15, msg, PINK, WIDTH / 2, HEIGHT * 0.93)

                # build buttons to take one item out of the inventory
                smallfont = pygame.font.SysFont('Corbel', 25)
                text = smallfont.render('Take one', True, PINK)
                pygame.draw.rect(map, LIGHT, [WIDTH - 150, HEIGHT * 0.96, 100, 40])
                # superimposing the text onto our button
                map.blit(text, (WIDTH - 150, HEIGHT * 0.96))

        # draw a rectangle shaped player
        self.rect = pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)


#
# main section
#
# player initialization:
player = Player(AREA_START_X, AREA_START_Y + AREA_BASE_H / 2)
running = True
while running:

    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Actions - key down
        if event.type == pygame.KEYDOWN:
            # left arrow pressed
            if event.key == pygame.K_LEFT:
                player.left_pressed = True
            # right arrow pressed
            if event.key == pygame.K_RIGHT:
                player.right_pressed = True
            # up arrow pressed
            if event.key == pygame.K_UP:
                player.up_pressed = True
            # down arrow pressed
            if event.key == pygame.K_DOWN:
                player.down_pressed = True
        # Actions - key up
        if event.type == pygame.KEYUP:
            # left arrow released
            if event.key == pygame.K_LEFT:
                player.left_pressed = False
            # right arrow released
            if event.key == pygame.K_RIGHT:
                player.right_pressed = False
            # up arrow released
            if event.key == pygame.K_UP:
                player.up_pressed = False
            # down arrow released
            if event.key == pygame.K_DOWN:
                player.down_pressed = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if the mouse is clicked on the Take one button
            # one item is taken from the prize list
            if WIDTH -150 <= mouse[0] <= WIDTH -50 and HEIGHT *0.96 <= mouse[1] <= HEIGHT *0.96 + 40:
                prizes = PRIZES_LIST[AREA_NAMES.index(cur_area)]
                if len(prizes) > 0:
                    prize_names = prizes[0]
                    prize_quantity = prizes[1]
                    # take off one item from the inventory after each click
                    for i in range(len(prize_quantity)):
                        if prize_quantity[i] > 0:
                            prize_quantity[i] -= 1
                            break
                    # update the inventory
                    msg = "Inventory: "
                    for i in range(len(prize_names)):
                        msg += str(prize_quantity[i]) + " " + prize_names[i] + " "
                    updateText(15, msg, PINK, WIDTH / 2, HEIGHT * 0.93)

    # set window color
    map.fill((SCREEN_R, SCREEN_G, SCREEN_B))

    # load all the areas
    loadAreas()

    player.draw(map)
    # player.update(cur_x, cur_y, cur_w, cur_h, "")
    player.update_default()
    # display everything
    pygame.display.flip()

    # run the while loop FREQUENCY times per second
    clock.tick(FREQUENCY)
