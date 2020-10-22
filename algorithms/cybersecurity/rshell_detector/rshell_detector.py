#!/usr/bin/env python3

from scapy.all import *

import argparse
import os
import socket
import subprocess
import sys


# main configurations
DEBUG = False
IFACE = conf.iface
FILTER = ''
SERVER_IP = socket.gethostbyname(socket.gethostname())

# hard-coded lists
directory_traversals = ['~', '.', '..', ':/']
whitelisted_commands = ['command']


'''
	Checks for directory traversal signs like '~', '.', '..' and ':/'.
'''
def contains_directory_traversal(payload):
	payload_lst = payload.replace("\\", "/").split("/")
	
	for dt in directory_traversals:
		if dt in payload_lst:
			return True
	return False


'''
	Checks payload for valid terminal commands.
	Assumption is that the script is running on a similar OS as the payload-receiver.
'''
def contains_valid_command(payload):
	payload_lst = payload.replace("|", "").split(" ")

	for p in payload_lst:
		output = ''
		if p and p not in whitelisted_commands:
			if sys.platform.startswith('linux'):
				try:
					output = subprocess.check_output('command -v ' + p, shell=True)
				except:
					# command -v command returns non-zero exit code when input command DOES NOT exist
					if DEBUG:
						print('Input command', p, 'not found on linux terminal')
					continue

			elif sys.platform.startswith('win32'):
				try:
					# checks for internal commands like dir and cd
					output = subprocess.check_output('help ' + p, shell=True)
				except:
					# help command returns non-zero exit code when input command exists
					return True
				else:
					try:
						# checks for external commands like python.exe and tshark.exe inside PATH
						output = ''
						output = subprocess.check_output('where ' + p, shell=True, stderr=open(os.devnull, 'w'))
					except:
						# where command returns non-zero exit code when input command DOES NOT exist
						if DEBUG:
							print('Input command', p, 'not found on windows command prompt')
						continue

			else:
				# no support for cygwin and darwin yet
				print(sys.platform, "is not supported yet!")

			if output:
				return True
	return False


'''
	Parses command-line arguments.
'''
def args_setup():
	ap = argparse.ArgumentParser()
	ap.add_argument('-v', '--verbose', required=False, help='verbose mode', nargs='?', const='')
	ap.add_argument('-if', '--iface', required=False, help='interface', nargs='?', const='')
	ap.add_argument('-fi', '--filter', required=False, help='filter', nargs='?', const='')
	
	args = vars(ap.parse_args())
	
	if args['verbose'] is not None:
		global DEBUG
		DEBUG = True
	if args['iface'] is not None:
		global IFACE
		IFACE = args['iface']
	if args['filter'] is not None:
		global FILTER
		FILTER = args['filter']
		
	return args
	

'''
	Checks TCP packets for unencrypted and unencoded terminal commands (reverse shell).
	Checks ICMP packets for unencrypted and unencoded terminal commands (ICMP tunneling).
'''
def network_monitoring(pkt):

	# classify TCP packets
	if pkt.haslayer(TCP):
		payload = bytes(pkt[TCP].payload).decode(encoding="latin-1").replace("\n", " ")
		
		if contains_valid_command(payload):
			print("Command detected in TCP packet:")
			print(payload)

		elif contains_directory_traversal(payload):
			print("Directory traversal detected in TCP packet:")
			print(payload)
				
	# classify ICMP packets
	elif pkt.haslayer(ICMP):
		payload = bytes(pkt[ICMP].payload).decode().replace("\n", " ")

		if contains_valid_command(payload):
			print("Command detected in ICMP packet:")
			print(payload)

		elif contains_directory_traversal(payload):
			print("Directory traversal detected in ICMP packet:")
			print(payload)
	

if __name__ == '__main__':
	args_setup()
	sniff(iface=IFACE, filter=FILTER, prn=network_monitoring)