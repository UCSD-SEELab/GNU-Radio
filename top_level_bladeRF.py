'''*-----------------------------------------------------------------------*---
                                                          Author: Jason Ma
                                                          Date  : May 22 2017

    File Name  : top_level_bladeRF.py
    Description: Used for either transmitting or receiving data using the
                 appropriate GNURadio modules and a BladeRF board. 
                 
             .-------------top_level_bladeRF-----------.
            /     /           |             \           \
rx_processor   scanner   blade_rx   gnuradio_interface  .--------------------.
                                             |          | Additional Sensors |
                      .--------------------------.      |                    |
                      | GNURadio Generated Files |      | hardware           |
                      |                          |      |____________________|
                      | ofdm_transmitter         |         
                      | ofdm_receiver            |
                      |__________________________| 

- top_level_bladeRF loads the FPGA onto the BladeRF using blade_rx. It then 
  starts and maintains all the other threads:
  - gnuradio_interface
  - rx_processor
  - scanner
  - hardware
  It allows for smooth handling of exits (including Ctrl+C).

- gnuradio_interface calls rx or tx GNURadio schemes depending on configuration
  to either receive or transmit data using whatever modulation scheme has been
  implemented. The idea behind this file is to make it modular, being capable of 
  calling any gnuradio generated files that write to the appropriate file and 
  implement the main call.

- rx_processor processes the data received, capable of accessing the bitstream 
  containing communication data, GPS, and anything else being collected. This 
  can be set to work on old or new data.

- scanner has peak detection and RSSI measuring capability.

- hardware interfaces with the air quality sensor, modified slightly from 
  Michael / Christine's code to work with top level's callbacks
---*-----------------------------------------------------------------------*'''

import blade_rx
#import bladeRF_scanner
import gnuradio_interface

#import socket
import sys
from time import time, sleep

'''----------------------------------------------------------------------------
Config variables

GLOBAL PARAM CONFIG:
- Command line overwrites all
- Config file overwrites file defaults
- File defaults (specified here) in case config file/cmdline args not available
----------------------------------------------------------------------------'''
config_file = 'io/config.cfg'

class config():
  def __init__(self):
    #[DEFAULT CONFIG] Changing these will likely NOT change behavior.
    #                 Please change config file or specify command line args
    #top_level_bladeRF config
    self.run_time = 10000

    self.center_freq = 433.92 * 1000000
    self.bandwidth   = 1.5 * 1000000
    self.baud_rate   = 50000 #TODO currently NOT being used by gnuradio_interface effectively

    self.lnagain = 6
    self.rxvga1 = 30
    self.rxvga2 = 30

    #commands to send bladerf
    self.commands = ['cal lms', 'xb 300 enable', 'xb 300 lna on']

    #gnuradio_interface parameters
    self.tx = False
    self.rx = True
    self.tx_time = 10000
    self.rx_time = 10000

    self.udp_rx_ip = "127.0.0.1"
    self.udp_rx_port = 9002

    self.udp_tx_ip = "127.0.0.1"
    self.udp_tx_port = 9000
    self.udp_repeat = 5

    #rx_processor parameters
    self.rx_process = False
    self.gps_tagging = False
    self.pre_headers = ['SL1', 'SL2', 'SL3']
    self.post_headers = ['EL4', 'EL5', 'EL6']
    self.in_file  = 'io/_out'

    #scanner parameters
    self.scan = False
    self.scan_best_freqs = False
    self.section_bw = 50000
    self.fft_size = 4096
    self.fft_file = 'io/log_power_fft_data.bin'

    #hardware parameters
    self.air_sensor = False

  def load_config(self, config_file):
    self.options = {}

    with open(config_file, 'r') as f:
      for line in f:

        if len(line.strip()) > 0 and line.strip()[0] == '#':
          continue

        line = line.split(' ')

        #only set options for lines where there are exactly 2 arguments, key val
        if len(line) >= 2:
          line[0] = line[0].lower()
          self.options[line[0]] = line[1].strip()
        elif len(line) > 0 and line[0] != '\n':
          print("[main] [warn] Invalid config param found:", line)

  def parse_config(self):
    if not self.options:
      print("[main] Config not loaded.")
      return

    if self.options['run_time']: self.run_time = int(self.options['run_time'])
    if self.options['center_freq']: self.center_freq = int(self.options['center_freq'])
    if self.options['bandwidth']: self.bandwidth = int(self.options['bandwidth'])
    if self.options['baud_rate']: self.baud_rate = int(self.options['baud_rate'])

    if self.options['tx']: self.tx = self.options['tx'] == 'True'
    if self.options['rx']: self.rx = self.options['rx'] == 'True'
    if self.options['tx_time']: self.tx_time = int(self.options['tx_time'])
    if self.options['rx_time']: self.rx_time = int(self.options['rx_time'])
    if self.options['lnagain']: self.lnagain = int(self.options['lnagain'])
    if self.options['rxvga1']: self.rxvga1 = int(self.options['rxvga1'])
    if self.options['rxvga2']: self.rxvga2 = int(self.options['rxvga2'])

    if self.options['udp_rx_ip']: self.udp_rx_ip = self.options['udp_rx_ip']
    if self.options['udp_tx_ip']: self.udp_tx_ip = self.options['udp_tx_ip']
    if self.options['udp_rx_port']: self.udp_rx_port = int(self.options['udp_rx_port'])
    if self.options['udp_tx_port']: self.udp_tx_port = int(self.options['udp_tx_port'])
    if self.options['udp_repeat']: self.udp_repeat = int(self.options['udp_repeat'])

    if self.options['rx_process']: self.rx_process = self.options['rx_process'] == 'True'
    if self.options['gps_tagging']: self.gps_tagging = self.options['gps_tagging'] == 'True'
    if self.options['in_file']: self.in_file = self.options['in_file']

    if self.options['scan']: self.scan = self.options['scan'] == 'True'
    if self.options['scan_best_freqs']: self.scan_best_freqs = self.options['scan_best_freqs'] == 'True'
    if self.options['section_bw']: self.section_bw = int(self.options['section_bw'])
    if self.options['fft_size']: self.fft_size = int(self.options['fft_size'])
    if self.options['fft_file']: self.fft_file = self.options['fft_file']

