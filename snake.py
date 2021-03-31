from tkinter import *
import random

class Snake:
    body = [[5,2],[5,3],[5,4],[5,5]]
    dirx = 0 
    diry = 0

    def print(self):
        print(self.body)

    def check_head(self, i):
        if i == self.body[0]:
            return True
        else:
            return False

    def check(self,i):
        if i in self.body[1:]:
            return True
        else:
            return False

    def take_step(self, width, height):
        newx = self.body[0][0] + self.dirx
        newy = self.body[0][1] + self.diry

        newx = s.check_bound(s, newx, width)
        newy = s.check_bound(s, newy, height)

        self.body.insert(0, [newx, newy])
        self.body.pop()
        
    def check_bound(self, i, max):
        if i < 0:
            i += max
        elif i >= max:
            i -= max
        return i

    def add_body(self, width, height):
        newx = self.body[len(self.body) -1][0] - self.dirx
        newy = self.body[len(self.body) - 1][1] - self.diry

        newx = s.check_bound(s, newx, width)
        newy = s.check_bound(s, newy, height)

        self.body.append([newx, newy])

    def change_direction(self, key):
        if key == 'w':
            self.dirx = 0
            self.diry = -1
        elif key == 'a':
            self.dirx = -1
            self.diry = 0
        elif key == 's':
            self.dirx = 0
            self.diry = 1
        elif key == 'd':
            self.dirx = 1
            self.diry = 0


class Apple:
    x = 0
    y = 0

    def __init__(self, width, height):
        self.x = random.randint(0, width - 1)
        self.y = random.randint(0, height - 1)

    def set_pos(self, width, height):
        self.x = random.randint(0, width - 1)
        self.y = random.randint(0, height - 1)

def check_app_coll(a, s):
    if s.check_head(s, [a.x, a.y]):
        return True
    else:
        return False

height = 10
width = 15
score = 0

s = Snake
a = Apple(width, height)

while True:
    key = input()

    if key == 'f':
        break

    s.change_direction(s, key)
    s.take_step(s, width, height)

    if check_app_coll(a, s):
        a.set_pos(width, height)
        s.add_body(s, width, height)
        score += 1

    print("+",end='')
    for k in range(0, width):
        print("-",end='')
    print("+\tscore: ", score)

    for i in range(0,height):
        print("|", end='')
        for k in range(0,width):
            if a.x == k and a.y == i:
                print("A", end='')
            elif s.check_head(s, [k,i]) == True:
                print("x", end='')
            elif s.check(s, [k, i]) == True:
                print("o", end='')
            else:
                print(" ",end='')
        print("|")

    print("+",end='')
    for k in range(0, width):
        print("-",end='')
    print("+")