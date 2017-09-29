#start  11:12
## This program computes the average number of moves it would take a rook 
## to move off of an n-dimesional chess board.  Each move is still two dimensional
## with the dimensions chosen at random.

import random

import matplotlib.pyplot as plt

## M is max integer to be tested
M = 15

## m is number of trials per integer
m = 10000

##board_dim is number of dimensions of board
board_dim = 2 +  random.randrange(98)

## dim_len is length (number of squares) of each dimension. For a standard
## Chessboard dim_len = 8
side_len = 8 + random.randrange(92)

def run_trial(n):
    ## set random initial coords
    coords = []
    for j in range(board_dim):
        coords.append(random.randrange(side_len))
    for k in range(n):

        ## select dimesions in which to move
        xdim = random.randrange(board_dim)
        ydim = random.randrange(board_dim)
        while xdim == ydim:
            ydim = random.randrange(board_dim)
        
                  

        ## xpm, ypm control the direction of movement in xdim, ydim.
        xpm = 1
        ypm = 1

        ## set values for random move
        xlen = 1
        ylen = 2  
        if random.random() > .5:
            xlen = 2
            ylen = 1
        if random.random() > .5:
            xpm = -1
        if random.random() > .5:
            ypm = -1

        ##update coordinates
        new_x = coords[xdim] + xlen*xpm
        new_y = coords[ydim] + ylen*ypm
        coords = coords[:xdim] + [new_x] + coords[xdim+1:]
        coords = coords[:ydim] + [new_y] + coords[ydim+1:]
        #print(coords)
        

        ## check in on board, if off return number of moves 
        if max(coords) > side_len -1 or min(coords) < 0:
            #print (max(coords), min(coords), max(coords) > 7, min(coords) < 0)
            #print ("")
            #print ("")
            return k+1
    ## if on board at end return -1
    #print ("")
    #print ("")
    return -1

## run m trials and compute proportion of trials on after n moves.
def run_trials_for_n(n):
    results =[]
    for k in range(m):
        results.append(run_trial(n))
    return results.count(-1)/float(len(results))

## run trials for a range of integers from 0 to M
def run_trials():
    probs = [1]
    ratios = [1]
    for n in range(M+1):
        probs.append(run_trials_for_n(n))
        ratios.append(probs[n+1]/probs[n])
    print ("The expectations of a rook moving in two dimensions not falling off a chessboard")
    print ("board dimension:", board_dim)
    print ("side length:", side_len)
    for n in range(M):
        print ("Turns:", n, "      ", "expectation:", probs[n+1])
    rsum = 0
    for ratio in ratios[2:]:
        rsum += ratio
    ravg = rsum/len(ratios[2:])
    print ("this is well approximated by: f(n) =", ratios[2], "*(", ravg, ")^n")
    fig = plt.figure()
    plt.plot(probs[1:])
    fig.savefig("probs.png")



run_trials()       
    
    
