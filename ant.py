import pygame as pg
import numpy as np
import math
import random


WINSIZE = [400, 400]
CANSIZE = [100, 100]

#DON'T TOUCH
TURN_LEFT = -1 #"L"
TURN_RIGHT = 1 #"R"
TURN_STRAIGHT = 0 #"S"
TURN_U = 2 #U

RULES = "SLRU" # CHANGE ME!

TURNS = {"L":TURN_LEFT, "R":TURN_RIGHT, "S":TURN_STRAIGHT, "U":TURN_U}
UP = (0,-1)
RIGHT = (1,0)
LEFT = (-1,0)
DOWN = (0,1)

DIRECTIONS = [UP, RIGHT, DOWN, LEFT]
#END DON'T TOUCH

WHITE = (255,255,255,255)
RED = (255, 0, 0,255)
GREEN = (0,255,0,255)
BLUE = (0,0,255,255)
BLACK = (0,0,0,255)
YELLOW = (255,255,0,255)
CYAN = (0,255,255,255)

PALETTE = [WHITE, BLACK, CYAN, BLUE, GREEN, YELLOW, RED, MGRAY]
LGRAY = (200,200,200,255)
MGRAY = (150,150,150,255)
DGRAY = (100, 100, 100, 255)

ts = {WHITE:(LGRAY,TURN_LEFT), LGRAY:(DGRAY,TURN_LEFT), DGRAY:(BLACK,TURN_RIGHT), BLACK:(WHITE,TURN_RIGHT)}


class Ant():
    def __init__(self):
        self.pos = (50,50)
        self.dir = UP
        self.rules = ts
        
    def move(self):
        self.pos = np.add(self.pos,self.dir)
        self.pos = (self.pos[0]%CANSIZE[0], self.pos[1]%CANSIZE[1])
        
    def turn(self, d):
        #I'm a genius
        self.dir = DIRECTIONS[(DIRECTIONS.index(self.dir)+d)%4]
        
# converts a name (eg "LRLRL") and a list of colors into a dict to be used
def genRulesString(seed=0):
    if seed == 0:
        seed = random.randint(4, 4096)
        
    terms = math.ceil(math.log(seed,4))
    mask = 3
    shifts = 0
    s = ""
    for i in range(terms):
        s += list(TURNS)[(seed&mask)>>shifts]
        mask <<= 2
        shifts += 2
    return s
    
def genStates(name, palette):
    n = len(palette)
    if len(name) > len(palette):
        raise Exception("Not enough colors. {} states but only {} colors".format(len(name), len(palette)))
        
    states = {}
    for i in range(len(name)):
        states[palette[i]] = (palette[(i+1)%n], TURNS[name[i]])
    
	# make sure the states are cyclic
    if len(name) < len(palette):
        states[palette[len(name)-1]] = (palette[0], TURNS[name[i]])

    return states
    
      
def add(x, y):
    return ((x[0]+y[0]),(x[1]+y[1]))    

def update(surface,ant):
    p = tuple(surface.get_at(ant.pos))
    state = ant.rules[p]
    new_color = state[0]
    turn = state[1]
    surface.set_at(ant.pos, new_color)
    ant.turn(turn)
    ant.move()
    
def main():
    clock = pg.time.Clock()

    pg.init()
    screen = pg.display.set_mode(WINSIZE)
    
    canvas = pg.Surface((100,100))
    pg.display.set_caption("Ant")

    screen.fill(PALETTE[0])
    canvas.fill(PALETTE[0])

    ant1 = Ant()
    if RULES == "":
        rules = genRulesString()
        print(rules)
    else:
        rules = RULES
    ant1.rules = genStates(rules, PALETTE)

    
    done = 0

    while not done:
        update(canvas,ant1)
        pg.transform.scale(canvas, screen.get_size(), screen)
        pg.display.update()
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                done = 1
                break

        clock.tick(120)
    pg.quit()

if __name__ == "__main__":
    main()

#LRU Dancer
#LLR Highway
#LRS Draws cardinal lines and cleans them up
#LURSR Expands quickly as a blob
#LURSL Expands quickly as a blob
#LRRSL Expands as a squarish blob
#LLRR Expands symetrically like a brain
#LRSLR Lots of orthogonal lines with a blob in the middle
#LRULR Dancer
#LLUL Flag then a counting cycle?
#LLLRRR Diagonal highway
#LS Symmetric counter
#SLRU Fills the screen in very cool orderly ways