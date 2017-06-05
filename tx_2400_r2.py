#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Tx 2400 R2
# Generated: Mon Jun  5 16:26:30 2017
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


class tx_2400_r2(gr.top_block):

    def __init__(self, center_freq=433920000):
        gr.top_block.__init__(self, "Tx 2400 R2")

        ##################################################
        # Parameters
        ##################################################
        self.center_freq = center_freq

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 10
        self.baud_rate = baud_rate = 2500
        self.txvga2 = txvga2 = 25
        self.txvga1 = txvga1 = -4
        self.samp_rate_tx = samp_rate_tx = 400000
        self.samp_rate_rx = samp_rate_rx = 1000000
        self.samp_rate = samp_rate = int(baud_rate * sps)
        self.freq = freq = 433920000
        self.filename_tx = filename_tx = '_send.bin'

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
        self.osmosdr_sink_0.set_gain(txvga2, 0)
        self.osmosdr_sink_0.set_if_gain(0, 0)
        self.osmosdr_sink_0.set_bb_gain(txvga1, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(1500000, 0)

        self.digital_gfsk_mod_0 = digital.gfsk_mod(
            samples_per_symbol=sps,
            sensitivity=1.0,
            bt=1,
            verbose=False,
            log=False,
        )
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '_send.bin', False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.digital_gfsk_mod_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.osmosdr_sink_0, 0))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_samp_rate(int(self.baud_rate * self.sps))

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        self.set_samp_rate(int(self.baud_rate * self.sps))

    def get_txvga2(self):
        return self.txvga2

    def set_txvga2(self, txvga2):
        self.txvga2 = txvga2
        self.osmosdr_sink_0.set_gain(self.txvga2, 0)

    def get_txvga1(self):
        return self.txvga1

    def set_txvga1(self, txvga1):
        self.txvga1 = txvga1
        self.osmosdr_sink_0.set_bb_gain(self.txvga1, 0)

    def get_samp_rate_tx(self):
        return self.samp_rate_tx

    def set_samp_rate_tx(self, samp_rate_tx):
        self.samp_rate_tx = samp_rate_tx
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate_tx)

    def get_samp_rate_rx(self):
        return self.samp_rate_rx

    def set_samp_rate_rx(self, samp_rate_rx):
        self.samp_rate_rx = samp_rate_rx

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_sink_0.set_center_freq(self.freq, 0)

    def get_filename_tx(self):
        return self.filename_tx

    def set_filename_tx(self, filename_tx):
        self.filename_tx = filename_tx


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-f", "--center-freq", dest="center_freq", type="intx", default=433920000,
        help="Set center_freq [default=%default]")
    return parser


def main(top_block_cls=tx_2400_r2, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(center_freq=options.center_freq)

    while True:
        print '[tx] Transmitting message'
        tb.start()
        
        wait_start = time.time()
        while(time.time() - wait_start < 0.25):
            time.sleep(0.01)
    
        tb.stop()
        tb.wait()

if __name__ == '__main__':
    main()
