#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Decodeur NOAA GNU Radio WAV
# Author: F4IMY
# Generated: Sat Feb 11 23:00:42 2023
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


class decodeur_NOAA15_WAV(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Decodeur NOAA GNU Radio WAV")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000
        self.rf_rate = rf_rate = 2e6
        self.freq = freq = 137.62e6

        ##################################################
        # Blocks
        ##################################################
        self.sdrplay_rsp1a_source_0 = sdrplay.rsp1a_source(freq, 1536, True, 40, True, True,
                False, 450, 1, rf_rate, True, False, 0, False,
                '0')

        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=4,
                taps=None,
                fractional_bw=None,
        )
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink('/home/pi/Dev/GR_NOAA_script/record.wav', 1, samp_rate, 16)
        self.audio_sink_0 = audio.sink(samp_rate, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=samp_rate,
        	audio_decimation=1,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.audio_sink_0, 0))
        self.connect((self.analog_wfm_rcv_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.sdrplay_rsp1a_source_0, 0), (self.rational_resampler_xxx_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rf_rate(self):
        return self.rf_rate

    def set_rf_rate(self, rf_rate):
        self.rf_rate = rf_rate

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.sdrplay_rsp1a_source_0.set_rf_freq(self.freq)


def main(top_block_cls=decodeur_NOAA15_WAV, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
