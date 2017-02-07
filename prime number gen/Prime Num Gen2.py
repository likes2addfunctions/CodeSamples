import os
import ast

from sys import executable
from subprocess import Popen, CREATE_NEW_CONSOLE

os.chdir(os.path.dirname(os.path.abspath(__file__)))

init_file = open("merge info.py")
merge_info = ast.literal_eval(init_file.read())
init_file.close()

init_file = open("top_list.py")
start_list_num = ast.literal_eval(init_file.read())[0]
start_temp_num = ast.literal_eval(init_file.read())[1]

init_file.close()    
	
pfname = "Prime Lists\primesy_" + str(start_list_num) + "_to_" + str(start_list_num + 100000000) + ".py"
init_file = open(pfname)
primesy = ast.literal_eval(init_file.read())
init_file.close()

#~ new_merge_info = [primesy[-1]- primesy[-1]%5000000,primesy[-1] + 5000000 - primesy[-1]%5000000,0,0]

new_merge_info = [start_temp_num,start_temp_num + 5000000,0,0]

up_file = open("merge info.py", "w")
up_file.write(str(new_merge_info))
up_file.close()






Popen([executable, 'Prime Num GenA2.py'], creationflags=CREATE_NEW_CONSOLE)
Popen([executable, 'Prime Num GenB2.py'], creationflags=CREATE_NEW_CONSOLE)
Popen([executable, 'Prime Num GenC2.py'], creationflags=CREATE_NEW_CONSOLE)
Popen([executable, 'Prime Num GenD2.py'], creationflags=CREATE_NEW_CONSOLE)
Popen([executable, 'Merger.py'], creationflags=CREATE_NEW_CONSOLE)


    
