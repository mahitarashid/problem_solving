import math
import random
import pygame

class Cube(object):
    '''
        Cube is the building block of the Snake
    '''
    rows = 20
    w = 500
    def __init__(self, start, dirnx = 1, dirny = 0, color = (230, 95, 92)):
        self.pos = start
        self.dirnx = 1 ##will start moving right when we run the program
        self.dirny = 0
        self.color = color
        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    
    def draw(self, surface, eyes = False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        #pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2)) #so you can 
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis, dis)) #so you can 

        #print(f"dis={dis}, w={self.w}, rows={self.rows}")
        #print(self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        #see the white lines of the grid (the Snake won't block them)
        if eyes:
            center = dis//2 #middle of Cube
            radius = 3
            circleMiddle = (i * dis + center - radius, j * dis + 8) #x is 8 pixels up everytime
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class Snake(object):
    '''
        Snake object is essentially composed of
        - body: an increasingly larger list of cubes
        - turns: next turns to take
    '''
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos) #Cube at given position
        self.body.append(self.head) 
        self.dirnx = 0 #x direction for moving Snake 
        self.dirny = 1 #y dir
        
    def move(self):
        #event = pygame.event.wait()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            elif event.type == pygame.KEYDOWN:

                keys = pygame.key.get_pressed() #gets all key values, if they're pressed or not
                
                #for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    #key: current position of the Snake's head (equals what direction we turned)

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        # -- Get the elements of body--currently head only    
        for i, c in enumerate(self.body): #get index and Cube object in self.body
            p = c.pos[:]
            print(f"Got p={p}")
            if p in self.turns:
                turn = self.turns[p]
                print(f"Found turn={turn}")
                c.move(turn[0], turn[1]) #which way to move
                if i == len(self.body) - 1: #if we're on last Cube
                    self.turns.pop(p) #remove that turn
                    
            else:
                ## checking whether or not we've reached the edge of the screen
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows - 1, c.pos[1]) #if moving left & at edge, then change position to right side by changing x value by 1
                elif c.dirnx == 1 and c.pos [0] >= c.rows-1: c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos [1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows - 1)
                else: 
                    c.move(c.dirnx, c.dirny) #not at edge, just move normally in the specified direction
            
    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head) 
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        
    def addCube(self):
        tail = self.body[-1]  # last cube
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0: # direction is to the right
            self.body.append (Cube((tail.pos[0] - 1, tail.pos[1]))) 
        elif dx==-1 and dy == 0:
            self.body.append (Cube((tail. pos[0] + 1, tail.pos[1]))) 
        elif dx == 0 and dy == 1:
            self.body.append (Cube((tail.pos[0], tail.pos[1]-1))) 
        elif dx == 0 and dy == -1:
            self.body.append (Cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
    
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True) #draw eyes
            else:
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    
    x = 0
    y = 0
    for l in range(rows):
        x += sizeBtwn
        y += sizeBtwn
        #draws 2 lines during every loop of this for loop
        #                             position:     start.   end.  
        pygame.draw.line(surface, (245, 247, 220), (x, 0), (x, w))
        pygame.draw.line(surface, (245, 247, 220), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((15, 3, 38))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()
    

def randomSnack(rows, item):
    positions = item.body #new list, equal to a Snake object

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0: #list of a filtered list,
        #see if any of the positions are the same as the current position of the Snake
            continue
        else:
            break
    return (x, y)


def main():
    global width, rows, s, snack
    width = 500
    height = 500
    rows = 20 ##must be evenly divisible by 500
    win = pygame.display.set_mode((width, height))
    s = Snake((230, 95, 92), (10, 10)) ##starts with color red, position (10, 10)
    snack = Cube(randomSnack(rows, s), color = (181, 217, 156))
    flag = True 
              
    clock = pygame.time.Clock()
    
    redrawWindow(win)

              
    while flag:
        pygame.time.delay(100) ##delays 50 milliseconds everytime to program isn't too fast  
        clock.tick(10) ##game doesn't run over 10 frames per second, not too fast
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = Cube(randomSnack(rows, s), color = (181, 217, 156))
        
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x + 1:])):
                print('Score: ', len(s.body))
                s.reset((10, 10))
                break

        redrawWindow(win)


    pass


main()