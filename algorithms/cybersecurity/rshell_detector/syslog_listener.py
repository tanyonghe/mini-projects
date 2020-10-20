#!/usr/bin/env python3

import socket


# main configurations
SOCKET_IP = 'localhost'
SOCKET_PORT = 514
MAX_DATA_SIZE = 1024


def setup_socket():
	print("Setting up socket on " + SOCKET_IP + " port " + str(SOCKET_PORT) + " ...")
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((SOCKET_IP, SOCKET_PORT))

	print("Listening on socket...")

	s.listen(1)
	conn, addr = s.accept()

	print("Accepted a socket connection!")
	
	return (conn, addr)


def collect_socket_data(conn, addr):
	while 1:
		try:
			data = conn.recv(MAX_DATA_SIZE)
			if not data:
				break
			print(data.decode())
			conn.sendall(data)
		except KeyboardInterrupt:
			conn.close()
		
		
if __name__== "__main__":
	(conn, addr) = setup_socket()
	collect_socket_data(conn, addr)