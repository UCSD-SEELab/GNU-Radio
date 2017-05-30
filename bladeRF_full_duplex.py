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
tx = False
rx = True
scan_best_freqs  = False

center_freq = 2450000000
bandwidth   = 1500000

#transmit variables
out_file = '_send.bin'
tx_time = 10

#receive variables
in_file  = '_out.bin'
rx_new = True
rx_process = True
rx_time = 1

'''[gr_thread]-----------------------------------------------------------------
  Gnuradio interface which allows for callbacks to be made, parallelizing work
  and preventing race conditions on file accesses.
----------------------------------------------------------------------------'''
class gr_thread(threading.Thread):
  def __init__(self, cen_freq=center_freq, baud_rate=2500):
    super(gr_thread, self).__init__()
    self.cen_freq = cen_freq
    self.file_busy = False
    self.daemon = True
    self.baud_rate = baud_rate
    self.start()
    ''' TODO set_baud_rate doesn't seem to be working, neither does center_freq
    if tx:
      self.gr_tx = tx_2400_r2.tx_2400_r2()
      self.gr_tx.set_baud_rate(self.baud_rate)
    elif rx:
      self.gr_rx = rx_2400_r2.rx_2400_r2()
      self.gr_rx.set_baud_rate(self.baud_rate)
    '''
  
  '''[file_ready_callback]-----------------------------------------------------
    Gives gr_thread a notification that the in_file is ready for access.
  --------------------------------------------------------------------------'''
  def file_ready_callback(self):
    self.file_busy = True
    print '[gr_thread] File ready callback received.'

  '''[tx]----------------------------------------------------------------------
    Writes predefined messages to out_file, then transmits continuously until 
    program termination.
  --------------------------------------------------------------------------'''
  def tx(self):
    print 'Transmitting on: ' + str(self.cen_freq)

    #length 256 message
    message1 = [x for x in range(255)]

    #length 75 message
    message2 = []
    for i in range(1):
      for j in range(ord('0'), ord('z') + 1):
        message2.append(j)

    #length 26 message
    message3 = []
    for i in range(1):
      for j in range(ord('a'), ord('z') + 1):
        message3.append(j)

    #transmit messages continuously
    while True:
      pre_header = 'SL1'
      post_header = 'ED1'
      write_message(out_file, message2, pre_header, post_header)
      tx_2400_r2.main(None, None, tx_time, center_freq, out_file)

      pre_header = 'SL2'
      post_header = 'ED2'
      write_message(out_file, message3, pre_header, post_header)
      tx_2400_r2.main(None, None, tx_time, center_freq, out_file)

      #broadcast device id as well as best frequencies
      #wait for an expected device to connect and broadcast
      #propose a frequency change to one of the best current freqs
      #receive acknowledge before changing frequency
      #receive acknowledgement of connection on new frequency

  '''[rx]----------------------------------------------------------------------
    Starts a rx_processor on a different thread and schedules in_file accesses
    accordingly with the rx_processor to ensure the in_file is being utilized
    fully and processing old samples can be done while reading new samples.
  --------------------------------------------------------------------------'''
  def rx(self):
    print 'Receiving on: ' + str(self.cen_freq)

    pre_headers = ['SL1', 'SL2']
    post_headers = ['ED1', 'ED2']

    rx_m_p = rx_processor(self, pre_headers, post_headers)

    while True:
      #wait for file ready before calling rx_2400_r2.main()
      while not self.file_busy:
        time.sleep(0.1)

      if rx_new:
        #start_rx = time.time() * 1000
        rx_2400_r2.main(None, None, rx_time, center_freq)
        #end_rx = time.time() * 1000
        #rx_time = end_rx - start_rx
        #TODO pass this into file_ready_callback so processor knows time frame
      else:
        time.sleep(5)

      self.file_busy = False

      if rx_process:
        print '[gr_thread] File filled.'
        rx_m_p.file_ready_callback()

      #receive messages, print out data rate
      #broadcast device id as well as best frequencies
      #wait for proposal
      #accept if reasonable, otherwise reset process
      #broadcast acknowledgement of frequency change
      #change frequency
      #broadcast acknowledgement of connection on new frequency

  '''[run]---------------------------------------------------------------------
    Starts when thread is run.
  --------------------------------------------------------------------------'''
  def run(self):
    if tx:
      self.tx()
    elif rx:
      self.rx()
    
  '''[rx_processor]------------------------------------------------------------
    Reads in and processes received samples. Reading in is done on a callback
    system so the file is not accessed while it is being written to, but
    processing is done in parallel with receiving new samples.
  --------------------------------------------------------------------------'''
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

  '''[update_headers]----------------------------------------------------------
    Updates the headers being looked for

    pre_headers  - beginning headers
    post_headers - ending headers
  --------------------------------------------------------------------------'''
  def update_headers(self, pre_headers, post_headers):
    pre_h = pre_headers
    post_h = post_headers

  '''[file_ready_callback]-----------------------------------------------------
    Gives gr_thread a notification that the in_file is ready for access.
  --------------------------------------------------------------------------'''
  def file_ready_callback(self):
    self.file_busy = True
    print '[rx_processor] File ready callback received.'

  '''[rx_spin]-----------------------------------------------------------------
    Reads stream into a list containing bitstream for further processing later.
  --------------------------------------------------------------------------'''
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
    print '[rx_processor] File read complete.'

  '''[extract_by_headers]------------------------------------------------------
    Look for pre and post headers in bitstream, extract message if found.

    pre_headers  - headers marking beginning of message
    post_headers - headers marking end of message
  --------------------------------------------------------------------------'''
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
        #read string of characters of length of header
        for j in range(len(pre_header)):
          n += read_byte(message, i + j * 8, 'c')

        #found start header
        if n == pre_header:
          start_i = i + len(pre_header) * 8
          print '-----[TRANSMISSION START FOUND]-[' + pre_header + ']-[' + str(i) + ']'
        
        #found end header
        if n == post_header:
          end_i = i

          #TODO handle case where start_i = 0, don't just print crap out
          #if start_i == 0:
          #  continue

          #read in 8-bit checksum
          checksum = read_byte(message, start_i)

          #account for checksum being read in
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

  '''[run]---------------------------------------------------------------------
    Starts when thread is run.
  --------------------------------------------------------------------------'''
  def run(self):
    print '[rx_processor] Thread running'
    while True:
      if self.file_busy:

        #access stream
        self.rx_spin()

        #done accessing stream
        self.file_busy = False
        self.gr_thread.file_ready_callback()

        #process stream
        extracted = self.extract_by_headers(self.pre_h, self.post_h, self.message)
        
        print '[rx_processor] Stream processed.'

