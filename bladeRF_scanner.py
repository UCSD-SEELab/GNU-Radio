'''*-----------------------------------------------------------------------*---
                                                          Author: Jason Ma
                                                          Date  : May 21 2017
    File Name  : bladeRF_scanner.py
    Description: Contains scanner utilities usable with GNURadio generated bin
                 files containing bladeRF FFT data.

                 detect_peaks - find most significant peaks in FFT
                 select_usable_by_section - find usable bands to communicate on
---*-----------------------------------------------------------------------*'''

#import scipy
import struct

import bladeRF_fft

'''----------------------------------------------------------------------------
Config variables
----------------------------------------------------------------------------'''
center_freq  = 855000000
bandwidth    = 6000000
section_bw   = 50000
max_usable   = 50
fft_size     = 2048
fft_filename = 'log_power_fft_data.bin'

'''[detect_peaks]--------------------------------------------------------------
  Finds peaks within fft_windows, including the DC spike of the antenna.

  cen_freq   - center frequency
  bw         - bandwidth
  section_bw - width of each section
  max_peaks  - max amount of peaks to return
  fft_size   - number of data points in each FFT window
  filename   - file containing the FFT data
  return     - vector containing peaks of the data
----------------------------------------------------------------------------'''
def detect_peaks(cen_freq, bw, max_peaks, fft_size, filename):
  f = scipy.fromfile(open(filename), dtype=scipy.float32)
  print len(f)

  peak_counts = []

  for i in range(fft_size):
    peak_counts.append(0)

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

  print all_peaks
  print len(all_peaks)

  #add all these frequencies
  peak_freqs = []
  for i in range(fft_size):
    if i in all_peaks:
      peak_freqs.append(cen_freq - (bw / 2) + (bw * i / fft_size))

  #for i in range(fft_size):
    #print peak_counts[i]

  print peak_freqs

  return peak_freqs

'''[select_usable_by_section]--------------------------------------------------
  Finds most usable channels of specified section_bw

  cen_freq   - center frequency
  bw         - bandwidth
  section_bw - width of each section
  max_usable - max amount of usable frequencies to return
  fft_size   - number of data points in each FFT window
  filename   - file containing the FFT data
----------------------------------------------------------------------------'''
def select_usable_by_section(cen_freq, bw, section_bw, max_usable, fft_size, filename):
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


'''[Actual script]----------------------------------------------------------'''

#gather samples
bladeRF_fft.main()

#select the best frequency by noise over time
select_usable_by_section(center_freq, bandwidth, section_bw, max_usable, fft_size, fft_filename)