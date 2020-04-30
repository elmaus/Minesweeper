import tkinter as tk
from tkinter import messagebox
import random

import sys
sys.setrecursionlimit(20000)


class Tile(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, args[0], width=2, height=1, text='', font=('Roboto', 8, 'bold'), bg='white',
                           command=kwargs['command'])
        self.is_bomb = False
        self.adjacent_bomb = 0
        self.searched = False


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self)
        self.title("Sam's Minesweeper")
        self.wm_iconbitmap('eyecon.ico')
        self._row = 20
        self._col = 20
        self.tiles = []
        self.number_of_bombs = 50
        self.time = 0
        self.game = 'standby'
        self.not_bomb = 0


        ####### list to loop for adding and subtraction rows and columns of adjacent tiles
        #### for 8 (top, left, right, bottom and 4 corners) rows and columns arround adjacent tiles
        self.adj_row = [-1, -1, -1, 0, +1, +1, +1, 0]
        self.adj_col = [-1, 0, +1, +1, +1, 0, -1, -1]
        #### for 4 (top, left, right, bottom) rows and columns arround adjacent tiles
        self.ar = [-1, 0, +1, 0]
        self.ac = [0, +1, 0, -1]
        ####### ----------------------------------------------------------------------------------


        ###### ------------------ GUI ------------------######
        self.frame1 = tk.Frame(self, relief='raised')
        self.frame1.pack()
        #### -------------------
        self.ref_btn = tk.Button(self.frame1, text='Refresh', width=20, command=lambda:self.refresh())
        self.ref_btn.pack()
        #### -------------------
        self.frame2 = tk.Frame(self, relief='groove', bd=4)
        self.frame2.pack()
        ###### ------------------ GUI ------------------######

        self.GenerateTiles()


    def refresh(self):

        ''' Refresh the game and make all the components configuration back to default '''

        for i in range(self._row):
            for j in range(self._col):
                target = self.tiles[i][j]
                target.configure(text='', relief='raised', bg='white')
                target.adjacent_bomb = 0
                target.is_bomb = False
                target.searched = False
        self.generate_bomb()
        self.count_adjacent_bomb()


    def GenerateTiles(self):

        ''' Creating tiles '''

        for i in range(self._row):
            y = []
            for j in range(self._col):
                t = Tile(self.frame2, command=lambda i=i, j=j:self.search(i, j))
                t.grid(row=i, column=j)
                y.append(t)
            self.tiles.append(y)

        # then create bombs from these tiles and count adjacent tiles width bomb
        self.generate_bomb()
        self.count_adjacent_bomb()


    def check_win(self):

        ''' check if there is no empty tiles to open '''

        if self.not_bomb == self._row * self._col - self.number_of_bombs:
            self.game = 'standbay'
            tk.messagebox.showinfo('Congratulation!', "You win!")


    def explode(self):

        ''' revealing all the tiles '''

        for i in range(self._row):
            for j in range(self._col):
                target = self.tiles[i][j]
                if target.is_bomb:
                    target.configure(text='*', relief='sunken', bg='red')
                else:
                    if target.adjacent_bomb == 0:
                        target.configure(relief='sunken', bg='dark grey')
                    else:
                        target.configure(text=target.adjacent_bomb, relief='sunken', bg='dark grey')



    def search(self, x, y):

        '''
            start the timer on the first click
            check if the tile is a bomb
            if the tile has a adjacent bomb, will reveal the umber of adjacent bomb
            if the tile has no adjacent bomb, will pass all adjacent tile to this function recursively
        '''

        target = self.tiles[x][y]

        if target.is_bomb:
            self.time = 0
            self.game = 'standby'
            self.explode()
            return

        if target.searched:
            return

        if target.adjacent_bomb > 0:
            target.configure(text=target.adjacent_bomb, relief='sunken', bg='dark grey')
            target.searched = True
            return
        if target.adjacent_bomb == 0:
            target.configure(relief='sunken', bg='dark grey')
            target.searched = True
            for ai, aj in zip(self.ar, self.ac):
                if x + ai >= 0 and x + ai <= self._row - 1 and y + aj <= self._col - 1 and y + aj >= 0:
                    self.search(x + ai, y + aj)
                else:
                    return


    def generate_bomb(self):

        ''' creating bombs '''

        for i in range(self.number_of_bombs):
            is_a_bomb = False
            while not is_a_bomb:
                bomb = self.tiles[random.randint(0, self._row - 1)][random.randint(0, self._col - 1)]
                if bomb.is_bomb == False:
                    bomb.is_bomb = True
                    is_a_bomb = True
        return


    def count_adjacent_bomb(self):
        for i in range(self._row):
            for j in range(self._col):
                tile = self.tiles[i][j]
                for ai, aj in zip(self.adj_row, self.adj_col):
                    if tile.is_bomb == False:
                        if i + ai >= 0 and i + ai <= self._row - 1 and j + aj <= self._col - 1 and j + aj >= 0:
                            if self.tiles[i + ai][j + aj].is_bomb:
                                tile.adjacent_bomb +=1



if __name__ == '__main__':
    app = App()
    app.mainloop()
