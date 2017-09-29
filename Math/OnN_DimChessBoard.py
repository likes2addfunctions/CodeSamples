#start  11:12
## This program computes the average number of moves it would take a rook 
## to move off of an n-dimesional chess board.  Each move is still two dimensional
## with the dimensions chosen at random.

import random

import matplotlib.pyplot as plt

## M is max integer to be tested
M = 10

## m is number of trials per integer
m = 2000

##board_dim is number of dimensions of board
board_dim = 10

def run_trial(n):
    ## set random initial coords
    coords = []
    for j in range(board_dim):
        coords.append(random.randrange(8))
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
        if max(coords) > 7 or min(coords) < 0:
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
    print ("The probability of a rook moving in two dimensions not falling off")
    print ("an", board_dim, "dimensional chess board after n moves is well approximated by:")
    print (ratios[2], "*(", ratios[3], ")^n")
    print (probs)       
    fig = plt.figure()
    plt.plot(probs[1:])
    fig.savefig("probs.png")



run_trials()       
    
    
