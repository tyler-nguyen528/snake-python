from tkinter import *
import random
import threading
import time

scale = 20 #make sure the width and height are both divisible by scale
global speed #in milliseconds

def game(w, s, a):          #Game logic for single player
    w.Can.delete("all")

    s.change_direction()
    s.take_step(width, height)

    if s.check(s.body[0]):
        w.end(1)
        return

    if s.check_app_coll(a):
        a.set_pos(width, height)
        s.add_body(width, height)
        w.score += 1
        w.label['text'] = "Score: " + str(w.score)

    w.Can.create_rectangle(a.x - scale/2, a.y - scale/2, a.x + scale/2, a.y + scale/2, fill="red")
    w.Can.create_oval(s.body[0][0] - scale/2,s.body[0][1] - scale/2,s.body[0][0] + scale/2,s.body[0][1] + scale/2, fill="yellow")

    for i in range(1, len(s.body)):
        w.Can.create_oval(s.body[i][0] - scale/2,s.body[i][1] - scale/2,s.body[i][0] + scale/2,s.body[i][1] + scale/2, fill="blue")

    w.m.after(speed, game, w, s ,a)


def game2(w, s, s2, a):     #Game Logic for 2 player mode
    w.Can.delete("all")

    s.change_direction()
    s2.change_direction()
    s.take_step(width, height)
    s2.take_step(width, height)

    if s.check(s.body[0]): #2 Player, Player 1 hit themselves
        w.end(2)
        return
        
    if s2.check(s2.body[0]): #2 Player, Player 2 hit themselves
        w.end(3)
        return

    if s2.check(s.body[0]): #2 Player, Player 1 hit Player 2's body
        w.end(4)
        return

    if s.check(s2.body[0]): #2 Player, Player 2 hit Player 1's body
        w.end(5)
        return

    if s.check_app_coll(a):
        a.set_pos(width, height)
        s.add_body(width, height)

    if s2.check_app_coll(a):
        a.set_pos(width, height)
        s2.add_body(width, height)

    #draw apple
    w.Can.create_rectangle(a.x - scale/2, a.y - scale/2, a.x + scale/2, a.y + scale/2, fill="red")

    #draw head of player 1 snake
    w.Can.create_oval(s.body[0][0] - scale/2,s.body[0][1] - scale/2,s.body[0][0] + scale/2,s.body[0][1] + scale/2, fill="yellow")
    #draw body of player 1 snake
    for i in range(1, len(s.body)):
        w.Can.create_oval(s.body[i][0] - scale/2,s.body[i][1] - scale/2,s.body[i][0] + scale/2,s.body[i][1] + scale/2, fill="blue")

    #draw player 2 snake
    w.Can.create_oval(s2.body[0][0] - scale/2,s2.body[0][1] - scale/2,s2.body[0][0] + scale/2,s2.body[0][1] + scale/2, fill="green")
    #draw body of player 2 snake
    for i in range(1, len(s2.body)):
        w.Can.create_oval(s2.body[i][0] - scale/2,s2.body[i][1] - scale/2,s2.body[i][0] + scale/2,s2.body[i][1] + scale/2, fill="purple")

    w.m.after(speed, game2, w, s, s2 ,a)

class Snake:                #class for snake body (player controlled object)
    body = 0
    dirx = 0    #current direction in the x axis
    diry = -1   #current direction in the y axis **Negative means Up, positive means down
    newx = 0    #buffer for direction in the x axis
    newy = -1   #buffer for direction in the y axis  **Negative means Up, positive means down

    def __init__(self, width, height):
        self.body = [[300,200],[300,200+1*scale],[300,200+2*scale],[300,200+3*scale],[300,200+4*scale]]
        self.width = width
        self.height = height

    def check_head(self, i):    #check first node
        if i == self.body[0]:
            return True
        else:
            return False

    def check(self,i):          #check if i node has the same coords as a body part (for collisions)
        if i in self.body[1:]:
            return True
        else:
            return False

    def take_step(self, width, height):         #update each node of the body with the current direction
        newx = self.body[0][0] + scale*self.dirx
        newy = self.body[0][1] + scale*self.diry

        newx = s.check_bound(newx, width)
        newy = s.check_bound(newy, height)

        self.body.insert(0, [newx, newy])
        self.body.pop()
        
    def check_app_coll(self, a):                #check if the head node of the current snake has the same coords as the apple
        if self.check_head([a.x, a.y]):
            return True
        else:
            return False

    def check_bound(self, i, max):              #check if a body node is at the border so that it can loop back around
        if i <= 0:
            i += max - scale
        elif i >= max:
            i -= max - scale
        return i

    def add_body(self, width, height):
        newx = self.body[len(self.body) -1][0] - self.dirx
        newy = self.body[len(self.body) - 1][1] - self.diry

        newx = s.check_bound(newx, width)
        newy = s.check_bound(newy, height)

        self.body.append([newx, newy])

    def check_input(self, press):
        if press.char == 'w' and self.diry != 1:
            self.newx = 0
            self.newy = -1
        if press.char == 'a' and self.dirx != 1:
            self.newx = -1
            self.newy = 0
        if press.char == 's' and self.diry != -1:
            self.newx = 0
            self.newy = 1
        if press.char == 'd' and self.dirx != -1:
            self.newx = 1
            self.newy = 0

    def change_direction(self):
        self.dirx = self.newx
        self.diry = self.newy

    def reset(self):
        self.body = [[300,200],[300,200+1*scale],[300,200+2*scale],[300,200+3*scale],[300,200+4*scale]]
        self.dirx = 0 
        self.diry = -1
        self.newx = 0
        self.newy = -1

