import math
import random

# print a row of the board
def print_row(row):
    r = ''
    for i in range(len(row)):
        r += str(row[i])
    return r

# print the entire board
def print_board(board):
    for i in range(len(board)):
        print(print_row(board[i]))
    return

# create a fully hidden board
def start_board(rows, columns):
    hidden_space = '_'
    board = []
    for j in range(rows):
        row = []
        for i in range(columns):
            row.append(hidden_space)
        board.append(row)
    return board

# create an empty board with a safe space around a player's initial choice
def empty_board(rows, columns, player_row, player_column):
    empty_space = ' '
    free_space = 'f'
    board = []
    for j in range(rows):
        row = []
        for i in range(columns):
            row.append(empty_space)
        board.append(row)
    board[player_row][player_column] = free_space
    if player_row>0:
        board[player_row-1][player_column] = free_space
        if player_column>0: board[player_row-1][player_column-1] = free_space
        if player_column<columns-1: board[player_row-1][player_column+1] = free_space
    if player_column>0:
        board[player_row][player_column-1] = free_space
        if player_row<rows-1: board[player_row+1][player_column-1] = free_space
    if player_row<rows-1:
        board[player_row+1][player_column] = free_space
        if player_column<columns-1: board[player_row+1][player_column+1] = free_space
    if player_column<columns-1: board[player_row][player_column+1] = free_space
    return board

# add an appropriate number of mines to the board while avoiding the player's
# initial move
def add_mines(board, mines, rows, columns):
    i=0
    prob = mines/(rows*columns)
    while i<mines:
        r = math.floor(random.random()*rows)
        c = math.floor(random.random()*columns)
        if board[r][c] != 'f':
            board[r][c] = 'm'
            i += 1
    for j in range(rows):
        for k in range(columns):
            if board[j][k] == 'f': board[j][k] = ' '
    return board

# increment the value of a spot on the board accordingly to its current value
def increase_number(spot):
    if spot == ' ': return 1
    if spot == 'm': return 'm'
    else: return spot+1    

# increment the values of all spots beside a mine
def add_numbers(board, row, column):
    up, down, left, right = row-1, row+1, column-1, column+1
    if board[row][column] == 'm':
        if up>=0:
            board[up][column] = increase_number(board[up][column])
            if left>=0: board[up][left] = increase_number(board[up][left])
            if right<len(board[row]): board[up][right] = increase_number(board[up][right])
        if down<len(board):
            board[down][column] = increase_number(board[down][column])
            if left>=0: board[down][left] = increase_number(board[down][left])
            if right<len(board[row]): board[down][right] = increase_number(board[down][right])
        if left>=0: board[row][left] = increase_number(board[row][left])
        if right<len(board[row]): board[row][right] = increase_number(board[row][right])
    return

# create the full board with mines and appropriate numbers
def full_board(board, rows, columns):
    for i in range(rows):
        for j in range(columns):
            add_numbers(board,i,j)
    return board

