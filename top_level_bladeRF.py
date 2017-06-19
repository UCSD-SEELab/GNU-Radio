'''*-----------------------------------------------------------------------*---
                                                          Author: Jason Ma
                                                          Date  : May 22 2017

    File Name  : top_level_bladeRF.py
    Description: Allows for either transmitting or receiving data using the
                 appropriate GNURadio modules and a BladeRF board. 
                 
                 .-------------top_level_bladeRF-----------.
                /     /           |             \           \
    rx_processor   scanner   blade_rx   gnuradio_interface   hardware
                                       /                  \         
                             rx_2400_r2                    tx_2400_r2  

                 - top_level_bladeRF initializes all the other threads:
                   - gnuradio_interface
                     - rx_processor
                   - scanner
                   It allows for smooth exiting so nothing gets locked up.

                 - gnuradio_interface calls either rx_2400_r2 or tx_2400_r2
                   depending on configuration to either receive or transmit
                   data using FSK modulation. It also starts a rx_processor
                   thread to process either old or live data.

                 - rx_processor processes the data received, including the
                   bitstream containing communication data, GPS, and anything
                   else being collected. This can be set to work on old or new
                   data.

                 - scanner has peak detection and RSSI measuring capability.

                 - hardware interfaces with the air quality sensor, modified 
                   slightly from Michael / Christine's code to work with top 
                   level's callbacks

                 A good portion of this was inspired by and builds on Stephen 
                 Wayne's FSK GNURadio modules.
---*-----------------------------------------------------------------------*'''

import blade_rx
import bladeRF_scanner
import gnuradio_interface

import sys
import time

'''----------------------------------------------------------------------------
Config variables
----------------------------------------------------------------------------'''
scan_best_freqs = False
run_time =10000

center_freq = 433920000
bandwidth   = 1500000
baud_rate   = 2500

#receive variables
in_file  = '_out.bin'
fft_file = 'log_power_fft_data.bin'
rx_process = True
rx_new     = True
print_received_transmissions = True
air_sensor = False

pre_headers = ['SL1', 'SL2', 'SL3']
post_headers = ['ED1', 'ED2', 'ED3']


'''----------------------------------------------------------------------------
Conditional imports
----------------------------------------------------------------------------'''

if air_sensor:
  import hardware

if rx_process:
  import rx_processor

'''[main]----------------------------------------------------------------------
  Initializes gnuradio_interface and bladeRF_scanner threads, which handle
  data collection and processing independently.
----------------------------------------------------------------------------'''
def main():

  global center_freq

  try:
    #loads fpga
    sdr = blade_rx.blade_rf_sdr(1)

    gr = gnuradio_interface.gr_thread(center_freq, baud_rate)

    scanner = bladeRF_scanner.bladeRF_scanner()

    if rx_process:
      rx_p = rx_processor.rx_processor(pre_headers, post_headers)

    if air_sensor:
      air_q_s = hardware.AirSensor()

    #get list of best frequencies
    if scan_best_freqs:
      #best_freqs = bladeRF_scanner.main()
      #TODO need to fix above line, main is deprecated
      best_freqs = scanner.select_usable_by_section(center_freq, bandwidth)

      #take lowest interference frequency and set it to center_freq for now
      center_freq = best_freqs[0]

      #do something with it

    gr.start()
    scanner.start()

    if rx_process:
      rx_p.start()

    #if air_sensor:
    #  air_q_s.start()

    start_time = time.time()
    while time.time() - start_time < run_time:

      wait_start = time.time()
      while(time.time() - wait_start < 1):
        time.sleep(0.1)

      print '\n[main] sending filewrite sync'
      scanner.filewrite_callback()

      if rx_process:
        rx_p.filewrite_callback()

      if air_sensor:
        air_q_s.filewrite_callback()

  except KeyboardInterrupt:
    print '\n[main] Ctrl+c received. Ending program'
    gr.end_callback()
    scanner.end_callback()

    if rx_process:
      rx_p.end_callback()

    if air_sensor:
      air_q_s.end_callback()
    sys.exit(1)

  print '[main] Time reached. Ending program'
  gr.end_callback()
  scanner.end_callback()

  if rx_process:
    rx_p.end_callback()

  if air_sensor:
      air_q_s.end_callback()

  sys.exit(1)

if __name__ == '__main__':
  main()
