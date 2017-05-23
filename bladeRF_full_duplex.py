'''*-----------------------------------------------------------------------*---
                                                          Author: Jason Ma
                                                          Date  : May 22 2017
    File Name  : bladeRF_full_duplex.py
    Description: Communication protocols for bladeRF to bladeRF communications
---*-----------------------------------------------------------------------*'''


'''----------------------------------------------------------------------------
Config variables
----------------------------------------------------------------------------'''
datarate_test_transmitting = True
center_freq = 430500000
bandwidth = 28000000

'''[init_comms]----------------------------------------------------------------
  Attempts to initialize communications with a drone using a certain id.
----------------------------------------------------------------------------'''
#def init_comms(my_id, their_id, best_freqs):
  #broadcast best frequencies for this drone and await response


'''[datarate_test_tx]----------------------------------------------------------
  Constantly send data over radio
----------------------------------------------------------------------------'''
def datarate_test_tx(cen_freq):
  print 'Transmitting on: ' + str(cen_freq)

  #broadcast device id as well as best frequencies

  #wait for an expected device to connect and broadcast

  #propose a frequency change to one of the best current freqs

  #receive acknowledge before changing frequency

  #receive acknowledgement of connection on new frequency

'''[datarate_test_rx]----------------------------------------------------------
  Attempt to receive data and measure datarate
----------------------------------------------------------------------------'''
def datarate_test_rx(cen_freq, bw):
  print 'Receiving on: ' + str(cen_freq)

  #broadcast device id as well as best frequencies

  #wait for proposal

  #accept if reasonable, otherwise reset process

  #broadcast acknowledgement of frequency change

  #change frequency

  #broadcast acknowledgement of connection on new frequency


'''[Actual script]----------------------------------------------------------'''

if(datarate_test_transmitting)
  datarate_test_tx(center_freq)
else
  datarate_test_rx(center_freq, bandwidth)