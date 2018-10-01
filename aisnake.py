#!/usr/bin/python

#           _____    _____             _        
#     /\   |_   _|  / ____|           | |       
#    /  \    | |   | (___  _ __   __ _| | _____ 
#   / /\ \   | |    \___ \| '_ \ / _` | |/ / _ \
#  / ____ \ _| |_   ____) | | | | (_| |   <  __/
# /_/    \_\_____| |_____/|_| |_|\__,_|_|\_\___|
#
#                 _   _                         _   _                              
#     /\         | | | |                       | \ | |                             
#    /  \   _ __ | |_| |__   ___  _ __  _   _  |  \| | __ _ _   _ _   _  ___ _ __  
#   / /\ \ | '_ \| __| '_ \ / _ \| '_ \| | | | | . ` |/ _` | | | | | | |/ _ \ '_ \ 
#  / ____ \| | | | |_| | | | (_) | | | | |_| | | |\  | (_| | |_| | |_| |  __/ | | |
# /_/    \_\_| |_|\__|_| |_|\___/|_| |_|\__, | |_| \_|\__, |\__,_|\__, |\___|_| |_|
#                                        __/ |         __/ |       __/ |           
#                                       |___/         |___/       |___/            
#   An AI written in python 3 to play snake.
#   AI Snake by Anthony Nguyen 001390353
#   This program was written for CS 3750.03
#   Finished Mon Oct 1 16:00:45 PDT 2018
#
#   Run on terminal using command:
#   $ python aisnake.py
#   or
#   $ ./aisnake.py
#
#
#   Optional arguments:
#   $ python aisnake.py <ROWS> <COLUMNS> <SPEED>
#
#   Example:
#   $ python aisnake.py 20 20 50
#
#   PLEASE BE SURE TO RESIZE YOUR TERMINAL ACCORDINGLY

import time
import sys
import curses
from random import randint

# Map class will keep the location of all symbols
# Also includes fitness function for distance between snake and food
class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.chars = {
                0: ' . ',
                1: ' # ',
                2: ' @ ',
                3: ' * ',
                }
        self.create_map()
        self.player_pos = []
        self.create_food()

    # create map of size w x h 
    def create_map(self):
        self.map = [[0 for j in range(self.h)] for i in range(self.w)]

    def reset_map(self):
        self.map = [[j if j!=1 and j!=2 else 0 for j in i] for i in self.map]
    
    # place food in random location
    def create_food(self):
        food_created = True
        while(food_created):
            i = randint(0, self.w-1)
            j = randint(0, self.h-1)
            food = [i, j]

            if food not in self.player_pos:
                self.map[i][j] = 3
                food_created = False
    
    def run(self, screen):
        w = self.w
        h = self.h
        self.reset_map()
        for i, j in self.player_pos:
            self.map[i][j] = 1
        player = self.player_pos[-1]
        self.map[player[0]][player[1]] = 2
        for i in range(w):
            row = ''
            for j in range(h):
                row += self.chars[ self.map[i][j] ]
            screen.addstr(i, 0, row)

    #return food location
    def get_food(self):
        for i in range(self.w):
            for j in range(self.h):
                if self.map[i][j] == 3:
                    return [i, j]
        return [-1, -1]

    #fitness function. calculates distance between snake and food
    def get_next_dist(self, a, b):
        food_x = -1
        food_y = -1
        for i in range(self.w):
            for j in range(self.h):
                if self.map[i][j] == 3:
                    food_x = i
                    food_y = j
        play_x= -1
        play_y = -1
        for i in range(self.w):
            for j in range(self.h):
                if self.map[i][j] == 2:
                    play_x = i+b
                    play_y = j+a
        if play_x < 0:
            return 999
        elif play_x > self.w -1:
            return 999
        elif play_y < 0:
            return 999
        elif play_y > self.h -1:
            return 999
        if self.map[play_x][play_y] == 1:
            return 999

        dist = ((play_x-food_x)**2+(play_y-food_y)**2)**(1/2)

        return dist

    # detects food collision with player
    def food_collision(self):
        player = self.player_pos[-1]
        food = self.get_food()
        return food == player

