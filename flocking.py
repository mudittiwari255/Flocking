from random import randint
import random
from Tkinter import *
import math

#Screen's Aspect Ratio
HEIGHT  = 684   
WIDTH = 480
#Number of Birds  osah oahoho hi iho[ ] hoi[h fffffffffffffffffffffffffffff]

AMOUNT = 0
WALL = 10   #Useless
R = 30
N_R = 100
clumping_factor = 8
schooling_factor = 100
boids = []
hurdle = True

class TwoD:

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return 'TwoD(%s, %s)' % (self.x, self.y)

    def __add__(self, other):
        return TwoD(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return TwoD(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return TwoD(self.x * other, self.y * other)

    def __div__(self, other):
        return TwoD(self.x / other, self.y / other)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __idiv__(self, other):
        if isinstance(other, TwoD):
            self.x /= other.x if other.x else 1
            self.y /= other.y if other.y else 1
        else:
            self.x /= other
            self.y /= other
        return self
    def mag(self):
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5
    def byAxis(self, axis):
        if axis == 1:
            return self.y
        else:
            return self.x
    def unit(self):
    	self.x = self.x * (1 / self.mag())
    	self.y = self.y * (1 / self.mag())
    	return self
def transform(tuples):
    return TwoD(tuples[0], tuples[1])

#Boid's Class

class Node:
    #Constructor or Initialiser
    def __init__(self, position , velocity, left, right):
        self.position = transform(position)
        self.velocity = transform(velocity)
    
    def __repr__(self):
        return '<Pos: x = %s, y = %s><Vel: x = %s, y = %s> ' % (self.position.x, self.position.y, self.velocity.x, self.velocity.y)
    
    def rule1(self, boids):
        # clumping
        vector = TwoD(0, 0)
        for boid in boids:
            if boid is not self:
                vector += boid.position
        if len(boids) > 1:
            vector /= len(boids) - 1
        return (vector - self.position) / clumping_factor

    def rule2(self, boids):
        # avoidance
        vector = TwoD(0, 0)
        for boid in boids:
            if boid is not self:
                if (self.position - boid.position).mag() < R:
                    vector -= (boid.position - self.position)
        return vector
    def rule5(self, h):
        vector = TwoD(0,0)
        if (self.position - h).mag() < 50:
            vector -= (h - self.position)
        return vector
    def rule3(self, boids):
        # schooling
        vector = TwoD(0, 0)
        for boid in boids:
            if boid is not self:
                vector += boid.velocity
        if len(boids) > 1:
            vector /= len(boids)  - 1
        return (vector - self.velocity) / schooling_factor
    #Updates velocity
    def rule4(self, boids):
        return (boids[0].position - self.position)/100
    def bound_position(self):
        v = TwoD(0,0)
        if self.position.x < 10:
            v.x = 10
        elif self.position.x > WIDTH -10:
            v.x = -10
        if self.position.y < 10:
            v.y = 10
        elif self.position.y > HEIGHT - 10:
            v.y = -10
        return v

    def distance(self, point):
        x1 = point[0]
        y1 = point[1]
        x2 = self.position.x
        y2 = self.position.y
        return ((x1 - x2)**2 +(y1 - y2)**2)**0.5

    def boundPos(self, width, height):
        x = 0
        y = 0
        if self.position.x < 0 :
            x = 10
        elif self.position.x > width :
            x = -10
        if self.position.y < 0 : 
            y = 10
        elif self.position.y > 0 : 
            y = -10
        return TwoD(x,y)
    
    def boid_vision(self):
        x0 = self.position.x
        y0 = self.position.y
        if self.velocity.x != 0 :
            slope = float(self.velocity.y) / float(self.velocity.x)
            slope1 = math.atan(math.radians(slope)) + 2*math.pi / 3
            C1 = y0 - slope1 * x0
            x3 = x0 + math.sqrt(100**2/(1 + slope1 ** 2))
            x4 = slope1 * x3 + C1
            slope2 = math.atan(math.radians(slope)) - 2*math.pi /3
            C2 = y0 - slope2 * x0
            x5 = x0 + math.sqrt(100**2/(1 + slope2**2))
            x6 = slope2 * x5 + C2
            c, r = circumcircle((x0,y0),(x3,x4),(x5,x6))
        else:
            c = (x0,y0)
            r = 100
        return c,r
    
    def random_motion(self):
        self.velocity = transform(rand(n))

def limit_speed(boid):
    if boid.velocity.mag() > 10 :
        boid.velocity /= boid.velocity.mag() / 5

def float_compare(x,y):
    if x>y:
        return 1
    elif x==y:
        return 0
    else:
        return -1   

def mouse_event(eventorigin):
    x = eventorigin.x
    y = eventorigin.y
    boids.append(Node((x,y),(0.5,0.5),None,None))

def draw():
    graph.delete(ALL)
    #graph.create_rectangle(0,0,50,50, fill = 'blue')
    #graph.create_rectangle(WIDTH, HEIGHT , WIDTH - 50, HEIGHT - 50, fill = 'blue')
    if hurdle is True:
        global j
        j = 200
        y1 = j
        x1 = j
        x2 = j + 40
        y2 = j + 40
        graph.create_oval((x1,y1,x2,y2), fill = 'green')
    for boid in boids:
        if len(find_neighbour(boid,boids)) is 0:
            x1 = boid.position.x - 5
            y1 = boid.position.y - 5
            x2 = boid.position.x + 5
            y2 = boid.position.y + 5
            graph.create_oval((x1, y1, x2, y2), fill = 'red')
        else:
            x1 = boid.position.x - 5
            y1 = boid.position.y - 5
            x2 = boid.position.x + 5
            y2 = boid.position.y + 5        
            graph.create_oval((x1, y1, x2, y2), fill = 'black')
        x0 = boid.position.x
        y0 = boid.position.y
        x3 = boid.velocity.x + boid.position.x
        x4 = boid.velocity.y + boid.position.y
        if boid.velocity.x != 0:
            slope = float(boid.velocity.y) / float(boid.velocity.x)
            C = y0 - slope * x0
            x3 = x0 + math.sqrt(12**2/(1 + slope ** 2))
            x4 = slope * x3 + C
        #if len(find_neighbour(boid,boids)) is 0: 
        #    x3 = boid.velocity.x + boid.position.x
        #    x4 = boid.velocity.y + boid.position.y
        graph.create_line(x0,y0,x3,x4,arrow =LAST, fill = 'black')
    graph.update()

def generateBoids(amount , width, height):
    for i in range(amount):
        x = randint(10,width-10)
        y = randint(10,height - 10)
        boids.append(Node((x,y),(0.5,0.5),None,None))

def simulate_wall(boid):
    if boid.position.x < WALL:
        boid.velocity.x += 20
    elif boid.position.x > WIDTH - WALL:
        boid.velocity.x -= 20
    if boid.position.y < WALL:
        boid.velocity.y += 20
    elif boid.position.y > HEIGHT - WALL:
        boid.velocity.y -= 20

def simulate_wall1(boid):
    if boid.position.x < WALL - 10:
        boid.position.x = WIDTH -10
    elif boid.position.x > WIDTH + 10:
        boid.position.x = WALL + 10
    if boid.position.y < WALL - 10:
        boid.position.y = HEIGHT + 10
    if boid.position.y > HEIGHT + 10:
        boid.position.y = WALL + 10

def move_things1():
    for boid in boids:
        nbr = find_neighbour(boid, boids)
        v1 = boid.rule1(nbr)
        v2 = boid.rule2(nbr)
        v3 = boid.rule3(nbr)
        h = transform((j + 15, j + 15))
        v4 = boid.rule5(h)
        #v5 = boid.bound_position()
        if len(nbr) is 0:
            boid.velocity = TwoD(random.uniform(0,10), random.uniform(0,10))
        else:
            boid.velocity = boid.velocity + v1 + v2 + v3 + v4
        limit_speed(boid)
       #print boid.velocity
        boid.position = boid.position + boid.velocity
        #simulate_wall1(boid)
def find_distance(A,B):
    d1 = A.position.x - B.position.x
    d2 = A.position.y - B.position.y
    return math.sqrt(d1**2 + d2**2)

def find_neighbour(hero,boids):
    dist = N_R
    nbr = []
    for boid in boids:
        if boid is not hero:
            d = find_distance(hero, boid)
            if (d < dist):
                nbr.append(boid)
    return nbr
def find_neighbour2(hero, boids):
    dist = N_R
    nbr = []
    for boid in boids:
        #if boid is not hero:
        c,r = hero.boid_vision()
        graph.create_oval(c[0]-r, c[1] - r, c[0] + r, c[1] + r)
        if math.sqrt((boid.position.x - c[0])**2 + (boid.position.y - c[1])**2) <= r:
            nbr.append(boid)
    return nbr
def main():
    initialise()
    graph.bind("<Button 1>",mouse_event)
    mainloop()


def initialise():
    # Setup simulation variables.
    global node
    #arr = [(250,300),(200,300),(300,400),(300,200),(400,200)]
    generateBoids(AMOUNT, WIDTH, HEIGHT)
    build_graph()
def not_randomaly_generate_boids(arr):
    for elements in arr:
        boids.append(Node(elements, (0,0), None, None))    
def build_graph():
    global graph
    root = Tk()
    root.overrideredirect(False)
    root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, (root.winfo_screenwidth() - WIDTH) / 2, (root.winfo_screenheight() - HEIGHT) / 2))
    root.bind_all('<Escape>', lambda event: event.widget.quit())
    graph = Canvas(root, width=WIDTH, height=HEIGHT, background='white')
    graph.after(40,update)
    graph.pack()
def update():
    draw()
    move_things1()
    graph.after(40, update)
    
if __name__ == '__main__':
    main()

