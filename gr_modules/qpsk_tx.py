#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Qpsk Tx
# Generated: Tue Oct 17 03:32:44 2017
##################################################


#from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import sys
import time
from gnuradio import qtgui


class qpsk_tx(gr.top_block):

    def __init__(self, center_freq=440000000, filename="_send.bin"):
        gr.top_block.__init__(self, "Qpsk Tx")
        
        self.center_freq = center_freq
        self.filename = filename

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 4
        self.excess_bw = excess_bw = 0.35
        self.txvga2 = txvga2 = 25
        self.txvga1 = txvga1 = -4
        self.samp_rate_tx = samp_rate_tx = 400000
        self.samp_rate = samp_rate = 24900
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(1, sps, 1, excess_bw, 45)
        self.qpsk = qpsk = digital.constellation_rect(([0.707+0.707j, -0.707+0.707j, -0.707-0.707j, 0.707-0.707j]), ([0, 1, 2, 3]), 4, 2, 2, 1, 1).base()
        self.freq = freq = 440e6
        self.arity = arity = 4

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + 'bladerf=0' )
        self.osmosdr_sink_0.set_sample_rate(samp_rate_tx)
        self.osmosdr_sink_0.set_center_freq(freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(txvga2, 0)
        self.osmosdr_sink_0.set_if_gain(0, 0)
        self.osmosdr_sink_0.set_bb_gain(txvga1, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(1500000, 0)

        self.digital_constellation_modulator_0 = digital.generic_mod(
          constellation=qpsk,
          differential=False,
          samples_per_symbol=sps,
          pre_diff_code=True,
          excess_bw=excess_bw,
          verbose=False,
          log=False,
          )
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, 'C:\\Projects\\gr-bladerf-utils\\_send.bin', True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.osmosdr_sink_0, 0))


    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.set_freq(self.center_freq)

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename
        self.set_filepath(self.prefix + self.filename)
        
    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "qpsk_tx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(1, self.sps, 1, self.excess_bw, 45))

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw
        self.set_rrc_taps(firdes.root_raised_cosine(1, self.sps, 1, self.excess_bw, 45))

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

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_sink_0.set_center_freq(self.freq, 0)

    def get_arity(self):
        return self.arity

    def set_arity(self, arity):
        self.arity = arity

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        self.set_samp_rate(int(self.baud_rate * self.sps))

    def get_filepath(self):
        return self.filepath

    def set_filepath(self, filepath):
        self.filepath = filepath
        self.blocks_file_source_0.open(self.filepath, True)


def argument_parser():

    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option(
        "-f", "--center-freq", dest="center_freq", type="intx", default=433920000,
        help="Set center_freq [default=%default]")
    parser.add_option(
        "-n", "--filename", dest="filename", type="string", default="_send.bin",
        help="Set filename [default=%default]")
    return parser

def main(top_block_cls=qpsk_tx, options=None, tx_time=1000, freq=None, fn=None):

    top_block_cls=qpsk_tx
    tb = top_block_cls()
    tb.start()
    #tb.show()

    if options is None:
        options, _ = argument_parser().parse_args()

    if freq is not None and fn is not None:
        options.center_freq = freq
        options.filename=fn
    tb = top_block_cls(center_freq=options.center_freq, filename=options.filename)
    
    filenames = []
    filenames.append('_send1.bin')
    filenames.append('_send2.bin')
    filenames.append('_send3.bin')

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
