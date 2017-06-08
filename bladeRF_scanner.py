'''*-----------------------------------------------------------------------*---
                                                          Author: Jason Ma
                                                          Date  : May 21 2017
    File Name  : bladeRF_scanner.py
    Description: Contains scanner utilities usable with GNURadio generated bin
                 files containing bladeRF FFT data.

                 detect_peaks - find most significant peaks in FFT
                 select_usable_by_section - find usable bands to communicate on
---*-----------------------------------------------------------------------*'''

import rx_2400_r2

import struct
import threading
import time

'''----------------------------------------------------------------------------
Config variables
----------------------------------------------------------------------------'''
center_freq  = 433920000
bandwidth    = 1500000
section_bw   = 50000
max_usable   = 50
fft_size     = 1024
fft_filename = 'log_power_fft_data.bin'

class bladeRF_scanner(threading.Thread):

  '''[__init__]----------------------------------------------------------------
    Initializes bladeRF_scanner with appropriate center frequency and bandwidth

    cen_freq - frequency that is being scanned
    bw       - bandwidth of scanner
  --------------------------------------------------------------------------'''
  def __init__(self, cen_freq=center_freq, bw=bandwidth):
    super(bladeRF_scanner, self).__init__()
    self.cen_freq = cen_freq
    self.bw = bw
    self.daemon = True
    self.callback = False
    self.filewrite = False

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
    print '[scanner] Callback received. Shutting down.'

  '''[detect_peaks]------------------------------------------------------------
    Finds peaks within fft_windows, including the DC spike of the antenna.

    cen_freq   - center frequency
    bw         - bandwidth
    section_bw - width of each section
    max_peaks  - max amount of peaks to return
    fft_size   - number of data points in each FFT window
    filename   - file containing the FFT data
    pos        - position to start at in file
    return     - vector containing peaks of the data
  --------------------------------------------------------------------------'''
  def detect_peaks(self, cen_freq, bw, max_peaks, fft_size, filename, pos):
    
    #f = scipy.fromfile(open(filename), dtype=scipy.float32)
    
    f = []
    with open(filename, 'rb') as file:
      file.seek(pos)
      flt = file.read(4)
      while flt:
        f.append(struct.unpack('f', flt)[0])
        flt = file.read(4)
        #f.append(struct.unpack('f' * (len(line) / 4), line)[0])

      new_pos = file.tell()

    print len(f)

    peak_counts = [0] * fft_size

    #iterate one fft at a time and find peaks
    for i in range(len(f) / fft_size):
      sub_f = f[i * fft_size : (i + 1) * fft_size]
      
      #calc average db as a general cutoff
      total_db = 0
      for j in range(fft_size):
        total_db += sub_f[j]

      avg_db = total_db / fft_size

      #print avg_db

      #find peaks
      peaks = []
      for j in range(fft_size):
        if sub_f[j] > avg_db:
          #find local max
          #TODO could look more like 10-50 points on either side
          while j + 1 < fft_size and sub_f[j + 1] > sub_f[j]:
            j += 1

          while j - 1 >= 0 and sub_f[j - 1] > sub_f[j]:
            j -= 1


          #prevent duplicates, DC spike from getting added
          #if (sub_f[j], j) not in peaks and j != 0 and j != fft_size - 1:

          #prevent duplicates, keep DC spike
          if (sub_f[j], j) not in peaks:
            peaks.append((sub_f[j], j))
      
      #remove smaller peaks until top few remain
      while len(peaks) > max_peaks:
        peaks.remove(min(peaks))
      
      #add to count of this peak in overall peaks
      for peak in peaks:
        peak_counts[peak[1]] += 1
    
    #find average overall peak counts
    total_count = 0
    for i in range(fft_size):
      total_count += peak_counts[i]

    avg_count = total_count / fft_size

    #find all frequencies where peak counts exceeded average
    all_peaks = []
    for i in range(fft_size):
      if peak_counts[i] > avg_count:
        all_peaks.append(i)

    #print all_peaks
    #print len(all_peaks)

    #add all these frequencies
    peak_freqs = []
    for i in range(fft_size):
      if i in all_peaks:
        peak_freqs.append(cen_freq - (bw / 2) + (bw * i / fft_size))

    #for i in range(fft_size):
      #print peak_counts[i]

    #print peak_freqs

    return peak_freqs, new_pos


  '''[scanner_spin]------------------------------------------------------------
    Reads in latest data from file

    pos    - position to begin reading from
    return - position at current end of file
  --------------------------------------------------------------------------'''
  def scanner_spin(self, pos):
    fft = []
    with open(fft_filename, 'rb') as f:
      f.seek(pos)
      float_val = f.read(4)
      while float_val:
        fft.append(struct.unpack('f', float_val)[0])
        float_val = f.read(4)

      print '[scanner] Fft length: ' + str(len(fft))

      return fft, f.tell()


  '''[RSSI]--------------------------------------------------------------------
    Finds max value in fft data, then returns it in dB format.

    fft    - fft data
    return - max peak in fft

    TODO - cen_freq and bw are not needed, but might be interesting as a way
           of finding what freq the max peak is at, although it is almost 
           always cen_freq
  --------------------------------------------------------------------------'''
  def RSSI(self, cen_freq, bw, fft):
    max_val = -1000000
    for i in range(len(fft)):
      if fft[i] > max_val:
        max_val = fft[i]

    return max_val

  '''[select_usable_by_section]------------------------------------------------
    Finds most usable channels of specified section_bw

    cen_freq   - center frequency
    bw         - bandwidth
    section_bw - width of each section
    max_usable - max amount of usable frequencies to return
    fft_size   - number of data points in each FFT window
    filename   - file containing the FFT data
    return     - most usable frequencies in list, with max size max_usable
  --------------------------------------------------------------------------'''
  def select_usable_by_section(self, cen_freq, bw, section_bw=50000, max_usable=50, fft_size=2048, filename='log_power_fft_data.bin'):
    #f = scipy.fromfile(open(filename), dtype=scipy.float32)
      
    f = []
    with open(filename, 'rb') as file:
      flt = file.read(4)
      while flt:
        f.append(struct.unpack('f', flt)[0])
        flt = file.read(4)
        #f.append(struct.unpack('f' * (len(line) / 4), line)[0])

    #print f
    
    section_counts = []

    for i in range(bw / section_bw):
      section_counts.append(0)

    #iterate one fft at a time and find max power on each section
    for i in range(len(f) / fft_size):
      sub_f = f[i * fft_size : (i + 1) * fft_size]
      
      #iterate through each section
      for j in range(len(section_counts)):
        section_max = -1000000

        #iterate through all fft points that correspond to section, find max
        for k in range(j * fft_size / len(section_counts), (j + 1) * fft_size / len(section_counts)):
          if sub_f[k] > section_max:
            section_max = sub_f[k]
        
        #add max to section_counts for that section
        section_counts[j] += section_max
    
    #find avg section count
    total_count = 0
    for i in range(len(section_counts)):
      total_count += section_counts[i]
    avg_count = total_count / len(section_counts)

    #add all sections with better than average counts to usable freqs
    usable_pairs = []
    for i in range(len(section_counts)):
      if section_counts[i] < avg_count:
        usable_pairs.append((section_counts[i], cen_freq - (bw / 2) + i * section_bw))

    #sort the pairs by power and filter out the weakest frequencies
    usable_pairs = sorted(usable_pairs)[:max_usable]

    #extract usable_freqs from usable_pairs
    usable_freqs = [x[1] for x in usable_pairs]

    print usable_freqs
      
    return usable_freqs


  '''[run]---------------------------------------------------------------------
    Starts when thread is run
  --------------------------------------------------------------------------'''
  def run(self):
    print '[scanner] Thread running'

    curr_file_pos = 0
    with open('rssi_data', 'w+') as f:
      while True:

        if self.callback:
          break

        while not self.filewrite:
          time.sleep(0.1)

        self.filewrite = False

        fft, curr_file_pos = self.scanner_spin(curr_file_pos)
        rssi = self.RSSI(self.cen_freq, self.bw, fft)
        print '[scanner] RSSI: ' + str(rssi) + '\tFreq: ' + str(self.cen_freq)
        f.write(str(rssi) + '\n')

#TODO for reference only, delete when the reference to this from 
#     top_level_bladeRF.py is removed

#def main():
  #gather samples
  #bladeRF_fft.main()

  #select the best frequency by noise over time
  #return select_usable_by_section(center_freq, bandwidth, section_bw, max_usable, fft_size, fft_filename)

'''[Actual script]----------------------------------------------------------'''
#if __name__ == '__main__':
#  main()
  
