import time
import sys
import random
import os
import datetime

def quickexp2(a,b, exp):
    count = 1
    mod = a % b
    while 2**count <exp+1:
        mod = ((mod%b) * (mod%b)) % b
        count = count + 1
    return mod
    
def binarylist(num):
    j=1
    tempnum = num
    exponents = []
    while 2**(j+1) < num:
        j = j+1
    z = 2**j
    if z*2 == num:
        return[j+1]
    exponents = exponents + [j]
    j = j-1
    tempnum = tempnum - z
    while not(tempnum < 1) and (j > -1):
        z = 2**j
        if z < tempnum+1:
            exponents = exponents + [j]
            tempnum = tempnum - z        
        j = j-1
    return exponents
    
    
def quickexp(a,b,exp):
    exponents = binarylist(exp)
    prod = 1
    for k in exponents:
        prod = (quickexp2(a,b,2**k)%b) * prod
    answer = prod % b
    return answer
    
def RMTestRand(num):
    
    alst = []
    
    ### find r,s such that num = (2^r)*s + 1
    s=1
    m = (num-1)/(2)
    while m%2 == 0:
        s = s+1
        m = m/2
    
    for k in range(10):
        b = random.randrange(100)
        a = HundredPrimes[b]
        alst = alst + [a]
        if not (RMatestRand(num, a,m,s)):
#            print num, "is composite"
            return False
        k=k+1

    ### if all tests pass
    print "!!!"
    print num
    print "passed the test for", alst
    return True
 
def RMatestRand(num, a,m,s):
### implement Rabin-Miller test part one
    temp = quickexp(a,num,m) 
    if (temp == 1) or (temp == num - 1):
        return True
        
### implement Rabin-Miller test part two    
    j = 0
    while j < s:
        temp = quickexp(a,num,(2**j)*m) % num
        if temp == num-1:
            return True
        if temp == 1:
            return False
        j=j+1       
    return False

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

start = time.clock()
last = start

HundredPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]   
            
digits = random.randrange(100,150)
                   
k = 2* int(random.randrange(10**digits, 10**(digits+1))) + 1

#k = 2* int(random.random()*10**(random.randrange(150, 308))) + 1
PossiblePrimes = []
chunk = 10000
printstr = "Searching " +  str(chunk) + " " + str( len(str(k))) + "-digit, odd numbers starting with " + str(k)                     
print printstr
print "."
j = 0

DTnow = datetime.datetime.now()
print DTnow.strftime("%H%M%b%d")

while j < chunk:
    if RMTestRand(k):
        PossiblePrimes = PossiblePrimes = [k]
    j = j+1
    k = k+2
    if j%50 == 0:
        if j%50 == 0:
            DTnow = datetime.datetime.now()
            print DTnow.strftime("%H%M%b%d")
            fname = "PossiblePrimes" + DTnow.strftime("%H%M%b%d") + ".py"
            print "loading", fname
            init_file = open(fname ,"w")
            init_file.write(str(PossiblePrimes))
            init_file.close
            PossiblePrimes = []
            print chunk-j, "numbers left. Press <ctrl>-c to break"
        else:
            print "."

     
    
        
end = time.clock()
print end-start
#print primelist
