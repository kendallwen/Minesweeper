import math
import random
import numpy as np

class Minesweeper:
    def __init__(self):
        self.row = 24
        self.col = 24
        self.mines = 99
        self.size = self.row * self.col
        self.started = False
        self.won = False
        self.gameOver = False
        self.player_board = np.zeros([self.row, self.col])
        self.full_board = np.zeros([self.row, self.col])
    
    # create an empty board with a safe space around a player's initial choice
    def start(self, player_row, player_column):
        free_space = -1
        self.full_board[player_row][player_column] = free_space
        if player_row>0:
            self.full_board[player_row-1][player_column] = free_space
            if player_column>0: self.full_board[player_row-1][player_column-1] = free_space
            if player_column<self.col-1: self.full_board[player_row-1][player_column+1] = free_space
        if player_column>0:
            self.full_board[player_row][player_column-1] = free_space
            if player_row<self.row-1: self.full_board[player_row+1][player_column-1] = free_space
        if player_row<self.row-1:
            self.full_board[player_row+1][player_column] = free_space
            if player_column<self.col-1: self.full_board[player_row+1][player_column+1] = free_space
        if player_column<self.col-1: self.full_board[player_row][player_column+1] = free_space
        self.add_mines(player_row, player_column)
        self.make_board()
        self.expand(player_row, player_column)
        print(self.player_board)
        self.started = True
    
    # add an appropriate number of mines to the board while avoiding the player's
    # initial move
    def add_mines(self, player_row, player_column):
        i=0
        prob = self.mines/(self.row*self.col)
        while i<self.mines:
            r = math.floor(random.random()*self.row)
            c = math.floor(random.random()*self.col)
            if not self.full_board[r][c] == -1 or np.isnan(self.full_board[r][c]):
                self.full_board[r][c] = np.nan
                i += 1
        for j in range(self.row):
            for k in range(self.col):
                if self.full_board[j][k] == -1: self.full_board[j][k] = 0
    
    # increment the value of a spot on the board accordingly to its current value
    def increase_number(self, spot):
        if spot == 0: return 1
        if np.isnan(spot): return np.nan
        else: return spot+1    
    
    # increment the values of all spots beside a mine
    def add_numbers(self, row, column):
        up, down, left, right = row-1, row+1, column-1, column+1
        if np.isnan(self.full_board[row][column]):
            if up>=0:
                self.full_board[up][column] = self.increase_number(self.full_board[up][column])
                if left>=0: self.full_board[up][left] = self.increase_number(self.full_board[up][left])
                if right<len(self.full_board[row]): self.full_board[up][right] = self.increase_number(self.full_board[up][right])
            if down<len(self.full_board):
                self.full_board[down][column] = self.increase_number(self.full_board[down][column])
                if left>=0: self.full_board[down][left] = self.increase_number(self.full_board[down][left])
                if right<len(self.full_board[row]): self.full_board[down][right] = self.increase_number(self.full_board[down][right])
            if left>=0: self.full_board[row][left] = self.increase_number(self.full_board[row][left])
            if right<len(self.full_board[row]): self.full_board[row][right] = self.increase_number(self.full_board[row][right])
    
    # create the full board with mines and appropriate numbers
    def make_board(self):
        for i in range(self.row):
            for j in range(self.col):
                self.add_numbers(i,j)
    
    # expand the board based on a player's move
    def expand(self, r, c):
        if not np.isnan(self.full_board[r][c]):
            self.player_board[r][c] = self.full_board[r][c]
        if self.full_board[r][c] == 0:
            self.player_board[r][c] = -1
            if r-1 >= 0: 
                self.expand(r-1, c)
                if c-1 >= 0:
                    if not self.player_board[r-1][c-1] == -1:
                        self.expand(r-1, c-1) 
                if c+1 < self.col:
                    if not self.player_board[r-1][c+1] == -1:
                        self.expand(r-1, c+1)
            if r+1 < self.row:
                if not self.player_board[r+1][c] == -1:
                        self.expand(r+1, c)
                if c-1 >= 0:
                    if not self.player_board[r+1][c-1] == -1:
                        self.expand(r+1, c-1)
                if c+1 < self.col:
                    if not self.player_board[r+1][c+1] == -1:
                        self.expand(r+1, c+1)
            if c-1 >= 0:
                if not self.player_board[r][c-1] == -1:
                    self.expand(r, c-1)
            if c+1 < self.col:
                if not self.player_board[r][c+1] == -1:
                    self.expand(r, c+1)

    # count number of hidden spots on a board
    def count_hidden(self):
        count = 0
        for i in range(self.row):
            for j in range(self.col):
                if self.player_board[i][j]==0: count = count+1
        return count
    
    def play_move(self, r, c):
        if self.started:
            if np.isnan(self.full_board[r][c]):
                self.gameOver = True
                print('Need more training')
            else:
                self.expand(r, c)
                print(self.player_board)
                if self.count_hidden() == self.mines:
                    self.gameOver = True
                    self.won = True
        else:
            self.start(r, c)
        return self.count_hidden()