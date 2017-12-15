import math
import random

def minesweeper():
    mines = int(input("How many mines would you like? ")) # Number of mines
    rows = int(input("How many rows in the board? ")) # Number of rows
    cols = int(input("How many columns in the board? ")) # Number of columns
    # this block prints boards
    def print_row(row, pos):
        if pos < len(row): return str(row[pos]) + print_row(row,pos+1)
        else: return ''    
    def print_board(b, c_row):
        if c_row < rows:
            print(print_row(b[c_row],0))
            return print_board(b, c_row+1)
        else:
            return    
    # this block creates the initial fully hidden board
    hidden_space = ['_']
    def start_board(board, size, spot):
        def create_row(row, size, spot):
            if spot<size:
                row = row + hidden_space
                return create_row(row, size, spot+1)
            return row
        row = [create_row(hidden_space, cols, 1)]
        if spot < size:
            board = board + row
            return start_board(board, size, spot+1)
        return board
    player_board = start_board([], rows, 0)
    print_board(player_board, 0)    
    # this block creates the full revealed board
    single_space = [' '] # Single block on the board
    # empty_board(board, size, spot) creates an empty minesweeper board with
    # user specified rows and columns
    frow = int(input("select row: "))
    fcolumn = int(input("select column: "))
    def empty_board(board, size, spot):
        # create_row(row, size, spot) creates a single row for the board
        def create_row(row, size, spot):
            if spot < size:
                row = row + single_space
                return create_row(row, size, spot+1)
            return row
        row = [create_row(single_space, cols, 1)] # A single row
        if spot < size:
            board = board + row
            return empty_board(board, size, spot+1)
        board[frow][fcolumn] = 'f'
        if frow>0 and fcolumn>0: board[frow-1][fcolumn-1] = 'f'  
        if frow>0: board[frow-1][fcolumn] = 'f'
        if frow>0 and fcolumn<cols-1: board[frow-1][fcolumn+1] = 'f'
        if fcolumn>0: board[frow][fcolumn-1] = 'f'
        if fcolumn<cols-1: board[frow][fcolumn+1] = 'f'
        if frow<rows-1 and fcolumn>0: board[frow+1][fcolumn-1] = 'f'
        if frow<rows-1: board[frow+1][fcolumn] = 'f'
        if frow<rows-1 and fcolumn<cols-1: board[frow+1][fcolumn+1] = 'f'
        return board
    empty = empty_board([], rows, 0) # The empty board
    prob = mines / (rows * cols) # Probability of hitting a mine
    # this block produces the complete game board
    def add_mines(board, cmine, r, c):
        if cmine < mines:
            if r < rows:
                if c < cols:
                    if board[r][c] != 'f':
                        if random.random() < prob:
                            board[r][c] = 'm'
                            return add_mines(board, cmine+1, r, c+1)
                        else: return add_mines(board, cmine, r, c+1)
                    else: return add_mines(board, cmine, r, c+1)
                else: return add_mines(board, cmine, r+1, 0)
            else: return add_mines(board, cmine, 0, 0)
        else: return board
    def remove_f(board,r,c):
        if r< rows:
            if c< cols:
                if board[r][c] == 'f':
                    board[r][c] = ' '
                    return remove_f(board,r,c+1)
                else: return remove_f(board,r,c+1)
            else: return remove_f(board,r+1,0)
        else: return board
    mine_board = remove_f(add_mines(empty,0,0,0),0,0)
    def count_mine(board, r, c):
        def add_one(spot):
            if spot == ' ': return 1
            if spot == 'm': return 'm'
            else: return spot+1
        up, down, left, right = r-1, r+1, c-1, c+1
        if board[r][c] == 'm':
            if up>=0 and left>=0: board[r-1][c-1] = add_one(board[r-1][c-1])
            if up>=0: board[r-1][c] = add_one(board[r-1][c])
            if up>=0 and right<cols: 
                board[r-1][c+1] = add_one(board[r-1][c+1])
            if left>=0: board[r][c-1] = add_one(board[r][c-1])
            if right<cols: board[r][c+1] = add_one(board[r][c+1])
            if down<rows and left>=0: board[r+1][c-1] = add_one(board[r+1][c-1])
            if down<rows: board[r+1][c] = add_one(board[r+1][c])
            if down<rows and right<cols: 
                board[r+1][c+1] = add_one(board[r+1][c+1])
            return board
        else: return board
    def full_board(board, r, c):
        if r < rows:
            if c < cols:
                board = count_mine(board, r, c)
                return full_board(board, r, c+1)
            else: return full_board(board, r+1, 0)
        else: return board
    end_board = full_board(mine_board,0,0)
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
    def blank_block(r,c):
        above = blank_above([[r,c]],0)
        below = blank_below(above,len(b_list)-1)
        return blank_above(below,0) 
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
        print_board(end_board,0)
    else:
        print_board(player_board,0)
        def nextturn():
            nrow = int(input("select row: "))
            ncolumn = int(input("select column: "))
            if end_board[nrow][ncolumn] == 'm':
                print("GG please try again :(")
                print_board(end_board,0)
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
                    print_board(end_board,0)
                    return 'Congratulations! You win!'
                else: 
                    print_board(player_board,0)
                    return nextturn()                
            else:
                player_board[nrow][ncolumn] = end_board[nrow][ncolumn]                
                if str(player_board).count('_') == mines:
                    print_board(end_board,0)
                    return 'Congratulations! You win!'
                else: 
                    print_board(player_board,0)
                    return nextturn()
        return nextturn()