from sys import getsizeof
from pyautogui import size
import numpy as np
import time
import pickle
import socket
import os
import os.path
import struct
import cv2
import threading

sock = socket.socket()
sock.bind(('', 8888))
sock.listen(1)
conns = []
connected = False


def recv_data():
	while True:
		if connected:
			data = receive_arr()
			show_data(data)
		else:
			continue


def show_data(data):
	key = cv2.waitKey(10)
	if key == ord('q'):
		quit()
	elif key == ord('s'):
		cv2.imwrite(os.path.join(os.getcwd(), str(time.time()) + '.png'), data)
	cv2.imshow('SpyThing', data)


def receive_arr():
	conn = conns[0]
	data = b''
	payload_size = struct.calcsize('L')
	while len(data) < payload_size:
		data += conn.recv(4096)
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	msg_size = struct.unpack('L', packed_msg_size)[0]
	while len(data) < msg_size:
		data += conn.recv(4096)
	conn.send(b'RECVD')
	frame_data = data[:msg_size]
	data = data[msg_size:]
	frame = pickle.loads(frame_data)
	screen_w, screen_h = size()
	return cv2.resize(frame, (int(screen_w * 0.85), int(screen_h * 0.85)), interpolation=cv2.INTER_AREA)


def accept_connection():
	global connected
	while True:
		if connected:
			break
		else:
			conn, addr = sock.accept()
			print(addr, 'has connected')
			conns.append(conn)
			connected = True


if __name__ == '__main__':
	threads = [threading.Thread(target=accept_connection),
			   threading.Thread(target=recv_data)]
	for thread in threads:
		thread.start()
	print('started threads')
