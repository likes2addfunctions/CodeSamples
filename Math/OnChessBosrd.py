import random

import matplotlib.pyplot as plt

def run_trial(n):
    ## set random initial coords
    x = random.randrange(8)
    y = random.randrange(8)
    for k in range(n):

        ## xlen, ylen control magnitude of movement
        xlen = 1
        ylen = 2

        ## xpm, ypm control the direction of movement
        xpm = 1
        ypm = 1

        ## set values for random move
        if random.random() > .5:
            xlen = 2
            ylen = 1
        if random.random() > .5:
            xpm = -1
        if random.random() > .5:
            ypm = -1

        ##update coordinates
        x += xlen*xpm
        y += ylen*ypm

        ## check in on board, if off return number of moves 
        if max(x,y) > 7 or min(x,y) < 0:
            return k+1
    ## if on board at end return -1
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
    print "prob of not falling off after n moves is well approximated by:"
    print ratios[2], "*(", ratios[3], ")^n"       
    fig = plt.figure()
    plt.plot(probs[1:])
    fig.savefig("probs.png")

## M is max integer to be tested
M = 10

## m is number of trials per integer
m = 200000


run_trials()       
    
    