def minesweeper():
    mines = int(input("How many mines would you like? ")) # Number of mines
    rows = int(input("How many rows in the board? ")) # Number of rows
    cols = int(input("How many columns in the board? ")) # Number of columns    
    # this block creates the initial fully hidden board
    player_board = start_board(rows, cols)
    print_board(player_board)    
    # user specified rows and columns
    frow = int(input("select row: "))
    fcolumn = int(input("select column: "))
    mine_board = add_mines(empty_board(rows, cols, frow, fcolumn), mines, rows, cols)
    end_board = full_board(mine_board,rows,cols)
    
    # count the number of blank spaces
    def count_blank(blist,r,c):
        if r < rows:
            if c < cols:
                if end_board[r][c] == ' ':
                    blist.append([r,c])
                    return count_blank(blist,r,c+1)
                else: return count_blank(blist,r,c+1)
            else: return count_blank(blist,r+1,0)
        else: return blist
    b_list = count_blank([],0,0)
    
    # determine how many blank spaces are above a spot on the board
    def blank_above(bblock,pos):
        if pos < len(b_list):
            if (([b_list[pos][0]-1,b_list[pos][1]] in bblock or
                 [b_list[pos][0]+1,b_list[pos][1]] in bblock or
                 [b_list[pos][0],b_list[pos][1]+1] in bblock or
                 [b_list[pos][0],b_list[pos][1]-1] in bblock)
                and not [b_list[pos][0],b_list[pos][1]] in bblock):
                bblock.append(b_list[pos])
                return blank_above(bblock,pos+1)
            else: return blank_above(bblock,pos+1)
        else: return bblock
        
    # determine how many blank spaces are below a spot on the board
    def blank_below(bblock,pos):
        if pos >= 0:
            if (([b_list[pos][0]-1,b_list[pos][1]] in bblock or
                 [b_list[pos][0]+1,b_list[pos][1]] in bblock or
                 [b_list[pos][0],b_list[pos][1]+1] in bblock or
                 [b_list[pos][0],b_list[pos][1]-1] in bblock)
                and not [b_list[pos][0],b_list[pos][1]] in bblock):
                bblock.append(b_list[pos])
                return blank_below(bblock,pos-1)
            else: return blank_below(bblock,pos-1) 
        else: return bblock
        
    # examine larger areas of blank space around a spot
    def blank_block(r,c):
        above = blank_above([[r,c]],0)
        below = blank_below(above,len(b_list)-1)
        return blank_above(below,0) 
    
    # determine the number of spots around a player's move to reveal
    # if the move selects a blank spot
    def freveal_list(rlist,r,c):    
        blanks = blank_block(frow,fcolumn)
        if r < rows:
            if c < cols:
                if ([r,c] in blanks or [r-1,c] in blanks or [r+1,c] in blanks 
                    or [r,c-1] in blanks or [r,c+1] in blanks):
                    rlist.append([r,c])
                    return freveal_list(rlist,r,c+1)
                else: return freveal_list(rlist,r,c+1)
            else: return freveal_list(rlist,r+1,0)
        else: return rlist
        
    # expand the players board such that they see the appropriate result
    def fexpand_board(r,c):
        if end_board[r][c] == 'm':
            return print("GG please try again :(")
        if end_board[r][c] == ' ':
            reveal = freveal_list([],0,0)
            def reveal_board(pos):
                if pos<len(reveal):
                    r1 = reveal[pos][0]
                    c1 = reveal[pos][1]                    
                    player_board[r1][c1] = end_board[r1][c1]
                    return reveal_board(pos+1)
                else: return
            return reveal_board(0)
        else:
            player_board[r][c] = end_board[r][c]
    fexpand_board(frow,fcolumn)
    if str(player_board).count('_') == mines:
        print("Congratulations! You win!")
        print_board(end_board)
    else:
        print_board(player_board)
        def nextturn():
            nrow = int(input("select row: "))
            ncolumn = int(input("select column: "))
            if end_board[nrow][ncolumn] == 'm':
                print("GG please try again :(")
                print_board(end_board)
                return
            if end_board[nrow][ncolumn] == ' ':
                def nreveal_list(rlist,r,c):    
                    blanks = blank_block(nrow,ncolumn)
                    if r < rows:
                        if c < cols:
                            if ([r,c] in blanks or [r-1,c] in blanks or 
                                [r+1,c] in blanks or [r,c-1] in blanks or 
                                [r,c+1] in blanks):
                                rlist.append([r,c])
                                return nreveal_list(rlist,r,c+1)
                            else: return nreveal_list(rlist,r,c+1)
                        else: return nreveal_list(rlist,r+1,0)
                    else: return rlist
                reveal = nreveal_list([],0,0)
                def reveal_board(pos):
                    if pos<len(reveal):
                        r1 = reveal[pos][0]
                        c1 = reveal[pos][1]
                        player_board[r1][c1] = end_board[r1][c1]
                        return reveal_board(pos+1)
                reveal_board(0)
                if str(player_board).count('_') == mines:
                    print_board(end_board)
                    return 'Congratulations! You win!'
                else: 
                    print_board(player_board)
                    return nextturn()                
            else:
                player_board[nrow][ncolumn] = end_board[nrow][ncolumn]                
                if str(player_board).count('_') == mines:
                    print_board(end_board)
                    return 'Congratulations! You win!'
                else: 
                    print_board(player_board)
                    return nextturn()
        return nextturn()