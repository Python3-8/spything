from sys import getsizeof
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


def connect():
    global connected
    while True:
        if connected:
            break
        else:
            print('not connected')
            try:
                print('trying to connect')
                sock.connect(('192.168.1.86', 8888))
                print('connected')
                connected = True
            except Exception as err:
                print(str(err))
                print('errored out')


if __name__ == '__main__':
    threads = [threading.Thread(target=connect),
               threading.Thread(target=send_data)]
    for thread in threads:
        thread.start()
    print('started threads')