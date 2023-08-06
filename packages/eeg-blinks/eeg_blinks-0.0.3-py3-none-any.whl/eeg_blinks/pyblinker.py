import logging

import pandas as pd

from eeg_blinks import default_setting
from eeg_blinks.vislab.blink_posi_vislab import BlinkFrameValley
from eeg_blinks.utilities.extractBlinkProperties import BlinkProperties
from eeg_blinks.utilities.fit_blink import FitBlinks
from eeg_blinks.utilities.getCandidateSignal import PrepareSelection,ChannelSelection
from eeg_blinks.utilities.misc import create_annotation
from eeg_blinks.viz.viz_pd import viz_complete_blink_prop

logging.getLogger().setLevel(logging.INFO)


class BlinkDetector:
    def __init__(self, raw_data, visualize=False, annot_label=None,filter_bad=False):
        self.filter_bad=filter_bad
        self.raw_data = raw_data
        self.viz_data = visualize
        self.annot_label = annot_label
        self.sfreq = self.raw_data.info['sfreq']
        self.params = default_setting.params
        self.channel_list = self.raw_data.ch_names
        self.all_data_info = []
        self.all_data = []

    def prepare_raw_signal(self):
        self.raw_data.pick_types(eeg=True)
        self.raw_data.filter(0.5, 20.5, fir_design='firwin')
        self.raw_data.resample(100)
        return self.raw_data

    def process_channel_data(self, channel):

        df = BlinkFrameValley(self.raw_data.get_data(picks=channel)[0], self.sfreq, self.params, channel, self.sfreq).blink_frame
        df = FitBlinks(data=self.raw_data.get_data(picks=channel)[0], df=df).frame_blinks
        # df = extracBlinkProperties(self.raw_data.get_data(picks=channel)[0], df, self.sfreq)
        df=BlinkProperties(self.raw_data.get_data(picks=channel)[0], df, self.sfreq).df_res
        d = PrepareSelection(signal=self.raw_data.get_data(picks=channel)[0], df=df, params=self.params, ch=channel).get_param_for_selection()
        self.all_data_info.append(dict(df=df, ch=channel))
        self.all_data.append(d)

    @staticmethod
    def filter_point(ch,all_data_info):
        return list(filter(lambda all_data_info: all_data_info['ch'] == ch, all_data_info))[0]


    def filter_bad_blink(self,df):
        # filter_bad = False
        if self.filter_bad:
            df = df[df['blink_quality'] == 'Good']
        return df


    def generate_viz(self,data,df):
        fig_data = [viz_complete_blink_prop(data, row, self.sfreq) for index, row in df.iterrows()]

        return fig_data
    def get_blink_stat(self):
        for channel in self.channel_list:
            self.process_channel_data(channel)

        ch_blink_stat = pd.DataFrame(self.all_data)
        ch_selected = ChannelSelection(df=ch_blink_stat, params=self.params).df
        ch = ch_selected.loc[0, 'ch']
        nGoodBlinks = ch_selected.loc[0, 'numberGoodBlinks']
        data = self.raw_data.get_data(picks=ch)[0]
        rep_blink_channel = self.filter_point(ch,self.all_data_info)
        df = rep_blink_channel['df']

        df=self.filter_bad_blink(df)
        # df.to_pickle('unit_test_1.pkl')

        annot_description = self.annot_label if self.annot_label else 'eye_blink'
        annot = create_annotation(df, self.sfreq, annot_description)
        if self.viz_data:
            fig_data=self.generate_viz(self,data,df)
            return annot, ch, nGoodBlinks, fig_data, df

        return annot, ch, nGoodBlinks,df