'''*-----------------------------------------------------------------------*---
                                                          Author: Jason Ma
                                                          Date  : May 22 2017
    File Name  : bladeRF_full_duplex.py
    Description: Communication protocols for bladeRF to bladeRF communications.
                 A good portion of this was inspired by and uses Stephen 
                 Wayne's FSK communication protocols.
---*-----------------------------------------------------------------------*'''

import tx_2400_r2
import rx_2400_r2
import struct
import bladeRF_scanner
import blade_rx
import sys
import threading
import time

'''----------------------------------------------------------------------------
Config variables
----------------------------------------------------------------------------'''
tx = True
rx = False
scan_best_freqs  = False

center_freq = 433000000
bandwidth   = 1500000

#transmit variables
out_file = '_send.bin'

#receive variables
in_file  = '_out.bin'
rx_new = True
rx_process = True

class gr_thread(threading.Thread):
  def __init__(self, cen_freq=center_freq, baud_rate=5000):
    super(gr_thread, self).__init__()
    self.cen_freq = cen_freq
    self.file_busy = True
    self.daemon = True
    self.baud_rate = baud_rate
    self.start()
    '''
    if tx:
      self.gr_tx = tx_2400_r2.tx_2400_r2()
      self.gr_tx.set_baud_rate(self.baud_rate)
    elif rx:
      self.gr_rx = rx_2400_r2.rx_2400_r2()
      self.gr_rx.set_baud_rate(self.baud_rate)
    '''
  
  def file_ready_callback(self):
    self.file_busy = True
    print '[gr_thread] File ready callback received.'

  def tx(self):
    print 'Transmitting on: ' + str(self.cen_freq)

    #write message to send
    #message = [x for x in range(255)]
    message = []
    for i in range(1):
      for j in range(ord('A'), ord('z') + 1):
        message.append(j)
    pre_header = 'SL1'
    post_header = 'ED1'

    while True:
      pre_header = 'SL1'
      post_header = 'ED1'
      write_message(out_file, message, pre_header, post_header)
      tx_2400_r2.main(out_file)

      pre_header = 'SL2'
      post_header = 'ED2'
      write_message(out_file, message, pre_header, post_header)
      tx_2400_r2.main(out_file)

  def rx(self):
    print 'Receiving on: ' + str(self.cen_freq)

    pre_headers = ['SL1', 'SL2']
    post_headers = ['ED1', 'ED2']

    rx_m_p = rx_processor(self, pre_headers, post_headers)

    while True:
      #wait for file ready
      while not self.file_busy:
        time.sleep(0.1)

      if rx_new:
        rx_2400_r2.main()
      else:
        time.sleep(5)

      self.file_busy = False

      if rx_process:
        print '[gr_thread] File filled.'
        rx_m_p.file_ready_callback()

  def run(self):
    if tx:
      self.tx()
    elif rx:
      self.rx()
    

