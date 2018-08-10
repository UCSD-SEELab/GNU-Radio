'''*-----------------------------------------------------------------------*---
                                                         Author: Jason Ma
                                                         Date  : Jun 13 2018
                                      TODO

  File Name  : bertest.py
  Description: TODO
---*-----------------------------------------------------------------------*'''

import socket
import fcntl
import struct
import time

sdr_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SDR_IF = 'tun0'
SDR_PORT = 9002

RX_IP = '192.168.0.1'
RX_PORT = 9001

INTERVAL = 1

RX = 0
TX = 1
MANUAL = 2
MODE = TX

#TODO figure out what to TX, do this in a way that is easy to change
TX_PATTERN = b'\xff\x00\xff\x00' * 10

'''[get_ip_address]------------------------------------------------------------
  Gets IP address of interface
  ifname - name of interface
----------------------------------------------------------------------------'''
def get_ip_address(ifname):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', str.encode(ifname[:15])))[20:24])

'''[main]----------------------------------------------------------------------
  TODO
----------------------------------------------------------------------------'''
def main():

  print("[main] Test starting")
  
  sdr_s.connect(('localhost', SDR_PORT))

  total_bytes = 0
  test_start = time.time()
  start = time.time()

  first_packet = True
  #connect to socket server as client. Print total number of packets received over time
  
  if MODE == RX:
    try:
      while True:
        data, addr = sdr_s.recvfrom(20)
        
        if first_packet:
          test_start = time.time()
          first_packet = False
        
        total_bytes += len(data)
        #print("[main] [RX] " + str(data))
        #print("[main] [Rx] " + str(int.from_bytes(data, byteorder='big')))

        now = time.time()
        if(now - start > INTERVAL):
          total_time = now - test_start
          print("[main] Total RX: " + str(total_bytes) + " b | Time: " + str(total_time))
          start = time.time()
    except KeyboardInterrupt:
      print("[main] Ctrl+C detected. Ending test")
    
      total_time = time.time() - test_start

      print("[main] Test results:")
      print("[main] Total bytes RXed: " + str(total_bytes) + " b | Total Time: " + str(total_time) + "s")
  elif MODE == TX:
    try:
      while True:
        sdr_s.sendto(TX_PATTERN, ('localhost', SDR_PORT))
        total_bytes += len(TX_PATTERN)
        
        now = time.time()
        if(now - start > INTERVAL):
          print("[main] Total TX: " + str(total_bytes) + " b")
          start = time.time()
        else:
          time.sleep(0.01)
    except KeyboardInterrupt:
      print("[main] Ctrl+C detected. Ending test")

      total_time = time.time() - test_start

      print("[main] Test results:")
      print("[main] Total bytes TXed: " + str(total_bytes) + " b | Total Time: " + str(total_time) + "s")

  elif MODE == MANUAL:
    try:
      while True:

       data, addr = sdr_s.recvfrom(20)
        
       if first_packet:
         test_start = time.time()
         first_packet = False
        
       total_bytes += len(data)

       now = time.time()
       if(now - start > INTERVAL):
         total_time = now - test_start
         print("[main] Total RX: " + str(total_bytes) + " b | Time: " + str(total_time))
         start = time.time()

       if time.time() - test_start >= 15.0:
         total_time = now - test_start
         print("[main] Test results:")
         print("[main] Total bytes RXed: " + str(total_bytes) + " b | Total Time: " + str(total_time) + "s")
         break

    except KeyboardInterrupt:
      print("[main] Ctrl+C detected. Ending test")

      total_time = time.time() - test_start

      print("[main] Test results:")
      print("[main] Total bytes TXed: " + str(total_bytes) + " b | Total Time: " + str(total_time) + "s")

  

if __name__ == "__main__":
  main()
