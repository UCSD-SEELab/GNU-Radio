#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Rx Jason
# Generated: Thu Oct 26 16:08:45 2017
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import math
import osmosdr
import time


class rx_jason(gr.top_block):

    def __init__(self, center_freq=440000000):
        gr.top_block.__init__(self, "Rx Jason")

        ##################################################
        # Parameters
        ##################################################
        self.center_freq = center_freq

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 10
        self.samp_rate = samp_rate = 4000000
        self.rx_vga_gain = rx_vga_gain = 35
        self.rx_lna_gain = rx_lna_gain = 6
        self.freq = freq = 440000000
        self.baud_rate = baud_rate = 500000
        self.bandwidth = bandwidth = 1500000

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0_0 = osmosdr.source( args="numchan=" + str(1) + " " + 'bladerf=0' )
        self.osmosdr_source_0_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0_0.set_center_freq(freq, 0)
        self.osmosdr_source_0_0.set_freq_corr(0, 0)
        self.osmosdr_source_0_0.set_dc_offset_mode(1, 0)
        self.osmosdr_source_0_0.set_iq_balance_mode(2, 0)
        self.osmosdr_source_0_0.set_gain_mode(False, 0)
        self.osmosdr_source_0_0.set_gain(0, 0)
        self.osmosdr_source_0_0.set_if_gain(10, 0)
        self.osmosdr_source_0_0.set_bb_gain(10, 0)
        self.osmosdr_source_0_0.set_antenna('', 0)
        self.osmosdr_source_0_0.set_bandwidth(0, 0)

        self.low_pass_filter_1 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, samp_rate, 240000, 120000, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 150000, 50000, firdes.WIN_HAMMING, 6.76))
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(8, 0.01, 0, 0.1, 0.01)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, 'C:\\Projects\\gr-bladerf-utils\\io\\_out.bin', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((0, ))
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 0, 1, 0)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.low_pass_filter_1, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.osmosdr_source_0_0, 0), (self.blocks_multiply_xx_0, 0))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate, 240000, 120000, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 150000, 50000, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_rx_vga_gain(self):
        return self.rx_vga_gain

    def set_rx_vga_gain(self, rx_vga_gain):
        self.rx_vga_gain = rx_vga_gain

    def get_rx_lna_gain(self):
        return self.rx_lna_gain

    def set_rx_lna_gain(self, rx_lna_gain):
        self.rx_lna_gain = rx_lna_gain

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_source_0_0.set_center_freq(self.freq, 0)

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-f", "--center-freq", dest="center_freq", type="intx", default=440000000,
        help="Set center_freq [default=%default]")
    return parser


def main(top_block_cls=rx_jason, options=None, rx_time=5, freq=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    if freq is not None:
        options.center_freq = freq
    tb = top_block_cls(center_freq=options.center_freq)

    tb.start()

    start_time = time.time()
    #count = 0

    while (time.time() - start_time < rx_time):
        time.sleep(0.1)

        '''
        count += 1

        if count % 30 == 10:
            print '[rx] Switching frequency to: 433920000'
            tb.set_center_freq(433920000)
        elif count % 30 == 20:
            print '[rx] Switching frequency to: 915000000'
            tb.set_center_freq(915000000)
        elif count % 30 == 0:
            print '[rx] Switching frequency to: 2450000000'
            tb.set_center_freq(2450000000)
        '''

    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