class rx_processor(threading.Thread):

  def __init__(self, gr_thread, pre_headers = [], post_headers = []):
    super(rx_processor, self).__init__()
    self.pre_h = pre_headers
    self.post_h = post_headers
    self.message = []
    self.file_busy = False
    self.gr_thread = gr_thread
    self.daemon = True
    self.start()

  def update_headers(self, pre_headers, post_headers):
    pre_h = pre_headers
    post_h = post_headers

  def file_ready_callback(self):
    self.file_busy = True
    print '[rx_processor] File ready callback received.'

  def rx_spin(self):
    with open(in_file, 'rb') as f:
      
      stuff = f.read(1)
      
      l = []
      while stuff != "":
        l.append(struct.unpack('B', stuff)[0])
        stuff = f.read(1)

      self.message = l

      print '[rx_processor] Bitstream Length: ' + str(len(l))
      #TODO do something with this
    self.file_busy = False
    print '[rx_processor] File read complete.'

  def extract_by_headers(self, pre_headers, post_headers, message):
    l = []

    print '[rx_processor] Processing stream'
    
    #look for headers in message
    for pre_header, post_header in zip(pre_headers, post_headers):
      print 'Looking for:', pre_header, post_header
      
      start_i = 0
      end_i = 0
      for i in range(0, len(message) - 8 * len(pre_header)):
        n = ''
        for j in range(len(pre_header)):
          #bin_num = int(''.join(str(x) for x in message[i+j*8:i+(j+1)*8]), 2)
          #n += chr(bin_num)
          n += read_byte(message, i + j * 8, 'c')

        if n == pre_header: #found start header
          start_i = i + len(pre_header) * 8
          print '-----[TRANSMISSION START FOUND]-[' + pre_header + ']-[' + str(i) + ']'

        if n == post_header: #found end header
          end_i = i

          #read in 8-bit checksum
          #checksum = int(''.join(str(x) for x in message[start_i:start_i+8]), 2)
          checksum = read_byte(message, start_i)

          #account for checksum
          start_i += 8

          #extract chars from rest of message between headers
          n = ''
          for curr_i in range(start_i, end_i, 8):
            n += read_byte(message, curr_i, 'c')
          
          print n

          print '-----[TRANSMISSION END FOUND  ]-[' + post_header + ']-[' + str(i) + ']'
          
          
          #verify checksum
          actual_checksum = 0
          for byte in n:
            actual_checksum += ord(byte)

          actual_checksum = actual_checksum % 256
          print 'Message_Checksum: ' + str(checksum)
          print 'Actual_checksum:  ' + str(actual_checksum)
          if checksum == actual_checksum:
            print 'Checksum valid'
            l.append(n)
          else:
            print 'Checksum invalid'
          print ''

    return l

  def run(self):
    print '[rx_processor] Thread running'
    while True:
      if self.file_busy:
        self.rx_spin()
        self.gr_thread.file_ready_callback()

        #for i in range(0, len(self.message), 8):
        #  print read_byte(self.message, i)
        extracted = self.extract_by_headers(self.pre_h, self.post_h, self.message)
        
        print '[rx_processor] Stream processed.'
      #else:
      #print '[rx_processor] File not ready yet.'

      
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
  #message = [x for x in range(255)]
  message = []
  for i in range(15):
    for j in range(255):
      message.append(j)
  pre_header = 'SL1'
  post_header = 'ED1'

  while(1):
    pre_header = 'SL1'
    post_header = 'ED1'
    write_message(out_file, message, pre_header, post_header)
    tx_2400_r2.main(out_file, center_freq = center_freq)

    pre_header = 'SL2'
    post_header = 'ED2'
    write_message(out_file, message, pre_header, post_header)
    tx_2400_r2.main(out_file, center_freq = center_freq)

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
    f.write(pre_header)

    print(ba)
    f.write(struct.pack('B', checksum))
    #ba = bytearray(pre_header)
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

  pre_headers = ['SL1', 'SL2']
  post_headers = ['ED1', 'ED2']

  rx_m_p = rx_processor(pre_headers, post_headers)

  while True:
    if rx_new:
      rx_2400_r2.main(center_freq = center_freq)
    else:
      time.sleep(1)

    if rx_process:
      rx_m_p.file_ready_callback()
      #time.sleep(1)

  #while(1):
  '''
  if not debug_old_rx:
    rx_2400_r2.main()

  stream = rx_spin()
  extract_by_headers(pre_headers, post_headers, stream)
  '''

  #receive messages, print out data rate

  #broadcast device id as well as best frequencies

  #wait for proposal

  #accept if reasonable, otherwise reset process

  #broadcast acknowledgement of frequency change

  #change frequency

  #broadcast acknowledgement of connection on new frequency

'''
def rx_spin():
  with open(in_file, 'rb') as f:
    
    
    stuff = f.read(1)
    
    l = []
    while stuff != "":
      l.append(struct.unpack('B', stuff)[0])
      stuff = f.read(1)
    return l
'''

'''
def extract_by_headers(pre_headers, post_headers, message):
  l = []
  
  #look for headers in message
  for pre_header, post_header in zip(pre_headers, post_headers):
    start_i = 0
    end_i = 0
    for i in range(0, len(message) - 8 * len(pre_header)):
      n = ''
      for j in range(len(pre_header)):
        #bin_num = int(''.join(str(x) for x in message[i+j*8:i+(j+1)*8]), 2)
        #n += chr(bin_num)
        n += read_byte(message, i + j * 8, 'c')

      if n == pre_header: #found start header
        start_i = i + len(pre_header) * 8
        print '-----[TRANSMISSION START FOUND]-[' + pre_header + ']-[' + str(i) + ']'

      if n == post_header: #found end header
        end_i = i

        #read in 8-bit checksum
        #checksum = int(''.join(str(x) for x in message[start_i:start_i+8]), 2)
        checksum = read_byte(message, start_i)
        print 'Checksum: ' + str(checksum)

        #account for checksum
        start_i += 8

        #extract chars from rest of message between headers
        n = ''
        for curr_i in range(start_i, end_i, 8):
          n += read_byte(message, curr_i, 'c')
        
        #print n

        print '\n-----[TRANSMISSION END FOUND  ]-[' + post_header + ']-[' + str(i) + ']'
        
        
        #verify checksum
        actual_checksum = 0
        for byte in n:
          actual_checksum += ord(byte)

        actual_checksum = actual_checksum % 256

        if checksum == actual_checksum:
          print 'Checksum valid'
          l.append(n)
        else:
          print 'Checksum invalid'
        print ''
        sys.stdout.flush()

  return l
'''
def read_byte(stream, start_ind, type='i'):
  value = int(''.join(str(x) for x in stream[start_ind:start_ind+8]), 2)

  if type == 'i':
    return value

  if type == 'c':
    return chr(value)


'''[Actual script]----------------------------------------------------------'''

sdr = blade_rx.blade_rf_sdr(1)
#sdr.set_bandwidth('all', 28)
sdr.set_center_freq('all', center_freq / 1000000)

if scan_best_freqs:
  best_freqs = bladeRF_scanner.main()

  #take lowest interference frequency and set it to center_freq for now
  center_freq = best_freqs[0]
'''
if(tx):
  bladeRF_tx(center_freq)

if(rx):
  bladeRF_rx(center_freq, bandwidth)
'''

gr = gr_thread()
gr.join()