'''----------------------------------------------------------------------------
Conditional imports and settings
----------------------------------------------------------------------------'''

'''[parse_args]----------------------------------------------------------------
  Validates command line args, then sets parameters as appropriate
----------------------------------------------------------------------------'''
def parse_args(argv, cfg, required=False):
  if len(sys.argv) < 3:
    if required:
      print("[main] Usage: python top_level_bladeRF [f | tx | rx | rxnp | p | m] <freq MHz>\n \
            \tf    - full duplex (both tx and rx)\n \
            \ttx   - transmit new samples\n \
            \trx   - receive new samples\n \
            \trxnp - receive, but do not process samples\n \
            \tp    - process pre-received samples from in_file\n \
            \tm    - manual selection\n \
            \tfreq - frequency to start at")
      sys.exit(1)
    else:
      if cfg.center_freq < 300000000 or cfg.center_freq > 3800000000:
        print("[main] Frequency cannot be < 300MHz or > 3.8GHz")
        sys.exit(1)
      return

  if sys.argv[1] == 'f': #full duplex
    print '[main] Mode:\tFull Duplex'
    cfg.tx = True
    cfg.rx = True
    cfg.rx_process = True
  elif sys.argv[1] == 'tx': #tx only
    print '[main] Mode:\tTX'
    cfg.tx = True
    cfg.rx = False
    cfg.rx_process = False
  elif sys.argv[1] == 'rx': #rx only
    print '[main] Mode:\tRX'
    cfg.tx = False
    cfg.rx = True
    cfg.rx_process = True
  elif sys.argv[1] == 'rxnp': #rx samples without processing
    print '[main] Mode:\tRX without processing'
    cfg.tx = False
    cfg.rx = True
    cfg.rx_process = False
  elif sys.argv[1] == 'p': #process only
    print '[main] Mode:\tProcessing only'
    cfg.tx = False
    cfg.rx = False
    cfg.rx_process = True
  elif sys.argv[1] == 'm': #manual mode
    print '[main] Mode:\tManual'
  else: #invalid input
    print("[main] Usage: python top_level_bladeRF [f | tx | rx | rxnp | p | m] <freq>\n \
          \tf    - full duplex (both tx and rx)\n \
          \ttx   - transmit new samples\n \
          \trx   - receive new samples\n \
          \trxnp - receive, but do not process samples\n \
          \tp    - process pre-received samples from in_file\n \
          \tm    - manual selection\n \
          \tfreq - frequency to start at")
    sys.exit(1)

  cfg.center_freq = float(sys.argv[2]) * 1000000

  if cfg.center_freq < 300 or cfg.center_freq > 3800:
    print("[main] Frequency cannot be < 300MHz or > 3.8GHz")
    sys.exit(1)

'''[end_all_threads]-----------------------------------------------------------
  Sends an end_callback to all threads in thread list
----------------------------------------------------------------------------'''
def end_all_threads(threads):
  print '[main] Ending program.'

  for thread in threads:
    thread.end_callback()

  sys.exit(1)

