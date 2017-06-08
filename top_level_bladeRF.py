'''*-----------------------------------------------------------------------*---
                                                          Author: Jason Ma
                                                          Date  : May 22 2017

    File Name  : top_level_bladeRF.py
    Description: Allows for either transmitting or receiving data using the
                 appropriate GNURadio modules and a BladeRF board. 
                 
                          top_level_bladeRF
                         /                 \
                    scanner                 gnuradio_interface 
                   /                       /        |         \
                 BladeRF         rx_2400_r2      tx_2400_r2    rx_processor

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

                 A good portion of this was inspired by and builds on Stephen 
                 Wayne's FSK GNURadio modules.
---*-----------------------------------------------------------------------*'''

import bladeRF_scanner
import blade_rx
import gnuradio_interface
import sys

'''----------------------------------------------------------------------------
Config variables
----------------------------------------------------------------------------'''
scan_best_freqs = False

center_freq = 433920000
bandwidth   = 1500000
baud_rate   = 2500

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

    #get list of best frequencies
    if scan_best_freqs:
      #best_freqs = bladeRF_scanner.main()
      #TODO need to fix above line, main is deprecated
      best_freqs = scanner.select_usable_by_section(center_freq, bandwidth)

      #take lowest interference frequency and set it to center_freq for now
      center_freq = best_freqs[0]

    gr.start()
    scanner.start()

    gr.join(1000)
  except KeyboardInterrupt:
    print '\n[main] Ctrl+c received. Shutting down program'
    gr.end_callback()
    scanner.end_callback()
    sys.exit(1)

if __name__ == '__main__':
  main()
