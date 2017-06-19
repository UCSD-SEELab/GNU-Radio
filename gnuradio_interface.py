'''*-----------------------------------------------------------------------*---
                                                          Author: Jason Ma
                                                          Date  : Jun 07 2017

    File Name  : gnuradio_interface.py
    Description: gnuradio_interface calls either rx_2400_r2 or tx_2400_r2
                 depending on configuration to either receive or transmit
                 data using FSK modulation. It also starts a rx_processor
                 thread to process either old or live data.
---*-----------------------------------------------------------------------*'''

from mavlink_stuff.ardupilot import ArduPilot
import tx_2400_r2
import rx_2400_r2
import rx_processor

import struct
import threading
import time

'''----------------------------------------------------------------------------
Config variables
----------------------------------------------------------------------------'''
tx = True
rx = False

#transmit variables
out_file = '_send.bin'
tx_time  = 1

#receive variables
rx_new   = True
rx_time  = 60

'''[gr_thread]-----------------------------------------------------------------
  Gnuradio interface which allows for callbacks to be made, parallelizing work
  and preventing race conditions on file accesses.
----------------------------------------------------------------------------'''
class gr_thread(threading.Thread):

  '''[__init__]----------------------------------------------------------------
    Initializes gr_thread with appropriate center freq and baud rate.

    cen_freq  - center frequency to rx/tx at
    baud_rate - bitrate of writing
  --------------------------------------------------------------------------'''
  def __init__(self, cen_freq=433920000, baud_rate=2500):
    super(gr_thread, self).__init__()
    self.cen_freq = cen_freq
    self.callback = False
    self.daemon = True
    self.baud_rate = baud_rate

  '''[end_callback]------------------------------------------------------------
    Ends thread
  --------------------------------------------------------------------------'''
  def end_callback(self):
    self.callback = True
    #self.rx_m_p.end_callback()
    print '[gr_thread] Callback received. Shutting down'

  '''[tx]----------------------------------------------------------------------
    Writes predefined messages to out_file, then transmits continuously until 
    program termination.
  --------------------------------------------------------------------------'''
  def tx(self):
    print 'Transmitting on: ' + str(self.cen_freq)

    out_files = []
    out_files.append('_send1.bin')
    out_files.append('_send2.bin')
    out_files.append('_send.bin')

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

    pre_header = 'SL1'
    post_header = 'ED1'
    write_message(out_files[0], message1, pre_header, post_header)

    pre_header = 'SL2'
    post_header = 'ED2'
    write_message(out_files[1], message2, pre_header, post_header)

    pre_header = 'SL3'
    post_header = 'ED3'
    write_message(out_files[2], message3, pre_header, post_header)

    tx_2400_r2.main(None, None, tx_time, self.cen_freq, out_file)

  '''[rx]----------------------------------------------------------------------
    Receives to _out.bin, which can be accessed while it is being written to
    by rx_processor either live or post run.
  --------------------------------------------------------------------------'''
  def rx(self):

    print 'Receiving on: ' + str(self.cen_freq)

    if rx_new:
      rx_2400_r2.main(None, None, rx_time, self.cen_freq)

  '''[run]---------------------------------------------------------------------
    Starts when thread is run.
  --------------------------------------------------------------------------'''
  def run(self):
    if tx:
      self.tx()
    elif rx:
      self.rx()

'''[write_message]-------------------------------------------------------------
  Write message to bin file

  file        - file to write to
  message     - message to transmit
  pre_header  - place before message
  post_header - place after message
  return      - checksum of message
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
  print ''

  with open(file, 'wb') as f:
    f.write(pre_header)
    f.write(struct.pack('B', checksum))
    ba = bytearray(message)
    f.write(ba)
    f.write(post_header)

    return checksum