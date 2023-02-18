#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Decodeur NOAA GNU Radio WAV
# Author: F4IMY
# Generated: Sat Feb 18 16:28:38 2023
##################################################


from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sdrplay


class decodeur_NOAA_WAV(gr.top_block):

    def __init__(self, freq=89.7e6):
        gr.top_block.__init__(self, "Decodeur NOAA GNU Radio WAV")

        ##################################################
        # Parameters
        ##################################################
        self.freq = freq

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000
        self.rf_rate = rf_rate = 0.25e6
        self.dec = dec = 1

        ##################################################
        # Blocks
        ##################################################
        self.sdrplay_rsp1a_source_0 = sdrplay.rsp1a_source(freq, 200, True, 20, True, True,
                False, 0, 1, rf_rate, True, False, 0, False,
                '0')

        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, rf_rate, 25e3, 5e3, firdes.WIN_HAMMING, 6.76))
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink('/home/pi/Dev/ARTSystem/GR_NOAA_script/record.wav', 1, samp_rate, 16)
        self.audio_sink_0 = audio.sink(samp_rate, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=samp_rate,
        	audio_decimation=5,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.audio_sink_0, 0))
        self.connect((self.analog_wfm_rcv_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.sdrplay_rsp1a_source_0, 0), (self.low_pass_filter_0, 0))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.sdrplay_rsp1a_source_0.set_rf_freq(self.freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rf_rate(self):
        return self.rf_rate

    def set_rf_rate(self, rf_rate):
        self.rf_rate = rf_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.rf_rate, 25e3, 5e3, firdes.WIN_HAMMING, 6.76))

    def get_dec(self):
        return self.dec

    def set_dec(self, dec):
        self.dec = dec


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-f", "--freq", dest="freq", type="eng_float", default=eng_notation.num_to_str(89.7e6),
        help="Set Frequency [default=%default]")
    return parser


def main(top_block_cls=decodeur_NOAA_WAV, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(freq=options.freq)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
