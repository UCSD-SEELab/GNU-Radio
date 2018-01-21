'''*-----------------------------------------------------------------------*---
                                                          Author: Jason Ma
                                                          Date  : Dec 20 2017

    File Name  : udp_tx.py
    Description: Sends data to UDP port bound to gnuradio transmission scheme.
---*-----------------------------------------------------------------------*'''

import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 9000
MESSAGE = "Hello, World!"

MPS = 2
sleep_time = 1.0 / MPS

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

try:
  #start_time = time.time()
  #while time.time() - start_time < 20:
  #  sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

  while True:
    start_time = time.time()
    while(time.time() - start_time < sleep_time):
      time.sleep(sleep_time / 10)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

except KeyboardInterrupt:
  print 'Ctrl+c received.'