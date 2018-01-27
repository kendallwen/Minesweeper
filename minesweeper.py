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

# expand the board based on a player's move
def expand(row, col, pboard, eboard):
    pboard[row][col] = eboard[row][col]
    if pboard[row][col]==' ':
        visited = []
        unvisited = []
        unvisited.append([row,col])
        # function to shorten typing to see if a spot has been visited
        def found(vr,vc):
            return [vr,vc] in visited or [vr,vc] in unvisited
        while(len(unvisited)!=0):
            cur = unvisited.pop()
            r = cur[0]
            c = cur[1]
            visited.append(cur)
            if r>0:
                pboard[r-1][c] = eboard[r-1][c]
                if eboard[r-1][c]==' 'and not found(r-1,c): 
                    unvisited.append([r-1,c])
                if c>0:
                    pboard[r-1][c-1] = eboard[r-1][c-1]
                    pboard[r][c-1] = eboard[r][c-1]
                    if eboard[r][c-1]==' ' and not found(r,c-1):
                        unvisited.append([r,c-1])
                if c<len(pboard[r])-1:
                    pboard[r-1][c+1] = eboard[r-1][c+1]
                    pboard[r][c+1] = eboard[r][c+1]
                    if eboard[r][c+1]==' ' and not found(r,c+1):
                        unvisited.append([r,c+1])
            if r<len(pboard)-1:
                pboard[r+1][c] = eboard[r+1][c]
                if eboard[r+1][c]==' ' and not found(r+1,c):
                    unvisited.append([r+1,c])
                if c>0:
                    pboard[r+1][c-1] = eboard[r+1][c-1]
                    if c>0:
                        pboard[r+1][c-1] = eboard[r+1][c-1]
                    if c<len(pboard[r])-1:
                        pboard[r+1][c+1] = eboard[r+1][c+1]
                            
# count number of hidden spots on a board
def count_hidden(board):
    count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j]=='_': count = count+1
    return count

# main game flow
def minesweeper():
    mines = int(input("How many mines would you like? ")) # Number of mines
    rows = int(input("How many rows in the board? ")) # Number of rows
    cols = int(input("How many columns in the board? ")) # Number of columns    
    # this block creates the initial fully hidden board
    player_board = start_board(rows, cols)
    print_board(player_board)    
    # mines added accordingly to player's first row and column choice
    frow = int(input("select row: "))
    fcolumn = int(input("select column: "))
    mine_board = add_mines(empty_board(rows, cols, frow, fcolumn), mines, rows, cols)
    end_board = full_board(mine_board,rows,cols)
    expand(frow,fcolumn,player_board,end_board)
    print_board(player_board)
    # game continues until the player wins or loses
    while count_hidden(player_board)>mines:
        row = int(input("select row: "))
        col = int(input("select column: "))
        if end_board[row][col]=='m':
            print_board(end_board)
            print("GG please try again")
            return
        else: 
            expand(row,col,player_board,end_board)
            print_board(player_board)
    print("CONGRATULATIONS! YOU WIN")
    return