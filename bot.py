import ImageGrab
import os
import time
import win32api, win32con
import math

"""
Coordinates calculated on home PC with game
window on left half of screen
x_pad = 222
y_pad = 351
x_max = 722
y_max = 851

"""

x_pad = 222
y_pad = 351

max_depth = 4

board = [[0 for x in range(4)] for x in range(4)]


#Dictionary for VK codes
VK_CODE = {'left':0x25,
           'up':0x26,
           'right':0x27,
           'down':0x28}

#Dictionary for square indices
SQUARE_COORDS = {0:(65,30),
                 1:(185,30),
                 2:(305,30),
                 3:(425,30),
                 4:(65,150),
                 5:(185,150),
                 6:(305,150),
                 7:(425,150),
                 8:(65,270),
                 9:(185,270),
                 10:(305,270),
                 11:(425,270),
                 12:(65,390),
                 13:(185,390),
                 14:(305,390),
                 15:(425,390)
                 }

#Dictionary for square indices in board array
SQUARE_INDICES = {0:(0,0),
                  1:(1,0),
                  2:(2,0),
                  3:(3,0),
                  4:(0,1),
                  5:(1,1),
                  6:(2,1),
                  7:(3,1),
                  8:(0,2),
                  9:(1,2),
                  10:(2,2),
                  11:(3,2),
                  12:(0,3),
                  13:(1,3),
                  14:(2,3),
                  15:(3,3)
                  }

#Dictionary for square scores
SQUARE_SCORES = {0:0,
                 2:0,
                 4:4,
                 8:11,
                 16:28,
                 32:65,
                 64:141,
                 128:300,
                 256:627,
                 512:1292,
                 1024:2643,
                 2048:5372,
                 4096:10874,
                 8192:21944
                 }

#dictionaly for square multipliers
SQUARE_MULTS = {0:2,
                1:2,
                2:2,
                3:2,
                4:1.25,
                5:1.25,
                6:1.25,
                7:1.25,
                8:1,
                9:1,
                10:1,
                11:1,
                12:0.8,
                13:0.8,
                14:0.8,
                15:0.8
                }
                 

def arrowKey(direction):
    win32api.keybd_event(VK_CODE[direction],0,0,0)
    time.sleep(.05)
    win32api.keybd_event(VK_CODE[direction],0,win32con.KEYEVENTF_KEYUP,0)

def screenGrab():
    box = (x_pad, y_pad, 722, 851)
    im = ImageGrab.grab(box)
    #im.save(os.getcwd() + '\\full_snap__' +str(int(time.time())) + '.png', 'PNG')
    return im