class Snake2(Snake):
    def __init__(self, width, height):
        self.body = [[700,200],[700,200+1*scale],[700,200+2*scale],[700,200+3*scale],[700,200+4*scale]]
        self.width = width
        self.height = height

    def check_input(self, press):
        if press.keycode == 38 and self.diry != 1:
            self.newx = 0
            self.newy = -1
        if press.keycode == 37 and self.dirx != 1:
            self.newx = -1
            self.newy = 0
        if press.keycode == 40 and self.diry != -1:
            self.newx = 0
            self.newy = 1
        if press.keycode == 39 and self.dirx != -1:
            self.newx = 1
            self.newy = 0


    def reset(self):
        self.body = [[700,200],[700,200+1*scale],[700,200+2*scale],[700,200+3*scale],[700,200+4*scale]]
        self.dirx = 0 
        self.diry = -1
        self.newx = 0
        self.newy = -1

class Apple:
    x = 0
    y = 0

    def __init__(self, width, height):
        self.x =scale* random.randint(1, width/scale-1)
        self.y = scale*random.randint(1, height/scale-1)

    def set_pos(self, width, height):
        self.x = scale* random.randint(1, width/scale-1)
        self.y = scale*random.randint(1, height/scale-1)


class Window:
    player_mode = 1
    diff_mode = 1

    def __init__(self, s, s2, a, score):
        self.s = s
        self.s2 = s2
        self.a = a
        self.score = score

        self.m = Tk()
        self.m.title("Snake")
        self.m.configure(bg="dark gray")

        self.butt_Frame = Frame(self.m, bg="dark gray")
        self.butt_Frame.pack(side=TOP, anchor='w')

        self.Can = Canvas(self.m, bg="white", height=600, width=1000)
        self.test_Butt = Button(self.butt_Frame, text='Start', width=20, state="disabled", command=lambda: self.choose_Mode())
        self.p1_Butt = Button(self.butt_Frame, text='1 Player', width=20, command=lambda: self.P1_start())
        self.p2_Butt = Button(self.butt_Frame, text='2 Players', width=20, command=lambda: self.P2_start())
        self.easy_Butt = Button(self.butt_Frame, text='Easy Mode', width=20, state="disabled", command=lambda: self.easy_Press())
        self.hard_Butt = Button(self.butt_Frame, text='Hard Mode', width=20, command=lambda: self.hard_Press())
        self.diff_label = Label(self.butt_Frame, font="System 10", text="Current Difficulty: Easy", bg="dark gray")
        
        #self.test_Butt.pack(in_=self.butt_Frame, padx = (25,15), pady=(5, 5), side=LEFT)
        self.test_Butt.pack(in_=self.butt_Frame, padx = (15,15), side=LEFT)
        self.p1_Butt.pack(in_=self.butt_Frame, side=LEFT)
        self.p2_Butt.pack(in_=self.butt_Frame, padx = (0,15),  side=LEFT)
        self.easy_Butt.pack(in_=self.butt_Frame, side=LEFT)
        self.hard_Butt.pack(in_=self.butt_Frame, padx = (0,15), side=LEFT)
        self.diff_label.pack(in_=self.butt_Frame, side=LEFT)

        self.Can.create_text(self.s.width/2,self.s.height/2, fill="black", font="System 20", text="Select a Mode!")
        
        self.Can.bind_all('<Key>', self.w_pressed)

        self.Can.pack(side=BOTTOM)

        self.m.resizable(False,False)

        self.m.mainloop()

    def end(self, end_state):
        if end_state == 1: #Single Player died
            self.Can.create_text(self.s.width/2,self.s.height/2, fill="black", font="System 100", text="Game Over!!!!!\nScore: "+ str(self.score) +"\nSelect a Mode")
            self.label.destroy()
        elif end_state == 2:    #2 Player, Player 1 hit themselves
            self.Can.create_text(self.s.width/2,self.s.height/2, fill="black", font="System 100", text="Player 1 Hit Themselves\nPlayer 2 Wins!!!\nSelect a Mode")
        elif end_state == 3:    #2 Player, Player 2 hit themselves
            self.Can.create_text(self.s.width/2,self.s.height/2, fill="black", font="System 100", text="Player 2 Hit Themselves\nPlayer 1 Wins!!!\nSelect a Mode")
        elif end_state == 4:    #2 Player, Player 1 hit Player 2's body
            self.Can.create_text(self.s.width/2,self.s.height/2, fill="black", font="System 100", text="Player 1 Crashed into Player 2\nPlayer 2 Wins!!!\nSelect a Mode")
        elif end_state == 5:    #2 Player, Player 2 hit Player 1's body
            self.Can.create_text(self.s.width/2,self.s.height/2, fill="black", font="System 100", text="Player 2 Crashed into Player 1\nPlayer 1 Wins!!!\nSelect a Mode")

        self.s.reset()
        self.s2.reset()

        self.score = 0
        
        self.p1_Butt["state"] = "normal"
        self.p2_Butt["state"] = "normal"

        if self.diff_mode == 1:  #re-add the difficulty text
            self.easy_Butt["state"] = "disabled"
            self.hard_Butt["state"] = "normal"
            diff_text = "Current Difficulty: Easy"
        else:
            self.easy_Butt["state"] = "normal"
            self.hard_Butt["state"] = "disabled"
            diff_text = "Current Difficulty: Hard"

        self.diff_label = Label(self.butt_Frame, font="System 10", text=diff_text, bg="dark gray")
        self.diff_label.pack(in_=self.butt_Frame, side=LEFT)

    def choose_Mode(self):
        self.test_Butt["state"] = "disabled"
        self.easy_Butt["state"] = "disabled"
        self.hard_Butt["state"] = "disabled"

        self.diff_label.destroy()    #remove difficulty text since the game is about to start

        global speed

        if self.diff_mode == 1: #easy/slower
            speed = 100
        elif self.diff_mode == 2: #hard/faster
            speed = 50

        if self.player_mode == 1:  #single player
            self.label = Label(self.butt_Frame, font="System 10", text="Score: "+ str(self.score), bg = "dark gray")
            self.label.pack(in_=self.butt_Frame, side=LEFT)

            self.p2_Butt["state"] = "disabled"

            self.countdown(4)
            self.m.after(3000, game, self, self.s, self.a)
        elif self.player_mode == 2: #2 player
            self.p1_Butt["state"] = "disabled"

            self.countdown(4)
            self.m.after(3000, game2, self, self.s, self.s2, self.a)

    def countdown(self, i):
        if i == 1:
            return
        else:
            i -= 1

        self.Can.delete("all")

        #draw head of player 1 snake
        self.Can.create_oval(self.s.body[0][0] - scale/2,self.s.body[0][1] - scale/2,self.s.body[0][0] + scale/2,self.s.body[0][1] + scale/2, fill="yellow")
        #draw body of player 1 snake
        for k in range(1, len(self.s.body)):
            self.Can.create_oval(self.s.body[k][0] - scale/2,self.s.body[k][1] - scale/2,self.s.body[k][0] + scale/2,self.s.body[k][1] + scale/2, fill="blue")

        if self.player_mode == 2:
            self.Can.create_oval(self.s2.body[0][0] - scale/2,self.s2.body[0][1] - scale/2,self.s2.body[0][0] + scale/2,self.s2.body[0][1] + scale/2, fill="green")
            #draw body of player 2 snake
            for j in range(1, len(s2.body)):
                self.Can.create_oval(self.s2.body[j][0] - scale/2,self.s2.body[j][1] - scale/2,self.s2.body[j][0] + scale/2,self.s2.body[j][1] + scale/2, fill="purple")

        
        self.Can.create_text(self.s.width/2,self.s.height/2, fill="black", font="System 100", text=str(i))
        self.m.after(1000, self.countdown, i)

    
    def easy_Press(self):
        self.diff_mode = 1
        self.easy_Butt["state"] = "disabled"
        self.hard_Butt["state"] = "normal"
        self.diff_label["text"] = "Current Difficulty: Easy"

    def hard_Press(self):
        self.diff_mode = 2
        self.easy_Butt["state"] = "normal"
        self.hard_Butt["state"] = "disabled"
        self.diff_label["text"] = "Current Difficulty: Hard"

    def P1_start(self):
        self.Can.delete("all")
        self.p1_Butt["state"] = "disabled"
        self.p2_Butt["state"] = "normal"
        self.test_Butt["state"] = "normal"
        self.Can.create_text(self.s.width/2,self.s.height/2, fill="black", font="System 20", text="Collect as Many Red Squares Without Hitting Yourself. Press Start!")
        self.player_mode = 1

    def P2_start(self):
        self.Can.delete("all")
        self.p1_Butt["state"] = "normal"
        self.p2_Butt["state"] = "disabled"
        self.test_Butt["state"] = "normal"
        self.Can.create_text(self.s.width/2,self.s.height/2, fill="black", font="System 20", text="Try to make the other player crash into your body! Press Start!")
        self.player_mode = 2

    def w_pressed(self, event):
        if event.char == 'w' or event.char == 'a' or event.char == 's' or event.char == 'd': 
            self.s.check_input(event)
        elif event.keycode == 37 or event.keycode == 38 or event.keycode == 39 or event.keycode == 40:
            self.s2.check_input(event)


height = 600
width = 1000
score = 0

s = Snake(width, height)
s2 = Snake2(width, height)
a = Apple(width, height)
w = Window(s, s2, a, score)