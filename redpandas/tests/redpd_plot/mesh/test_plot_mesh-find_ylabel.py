import unittest
import numpy as np
import pandas as pd
from libquantum.spectra import stft_from_sig
import redpandas.redpd_plot.mesh as rpd_mesh


class TestFindYlabelTfr(unittest.TestCase):
    def setUp(self) -> None:
        # Create audio mesh
        self.start_time = 0
        self.end_time = 10
        self.sample_rate_audio = 100
        self.signal_time_audio = np.arange(self.start_time, self.end_time, 1/self.sample_rate_audio)
        self.frequency = 3
        self.amplitude = 1
        self.sinewave_audio = self.amplitude * np.sin(2 * np.pi * self.frequency * self.signal_time_audio)

        # Create audio mesh
        self.audio_STFT, self.audio_STFT_bits, self.audio_time_stft_s, self.audio_frequency_stft_hz = \
            stft_from_sig(sig_wf=self.sinewave_audio,
                          frequency_sample_rate_hz=self.sample_rate_audio,
                          band_order_Nth=3)
        # Create barometer
        self.sample_rate_barometer = 31
        self.signal_time_barometer = np.arange(self.start_time, self.end_time, 1/self.sample_rate_barometer)
        self.sinewave_barometer_base = self.amplitude * np.sin(2 * np.pi * self.frequency * self.signal_time_barometer)
        self.sinewave_barometer = self.sinewave_barometer_base.reshape((1, len(self.sinewave_barometer_base)))

        # Create barometer mesh
        self.bar_stft_all = []
        self.bar_stft_time_all = []
        self.bar_stft_bits_all = []
        self.bar_stft_frequency_all = []

        for dimension in range(len(self.sinewave_barometer)):
            self.bar_STFT, self.bar_STFT_bits, self.bar_time_stft_s, self.bar_frequency_stft_hz = \
                stft_from_sig(sig_wf=self.sinewave_barometer[dimension],
                              frequency_sample_rate_hz=self.sample_rate_barometer,
                              band_order_Nth=3)

            self.bar_stft_all.append(self.bar_STFT)
            self.bar_stft_bits_all.append(self.bar_STFT_bits)
            self.bar_stft_time_all.append(self.bar_time_stft_s)
            self.bar_stft_frequency_all.append(self.bar_frequency_stft_hz)

        # Create accelerometer
        self.sample_rate_acc = 30
        self.signal_time_acc = np.arange(self.start_time, self.end_time, 1/(self.sample_rate_acc/3))
        self.length_for_signal = np.arange(self.start_time, self.end_time, 1/self.sample_rate_acc)
        self.sinewave_acc_base = self.amplitude * np.sin(2 * np.pi * self.frequency * self.length_for_signal)
        self.points_per_row = int(len(self.sinewave_acc_base)/3)
        self.sinewave_acc = self.sinewave_acc_base.reshape((3, self.points_per_row))

        # Create accelerometer mesh
        self.acc_stft_all = []
        self.acc_stft_time_all = []
        self.acc_stft_bits_all = []
        self.acc_stft_frequency_all = []
        for dimension in range(self.sinewave_acc.ndim):
            self.acc_STFT, self.acc_STFT_bits, self.acc_time_stft_s, self.acc_frequency_stft_hz = \
                stft_from_sig(sig_wf=self.sinewave_acc[dimension],
                              frequency_sample_rate_hz=self.sample_rate_acc,
                              band_order_Nth=3)

            self.acc_stft_all.append(self.acc_STFT)
            self.acc_stft_bits_all.append(self.acc_STFT_bits)
            self.acc_stft_time_all.append(self.acc_time_stft_s)
            self.acc_stft_frequency_all.append(self.acc_frequency_stft_hz)

        # Create df
        self.dict_to_df_multiple = {0: {"station_id": "1234567890",
                                        "audio_stft": self.audio_STFT,
                                        "audio_stft_bits": self.audio_STFT_bits,
                                        "audio_stft_time_s": self.audio_time_stft_s,
                                        "audio_stft_frequency_hz": self.audio_frequency_stft_hz},
                                    1: {"station_id": "2345678901",   # Add another station
                                        "audio_stft": self.audio_STFT,
                                        "audio_stft_bits": self.audio_STFT_bits,
                                        "audio_stft_time_s": self.audio_time_stft_s,
                                        "audio_stft_frequency_hz": self.audio_frequency_stft_hz}}
        self.df_data = pd.DataFrame(self.dict_to_df_multiple).T

        # Make bar/acc mesh arrays, add them to lists, add column to df.
        self.bar_stft_array = np.array(self.bar_stft_all)
        self.bar_stft_bits_array = np.array(self.bar_stft_bits_all)
        self.bar_stft_time_array = np.array(self.bar_stft_time_all)
        self.bar_stft_frequency_array = np.array(self.bar_stft_frequency_all)

        self.bar_stft_all_for_both_stations = []
        self.bar_stft_bits_all_for_both_stations = []
        self.bar_stft_time_all_for_both_stations = []
        self.bar_stft_frequency_all_for_both_stations = []

        self.acc_stft_array = np.array(self.acc_stft_all)
        self.acc_stft_bits_array = np.array(self.acc_stft_bits_all)
        self.acc_stft_time_array = np.array(self.acc_stft_time_all)
        self.acc_stft_frequency_array = np.array(self.acc_stft_frequency_all)

        self.acc_stft_all_for_both_stations = []
        self.acc_stft_bits_all_for_both_stations = []
        self.acc_stft_time_all_for_both_stations = []
        self.acc_stft_frequency_all_for_both_stations = []

        for number_stations_is_2 in range(2):
            self.acc_stft_all_for_both_stations.append(self.acc_stft_array)
            self.acc_stft_bits_all_for_both_stations.append(self.acc_stft_bits_array)
            self.acc_stft_time_all_for_both_stations.append(self.acc_stft_time_array)
            self.acc_stft_frequency_all_for_both_stations.append(self.acc_stft_frequency_array)

            self.bar_stft_all_for_both_stations.append(self.bar_stft_array)
            self.bar_stft_bits_all_for_both_stations.append(self.bar_stft_bits_array)
            self.bar_stft_time_all_for_both_stations.append(self.bar_stft_time_array)
            self.bar_stft_frequency_all_for_both_stations.append(self.bar_stft_frequency_array)

        # Add columns with mesh
        self.df_data["barometer_stft"] = self.bar_stft_all_for_both_stations
        self.df_data["barometer_stft_bits"] = self.bar_stft_bits_all_for_both_stations
        self.df_data["barometer_stft_time_s"] = self.bar_stft_time_all_for_both_stations
        self.df_data["barometer_stft_frequency_s"] = self.bar_stft_frequency_all_for_both_stations

        self.df_data["accelerometer_stft"] = self.acc_stft_all_for_both_stations
        self.df_data["accelerometer_stft_bits"] = self.acc_stft_bits_all_for_both_stations
        self.df_data["accelerometer_stft_time_s"] = self.acc_stft_time_all_for_both_stations
        self.df_data["accelerometer_stft_frequency_s"] = self.acc_stft_frequency_all_for_both_stations

    def yticks_for_1_sensor(self):
        self.yticks = rpd_mesh.find_ylabel_tfr(df=self.df_data,
                                               mesh_tfr_label=["audio_stft_bits"],
                                               sig_id_label="station_id")

        self.assertEqual(self.yticks, ["1234567890", "2345678901"])

    def yticks_for_more_sensor(self):
        self.yticks = rpd_mesh.find_ylabel_tfr(df=self.df_data,
                                               mesh_tfr_label=["audio_stft_bits", "accelerometer_stft_bits"],
                                               sig_id_label="station_id")

        self.assertEqual(self.yticks, ["1234567890", "2345678901"])

    def tearDown(self):
        self.start_time = None
        self.end_time = None
        self.sample_rate_audio = None
        self.signal_time_audio = None
        self.frequency = None
        self.amplitude = None
        self.sinewave_audio = None
        self.audio_STFT = None
        self.audio_STFT_bits = None
        self.audio_time_stft_s = None
        self.audio_frequency_stft_hz = None
        self.sample_rate_acc = None
        self.signal_time_acc = None
        self.length_for_signal = None
        self.sinewave_acc_base = None
        self.points_per_row = None
        self.sinewave_acc = None
        self.acc_stft_all = None
        self.acc_stft_time_all = None
        self.acc_stft_bits_all = None
        self.acc_stft_frequency_all = None
        self.acc_STFT = None
        self.acc_STFT_bits = None
        self.acc_time_stft_s = None
        self.acc_frequency_stft_hz = None
        self.dict_to_df_multiple = None
        self.df_data = None
        self.acc_stft_array = None
        self.acc_stft_bits_array = None
        self.acc_stft_time_array = None
        self.acc_stft_frequency_array = None
        self.acc_stft_all_for_both_stations = None
        self.acc_stft_bits_all_for_both_stations = None
        self.acc_stft_time_all_for_both_stations = None
        self.acc_stft_frequency_all_for_both_stations = None
        self.wiggle_num = None
        self.sample_rate_barometer = None
        self.signal_time_barometer = None
        self.sinewave_barometer_base = None
        self.sinewave_barometer = None
        self.bar_stft_all = None
        self.bar_stft_time_all = None
        self.bar_stft_bits_all = None
        self.bar_stft_frequency_all = None
        self.bar_STFT = None
        self.bar_STFT_bits = None
        self.bar_time_stft_s = None
        self.bar_frequency_stft_hz = None
        self.bar_stft_array = None
        self.bar_stft_bits_array = None
        self.bar_stft_time_array = None
        self.bar_stft_frequency_array = None
        self.bar_stft_all_for_both_stations = None
        self.bar_stft_bits_all_for_both_stations = None
        self.bar_stft_time_all_for_both_stations = None
        self.bar_stft_frequency_all_for_both_stations = None

if __name__ == '__main__':
    unittest.main()