#TODO integrate with new class or gnuradio_thread

'''[write_message]-------------------------------------------------------------
  Write message to bin file

  file        - file to write to
  message     - message to transmit
  pre_header  - place before message
  post_header - place after message
----------------------------------------------------------------------------'''
def write_message(file, message, pre_header, post_header):

  #calculate checksum of message by adding it all up
  checksum = 0

  ba = bytearray(message)
  for byte in ba:
    checksum += byte

  checksum = checksum % 256

  print '[write_message]-[' + str(checksum) + ']'
  print ba

  with open(file, 'wb') as f:
    f.write(pre_header)
    f.write(struct.pack('B', checksum))
    ba = bytearray(message)
    f.write(ba)
    f.write(post_header)

    return checksum

#TODO integrate with new class or gnuradio_thread

'''[read_byte]-----------------------------------------------------------------
  Read byte from bitstream and return the int or char representation

  stream    - stream to read from
  start_ind - start index of byte
  type      - 'i' for int, 'c' for char
----------------------------------------------------------------------------'''
def read_byte(stream, start_ind, type='i'):
  value = int(''.join(str(x) for x in stream[start_ind:start_ind+8]), 2)

  if type == 'i':
    return value

  if type == 'c':
    return chr(value)


'''[Actual script]----------------------------------------------------------'''

sdr = blade_rx.blade_rf_sdr(1)
#sdr.set_bandwidth('all', 1.5)
sdr.set_center_freq('all', center_freq / 1000000)

if scan_best_freqs:
  #get list of best frequencies
  best_freqs = bladeRF_scanner.main()

  #take lowest interference frequency and set it to center_freq for now
  center_freq = best_freqs[0]

gr = gr_thread()
gr.file_ready_callback()
gr.join()
