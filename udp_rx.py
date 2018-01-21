'''*-----------------------------------------------------------------------*---
                                                          Author: Jason Ma
                                                          Date  : Dec 20 2017

    File Name  : udp_rx.py
    Description: Listens to UDP port bound to gnuradio scheme for receiving.
---*-----------------------------------------------------------------------*'''

import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 9002
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((UDP_IP, UDP_PORT))

totalbytes = 0
time_passed = 0
minrate = 10000
maxrate = 0
try:
  while True:
    try:
      start_time = time.time()
      bytecount = 0
      while time.time() - start_time < 1:
        data, addr = sock.recvfrom(2048)
        #print "length:", str(len(data)), "message:", data
        bytecount += len(data)
      rate = bytecount / 1000.0
      print "RATE:", rate, 'kiB/s'

      if rate < minrate:
        minrate = rate

      if rate > maxrate:
        maxrate = rate

      totalbytes += bytecount
      time_passed += 1
    except Exception as e:
      print '[ERROR]', e
except KeyboardInterrupt:
  print '\n Ctrl+c received.'
  print 'TOTAL BYTES:', totalbytes
  print 'TOTAL TIME:', time_passed

  if time_passed != 0:
    print 'TOTAL RATE:', totalbytes / (1000.0 * time_passed), 'kiB/s'

  print 'MIN RATE:', minrate
  print 'MAX RATE:', maxrate
