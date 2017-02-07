### Portfolio note this was a tool I created to help my Statistics students
# understand sampling distributions. It simulates picking blue and silver marbles
# from a bag with prescribed proportion, p, and provides appropriate visualizations.


import random
import time
import matplotlib.pyplot as plt


p = .7924

def plen():
    if len(str(p)) > 5:
        return 10* 10**len(str(p))
    else:
        return 100000


def list_name(n):
    try:
        if str(n)[-2] == "1":
            printstr = str(n) + "th"
            return printstr
    except:
        True
    if str(n)[-1] == "1":
        printstr = str(n) + "st"
    elif str(n)[-1] == "2":
        printstr = str(n) + "nd"
    elif str(n)[-1] == "3":
        printstr = str(n) + "rd"
    else: 
        printstr = str(n) + "th"
    return printstr
        

def pick(n):
    print "Shaking the bag up to mix the balls"
    time.sleep(1)
    print " "
    print "Sampling", n, "balls from the bag of", plen(), "marbles"
    blue = 0
    silver = 0
    for k in range(n):
        time.sleep(1)
        print " " 
        print "Looking at the", list_name(k+1), "ball in this sample..."
        time.sleep(1)
        x = random.random()
        if x < p:
            blue = blue + 1
            printstr = "it is blue."
            print printstr
            
        else:
            silver = silver + 1
            printstr = "it is silver."
            print printstr            
    print " " 
    print "There are", blue, "blue balls in this sample of", n, ", p-hat = ", str(float(blue)/n) 
    time.sleep(.5)
    return blue

def quickPick(n):
    blue = 0
    for k in range(n):
        x = random.random()
        if x < p:
            blue = blue + 1
    return blue    
    
def makeSampleDist(numOfSamples,sampleSize):
    results = []
    for k in range(numOfSamples):
        results = results + [quickPick(sampleSize)]
        printstr = list_name(str(k+1)) + " sample complete, results recorded. Returning balls to the bag of", str(plen()), "marbles."
        print " "
        print printstr
        print " " 
    plt.hist(results)
    plt.xlim([0,sampleSize])
    plt.show()
    total_blue = 0
    for entry in results:
        total_blue = total_blue + entry
    x_bar = float(total_blue)/numOfSamples
    print "x-bar =", x_bar
    print "p-hat =", x_bar/sampleSize
    
makeSampleDist(30,30)
print p
