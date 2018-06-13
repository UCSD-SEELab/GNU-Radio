#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Simple Trx Mac
# Generated: Thu May 31 13:26:04 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt4 import Qt
from gmsk_radio import gmsk_radio  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import iio
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import mac
import pmt
import sip


class simple_trx_mac(gr.top_block, Qt.QWidget):

    def __init__(self, ampl=0.7, args='', arq_timeout=.1*0 + 0.04, broadcast_interval=1, dest_addr=1, max_arq_attempts=5 * 2, mtu=255, port='12345', radio_addr=0, samps_per_sym=4):
        gr.top_block.__init__(self, "Simple Trx Mac")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Simple Trx Mac")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "simple_trx_mac")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.ampl = ampl
        self.args = args
        self.arq_timeout = arq_timeout
        self.broadcast_interval = broadcast_interval
        self.dest_addr = dest_addr
        self.max_arq_attempts = max_arq_attempts
        self.mtu = mtu
        self.port = port
        self.radio_addr = radio_addr
        self.samps_per_sym = samps_per_sym

        ##################################################
        # Variables
        ##################################################
        self.tx_gain = tx_gain = 20
        self.tx_freq = tx_freq = 440000000
        self.samp_rate = samp_rate = 1000000
        self.rx_gain = rx_gain = 10
        self.rx_freq = rx_freq = 450000000
        self.rf_gain = rf_gain = 30
        self.if_gain = if_gain = 30
        self.bw = bw = 1000000
        self.bb_gain = bb_gain = 30

        ##################################################
        # Blocks
        ##################################################
        self.tab = Qt.QTabWidget()
        self.tab_widget_0 = Qt.QWidget()
        self.tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_0)
        self.tab_grid_layout_0 = Qt.QGridLayout()
        self.tab_layout_0.addLayout(self.tab_grid_layout_0)
        self.tab.addTab(self.tab_widget_0, 'General')
        self.tab_widget_1 = Qt.QWidget()
        self.tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_1)
        self.tab_grid_layout_1 = Qt.QGridLayout()
        self.tab_layout_1.addLayout(self.tab_grid_layout_1)
        self.tab.addTab(self.tab_widget_1, 'Gains')
        self.top_layout.addWidget(self.tab)
        self._tx_freq_tool_bar = Qt.QToolBar(self)
        self._tx_freq_tool_bar.addWidget(Qt.QLabel("tx_freq"+": "))
        self._tx_freq_line_edit = Qt.QLineEdit(str(self.tx_freq))
        self._tx_freq_tool_bar.addWidget(self._tx_freq_line_edit)
        self._tx_freq_line_edit.returnPressed.connect(
        	lambda: self.set_tx_freq(int(str(self._tx_freq_line_edit.text().toAscii()))))
        self.tab_layout_0.addWidget(self._tx_freq_tool_bar)
        self._samp_rate_tool_bar = Qt.QToolBar(self)
        self._samp_rate_tool_bar.addWidget(Qt.QLabel("samp_rate"+": "))
        self._samp_rate_line_edit = Qt.QLineEdit(str(self.samp_rate))
        self._samp_rate_tool_bar.addWidget(self._samp_rate_line_edit)
        self._samp_rate_line_edit.returnPressed.connect(
        	lambda: self.set_samp_rate(int(str(self._samp_rate_line_edit.text().toAscii()))))
        self.tab_layout_0.addWidget(self._samp_rate_tool_bar)
        self._rx_gain_tool_bar = Qt.QToolBar(self)
        self._rx_gain_tool_bar.addWidget(Qt.QLabel("rx_gain"+": "))
        self._rx_gain_line_edit = Qt.QLineEdit(str(self.rx_gain))
        self._rx_gain_tool_bar.addWidget(self._rx_gain_line_edit)
        self._rx_gain_line_edit.returnPressed.connect(
        	lambda: self.set_rx_gain(int(str(self._rx_gain_line_edit.text().toAscii()))))
        self.tab_layout_1.addWidget(self._rx_gain_tool_bar)
        self._rx_freq_tool_bar = Qt.QToolBar(self)
        self._rx_freq_tool_bar.addWidget(Qt.QLabel("rx_freq"+": "))
        self._rx_freq_line_edit = Qt.QLineEdit(str(self.rx_freq))
        self._rx_freq_tool_bar.addWidget(self._rx_freq_line_edit)
        self._rx_freq_line_edit.returnPressed.connect(
        	lambda: self.set_rx_freq(int(str(self._rx_freq_line_edit.text().toAscii()))))
        self.tab_layout_0.addWidget(self._rx_freq_tool_bar)
        self.plot = Qt.QTabWidget()
        self.plot_widget_0 = Qt.QWidget()
        self.plot_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.plot_widget_0)
        self.plot_grid_layout_0 = Qt.QGridLayout()
        self.plot_layout_0.addLayout(self.plot_grid_layout_0)
        self.plot.addTab(self.plot_widget_0, 'RX')
        self.plot_widget_1 = Qt.QWidget()
        self.plot_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.plot_widget_1)
        self.plot_grid_layout_1 = Qt.QGridLayout()
        self.plot_layout_1.addLayout(self.plot_grid_layout_1)
        self.plot.addTab(self.plot_widget_1, 'TX')
        self.top_layout.addWidget(self.plot)
        self._bw_tool_bar = Qt.QToolBar(self)
        self._bw_tool_bar.addWidget(Qt.QLabel("bw"+": "))
        self._bw_line_edit = Qt.QLineEdit(str(self.bw))
        self._bw_tool_bar.addWidget(self._bw_line_edit)
        self._bw_line_edit.returnPressed.connect(
        	lambda: self.set_bw(int(str(self._bw_line_edit.text().toAscii()))))
        self.tab_layout_0.addWidget(self._bw_tool_bar)
        self._tx_gain_tool_bar = Qt.QToolBar(self)
        self._tx_gain_tool_bar.addWidget(Qt.QLabel("tx_gain"+": "))
        self._tx_gain_line_edit = Qt.QLineEdit(str(self.tx_gain))
        self._tx_gain_tool_bar.addWidget(self._tx_gain_line_edit)
        self._tx_gain_line_edit.returnPressed.connect(
        	lambda: self.set_tx_gain(int(str(self._tx_gain_line_edit.text().toAscii()))))
        self.tab_layout_1.addWidget(self._tx_gain_tool_bar)
        self.simple_mac = mac.simple_mac(
        radio_addr,
        arq_timeout,
        max_arq_attempts,
        broadcast_interval,
        False,
        0.05,
        node_expiry_delay=10.0,
        expire_on_arq_failure=False,
        only_send_if_alive=False,
        prepend_dummy=False,
        )
        self._rf_gain_range = Range(0, 30, 1, 30, 100)
        self._rf_gain_win = RangeWidget(self._rf_gain_range, self.set_rf_gain, "rf_gain", "counter_slider", int)
        self.tab_layout_1.addWidget(self._rf_gain_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_c(
        	1024, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.01)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_1.enable_tags(-1, True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_1.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(2*1):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.plot_layout_0.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
        	1024, #size
        	samp_rate, #samp_rate
        	"TX", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.01)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_0.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(2*1):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.plot_layout_1.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"RX", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.01)
        self.qtgui_freq_sink_x_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_1.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_1.set_plot_pos_half(not True)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.pyqwidget(), Qt.QWidget)
        self.plot_layout_0.addWidget(self._qtgui_freq_sink_x_1_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"TX", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.plot_layout_1.addWidget(self._qtgui_freq_sink_x_0_win)
        self.pluto_source_0 = iio.pluto_source('ip:pluto.local', rx_freq, samp_rate, samp_rate, 0x8000, True, True, True, "manual", rx_gain, '', True)
        self.pluto_sink_0 = iio.pluto_sink('ip:pluto.local', tx_freq, samp_rate, samp_rate, 0x8000, False, 10.0, '', True)
        self.mac_virtual_channel_encoder_0 = mac.virtual_channel_encoder(dest_addr, True,mtu=mtu,
        chan_id=0,
        prepend_dummy=False,
        )
        self.mac_virtual_channel_decoder_0 = mac.virtual_channel_decoder(3, [0,1])
        self._if_gain_range = Range(0, 30, 1, 30, 100)
        self._if_gain_win = RangeWidget(self._if_gain_range, self.set_if_gain, "if_gain", "counter_slider", int)
        self.tab_layout_1.addWidget(self._if_gain_win)
        self.gmsk_radio_0 = gmsk_radio(
            rate=samp_rate,
            samps_per_sym=samps_per_sym,
            ampl=ampl,
            access_code_threshold=0 + 12 + 4*0,
        )
        self.blocks_tuntap_pdu_0 = blocks.tuntap_pdu('tun0', 10000, True)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("T"), 0.01)
        self._bb_gain_range = Range(0, 30, 1, 30, 100)
        self._bb_gain_win = RangeWidget(self._bb_gain_range, self.set_bb_gain, "bb_gain", "counter_slider", int)
        self.tab_layout_1.addWidget(self._bb_gain_win)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.simple_mac, 'ctrl_in'))    
        self.msg_connect((self.blocks_tuntap_pdu_0, 'pdus'), (self.mac_virtual_channel_encoder_0, 'in'))    
        self.msg_connect((self.gmsk_radio_0, 'msg_out'), (self.simple_mac, 'from_radio'))    
        self.msg_connect((self.mac_virtual_channel_decoder_0, 'out0'), (self.blocks_tuntap_pdu_0, 'pdus'))    
        self.msg_connect((self.mac_virtual_channel_encoder_0, 'out'), (self.simple_mac, 'from_app_arq'))    
        self.msg_connect((self.simple_mac, 'to_radio'), (self.gmsk_radio_0, 'msg_in'))    
        self.msg_connect((self.simple_mac, 'to_app'), (self.mac_virtual_channel_decoder_0, 'in'))    
        self.connect((self.gmsk_radio_0, 0), (self.pluto_sink_0, 0))    
        self.connect((self.gmsk_radio_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.gmsk_radio_0, 0), (self.qtgui_time_sink_x_0, 0))    
        self.connect((self.pluto_source_0, 0), (self.gmsk_radio_0, 0))    
        self.connect((self.pluto_source_0, 0), (self.qtgui_freq_sink_x_1, 0))    
        self.connect((self.pluto_source_0, 0), (self.qtgui_time_sink_x_1, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "simple_trx_mac")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_ampl(self):
        return self.ampl

    def set_ampl(self, ampl):
        self.ampl = ampl
        self.gmsk_radio_0.set_ampl(self.ampl)

    def get_args(self):
        return self.args

    def set_args(self, args):
        self.args = args

    def get_arq_timeout(self):
        return self.arq_timeout

    def set_arq_timeout(self, arq_timeout):
        self.arq_timeout = arq_timeout

    def get_broadcast_interval(self):
        return self.broadcast_interval

    def set_broadcast_interval(self, broadcast_interval):
        self.broadcast_interval = broadcast_interval

    def get_dest_addr(self):
        return self.dest_addr

    def set_dest_addr(self, dest_addr):
        self.dest_addr = dest_addr

    def get_max_arq_attempts(self):
        return self.max_arq_attempts

    def set_max_arq_attempts(self, max_arq_attempts):
        self.max_arq_attempts = max_arq_attempts

    def get_mtu(self):
        return self.mtu

    def set_mtu(self, mtu):
        self.mtu = mtu

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_radio_addr(self):
        return self.radio_addr

    def set_radio_addr(self, radio_addr):
        self.radio_addr = radio_addr

    def get_samps_per_sym(self):
        return self.samps_per_sym

    def set_samps_per_sym(self, samps_per_sym):
        self.samps_per_sym = samps_per_sym
        self.gmsk_radio_0.set_samps_per_sym(self.samps_per_sym)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        Qt.QMetaObject.invokeMethod(self._tx_gain_line_edit, "setText", Qt.Q_ARG("QString", str(self.tx_gain)))

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq
        Qt.QMetaObject.invokeMethod(self._tx_freq_line_edit, "setText", Qt.Q_ARG("QString", str(self.tx_freq)))
        self.pluto_sink_0.set_params(self.tx_freq, self.samp_rate, self.samp_rate, 10.0, '', True)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        Qt.QMetaObject.invokeMethod(self._samp_rate_line_edit, "setText", Qt.Q_ARG("QString", str(self.samp_rate)))
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.pluto_source_0.set_params(self.rx_freq, self.samp_rate, self.samp_rate, True, True, True, "manual", self.rx_gain, '', True)
        self.pluto_sink_0.set_params(self.tx_freq, self.samp_rate, self.samp_rate, 10.0, '', True)
        self.gmsk_radio_0.set_rate(self.samp_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        Qt.QMetaObject.invokeMethod(self._rx_gain_line_edit, "setText", Qt.Q_ARG("QString", str(self.rx_gain)))
        self.pluto_source_0.set_params(self.rx_freq, self.samp_rate, self.samp_rate, True, True, True, "manual", self.rx_gain, '', True)

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        Qt.QMetaObject.invokeMethod(self._rx_freq_line_edit, "setText", Qt.Q_ARG("QString", str(self.rx_freq)))
        self.pluto_source_0.set_params(self.rx_freq, self.samp_rate, self.samp_rate, True, True, True, "manual", self.rx_gain, '', True)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        Qt.QMetaObject.invokeMethod(self._bw_line_edit, "setText", Qt.Q_ARG("QString", str(self.bw)))

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--ampl", dest="ampl", type="eng_float", default=eng_notation.num_to_str(0.7),
        help="Set TX BB amp [default=%default]")
    parser.add_option(
        "-a", "--args", dest="args", type="string", default='',
        help="Set USRP device args [default=%default]")
    parser.add_option(
        "-t", "--arq-timeout", dest="arq_timeout", type="eng_float", default=eng_notation.num_to_str(.1*0 + 0.04),
        help="Set ARQ timeout [default=%default]")
    parser.add_option(
        "-b", "--broadcast-interval", dest="broadcast_interval", type="eng_float", default=eng_notation.num_to_str(1),
        help="Set Broadcast Interval [default=%default]")
    parser.add_option(
        "-d", "--dest-addr", dest="dest_addr", type="intx", default=1,
        help="Set Destination address [default=%default]")
    parser.add_option(
        "", "--max-arq-attempts", dest="max_arq_attempts", type="intx", default=5 * 2,
        help="Set Max ARQ attempts [default=%default]")
    parser.add_option(
        "", "--mtu", dest="mtu", type="intx", default=255,
        help="Set TCP Socket MTU [default=%default]")
    parser.add_option(
        "", "--port", dest="port", type="string", default='12345',
        help="Set TCP port [default=%default]")
    parser.add_option(
        "-l", "--radio-addr", dest="radio_addr", type="intx", default=0,
        help="Set Local address [default=%default]")
    parser.add_option(
        "", "--samps-per-sym", dest="samps_per_sym", type="intx", default=4,
        help="Set Samples/symbol [default=%default]")
    return parser


def main(top_block_cls=simple_trx_mac, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(ampl=options.ampl, args=options.args, arq_timeout=options.arq_timeout, broadcast_interval=options.broadcast_interval, dest_addr=options.dest_addr, max_arq_attempts=options.max_arq_attempts, mtu=options.mtu, port=options.port, radio_addr=options.radio_addr, samps_per_sym=options.samps_per_sym)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
