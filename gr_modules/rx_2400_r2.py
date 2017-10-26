#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Rx 2400 R2
# Generated: Fri Jun  2 06:54:55 2017
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import logpwrfft
from gnuradio.filter import firdes
from optparse import OptionParser
import ConfigParser
import math
import osmosdr
import time


class rx_2400_r2(gr.top_block):

    def __init__(self, center_freq=433920000):
        gr.top_block.__init__(self, "Rx 2400 R2")

        ##################################################
        # Parameters
        ##################################################
        self.center_freq = center_freq

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 10
        self.baud_rate = baud_rate = 2530
        self.samp_rate_tx = samp_rate_tx = 400000
        self.samp_rate = samp_rate = baud_rate * sps
        self.rx_vga_gain = rx_vga_gain = 35
        self.rx_lna_gain = rx_lna_gain = 6
        self.quad_gain = quad_gain = 8
        self.freq = freq = 2460000000
        self._fft_size_config = ConfigParser.ConfigParser()
        self._fft_size_config.read('default')
        try: fft_size = self._fft_size_config.getint('main', 'key')
        except: fft_size = 2048
        self.fft_size = fft_size

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
        self.osmosdr_source_0.set_bandwidth(1500000, 0)

        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate_tx, 6000, 6000, firdes.WIN_HAMMING, 6.76))
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
        	sample_rate=samp_rate_tx,
        	fft_size=fft_size,
        	ref_scale=2,
        	frame_rate=1,
        	avg_alpha=1.0,
        	average=False,
        )
        self.fir_filter_xxx_0 = filter.fir_filter_fff(16, (firdes.low_pass(1.0, baud_rate*sps, baud_rate, 0.25*baud_rate)))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_fff(sps, 2*3.14159265/100, (firdes.low_pass(1.0, baud_rate*sps, baud_rate, 0.25*baud_rate)), 32, 16, 1.5, 1)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*fft_size, 1)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, 'io/_out.bin', False)
        self.blocks_file_sink_0_0.set_unbuffered(True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*fft_size, 'io/log_power_fft_data.bin', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((0, ))
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(quad_gain)
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(-70, 1e-4, 0, True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.analog_pwr_squelch_xx_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.logpwrfft_x_0, 0))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.set_freq(self.center_freq)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_samp_rate(self.baud_rate * self.sps)
        self.fir_filter_xxx_0.set_taps((firdes.low_pass(1.0, self.baud_rate*self.sps, self.baud_rate, 0.25*self.baud_rate)))
        self.digital_pfb_clock_sync_xxx_0.update_taps((firdes.low_pass(1.0, self.baud_rate*self.sps, self.baud_rate, 0.25*self.baud_rate)))

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        self.set_samp_rate(self.baud_rate * self.sps)
        self.fir_filter_xxx_0.set_taps((firdes.low_pass(1.0, self.baud_rate*self.sps, self.baud_rate, 0.25*self.baud_rate)))
        self.digital_pfb_clock_sync_xxx_0.update_taps((firdes.low_pass(1.0, self.baud_rate*self.sps, self.baud_rate, 0.25*self.baud_rate)))

    def get_samp_rate_tx(self):
        return self.samp_rate_tx

    def set_samp_rate_tx(self, samp_rate_tx):
        self.samp_rate_tx = samp_rate_tx
        self.osmosdr_source_0.set_sample_rate(self.samp_rate_tx)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate_tx, 6000, 6000, firdes.WIN_HAMMING, 6.76))
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate_tx)

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

    def get_quad_gain(self):
        return self.quad_gain

    def set_quad_gain(self, quad_gain):
        self.quad_gain = quad_gain
        self.analog_quadrature_demod_cf_0.set_gain(self.quad_gain)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_source_0.set_center_freq(self.freq, 0)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-f", "--center-freq", dest="center_freq", type="intx", default=433920000,
        help="Set center_freq [default=%default]")
    return parser


def main(top_block_cls=rx_2400_r2, options=None, rx_time=5, freq=None):
    top_block_cls=rx_2400_r2
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
