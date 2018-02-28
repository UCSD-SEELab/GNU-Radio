'''*-----------------------------------------------------------------------*---
                                                          Author: Jason Ma
                                                          Date  : Jun 07 2017

    File Name  : rx_processor.py
    Description: rx_processor processes the data received, including the
                 bitstream containing communication data, GPS, and anything
                 else being collected. This can be set to work on old or new
                 data.
---*-----------------------------------------------------------------------*'''

import struct
import threading
import time

gps_file = 'io/gps_data'
bitstream_pos_file = 'io/bitstream_pos'

'''----------------------------------------------------------------------------
Config variables
----------------------------------------------------------------------------'''
print_verbose = True

'''[rx_processor]--------------------------------------------------------------
  Reads in and processes received samples. Reading in is done on a callback
  system so the file is not accessed while it is being written to, but
  processing is done in parallel with receiving new samples.
----------------------------------------------------------------------------'''
class rx_processor(threading.Thread):

  '''[__init__]----------------------------------------------------------------
    Initializes rx_processor to look for certain headers.

    pre_headers  - beginning headers
    post_headers - ending headers
  --------------------------------------------------------------------------'''
  def __init__(self, in_file, pre_headers, post_headers, rx_new, gps_new):
    super(rx_processor, self).__init__()
    self.daemon = True
    self.callback = False
    self.filewrite = False
    self.file_pos = 0
    self.in_file = in_file
    self.pre_h = pre_headers
    self.post_h = post_headers
    self.rx_new = rx_new
    self.gps_new = gps_new
    self.message = []

    #only import ardupilot stuff if needed
    if gps_new:
      from mavlink_stuff.ardupilot import ArduPilot

  '''[update_headers]----------------------------------------------------------
    Updates the headers being looked for

    pre_headers  - beginning headers
    post_headers - ending headers
  --------------------------------------------------------------------------'''
  def update_headers(self, pre_headers, post_headers):
    pre_h = pre_headers
    post_h = post_headers

  '''[filewrite_callback]------------------------------------------------------
    Begins a spin when this is called
  --------------------------------------------------------------------------'''
  def filewrite_callback(self):
    self.filewrite = True

  '''[end_callback]------------------------------------------------------------
    Ends thread
  --------------------------------------------------------------------------'''
  def end_callback(self):
    self.callback = True
    print '[rx_processor] Callback received. Shutting down.'

  '''[rx_spin]-----------------------------------------------------------------
    Reads stream into a list containing bitstream for further processing later.

    pos    - where to begin reading in the bitstream
    return - current end position of bitstream
  --------------------------------------------------------------------------'''
  def rx_spin(self, pos):
    with open(self.in_file, 'r') as f:

      f.seek(0, 2)
      print '[rx_processor] New bytes: ' + str(f.tell() - pos)
      '''
      f.seek(pos)

      
      stuff = f.read(1)
      
      if stuff == '':
        print '[rx_processor] EOF found'
        return f.tell()

      l = []
      while stuff != "":
        l.append(struct.unpack('B', stuff)[0])
        stuff = f.read(1)

      self.message = l

      print '[rx_processor] Starting at pos: ' + str(pos) + '\tBitstream Length: ' + str(len(l))
      #TODO do something with this
      #print '[rx_processor] File read complete.'
      '''
      return f.tell()

  '''[get_file_pos]------------------------------------------------------------
    Returns where in the bitstream the processor currently is.

    return - point at which all previous data has been processed
  --------------------------------------------------------------------------'''
  def get_file_pos(self):
    return self.file_pos

  '''[run]---------------------------------------------------------------------
    Starts when thread is run.
  --------------------------------------------------------------------------'''
  def run(self):
    print '[rx_processor] Initialized'
    self.file_pos = 0

    if self.gps_new:
      print '[rx_processor] Initializing GPS'
      gps = ArduPilot('udp:localhost:14550', 15200, True)
      gps.setDataStreams()

    while True:

      if self.callback:
        break

      while not self.filewrite:
        time.sleep(0.1)

      self.filewrite = False

      start_time = time.time() * 1000

      #access stream
      previous_pos = self.file_pos
      self.file_pos = self.rx_spin(self.file_pos)

      #write GPS data
      if self.gps_new:
        with open(gps_file, "a") as f_gps:
          print '[rx_processor] writing GPS and RSSI data'

          #write location data
          try:
            msg = gps.getLocation()
          except Exception:
            print '[rx_processor] [gps] exception: location'

          if msg is not None:
            f_gps.write(str(msg) + '\n')
          else:
            f_gps.write('nothing\n')

          #write heading data
          try:
            msg = gps.getHeading()
          except Exception:
            print '[rx_processor] [gps] exception: heading'

          if msg is not None:
            f_gps.write(str(msg) + '\n')
          else:
            f_gps.write('nothing\n')

          #write altitude data
          try:
            msg = gps.getAltitude()
          except Exception:
            print '[rx_processor] [gps] exception: altitude'

          if msg is not None:
            f_gps.write(str(msg) + '\n')
          else:
            f_gps.write('nothing\n')

      #write bitstream pos data
      if self.rx_new:
        with open(bitstream_pos_file, "a") as f_bs:
          f_bs.write(str(self.file_pos) + '\n')

      end_time = time.time() * 1000

      if self.file_pos == previous_pos:
        print '[rx_processor] No new data in bitstream'
        continue

      #process stream
      #extracted = extract_by_headers(self.pre_h, self.post_h, self.message)
      #if len(extracted) > 0:
      #  print '[rx_processor] Successful packet transfer!'
      #
      #print '[rx_processor] Valid Packets: ' + str(len(extracted)) + '\tTime: ' + str(end_time - start_time)

