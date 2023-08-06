import logging

import numpy as np
import pandas as pd

from eeg_blinks.utilities.misc import mad_matlab

logging.getLogger().setLevel(logging.INFO)


def _goodblink_based_corr_median_std(df, correlationThreshold):
    R2 = df['leftR2'] >= correlationThreshold
    R3 = df['rightR2'] >= correlationThreshold

    # Now calculate the cutoff ratios -- use default for the values
    good_data = df.loc[R2.values & R3.values, :]
    bestValues = good_data['maxValues'].array

    specifiedMedian = np.nanmedian(bestValues)
    specifiedStd = 1.4826 * mad_matlab(bestValues)

    return R2, R3, specifiedMedian, specifiedStd


def get_mask_optimise(df, indicesNaN, correlationThreshold, zScoreThreshold):
    """
    "used Feb 02 2023"
    The calculation of bestmedian,worst median, worrst rbobustst
    is from https://github.com/VisLab/EEG-Blinks/blob/16b6ea04101ecfa74fb1c9cbceb037324572687e/blinker/utilities/extractBlinks.m#L97

    :param df:
    :param indicesNaN:
    :param correlationThreshold:
    :param zScoreThreshold:
    :return:
    """
    R1 = ~indicesNaN
    R2, R3, specifiedMedian, specifiedStd = _goodblink_based_corr_median_std(df, correlationThreshold)

    R4 = df['maxValues'] >= max(0, specifiedMedian - zScoreThreshold * specifiedStd)
    R5 = df['maxValues'] <= specifiedMedian + zScoreThreshold * specifiedStd
    bool_test = R1.values & R2.values & R3.values & R4.values & R5.values

    return bool_test, specifiedMedian, specifiedStd


def getGoodBlinkMask(df, zThresholds):
    "used Feb 02 2023"
    ## These is the default value
    correlationThreshold_s1, correlationThreshold_s2, zScoreThreshold_s1, zScoreThreshold_s2 = zThresholds

    df['rightR2'] = df['rightR2'].abs()
    df_data = df[['leftR2', 'rightR2', 'maxValues']]
    G=df_data.isnull()
    indicesNaN = df_data.isnull().any(axis='columns')

    ### GET MASK OPTIMISE

    goodMaskTop_bool, bestMedian, bestRobustStd = get_mask_optimise(df_data, indicesNaN, correlationThreshold_s1,
                                                                    zScoreThreshold_s1)

    df_s2_bool, worstMedian, worstRobustStd = get_mask_optimise(df_data, indicesNaN, correlationThreshold_s2,
                                                                zScoreThreshold_s2)

    goodBlinkMask = np.reshape(goodMaskTop_bool | df_s2_bool, (-1, 1))  # Get any TRUE
    df['blink_quality'] = 'Good'
    df[['blink_quality']] = df[['blink_quality']].where(goodBlinkMask, other='Reject')
    return df, bestMedian, bestRobustStd




