import pygame as pg
import numpy as np


WINSIZE = [400, 400]

#DON'T TOUCH
TURN_LEFT = -1
TURN_RIGHT = 1
TURN_STRAIGHT = 0

UP = (0,-1)
RIGHT = (1,0)
LEFT = (-1,0)
DOWN = (0,1)

DIRECTIONS = [UP, RIGHT, DOWN, LEFT]
#END DON'T TOUCH

RED = (255, 0, 0,255)
GREEN = (0,255,0,255)
BLUE = (0,0,255,255)
BLACK = (0,0,0,255)
WHITE = (255,255,255,255)

LGRAY = (200,200,200,255)
MGRAY = (150,150,150,255)
DGRAY = (100, 100, 100, 255)

ts = {WHITE:(LGRAY,TURN_LEFT), LGRAY:(DGRAY,TURN_LEFT), DGRAY:(BLACK,TURN_RIGHT), BLACK:(WHITE,TURN_RIGHT)}


class Ant():
    def __init__(self):
        self.pos = (50,50)
        self.dir = UP
        
    def move(self):
        self.pos = np.add(self.pos,self.dir)
        
    def turn(self, d):
        #I'm a genius
        self.dir = DIRECTIONS[(DIRECTIONS.index(self.dir)+d)%4]
        
        
def add(x, y):
    return ((x[0]+y[0]),(x[1]+y[1]))    

def update(surface,ant):
    p = tuple(surface.get_at(ant.pos))
    state = ts[p]
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

    screen.fill(WHITE)
    canvas.fill(WHITE)

    ant = Ant()

    done = 0

    while not done:
        update(canvas,ant)
        pg.transform.scale(canvas, screen.get_size(), screen)
        pg.display.update()
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                done = 1
                break

        clock.tick(60)
    pg.quit()

if __name__ == "__main__":
    main()
