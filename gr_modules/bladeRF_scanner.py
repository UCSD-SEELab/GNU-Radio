'''*-----------------------------------------------------------------------*---
                                                          Author: Jason Ma
                                                          Date  : May 21 2017
    File Name  : bladeRF_scanner.py
    Description: Contains scanner utilities usable with GNURadio generated bin
                 files containing bladeRF FFT data.

                 detect_peaks - find most significant peaks in FFT
                 select_usable_by_section - find usable bands to communicate on
---*-----------------------------------------------------------------------*'''

import struct
import threading
import time

'''----------------------------------------------------------------------------
Config variables
----------------------------------------------------------------------------'''
max_usable   = 50

class bladeRF_scanner(threading.Thread):

  '''[__init__]----------------------------------------------------------------
    Initializes bladeRF_scanner with appropriate center frequency and bandwidth

    cen_freq - frequency that is being scanned
    bw       - bandwidth of scanner
  --------------------------------------------------------------------------'''
  def __init__(self, fft_filename, cen_freq, bw, section_bw, fft_size):
    super(bladeRF_scanner, self).__init__()
    self.daemon = True
    self.callback = False
    self.filewrite = False
    self.fft_filename = fft_filename
    self.cen_freq = cen_freq
    self.bw = bw
    self.section_bw = section_bw
    self.fft_size = fft_size

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

    max_peaks  - max amount of peaks to return
    pos        - position to start at in file
    return     - vector containing peaks of the data
  --------------------------------------------------------------------------'''
  def detect_peaks(self, max_peaks, pos):
    
    #f = scipy.fromfile(open(self.filename), dtype=scipy.float32)
    
    f = []
    with open(self.fft_filename, 'rb') as file:
      file.seek(pos)
      flt = file.read(4)
      while flt:
        f.append(struct.unpack('f', flt)[0])
        flt = file.read(4)
        #f.append(struct.unpack('f' * (len(line) / 4), line)[0])

      new_pos = file.tell()

    print len(f)

    peak_counts = [0] * self.fft_size

    #iterate one fft at a time and find peaks
    for i in range(len(f) / self.fft_size):
      sub_f = f[i * self.fft_size : (i + 1) * self.fft_size]
      
      #calc average db as a general cutoff
      total_db = 0
      for j in range(self.fft_size):
        total_db += sub_f[j]

      avg_db = total_db / self.fft_size

      #print avg_db

      #find peaks
      peaks = []
      for j in range(self.fft_size):
        if sub_f[j] > avg_db:
          #find local max
          #TODO could look more like 10-50 points on either side
          while j + 1 < self.fft_size and sub_f[j + 1] > sub_f[j]:
            j += 1

          while j - 1 >= 0 and sub_f[j - 1] > sub_f[j]:
            j -= 1


          #prevent duplicates, DC spike from getting added
          #if (sub_f[j], j) not in peaks and j != 0 and j != self.fft_size - 1:

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
    for i in range(self.fft_size):
      total_count += peak_counts[i]

    avg_count = total_count / self.fft_size

    #find all frequencies where peak counts exceeded average
    all_peaks = []
    for i in range(self.fft_size):
      if peak_counts[i] > avg_count:
        all_peaks.append(i)

    #print all_peaks
    #print len(all_peaks)

    #add all these frequencies
    peak_freqs = []
    for i in range(self.fft_size):
      if i in all_peaks:
        peak_freqs.append(self.cen_freq - (self.bw / 2) + (self.bw * i / self.fft_size))

    #for i in range(self.fft_size):
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
    with open(self.fft_filename, 'rb') as f:
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
  def RSSI(self, fft):
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
  def select_usable_by_section(self):
    #f = scipy.fromfile(open(filename), dtype=scipy.float32)
      
    f = []
    with open(self.fft_filename, 'rb') as file:
      flt = file.read(4)
      while flt:
        f.append(struct.unpack('f', flt)[0])
        flt = file.read(4)
        #f.append(struct.unpack('f' * (len(line) / 4), line)[0])

    #print f
    
    section_counts = []

    for i in range(self.bw / self.section_bw):
      section_counts.append(0)

    #iterate one fft at a time and find max power on each section
    for i in range(len(f) / self.fft_size):
      sub_f = f[i * self.fft_size : (i + 1) * self.fft_size]
      
      #iterate through each section
      for j in range(len(section_counts)):
        section_max = -1000000

        #iterate through all fft points that correspond to section, find max
        for k in range(j * self.fft_size / len(section_counts), (j + 1) * self.fft_size / len(section_counts)):
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
        usable_pairs.append((section_counts[i], self.cen_freq - (self.bw / 2) + i * self.section_bw))

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
    print '[scanner] Initialized'

    curr_file_pos = 0
    with open('rssi_data', 'w+') as f:
      while True:

        if self.callback:
          break

        while not self.filewrite:
          time.sleep(0.1)

        self.filewrite = False

        fft, curr_file_pos = self.scanner_spin(curr_file_pos)
        rssi = self.RSSI(fft)
        print '[scanner] RSSI: ' + str(rssi) + '\tFreq: ' + str(self.cen_freq)
        f.write(str(rssi) + '\n')

        #self.select_usable_by_section()
        #self.detect_peaks(50, curr_file_pos)

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
  
