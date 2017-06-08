import tx_2400_r2
import rx_2400_r2
import threading
import time
import struct
import rx_processor
from mavlink_stuff.ardupilot import ArduPilot

'''----------------------------------------------------------------------------
Config variables
----------------------------------------------------------------------------'''
tx = False
rx = True
pre_headers = ['SL1', 'SL2', 'SL3']
post_headers = ['ED1', 'ED2', 'ED3']

#transmit variables
out_file = '_send.bin'
tx_time = 1

#receive variables
in_file  = '_out.bin'
fft_file = 'log_power_fft_data.bin'
rx_process = True
rx_new     = True
rx_time    = 60
print_received_transmissions = True

'''[gr_thread]-----------------------------------------------------------------
  Gnuradio interface which allows for callbacks to be made, parallelizing work
  and preventing race conditions on file accesses.
----------------------------------------------------------------------------'''
class gr_thread(threading.Thread):
  def __init__(self, cen_freq=433920000, baud_rate=2500):
    super(gr_thread, self).__init__()
    self.cen_freq = cen_freq
    self.callback = False
    self.daemon = True
    self.baud_rate = baud_rate
    self.rx_m_p = rx_processor.rx_processor(self, pre_headers, post_headers)
  
  '''[end_callback]------------------------------------------------------------
    Ends thread
  --------------------------------------------------------------------------'''
  def end_callback(self):
    self.callback = True
    self.rx_m_p.end_callback()
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
    Starts a rx_processor on a different thread and schedules in_file accesses
    accordingly with the rx_processor to ensure the in_file is being utilized
    fully and processing old samples can be done while reading new samples.
  --------------------------------------------------------------------------'''
  def rx(self):

    print 'Receiving on: ' + str(self.cen_freq)

    if rx_process:
      self.rx_m_p.start()

    if rx_new:
      rx_2400_r2.main(None, None, rx_time, self.cen_freq)

    if rx_process:
      self.rx_m_p.join(1000)


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