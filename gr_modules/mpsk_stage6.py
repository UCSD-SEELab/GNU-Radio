#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Mpsk Stage6
# Generated: Mon Oct 16 17:03:02 2017
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import time


class mpsk_stage6(gr.top_block):

    def __init__(self, center_freq=440000000):
        gr.top_block.__init__(self, "Mpsk Stage6")

        ##################################################
        # Parameters
        ##################################################
        self.center_freq = center_freq

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 4
        self.nfilts = nfilts = 32
        self.baud_rate = baud_rate = 2530
        self.taps = taps = [1.0, 0.25-0.25j, 0.50 + 0.10j, -0.3 + 0.2j]
        self.sps_0 = sps_0 = 10
        self.samp_rate_tx = samp_rate_tx = 400000
        self.samp_rate_0 = samp_rate_0 = int(baud_rate * sps)
        self.samp_rate = samp_rate = 32000
        self.rx_vga_gain = rx_vga_gain = 35
        self.rx_lna_gain = rx_lna_gain = 6
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), 0.35, 11*sps*nfilts)
        self.qpsk_0 = qpsk_0 = digital.constellation_rect(([0.707+0.707j, -0.707+0.707j, -0.707-0.707j, 0.707-0.707j]), ([0, 1, 2, 3]), 4, 2, 2, 1, 1).base()
        self.qpsk = qpsk = digital.constellation_rect(([0.707+0.707j, -0.707+0.707j, -0.707-0.707j, 0.707-0.707j]), ([0, 1, 2, 3]), 4, 2, 2, 1, 1).base()
        self.freq = freq = 440e6
        self.excess_bw = excess_bw = 0.35
        self.arity = arity = 4

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + 'bladerf=0' )
        self.osmosdr_source_0.set_sample_rate(samp_rate_tx)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(1, 0)
        self.osmosdr_source_0.set_iq_balance_mode(1, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(rx_lna_gain, 0)
        self.osmosdr_source_0.set_if_gain(0, 0)
        self.osmosdr_source_0.set_bb_gain(rx_vga_gain, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.digital_constellation_receiver_cb_0 = digital.constellation_receiver_cb(qpsk_0, 6.28/100.0, 0.10, 0.35)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, 'C:\\Projects\\gr-bladerf-utils\\_out.bin', False)
        self.blocks_file_sink_0_0.set_unbuffered(True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.digital_constellation_receiver_cb_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.digital_constellation_receiver_cb_0, 0))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_samp_rate_0(int(self.baud_rate * self.sps))
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), 0.35, 11*self.sps*self.nfilts))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), 0.35, 11*self.sps*self.nfilts))

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        self.set_samp_rate_0(int(self.baud_rate * self.sps))

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps

    def get_sps_0(self):
        return self.sps_0

    def set_sps_0(self, sps_0):
        self.sps_0 = sps_0

    def get_samp_rate_tx(self):
        return self.samp_rate_tx

    def set_samp_rate_tx(self, samp_rate_tx):
        self.samp_rate_tx = samp_rate_tx
        self.osmosdr_source_0.set_sample_rate(self.samp_rate_tx)

    def get_samp_rate_0(self):
        return self.samp_rate_0

    def set_samp_rate_0(self, samp_rate_0):
        self.samp_rate_0 = samp_rate_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rx_vga_gain(self):
        return self.rx_vga_gain

    def set_rx_vga_gain(self, rx_vga_gain):
        self.rx_vga_gain = rx_vga_gain
        self.osmosdr_source_0.set_bb_gain(self.rx_vga_gain, 0)

    def get_rx_lna_gain(self):
        return self.rx_lna_gain

    def set_rx_lna_gain(self, rx_lna_gain):
        self.rx_lna_gain = rx_lna_gain
        self.osmosdr_source_0.set_gain(self.rx_lna_gain, 0)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps

    def get_qpsk_0(self):
        return self.qpsk_0

    def set_qpsk_0(self, qpsk_0):
        self.qpsk_0 = qpsk_0

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_source_0.set_center_freq(self.freq, 0)

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw

    def get_arity(self):
        return self.arity

    def set_arity(self, arity):
        self.arity = arity


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-f", "--center-freq", dest="center_freq", type="intx", default=440000000,
        help="Set center_freq [default=%default]")
    return parser


def main(top_block_cls=mpsk_stage6, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(center_freq=options.center_freq)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
