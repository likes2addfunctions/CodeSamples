import os
import ast
import time
import datetime

init_file = open("merge info.py")
merge_info = ast.literal_eval(init_file.read())
init_file.close()

init_file = open("top_list.py")
start_list_num = ast.literal_eval(init_file.read())[0]
init_file.close()

pfname = "Prime Lists\primesy_" + str(start_list_num) + "_to_" + str(start_list_num + 100000000) + ".py"
init_file = open(pfname)
primesy = ast.literal_eval(init_file.read())
init_file.close()

newprimelst = primesy

save_step = 5000000

start_prime = merge_info[0]
goal = merge_info[1]
last_merge = merge_info[2]
double_merge = merge_info[3]

while 1:
	try:
		fname2 = "primesy_plus2_" + str(start_prime) + "_through_" + str(goal) + ".py"
		init_file = open(fname2)
		primesy_plus2 = ast.literal_eval(init_file.read())
		init_file.close()

		fname4 = "primesy_plus4_" + str(start_prime) + "_through_" + str(goal) + ".py"
		init_file = open(fname4)
		primesy_plus4 = ast.literal_eval(init_file.read())
		init_file.close()

		fname6 = "primesy_plus6_" + str(start_prime) + "_through_" + str(goal) + ".py"
		init_file = open(fname6)
		primesy_plus6 = ast.literal_eval(init_file.read())
		init_file.close()

		fname8 = "primesy_plus8_" + str(start_prime) + "_through_" + str(goal) + ".py"
		init_file = open(fname8)
		primesy_plus8 = ast.literal_eval(init_file.read())
		init_file.close()

		newprimelst = list(sorted(set(newprimelst + primesy_plus2 + primesy_plus4 + primesy_plus6 + primesy_plus8)))
		
		listnum = goal/100000000
		ufname = "Prime Lists\primesy_" + str(100000000*listnum) + "_to_" + str(100000000*(listnum+1)) + ".py"
		updated_file = open(ufname, "w+")
		updated_file.write(str(newprimelst))
		updated_file.close()

		os.remove(fname2)
		os.remove(fname4)
		os.remove(fname6)
		os.remove(fname8)

#		fname = "Thru Lists\primesy_"  + str(100000000*listnum) + "_through_" + str(goal) + ".py"
#		updated_file = open(fname, "w+")
#		updated_file.write(str(newprimelst))
#		updated_file.close()
		
		start_prime = start_prime + save_step
		goal = goal + save_step

		init_file = open("merge info.py", "w")
		new_merge_info = [start_prime, goal, goal, last_merge]
		init_file.write(str(new_merge_info)) 
		init_file.close()
		
		init_file = open("top_list.py", "w")
		init_file.write(str([start_list_num,goal]))
		init_file.close()
		
		if goal%100000000 == 0:
			newprimelst = []
			init_file = open("top_list.py", "w")
			init_file.write(str([goal,goal]))
			init_file.close()
			start_list_num = goal
	
		now = datetime.datetime.now()
		print "merged through", start_prime, "at", now.strftime("%H:%M")
		
	except:
		print "Waiting for files"
		time.sleep(30)
	
	