#Finds the number of each square
def getSquareNumbers():
    #get the screen
    im = screenGrab()

    #loop through all squares
    for sq in range(0,16):
        #get the color at the square's test point
        rgb = im.getpixel(SQUARE_COORDS[sq])
        val = getNumberFromRGB(rgb)
        if(val == -1):
            print "Unknown RGB ",rgb

        #store in board
        board[sq%4][sq//4] = val
        

#Returns the number of a square with given rgb values
def getNumberFromRGB(rgb):
    def distance(p1,p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)
    
    if(distance(rgb,(204, 192, 179)) <= 5):
        return 0
    elif(distance(rgb,(238, 228, 218)) <= 5):
        return 2
    elif(distance(rgb,(237, 224, 200)) <= 5):
        return 4
    elif(distance(rgb,(242, 177, 121)) <= 5):
        return 8
    elif(distance(rgb,(245, 149, 99)) <= 5):
        return 16
    elif(distance(rgb,(246, 124, 95)) <= 5):
        return 32
    elif(distance(rgb,(246, 94, 59)) <= 5):
        return 64
    elif(distance(rgb,(237, 207, 114)) <= 5):
        return 128
    elif(distance(rgb,(237, 204, 97)) <= 5):
        return 256
    elif(distance(rgb,(237, 200, 80)) <= 5):
        return 512
    elif(distance(rgb,(237, 197, 63)) <= 3):
        return 1024
    elif(distance(rgb,(237, 194, 46)) <= 5):
        return 2048
    else:
        return -1

#takes in a board, makes the given move, and returns the score of the move with the new board
def makeMove(array, direction):
    score = 0
    legal_move = 0 #whether or not the move does anything
    array_temp = [[0 for x in range(0,4)] for x in range(0,4)]
    for x in range(0,16):
        array_temp[x%4][x//4] = array[x%4][x//4]

    
    if(direction == 'left'):
        #loop through each row
        for y_ind in range(0,4):

            #start by shifting all blocks without adding
            for x_ind in range(0,4):

                #if the current square is empty, replace it with the next non-empty square
                if(array_temp[x_ind][y_ind] == 0):
                    #find next non-empty square
                    for x_temp in range(x_ind+1,4):
                        if(array_temp[x_temp][y_ind]):
                            #Move square to empty space
                            array_temp[x_ind][y_ind] = array_temp[x_temp][y_ind]
                            array_temp[x_temp][y_ind] = 0
                            legal_move = 1 #at least one legal move
                            break                    

            #now add like blocks
            for x_ind in range(0,3):
                #if blocks are equal
                if(array_temp[x_ind][y_ind] == array_temp[x_ind+1][y_ind] and array_temp[x_ind][y_ind] != 0): 
                    #Combine blocks and shift all others by one square
                    array_temp[x_ind][y_ind] *= 2
                    score += array_temp[x_ind][y_ind]
                    legal_move = 1

                    for x_temp in range(x_ind+1,3):
                        array_temp[x_temp][y_ind] = array_temp[x_temp+1][y_ind]

                    array_temp[3][y_ind] = 0

    if(direction == 'right'):
        #loop through each row
        for y_ind in range(0,4):

            #start by shifting all blocks without adding
            for x_ind in range(3,-1,-1):

                #if the current square is empty, replace it with the next non-empty square
                if(array_temp[x_ind][y_ind] == 0):
                    #find next non-empty square
                    for x_temp in range(x_ind-1,-1,-1):
                        if(array_temp[x_temp][y_ind]):
                            #Move square to empty space
                            array_temp[x_ind][y_ind] = array_temp[x_temp][y_ind]
                            array_temp[x_temp][y_ind] = 0
                            legal_move = 1 #at least one legal move
                            break                    

            #now add like blocks
            for x_ind in range(3,0,-1):
                #if blocks are equal
                if(array_temp[x_ind][y_ind] == array_temp[x_ind-1][y_ind] and array_temp[x_ind][y_ind] != 0): 
                    #Combine blocks and shift all others by one square
                    array_temp[x_ind][y_ind] *= 2
                    score += array_temp[x_ind][y_ind]
                    legal_move = 1

                    for x_temp in range(x_ind-1,0,-1):
                        array_temp[x_temp][y_ind] = array_temp[x_temp-1][y_ind]

                    array_temp[0][y_ind] = 0

    if(direction == 'up'):
        #loop through each column
        for x_ind in range(0,4):

            #start by shifting all blocks without adding
            for y_ind in range(0,4):

                #if the current square is empty, replace it with the next non-empty square
                if(array_temp[x_ind][y_ind] == 0):
                    #find next non-empty square
                    for y_temp in range(y_ind+1,4):
                        if(array_temp[x_ind][y_temp]):
                            #Move square to empty space
                            array_temp[x_ind][y_ind] = array_temp[x_ind][y_temp]
                            array_temp[x_ind][y_temp] = 0
                            legal_move = 1 #at least one legal move
                            break                    

            #now add like blocks
            for y_ind in range(0,3):
                #if blocks are equal
                if(array_temp[x_ind][y_ind] == array_temp[x_ind][y_ind+1] and array_temp[x_ind][y_ind] != 0): 
                    #Combine blocks and shift all others by one square
                    array_temp[x_ind][y_ind] *= 2
                    score += array_temp[x_ind][y_ind]
                    legal_move = 1

                    for y_temp in range(y_ind+1,3):
                        array_temp[x_ind][y_temp] = array_temp[x_ind][y_temp+1]

                    array_temp[x_ind][3] = 0

    if(direction == 'down'):
        #loop through each column
        for x_ind in range(0,4):

            #start by shifting all blocks without adding
            for y_ind in range(3,-1,-1):

                #if the current square is empty, replace it with the next non-empty square
                if(array_temp[x_ind][y_ind] == 0):
                    #find next non-empty square
                    for y_temp in range(y_ind-1,-1,-1):
                        if(array_temp[x_ind][y_temp]):
                            #Move square to empty space
                            array_temp[x_ind][y_ind] = array_temp[x_ind][y_temp]
                            array_temp[x_ind][y_temp] = 0
                            legal_move = 1 #at least one legal move
                            break                    

            #now add like blocks
            for y_ind in range(3,0,-1):
                #if blocks are equal
                if(array_temp[x_ind][y_ind] == array_temp[x_ind][y_ind-1] and array_temp[x_ind][y_ind] != 0): 
                    #Combine blocks and shift all others by one square
                    array_temp[x_ind][y_ind] *= 2
                    score += array_temp[x_ind][y_ind]
                    legal_move = 1

                    for y_temp in range(y_ind-1,0,-1):
                        array_temp[x_ind][y_temp] = array_temp[x_ind][y_temp-1]

                    array_temp[x_ind][0] = 0


    #Adjust score in case no squares moved
    if(legal_move == 0):
        score = -1
    
    return (array_temp, score)     

#Adds a 2 to the given space
def makeComputerMove(array, space):
    
    array_temp = [[0 for x in range(0,4)] for x in range(0,4)]
    for x in range(0,16):
        array_temp[x%4][x//4] = array[x%4][x//4]

    #set given square to 2
    array_temp[space%4][space//4] = 2

    return array_temp
    
#Copies board1 into board2 
def copyBoard(board1, board2):
    for x in range(0,16):
        board2[x%4][x//4] = board2[x%4][x//4]

def printBoard(array,text):
    print text
    print array[0][0], " ", array[1][0], " ",array[2][0]," ",array[3][0]
    print array[0][1], " ", array[1][1], " ",array[2][1]," ",array[3][1]
    print array[0][2], " ", array[1][2], " ",array[2][2]," ",array[3][2]
    print array[0][3], " ", array[1][3], " ",array[2][3]," ",array[3][3]
    print " "

#searches to the given depth, returning the best move and score
def search(array, depth):
    best_score = -1;
    best_move = 'down' #best move by default, always replaced unless no others are available
    moves = ['left','right','up']

    #search each move
    for move in moves:

        score = -1
        
        #make move
        move_results = makeMove(array,move)

        #if depth == 0 or score == -1, search no further
        if(depth <= 0 or move_results[1] == -1):
            score = move_results[1]
        else: #call search function again
            search_results = search(move_results[0],depth-1)

            #get score by adding move score to search score
            score = 0.8*(move_results[1] + search_results[1]) #multiply by fraction so each layer is progressively less weighted

        #Update best score and move
        if(score > best_score):
            best_score = score
            best_move = move

    #Return best move and score
    return (best_move,best_score)

#searches player moves to the given depth, returning the best move and score
def playerSearch(array, depth, ply):
    
    best_score = -1
    best_move = 'down' #best move by default, always replaced unless no others are available
    pv = [0 for x in range(0,ply+1)]
    moves = ['left','right','up','down']

    if(depth <= 0):
        return (best_move, evaluateBoard(array),'end')
    
    #search each move
    for move in moves:

        score = -1
        
        #make move
        (new_board, move_score) = makeMove(array,move)

        #if move is not successful
        if(move_score == -1):
            continue

        else: #call computer_search function
            (score, pv_temp) = computerSearch(new_board,best_score,depth - 1, ply + 1)

        #Update best score, move and pv
        if(score > best_score):
            best_score = score
            best_move = move
            pv[0] = move
            pv[1:] = pv_temp[::]

    #Return best move and score
    return (best_move, best_score, pv)

#searches all computer moves, returning the minimum score found
def computerSearch(array, best_score, depth, ply):

    pv = [0 for x in range(0,ply+1)]
    if(depth <= 0):
        return (evaluateBoard(array),"X")

    worst_score = 100000000
    total = 0
    moves_made = 0
    
    #Loop through all squares, make computer move if empty
    for sq in range(0,16):

        #Continue if square is not empty
        if(array[sq%4][sq//4] != 0):
            continue

        #make move
        new_board = makeComputerMove(array, sq)

        #call player_search function
        (temp, score, pv_temp) = playerSearch(new_board, depth - 1, ply + 1)

        #cutoff
        #if(score < best_score):
            #return (score, pv)

        #update average
        total += score
        moves_made += 1
        
        #update worst score
        if(score < worst_score):
            worst_score = score
            pv[0] = sq
            pv[1:] = pv_temp[::]

    #Adjustment for leaving square 0 or 1 open at any time during search
    if(array[0][0] == 0):
        worst_score *= (1 - 0.1*depth)

    if(array[1][0] == 0):
        worst_score *= (1 - 0.03*depth)



    return (worst_score, pv)

#Returns the score of the board
def evaluateBoard(array):

    score = 0
    maximum = 0
    for sq in range(0,16):
        score += SQUARE_SCORES[array[sq%4][sq//4]]*SQUARE_MULTS[sq]
        if(array[sq%4][sq//4] > maximum):
            maximum = array[sq%4][sq//4]

    #bonus for having highest square in top left
    if(array[0][0] == maximum):
        score *= 1.4

    return score
        
    
def main():
    print "Starting in 3"
    time.sleep(1)
    print "2"
    time.sleep(1)
    print "1"
    time.sleep(1)
    print "Start"
    print " "
    
    board[0][0] = 256
    board[0][1] = 8
    board[0][2] = 2
    board[0][3] = 4
    board[1][0] = 128
    board[1][1] = 0
    board[1][2] = 0
    board[1][3] = 0
    board[2][0] = 0
    board[2][1] = 0
    board[2][2] = 0
    board[2][3] = 0
    board[3][0] = 2
    board[3][1] = 0
    board[3][2] = 0
    board[3][3] = 0
    
    while True:

        getSquareNumbers()
        
        printBoard(board,'Original')

        (move, score, pv) = playerSearch(board,5,0)

        print "Move: ", move, " Score: ", score

        print "PV: ", pv[::],"\n\n"

        (left, score) = makeMove(board, 'left')
        #printBoard(left, 'Left')
        #print "Move score: ", score
        
        arrowKey(move)
        time.sleep(0.25)

if __name__ == '__main__':
    main()
