'''*-----------------------------------------------------------------------*---
                                                          Author: Jason Ma
                                                          Date  : May 22 2017
    File Name  : bladeRF_full_duplex.py
    Description: Communication protocols for bladeRF to bladeRF communications
---*-----------------------------------------------------------------------*'''

import tx_2400_r2
import rx_2400_r2
import struct
import bladeRF_scanner
import blade_rx
import sys

'''----------------------------------------------------------------------------
Config variables
----------------------------------------------------------------------------'''
datarate_test_tx = False
scan_best_freqs  = False

debug_old_rx = True
center_freq = 433000000
bandwidth   = 1500000

#transmit variables
out_file = '_send.bin'

#receive variables
in_file  = '_out.bin'

'''[init_comms]----------------------------------------------------------------
  Attempts to initialize communications with a drone using a certain id.
----------------------------------------------------------------------------'''
#def init_comms(my_id, their_id, best_freqs):
  #broadcast best frequencies for this drone and await response


'''[datarate_test_tx]----------------------------------------------------------
  Constantly send data over radio
----------------------------------------------------------------------------'''
def bladeRF_tx(cen_freq):
  print 'Transmitting on: ' + str(cen_freq)

  #write message to send
  message = [x for x in range(255)]
  pre_header = 'SL1'
  post_header = 'ED1'
  write_message(out_file, message, pre_header, post_header)

  while(1):
    tx_2400_r2.main(out_file)

  #transmit bytes over and over

  #TODO implement the below

  #broadcast device id as well as best frequencies

  #wait for an expected device to connect and broadcast

  #propose a frequency change to one of the best current freqs

  #receive acknowledge before changing frequency

  #receive acknowledgement of connection on new frequency

def write_message(file, message, pre_header, post_header):

  #calculate checksum of message by adding it all up
  checksum = 0

  ba = bytearray(message)
  for byte in ba:
    checksum += byte

  print(checksum)
  checksum = checksum % 256

  with open(file, 'wb') as f:
    #ba = bytearray(checksum)
    #f.write(ba)
    print(ba)
    f.write(struct.pack('B', checksum))
    #ba = bytearray(pre_header)
    f.write(pre_header)
    ba = bytearray(message)
    f.write(ba)
    #ba = bytearray(post_header)
    f.write(post_header)

    return checksum

'''[datarate_test_rx]----------------------------------------------------------
  Attempt to receive data and measure datarate
----------------------------------------------------------------------------'''
def bladeRF_rx(cen_freq, bw):
  print 'Receiving on: ' + str(cen_freq)

  pre_header = 'SL1'
  post_header = 'ED1'

  #while(1):
  if not debug_old_rx:
    rx_2400_r2.main()

  stream = rx_spin()
  extract_by_headers(['SL1'], ['ED1'], stream)

  #receive messages, print out data rate

  #broadcast device id as well as best frequencies

  #wait for proposal

  #accept if reasonable, otherwise reset process

  #broadcast acknowledgement of frequency change

  #change frequency

  #broadcast acknowledgement of connection on new frequency

def rx_spin():
  with open(in_file, 'rb') as f:
    
    
    stuff = f.read(1)
    
    l = []
    while stuff != "":
      l.append(struct.unpack('B', stuff)[0])
      stuff = f.read(1)
    return l

def extract_by_headers(pre_headers, post_headers, message):
  l = []
  
  #look for headers in message
  for pre_header, post_header in zip(pre_headers, post_headers):
    start_i = 0
    end_i = 0
    for i in range(0, len(message) - 8 * len(pre_header)):
      n = ''
      for j in range(len(pre_header)):
        bin_num = int(''.join(str(x) for x in message[i+j*8:i+(j+1)*8]), 2)
        n += chr(bin_num)

      if n == pre_header: #found start header
        start_i = i
        print '-----[TRANSMISSION START FOUND]-[' + pre_header + ']-[' + str(i) + ']'

      if n == post_header: #found end header
        end_i = i
        n = ''
        for curr_i in range(start_i, end_i, 8):
          bin_num = int(''.join(str(x) for x in message[curr_i:curr_i+8]), 2)
          print chr(bin_num),
          n += chr(bin_num)
        
        print '\n-----[TRANSMISSION END FOUND  ]-[' + post_header + ']-[' + str(i) + ']'
        print ''
        sys.stdout.flush()
        
        #verify checksum
        
        if checksum_valid:
          l.append(n)
  return l

'''[Actual script]----------------------------------------------------------'''

sdr = blade_rx.blade_rf_sdr(1)
#sdr.set_bandwidth('all', 28)
sdr.set_center_freq('all', center_freq / 1000000)

if scan_best_freqs:
  best_freqs = bladeRF_scanner.main()

  #take lowest interference frequency and set it to center_freq for now
  center_freq = best_freqs[0]

if(datarate_test_tx):
  bladeRF_tx(center_freq)
else:
  bladeRF_rx(center_freq, bandwidth)