class Player:
    def __init__(self):
        self.lost = False
        self.face = curses.KEY_RIGHT
        self.pos = [[0, 0], [0, 1], [0, 2], [0, 3]]

    #prevents ai from 180 turns
    def turn(self,key):
        if (self.face == curses.KEY_DOWN and key == curses.KEY_UP) or (self.face == curses.KEY_UP and key == curses.KEY_DOWN) or (self.face == curses.KEY_LEFT and key == curses.KEY_RIGHT) or (self.face == curses.KEY_RIGHT and key == curses.KEY_LEFT):
            return
        else:
            self.face = key
    
    #increase tail length by 1
    def grow(self):
        tail = self.pos[0][:]

        if self.pos[0][0] < self.pos[1][0]:
            tail[0] -= 1
        elif self.pos[0][0] > self.pos[1][0]:
            tail[1] += 1
        elif self.pos[0][1] < self.pos[1][1]:
            tail[1] -= 1           
        elif self.pos[0][1] > self.pos[1][1]:
            tail[1] += 1  

        tail = self.max(tail)
        self.pos.insert(0, tail)

    # check if still living
    def living(self):
        player = self.pos[-1]
        body = self.pos[:-1]
        return player not in body

    # deprecated
    def lose(self): 
        #self.lost = True
        #sys.exit() 
        return

    # allow snake to 'cheat' if needed
    def max(self, pt):
        if pt[0] > self.mp.w-1:
            pt[0] = 0
        elif pt[0] < 0:
            pt[0] = self.mp.w-1
        elif pt[1] < 0:
            pt[1] = self.mp.h-1
        elif pt[1] > self.mp.h-1:
            pt[1]=0
        return pt

    def gen_map(self, mp):
        self.mp = mp
    
    def quit(self):
        sys.exit()

    def ai_move(self):
        if self.lost:
            return
        else:
            player = self.pos[-1][:]
            fitness = [ self.mp.get_next_dist(0,-1) ,self.mp.get_next_dist(1,0) , self.mp.get_next_dist(0,1) , self.mp.get_next_dist(-1,0)  ] # up right down left
            if self.face == curses.KEY_UP:
                fitness[2] = 999
            if self.face == curses.KEY_RIGHT:
                fitness[3] = 999
            if self.face == curses.KEY_DOWN:
                fitness[0] = 999
            if self.face == curses.KEY_LEFT:
                fitness[1] = 999 
            move = fitness.index(min(fitness))
            if move == 0:
                player[0]-=1
                self.turn(curses.KEY_UP)
            elif move == 1:
                player[1]+=1
                self.turn(curses.KEY_RIGHT)
            elif move == 2:
                player[0]+=1
                self.turn(curses.KEY_DOWN)
            elif move == 3:
                player[1]-=1
                self.turn(curses.KEY_LEFT)
            player = self.max(player)
            del(self.pos[0])
            self.pos.append(player)
            self.mp.player_pos = self.pos
            if not self.living():
                self.lose()

            if self.mp.food_collision():
                curses.beep()
                self.grow()
                self.mp.create_food()


def main(screen):
    screen.timeout(0)
    width = 20
    height = 20
    speed = 100

    if len(sys.argv) > 1:
        width = int(sys.argv[1])
    if len(sys.argv) > 2:
        height = int(sys.argv[2])
    if len(sys.argv) > 3:
        speed = int(sys.argv[3])
    mp = Map(width,height)
    player = Player()
    player.gen_map(mp)
    while(1):
        key = screen.getch()
        if key != -1:
            player.quit(key)
        player.ai_move()
        mp.run(screen)
        screen.refresh()
        time.sleep(10/speed)
if __name__=='__main__':
    curses.wrapper(main)

