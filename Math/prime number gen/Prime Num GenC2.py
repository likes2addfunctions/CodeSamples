import os
import ast

def appendprimes():
	target = primes[-1]**2 - 1
	new_primes = []
	save_step = 5000000
	last_wr = ''
	double_wr = ''
	triple_wr = ''
	delta = 6
	if target < primes[-1]+delta:
		print "All primes up to", primes[-1], "known." , len(primes), "in total."
	if target > primes[-1]**2:
		print "Not enought primes to use this method for this target"
		return
	k = primes[-1] + delta
	adjuster = (primes[-1] + delta) % save_step
	while k < target:
		writecheck = k - adjuster + save_step
		if (writecheck)%save_step == 0:
			if last_wr == '':
				backup_filename = "primesy_plus"  + str(delta) + "_" + str(writecheck-save_step) + "_through_" + str(writecheck) + ".py" 
				backup_file = open(backup_filename, "w+")					
				backup_file.write(str(new_primes))
				backup_file.close()
				if not (new_primes == []):
					print  "+", str(delta), "List of primes appended! Primes of this form up to",\
						str(new_primes[-1]), "known." 
				new_primes = []
			else:
				backup_filename = "primesy_plus"  + str(delta) + "_" + str(last_wr) + "_through_" + str(writecheck) + ".py" 
				backup_file = open(backup_filename, "w+")					
				backup_file.write(str(new_primes))
				backup_file.close()
				if not (new_primes == []):
					print  "+", str(delta), "List of primes appended! Primes of this form up to",\
						str(new_primes[-1]), "known." 
				double_wr = last_wr
				new_primes = []
			last_wr = writecheck           
		if check_help(k):
			new_primes = new_primes + [k]
		k = k+8
	backup_filename = "primesy_plus"  + str(delta) + "_through_" + str(writecheck) + ".py" 
	backup_file = open(backup_filename, "w+")
	backup_file.write(str(new_primes))
	backup_file.close()
	print "List of primes appended! All primes up to",\
	str(k-1+delta), "known." , len(primes), "in total."
	return
	
def check_help(num):
	for p in primes_100:
		if num%p == 0:
			return 0
		if p**2 > num:
			return 1
			
os.chdir(os.path.dirname(os.path.abspath(__file__)))

init_file = open("top_list.py")
start_list_num = ast.literal_eval(init_file.read())
init_file.close()    
	
pfname = "Prime Lists\primesy_" + str(start_list_num) + "_to_" + str(start_list_num + 100000000) + ".py"
init_file = open(pfname)
primes = ast.literal_eval(init_file.read())
init_file.close()	
	
pfname = "Prime Lists\primesy_" + str(0) + "_to_" + str(100000000) + ".py"
init_file = open(pfname)
primes_100 = ast.literal_eval(init_file.read())
init_file.close() 
    

        
appendprimes()



    
