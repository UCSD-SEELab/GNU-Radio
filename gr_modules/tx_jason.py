#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Tx Jason
# Generated: Thu Oct 26 16:10:07 2017
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import time


class tx_jason(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Tx Jason")

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 8
        self.samp_rate_tx = samp_rate_tx = 4000000
        self.samp_rate = samp_rate = 1
        self.freq = freq = 440000000
        self.baud_rate = baud_rate = 500000

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=samp_rate_tx,
                decimation=samp_rate,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + 'bladerf=0' )
        self.osmosdr_sink_0.set_sample_rate(samp_rate_tx)
        self.osmosdr_sink_0.set_center_freq(freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(0, 0)
        self.osmosdr_sink_0.set_if_gain(10, 0)
        self.osmosdr_sink_0.set_bb_gain(10, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(1500000, 0)

        self.digital_gfsk_mod_0 = digital.gfsk_mod(
        	samples_per_symbol=sps,
        	sensitivity=1.0,
        	bt=1,
        	verbose=False,
        	log=False,
        )
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, 'C:\\Projects\\gr-bladerf-utils\\io\\_send.bin', True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.digital_gfsk_mod_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.osmosdr_sink_0, 0))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate_tx(self):
        return self.samp_rate_tx

    def set_samp_rate_tx(self, samp_rate_tx):
        self.samp_rate_tx = samp_rate_tx
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate_tx)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_sink_0.set_center_freq(self.freq, 0)

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate


def main(top_block_cls=tx_jason, options=None, tx_time=1000, freq=None, fn=None):

    tb = top_block_cls(center_freq=options.center_freq, filename=options.filename)
    
    filenames = []
    filenames.append('io/_send1.bin')
    filenames.append('io/_send2.bin')
    filenames.append('io/_send3.bin')

    freq1 = 433920000
    freq2 = 915000000
    freq3 = 2450000000

    while True:

        print '[tx] File: ' + filenames[0] + ' Freq: ' + str(tb.get_center_freq())
        #tb.set_filepath(filenames[0])
        #tb.set_center_freq(freq1)

        tb.start()
        start_time = time.time()

        while (time.time() - start_time < tx_time):
            time.sleep(0.1)

        tb.stop()
        tb.wait()


if __name__ == '__main__':
    main()
