#!/bin/python

import socket
import threading
import concurrent.futures
import sys
from datetime import datetime



print_lock= threading.Lock()



def check_digit(b_list): 
	
	for k in b_list:
		if(not k.isdigit()): 			
			return 1
	return 0				

#checks if the input IP is in the correct form
def validate_IP(IP):
	b_list=IP.split('.') 
	if (check_digit(b_list)== 0):	
				
		if(len(b_list)<4):
			print("Insert a valid IP")
			sys.exit()		
		else:	
			for element in b_list:
				i=int(float(element)) 
				if((i<0) or (i>256)):		
					print("Insert a valid IP")
					sys.exit()

#checks if the input port range is correct					
def port_range_validity():
	if len(sys.argv) == 4:
		if(not (sys.argv[2].isdigit() and sys.argv[3].isdigit())):
			print("Syntax error")
			print("Syntax: python3 scanner.py <ip> <from port> <to port> ") 
			sys.exit()
	else:	
		print("Invalid amount of arguments")
		print("Syntax: python3 scanner.py <ip> <from port> <to port> ")
		sys.exit()				

#print banner
def show_startup_message():

	print ("-" * 50)
	print("# PSCANEER #")	
	print ("Scanning target "+str(target))
	print ("Time started: "+str(datetime.now()))
	print ("-" * 50)
	
			
def scan_port(target,port):
	
	s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket.setdefaulttimeout(1)
	result = s.connect_ex((target, port)) #returns an error indicator
	if result == 0:
		print("port\t"+str(port)+"\tis opened")		
	s.close()
	
	
#Define our target
def define_target():		
	target=socket.gethostbyname(sys.argv[1]) #Translate hostname to IPv4		
	return target
		
	

def check_validity():
	if (len(sys.argv) == 4):
		port_range_validity()		
		validate_IP(sys.argv[1])
	else:
		print("Invalid amount of arguments")
		print("Syntax: python3 scanner.py <ip> <from port> <to port> ")
		sys.exit()	


check_validity()
target=define_target()
show_startup_message()


MIN = int(sys.argv[2])
MAX = int(sys.argv[3])


try:
	with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
		for port in range(MIN,MAX):			
			executor.submit(scan_port,target,port)
	
	
except KeyboardInterrupt:
	print("\nExiting program.")
	sys.exit()
	

except socket.gaierror:
	print ("Hostname could not be resolved.")	
	

except socket.error:
	print("Couldn't connecto to server.")
	sys.exit()				
