#!/usr/bin/env python3

import pexpect
import time
import sys
from re import search
from getpass import getpass
import logging

passwd = "Danni1993!"
#host = "10.20.20.14"
user = "admin"

accprofile_name = 'API-USER'
accprofile_rw = 'read' # There are three choices here (none,read, and read-write) if you desire individual settings for areas of control you will need to override them in the expect strings individually.
api_user_name = 'API'
slow_down = 0.5  # The time to sleep between commands because pexpect can run way too fast.
debug_flag = True
log_to_file = False
logging_file = "api_create.log"
debug_log_path = "./"
logging_path_and_file = debug_log_path + logging_file

# Debug setting test
if debug_flag == True:
	debug_flag_set = logging.DEBUG
else:
	debug_flag_set = logging.INFO
	
if log_to_file == True:
	logging.basicConfig(filename=logging_path_and_file,level=debug_flag_set,format='%(asctime)s:%(levelname)s:%(message)s')
	logging.debug("************* Begin of Instance ************* ")
else:
	logging.basicConfig(level=debug_flag_set,format='%(asctime)s:%(levelname)s:%(message)s')

def start_tunnel (host):
	
	try:
		tunnel_command = 'ssh ' + user + '@' + host
		ssh_tunnel = pexpect.spawn (tunnel_command % globals())
		#ssh_tunnel.logfile = sys.stdout.buffer  # Used for hard core troubleshooting
		logging.info("Setting new password")
		
		ssh_tunnel.expect('Are you sure you want to continue connecting (yes/no/[fingerprint])?')
	
		ssh_tunnel.sendline('yes')

		ssh_tunnel.expect ('New Password:')

		ssh_tunnel.sendline (passwd)

		ssh_tunnel.expect ('Confirm Password:')

		ssh_tunnel.sendline (passwd)
		
		logging.info("Password set")

		ssh_tunnel.expect('#')
		
		logging.info("Creating accprofile for API user")

		ssh_tunnel.sendline('config system accprofile')

		ssh_tunnel.expect('accprofile')	
		
		ssh_tunnel.sendline('edit ' + accprofile_name)
		
		ssh_tunnel.expect(accprofile_name)
		
		ssh_tunnel.sendline('set secfabgrp ' + accprofile_rw)
		ssh_tunnel.sendline('set ftviewgrp ' + accprofile_rw)
		ssh_tunnel.sendline('set authgrp ' + accprofile_rw)
		ssh_tunnel.sendline('set sysgrp ' + accprofile_rw)
		ssh_tunnel.sendline('set netgrp ' + accprofile_rw)
		ssh_tunnel.sendline('set loggrp ' + accprofile_rw)
		ssh_tunnel.sendline('set fwgrp ' + accprofile_rw)
		ssh_tunnel.sendline('set vpngrp '+ accprofile_rw)
		ssh_tunnel.sendline('set utmgrp ' + accprofile_rw)
		ssh_tunnel.sendline('set wanoptgrp ' + accprofile_rw)
		ssh_tunnel.sendline('set wifi ' + accprofile_rw)	
		
		ssh_tunnel.expect(accprofile_name)
		
		ssh_tunnel.sendline('end')
		
		logging.info("Created profile")
		
		ssh_tunnel.expect('#')
		
		logging.info("Creating api-user")
		
		ssh_tunnel.sendline('config system api-user')
		
		time.sleep(slow_down)
		
		ssh_tunnel.expect('api-user')
		
		ssh_tunnel.sendline('edit ' + api_user_name)
		
		time.sleep(slow_down)
		
		ssh_tunnel.expect(api_user_name)
		
		time.sleep(slow_down)
		
		logging.info("Setting api-user profile")
		
		ssh_tunnel.sendline('set accprofile ' + accprofile_name)
		
		ssh_tunnel.expect(api_user_name)
		
		time.sleep(slow_down)
		
		ssh_tunnel.sendline('set comments "API user for remote access"')
		
		ssh_tunnel.expect('#')
		
		ssh_tunnel.sendline('end')
		
		ssh_tunnel.expect('#')
		
		logging.info("Added api-user profile")
		
		time.sleep(slow_down)
		
		logging.info("Generating api key")
		
		ssh_tunnel.sendline('execute api-user generate-key ' + api_user_name)

		ssh_tunnel.expect('#')
		
		ssh_tunnel.sendline('exit')
		for line in ssh_tunnel:   # This is where I grab the key.
			x = str(line)
			key_search = "New"
			if search(key_search, str(x)):
				y = x.split()
				z = (y[3])
				key = z[0:30]
				print("API KEY: " + key)
		logging.info("Done with host")
		ssh_tunnel.kill(0)

		ssh_tunnel.expect (pexpect.EOF)
		
	except Exception as e:
		logging.info("Not responding or password already set")
		#print(str(e))
		
start_tunnel("10.20.20.15")