class BlinkProperties:
    '''
    Return a structure with blink shapes and properties for individual blinks
    '''
    def __init__(self, data, df, srate):
        self.data = data
        self.df = df
        self.srate = srate
        self.shutAmpFraction = 0.9
        self.pAVRThreshold = 3
        self.zThresholds = (0.90, 0.98, 2, 5)
        self.df_res=[]
        self.reset_index()
        self.get_good_blink_mask()
        self.set_blink_velocity()
        self.set_blink_duration()
        self.set_blink_amp_velocity_ratio_zero_to_max()
        self.amplitude_velocity_ratio_base()
        self.amplitude_velocity_ratio_tent()
        self.time_zero_shut()
        self.time_base_shut()
        self.extract_other_times()

    def reset_index(self):
        self.df.reset_index(drop=True, inplace=True)

    def get_good_blink_mask(self):
        self.df, self.bestMedian, self.bestRobustStd = getGoodBlinkMask(self.df, self.zThresholds)

    def set_blink_velocity(self):
        self.signal_l = self.data.shape[0]
        self.blinkVelocity = np.diff(self.data)

    def set_blink_duration(self):
        cols_int = ['rightBase']
        self.df[cols_int] = self.df[cols_int].astype(int)
        self.df['durationBase'] = (self.df['rightBase'] - self.df['leftBase']) / self.srate
        self.df['durationTent'] = (self.df['rightXIntercept'] - self.df['leftXIntercept']) / self.srate
        self.df['durationZero'] = (self.df['rightZero'] - self.df['leftZero']) / self.srate
        self.df['durationHalfBase'] = (self.df['rightBaseHalfHeight'] - self.df['leftBaseHalfHeight'] + 1) / self.srate
        self.df['durationHalfZero'] = (self.df['rightZeroHalfHeight'] - self.df['leftZeroHalfHeight'] + 1) / self.srate

    def set_blink_amp_velocity_ratio_zero_to_max(self):
        self.df[['leftZero', 'rightZero']] = self.df[['leftZero', 'rightZero']].astype(int)
        self.df['peaksPosVelZero'] = self.df.apply(lambda x: x['leftZero'] + np.argmax(self.blinkVelocity[x['leftZero']:x['maxFrames'] + 1]), axis=1)
        self.df['RRC'] = self.data[self.df['maxFrames'] - 1] / self.blinkVelocity[self.df['peaksPosVelZero']]
        self.df['posAmpVelRatioZero'] = (100 * abs(self.df['RRC'])) / self.srate
        self.df['downStrokevelFrame_del'] = self.df.apply(lambda x: x['maxFrames'] + np.argmin(self.blinkVelocity[x['maxFrames']:x['rightZero'] + 1]), axis=1)
        self.df['TTT'] = self.data[self.df['maxFrames'] - 1] / self.blinkVelocity[self.df['downStrokevelFrame_del']]
        self.df['negAmpVelRatioZero'] = (100 * abs(self.df['TTT'])) / self.srate

    def amplitude_velocity_ratio_base(self):
        self.df['peaksPosVelBase'] = self.df.apply(
            lambda x: x['leftBase'] + np.argmax(self.blinkVelocity[x['leftBase']:x['maxFrames'] + 1]), axis=1)
        self.df['KKK'] = self.data[self.df['maxFrames'] - 1] / self.blinkVelocity[self.df['peaksPosVelBase']]
        self.df['posAmpVelRatioBase'] = (100 * abs(self.df['KKK'])) / self.srate

        self.df['downStroke_del'] = self.df.apply(
            lambda x: x['maxFrames'] + np.argmin(self.blinkVelocity[x['maxFrames']:x['rightBase'] + 1]), axis=1)
        self.df['KKK'] = self.data[self.df['maxFrames'] - 1] / self.blinkVelocity[self.df['downStroke_del']]
        self.df['negAmpVelRatioBase'] = (100 * abs(self.df['KKK'])) / self.srate

    def amplitude_velocity_ratio_tent(self):
        self.df['pop'] = self.data[self.df['maxFrames'] - 1] / self.df['averRightVelocity']
        self.df['negAmpVelRatioTent'] = (100 * abs(self.df['pop'])) / self.srate

        self.df['opi'] = self.data[self.df['maxFrames'] - 1] / self.df['averLeftVelocity']
        self.df['WE'] = (100 * abs(self.df['opi']))
        self.df['posAmpVelRatioTent'] = self.df['WE'] / self.srate

    def time_zero_shut(self):
        self.df['closingTimeZero'] = (self.df['maxFrames'] - self.df['leftZero']) / self.srate
        self.df['reopeningTimeZero'] = (self.df['rightZero'] - self.df['maxFrames']) / self.srate

        self.df['ampThreshhold'] = self.shutAmpFraction * self.df['maxValues']
        self.df['start_shut_tzs'] = self.df.apply(
            lambda x: np.argmax(self.data[x['leftZero']:x['rightZero'] + 1] >= x['ampThreshhold']), axis=1)

        self.df['endShut_tzs'] = self.df.apply(
            lambda x: np.argmax(self.data[x['leftZero']:x['rightZero'] + 1][x['start_shut_tzs'] + 1:-1] <
                                self.shutAmpFraction * x['maxValues']), axis=1)

        ## PLease expect error here, some value maybe zero or lead to empty cell
        self.df['endShut_tzs'] = self.df['endShut_tzs'] + 1  ## temporary  to delete
        self.df['timeShutZero'] = self.df.apply(
            lambda x: 0 if x['endShut_tzs'] == np.isnan else x['endShut_tzs'] / self.srate, axis=1)
    def time_base_shut(self):
        self.df['ampThreshhold_tbs'] = self.shutAmpFraction * self.df['maxValues']
        self.df['start_shut_tbs'] = self.df.apply(
            lambda x: np.argmax(self.data[x['leftBase']:x['rightBase'] + 1] >= x['ampThreshhold_tbs']), axis=1)

        self.df['endShut_tbs'] = self.df.apply(
            lambda x: np.argmax(self.data[x['leftBase']:x['rightBase'] + 1][x['start_shut_tbs']:-1] <
                                self.shutAmpFraction * x['maxValues']), axis=1)

        self.df['timeShutBase'] = self.df.apply(
            lambda x: 0 if x['endShut_tbs'] == np.isnan else (x['endShut_tbs'] / self.srate), axis=1)

        ## Time shut tent
        self.df['closingTimeTent'] = (self.df['xIntersect'] - self.df['leftXIntercept']) / self.srate
        self.df['reopeningTimeTent'] = (self.df['rightXIntercept'] - self.df['xIntersect']) / self.srate

        self.df['ampThreshhold_tst'] = self.shutAmpFraction * self.df['maxValues']

        self.df[['leftXIntercept_int', 'rightXIntercept_int']] = self.df[['leftXIntercept', 'rightXIntercept']].astype(
            int)


        # warnings.warn('New upgrade')
        self.df=self.df[self.df.leftXIntercept_int<self.df.rightXIntercept_int]
        self.df.reset_index(drop=True,inplace=True)
        self.df['start_shut_tst'] = self.df.apply(
            lambda x: np.argmax(self.data[x['leftXIntercept_int']:x['rightXIntercept_int'] + 1] >= x['ampThreshhold']), axis=1)

        self.df['endShut_tst'] = self.df.apply(
            lambda x: np.argmax(self.data[x['leftXIntercept_int']:x['rightXIntercept_int'] + 1][x['start_shut_tst']:-1] <
                                self.shutAmpFraction * x['maxValues']), axis=1)
        ### Just in case got other issue, use this back, do not delete
        ## Since we already remove imblanace left_right intercept, maybe dah xperlu kot bawah ni
        # df['start_shut_tst'] = df.apply(
        #     lambda x: _start_shut(data, x['leftXIntercept_int'], x['rightXIntercept_int'], x['ampThreshhold']), axis=1)
        #
        #
        #
        # df['endShut_tst'] = df.apply(
        #     lambda x: _end_shut(data, x['leftXIntercept_int'], x['rightXIntercept_int'], x['start_shut_tst'],
        #                         x['maxValues'], shutAmpFraction), axis=1)

        self.df['timeShutTent'] = self.df.apply(
            lambda x: 0 if x['endShut_tst'] == np.isnan else (x['endShut_tst'] / self.srate), axis=1)

    def extract_other_times(self):
        ## Other times
        self.df['peakMaxBlink '] = self.df['maxValues']
        self.df['peakMaxTent'] = self.df['yIntersect']
        self.df['peakTimeTent'] = self.df['xIntersect'] / self.srate
        self.df['peakTimeBlink'] = self.df['maxFrames'] / self.srate

        dfcal = self.df[['maxFrames', 'peaksPosVelBase', 'peaksPosVelZero']]

        df_t = pd.DataFrame.from_records([[self.signal_l] * 3], columns=['maxFrames', 'peaksPosVelBase', 'peaksPosVelZero'])

        dfcal = pd.concat([dfcal, df_t]).reset_index(drop=True)

        dfcal['ibmx'] = dfcal.maxFrames.diff().shift(-1)

        dfcal['interBlinkMaxAmp'] = dfcal['ibmx'] / self.srate

        dfcal['ibmvb'] = 1 - dfcal['peaksPosVelBase']
        dfcal['interBlinkMaxVelBase'] = dfcal['ibmvb'] / self.srate  # peaksPosVelBase == velFrame

        dfcal['ibmvz'] = 1 - dfcal['peaksPosVelZero']
        dfcal['interBlinkMaxVelZero'] = dfcal['ibmvz'] / self.srate

        dfcal.drop(dfcal.tail(1).index, inplace=True)  # drop last n rows# peaksPosVelZero == velFrame
        dfnew = self.df[['maxValues', 'posAmpVelRatioZero']]

        R1 = dfnew['posAmpVelRatioZero'] < self.pAVRThreshold

        th_bm_brs = self.bestMedian - self.bestRobustStd
        R2 = dfnew['maxValues'] < th_bm_brs
        pMask = pd.concat([R1, R2], axis=1)
        pMasks = pMask.all(1)
        df_res = pd.merge(self.df, dfcal, on=['maxFrames'])
        self.df_res = df_res[~pMasks].reset_index(drop=True)
        # return df_res