'''[extract_by_headers]--------------------------------------------------------
  Look for pre and post headers in bitstream, extract message if found.

  pre_headers  - headers marking beginning of message
  post_headers - headers marking end of message
  return       - list containing extracted messages
----------------------------------------------------------------------------'''
def extract_by_headers(pre_headers, post_headers, message):
  l = []

  if print_verbose:
    print '[rx_processor] Processing stream'
  
  if pre_headers == [] or post_headers == []:
    print '[rx_processor] Warning: empty headers'

  if message == []:
    print '[rx_processor] Empty message detected.'
    return

  print '[rx_processor] Message length: ' + str(len(message))

  #look for headers in message

  #TODO this works ok for variable length headers, but look into trying each
  #header while iterating through so only have to iterate once.
  for pre_header, post_header in zip(pre_headers, post_headers):
    if print_verbose:
      print '[rx_processor] Looking for:', pre_header, post_header
    
    start_i = 0
    end_i = 0

    #TODO might be better to process stream 8 times, then search for headers in
    #the 8 bytestreams
    for i in range(0, len(message) - 8 * len(pre_header)):
      n = ''
      #read string of characters of length of header
      for j in range(len(pre_header)):
        n += read_byte(message, i + j * 8, 'c')

      #found start header
      if n == pre_header:
        start_i = i + len(pre_header) * 8
        if print_verbose:
          print '--[TRANSMISSION START FOUND]-[' + pre_header + ']-[' + str(i) + ']'
      
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
        
        if print_verbose:
          print '  ' + n
          print '--[TRANSMISSION END FOUND  ]-[' + post_header + ']-[' + str(i) + ']'
        
        
        #verify checksum
        actual_checksum = 0
        for byte in n:
          actual_checksum += ord(byte)
        actual_checksum = actual_checksum % 256

        if print_verbose:
          print '  Message_Checksum: ' + str(checksum)
          print '  Actual_checksum:  ' + str(actual_checksum)
        if checksum == actual_checksum:
          if print_verbose:
            print '  Checksum valid'
          l.append(n)
        else:
          if print_verbose:
            print '  Checksum invalid'

        if print_verbose:
          print ''

  return l

'''[read_byte]-----------------------------------------------------------------
  Read byte from bitstream and return the int or char representation

  stream    - stream to read from
  start_ind - start index of byte
  type      - 'i' for int, 'c' for char
  return    - either int or char representation of byte in bitstream
----------------------------------------------------------------------------'''
def read_byte(stream, start_ind, type='i'):
  value = int(''.join(str(x) for x in stream[start_ind:start_ind+8]), 2)

  if type == 'i':
    return value

  if type == 'c':
    return chr(value)