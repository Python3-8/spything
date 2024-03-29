from sys import getsizeof, argv
import threading
import pickle
import cv2
import socket
import struct

sock = socket.socket()
connected = False
cam = cv2.VideoCapture(0)


def send_data():
	while cam.isOpened():
		ret, frame = cam.read()
		if connected:
			pickled = pickle.dumps(frame)
			sock.sendall(struct.pack('L', len(pickled)) + pickled)
			sock.recv(1024)


def connect():
	global connected
	while True:
		if connected:
			break
		else:
			try:
				print('not connected')
				print('trying to connect')
				sock.connect((argv[1], 8888))
				print('connected')
				connected = True
			except Exception as err:
				print(err, 'errored out, retrying')


if __name__ == '__main__':
	threads = [threading.Thread(target=connect),
			   threading.Thread(target=send_data)]
	for thread in threads:
		thread.start()
	print('started threads')