'''[main]----------------------------------------------------------------------
  Initializes gnuradio_interface and bladeRF_scanner threads, which handle
  data collection and processing independently.
----------------------------------------------------------------------------'''
def main():

  try:
    #initialize config
    cfg = config()

    #override default config using config file
    cfg.load_config(config_file)
    cfg.parse_config()

    #override config file params with command line args
    parse_args(sys.argv, cfg)

    #conditional imports
    if cfg.air_sensor:
      import hardware

    if cfg.rx_process:
      import rx_processor

    if cfg.scan:
      import bladeRF_scanner

    #init threads
    print '[main] Tx:\t' + str(cfg.tx)
    print '[main] Rx:\t' + str(cfg.rx)
    print '[main] Rx_proc:\t' + str(cfg.rx_process)
    print '[main] Scanner:\t' + str(cfg.scan)
    print '[main] Aq_sen:\t' + str(cfg.air_sensor)
    print
    print '[main] Freq:\t' + str(cfg.center_freq / 1000000.0) + '\tMHz'
    print '[main] Bw:\t' + str(cfg.bandwidth / 1000000.0) + '\tMHz'

    threads = []
    filewrite_subscribers = []

    #loads fpga
    if cfg.tx or cfg.rx:
      print '[main] Initializing bladeRF'
      sdr = blade_rx.blade_rf_sdr(1)
      sdr.set_amplifier_gain(['lnagain', 'rxvga1', 'rxvga2'], [cfg.lnagain, cfg.rxvga1, cfg.rxvga2])
      
      for command in cfg.commands:
        sdr.send_exec(command)
        print '[main] Sending command:', command

      '''
      sdr.send_exec('cal lms')
      sdr.send_exec('xb 300 enable')
      sdr.send_exec('xb 300 lna on')
      '''

      print '[main] Init GNURadio interface'
      gr = gnuradio_interface.gr_thread(
        cfg.tx, 
        cfg.rx, 
        cfg.tx_time, 
        cfg.rx_time, 
        cfg.center_freq, 
        cfg.bandwidth, 
        cfg.baud_rate,
        cfg.udp_tx_ip,
        cfg.udp_tx_port,
        cfg.udp_rx_ip,
        cfg.udp_rx_port)
    
    if cfg.scan:
      print '[main] Init scanner'
      scanner = bladeRF_scanner.bladeRF_scanner(
        cfg.fft_file, 
        cfg.center_freq,
        cfg.bandwidth, 
        cfg.section_bw, 
        cfg.fft_size
      )

    if cfg.rx_process:
      print '[main] Init rx processor'
      rx_p = rx_processor.rx_processor(
        cfg.in_file, 
        cfg.pre_headers, 
        cfg.post_headers, 
        cfg.rx, 
        cfg.gps_tagging
      )

    if cfg.air_sensor:
      print '[main] Init hardware'
      air_q_s = hardware.AirSensor()

    #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #get list of best frequencies if necessary
    if cfg.scan_best_freqs:
      #best_freqs = bladeRF_scanner.main()
      #TODO need to fix above line, main is deprecated
      best_freqs = scanner.select_usable_by_section()

      #take lowest interference frequency and set it to center_freq for now
      center_freq = best_freqs[0]

      #do something with it

    # Start gnuradio interface if necessary
    if cfg.tx or cfg.rx:
      gr.start()
      threads.append(gr)

    # Start scanner if necessary
    if cfg.scan:
      scanner.start()
      threads.append(scanner)
      filewrite_subscribers.append(scanner)

    # Start rx processor if necessary
    if cfg.rx_process:
      rx_p.start()
      threads.append(rx_p)
      filewrite_subscribers.append(rx_p)

    # Start air sensor if necessary
    #if air_sensor:
    #  air_q_s.start()
    #  threads.append(air_q_s)
    #  filewrite_subscribers.append(air_q_s)

    # Initialize tx socket if transmitting

    start_time = time()
    wait_start = start_time
    while time() - start_time < cfg.run_time:

      wait_start += 1
      #make thread sleep until time to sync threads
      while(time() - wait_start < 1):
        sleep(0.1)

      print '\n[main] sync'
      
      if cfg.tx:
        message = "[main] hi!"
        print '[main] Tx message:' + message + ' | Repeat:' + str(cfg.udp_repeat)
        #for i in range(udp_repeat):
        #  sock.sendto(message, (udp_tx_ip, udp_tx_port))
      
      for thread in filewrite_subscribers:
        thread.filewrite_callback()
      
  except KeyboardInterrupt:
    print '\n[main] Ctrl+c received.'
    end_all_threads(threads)

  print '\n[main] Time reached.'
  end_all_threads()

if __name__ == '__main__':
  main()
