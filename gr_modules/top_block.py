#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Tue Apr 24 15:39:33 2018
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
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from ieee802_15_4_oqpsk_phy import ieee802_15_4_oqpsk_phy  # grc-generated hier_block
from optparse import OptionParser
import foo
import ieee802_15_4
import pmt
import sip


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.tx_gain = tx_gain = 0
        self.tx_freq = tx_freq = 915000000
        self.samp_rate = samp_rate = 1500000
        self.rx_gain = rx_gain = 30
        self.rx_freq = rx_freq = 440000000
        self.rf_gain = rf_gain = 15
        self.if_gain = if_gain = 10
        self.bw = bw = 1500000
        self.bb_gain = bb_gain = 10

        ##################################################
        # Blocks
        ##################################################
        self._samp_rate_tool_bar = Qt.QToolBar(self)
        self._samp_rate_tool_bar.addWidget(Qt.QLabel("samp_rate"+": "))
        self._samp_rate_line_edit = Qt.QLineEdit(str(self.samp_rate))
        self._samp_rate_tool_bar.addWidget(self._samp_rate_line_edit)
        self._samp_rate_line_edit.returnPressed.connect(
        	lambda: self.set_samp_rate(int(str(self._samp_rate_line_edit.text().toAscii()))))
        self.top_layout.addWidget(self._samp_rate_tool_bar)
        self._tx_gain_tool_bar = Qt.QToolBar(self)
        self._tx_gain_tool_bar.addWidget(Qt.QLabel("tx_gain"+": "))
        self._tx_gain_line_edit = Qt.QLineEdit(str(self.tx_gain))
        self._tx_gain_tool_bar.addWidget(self._tx_gain_line_edit)
        self._tx_gain_line_edit.returnPressed.connect(
        	lambda: self.set_tx_gain(int(str(self._tx_gain_line_edit.text().toAscii()))))
        self.top_layout.addWidget(self._tx_gain_tool_bar)
        self._tx_freq_tool_bar = Qt.QToolBar(self)
        self._tx_freq_tool_bar.addWidget(Qt.QLabel("tx_freq"+": "))
        self._tx_freq_line_edit = Qt.QLineEdit(str(self.tx_freq))
        self._tx_freq_tool_bar.addWidget(self._tx_freq_line_edit)
        self._tx_freq_line_edit.returnPressed.connect(
        	lambda: self.set_tx_freq(int(str(self._tx_freq_line_edit.text().toAscii()))))
        self.top_layout.addWidget(self._tx_freq_tool_bar)
        self._rx_gain_tool_bar = Qt.QToolBar(self)
        self._rx_gain_tool_bar.addWidget(Qt.QLabel("rx_gain"+": "))
        self._rx_gain_line_edit = Qt.QLineEdit(str(self.rx_gain))
        self._rx_gain_tool_bar.addWidget(self._rx_gain_line_edit)
        self._rx_gain_line_edit.returnPressed.connect(
        	lambda: self.set_rx_gain(int(str(self._rx_gain_line_edit.text().toAscii()))))
        self.top_layout.addWidget(self._rx_gain_tool_bar)
        self._rx_freq_tool_bar = Qt.QToolBar(self)
        self._rx_freq_tool_bar.addWidget(Qt.QLabel("rx_freq"+": "))
        self._rx_freq_line_edit = Qt.QLineEdit(str(self.rx_freq))
        self._rx_freq_tool_bar.addWidget(self._rx_freq_line_edit)
        self._rx_freq_line_edit.returnPressed.connect(
        	lambda: self.set_rx_freq(int(str(self._rx_freq_line_edit.text().toAscii()))))
        self.top_layout.addWidget(self._rx_freq_tool_bar)
        self._rf_gain_range = Range(0, 30, 1, 15, 200)
        self._rf_gain_win = RangeWidget(self._rf_gain_range, self.set_rf_gain, "rf_gain", "counter_slider", int)
        self.top_layout.addWidget(self._rf_gain_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_c(
        	1024, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_1.enable_tags(-1, True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(True)
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
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_const_sink_x_1 = qtgui.const_sink_c(
        	1024, #size
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_1.set_update_time(0.01)
        self.qtgui_const_sink_x_1.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_1.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_1.enable_autoscale(False)
        self.qtgui_const_sink_x_1.enable_grid(False)
        self.qtgui_const_sink_x_1.enable_axis_labels(True)
        
        if not True:
          self.qtgui_const_sink_x_1.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
                  "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_const_sink_x_1_win = sip.wrapinstance(self.qtgui_const_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_1_win)
        self._if_gain_range = Range(0, 30, 1, 10, 200)
        self._if_gain_win = RangeWidget(self._if_gain_range, self.set_if_gain, "if_gain", "counter_slider", int)
        self.top_layout.addWidget(self._if_gain_win)
        self.ieee802_15_4_rime_stack_0_0 = ieee802_15_4.rime_stack(([129]), ([131]), ([132]), ([23,42]))
        self.ieee802_15_4_rime_stack_0 = ieee802_15_4.rime_stack(([129]), ([131]), ([132]), ([23,42]))
        self.ieee802_15_4_oqpsk_phy_0_0 = ieee802_15_4_oqpsk_phy()
        self.ieee802_15_4_oqpsk_phy_0 = ieee802_15_4_oqpsk_phy()
        self.ieee802_15_4_mac_0_0 = ieee802_15_4.mac(True,0x8841,0,0x1aaa,0xffff,0x3344)
        self.ieee802_15_4_mac_0 = ieee802_15_4.mac(True,0x8841,0,0x1aaa,0xffff,0x3344)
        self._bw_tool_bar = Qt.QToolBar(self)
        self._bw_tool_bar.addWidget(Qt.QLabel("bw"+": "))
        self._bw_line_edit = Qt.QLineEdit(str(self.bw))
        self._bw_tool_bar.addWidget(self._bw_line_edit)
        self._bw_line_edit.returnPressed.connect(
        	lambda: self.set_bw(int(str(self._bw_line_edit.text().toAscii()))))
        self.top_layout.addWidget(self._bw_tool_bar)
        self.blocks_socket_pdu_0_0_0 = blocks.socket_pdu("UDP_SERVER", 'localhost', '52002', 10000, False)
        self.blocks_socket_pdu_0_0 = blocks.socket_pdu("UDP_SERVER", 'localhost', '52001', 10000, False)
        self.blocks_message_strobe_0_0 = blocks.message_strobe(pmt.intern(""), 10)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern(""), 10)
        self._bb_gain_range = Range(0, 30, 1, 10, 200)
        self._bb_gain_win = RangeWidget(self._bb_gain_range, self.set_bb_gain, "bb_gain", "counter_slider", int)
        self.top_layout.addWidget(self._bb_gain_win)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.ieee802_15_4_rime_stack_0, 'bcin'))    
        self.msg_connect((self.blocks_message_strobe_0_0, 'strobe'), (self.ieee802_15_4_rime_stack_0_0, 'bcin'))    
        self.msg_connect((self.blocks_socket_pdu_0_0, 'pdus'), (self.ieee802_15_4_rime_stack_0, 'bcin'))    
        self.msg_connect((self.blocks_socket_pdu_0_0_0, 'pdus'), (self.ieee802_15_4_rime_stack_0_0, 'bcin'))    
        self.msg_connect((self.ieee802_15_4_mac_0, 'pdu out'), (self.ieee802_15_4_oqpsk_phy_0, 'txin'))    
        self.msg_connect((self.ieee802_15_4_mac_0, 'app out'), (self.ieee802_15_4_rime_stack_0, 'fromMAC'))    
        self.msg_connect((self.ieee802_15_4_mac_0_0, 'pdu out'), (self.ieee802_15_4_oqpsk_phy_0_0, 'txin'))    
        self.msg_connect((self.ieee802_15_4_mac_0_0, 'app out'), (self.ieee802_15_4_rime_stack_0_0, 'fromMAC'))    
        self.msg_connect((self.ieee802_15_4_oqpsk_phy_0, 'rxout'), (self.ieee802_15_4_mac_0, 'pdu in'))    
        self.msg_connect((self.ieee802_15_4_oqpsk_phy_0_0, 'rxout'), (self.ieee802_15_4_mac_0_0, 'pdu in'))    
        self.msg_connect((self.ieee802_15_4_rime_stack_0, 'bcout'), (self.blocks_socket_pdu_0_0, 'pdus'))    
        self.msg_connect((self.ieee802_15_4_rime_stack_0, 'toMAC'), (self.ieee802_15_4_mac_0, 'app in'))    
        self.msg_connect((self.ieee802_15_4_rime_stack_0_0, 'bcout'), (self.blocks_socket_pdu_0_0_0, 'pdus'))    
        self.msg_connect((self.ieee802_15_4_rime_stack_0_0, 'toMAC'), (self.ieee802_15_4_mac_0_0, 'app in'))    
        self.connect((self.ieee802_15_4_oqpsk_phy_0, 0), (self.ieee802_15_4_oqpsk_phy_0_0, 0))    
        self.connect((self.ieee802_15_4_oqpsk_phy_0, 0), (self.qtgui_const_sink_x_1, 0))    
        self.connect((self.ieee802_15_4_oqpsk_phy_0, 0), (self.qtgui_time_sink_x_1, 0))    
        self.connect((self.ieee802_15_4_oqpsk_phy_0_0, 0), (self.ieee802_15_4_oqpsk_phy_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

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

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        Qt.QMetaObject.invokeMethod(self._samp_rate_line_edit, "setText", Qt.Q_ARG("QString", str(self.samp_rate)))
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        Qt.QMetaObject.invokeMethod(self._rx_gain_line_edit, "setText", Qt.Q_ARG("QString", str(self.rx_gain)))

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        Qt.QMetaObject.invokeMethod(self._rx_freq_line_edit, "setText", Qt.Q_ARG("QString", str(self.rx_freq)))

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


def main(top_block_cls=top_block, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
