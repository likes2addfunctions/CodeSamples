import time 

start = time.clock()

def check_help(num, lst):
    for p in lst:
	if num%p == 0:
	   return 0
	if p**2 > num:
		return 1

def gen1M():
    last = start
    k=3
    primes = [2]
    while k < 2000000:
        if (k+1)%50000 ==0:
            now = time.clock()
            print now-last
            last = now
        if check_help(k, primes):
            primes = primes + [k]
        k = k+2    
    return primes
		

		


GMPrimes = gen1M()

end = time.clock()

print end-start
