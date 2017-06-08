'''*-----------------------------------------------------------------------*---
                                                          Author: Jason Ma
                                                          Date  : May 22 2017

    File Name  : bladeRF_top_level.py
    Description: Allows for either transmitting or receiving data using the
                 appropriate GNURadio modules and a BladeRF board. 
                 
                          bladeRF_top_level
                         /        |        \
                 gr_thread     scanner     rx_processor
                   /       \      |      /
                 BladeRF      _out.bin
                              _send.bin

                 bladeRF_top_level initializes all the other threads:
                   - gr_thread
                   - scanner
                   - rx_processor

                 - gr_thread interfaces with GNURadio to open the BladeRF and
                 do whatever GNURadio wants to do with it.

                 - scanner has peak detection and RSSI measuring capability.

                 - rx_processor processes the data received, including the
                 bitstream containing communication data, GPS, and anything
                 else being collected.

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

'''[Actual script]----------------------------------------------------------'''
def main():

  global center_freq

  try:
    #loads fpga
    sdr = blade_rx.blade_rf_sdr(1)

    #get list of best frequencies
    if scan_best_freqs:
      best_freqs = bladeRF_scanner.main()

      #take lowest interference frequency and set it to center_freq for now
      center_freq = best_freqs[0]

    gr = gnuradio_interface.gr_thread(center_freq, baud_rate)
    scanner = bladeRF_scanner.bladeRF_scanner()

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
