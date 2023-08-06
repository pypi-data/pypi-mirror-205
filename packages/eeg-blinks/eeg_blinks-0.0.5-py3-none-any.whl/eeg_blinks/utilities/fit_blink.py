

import logging

from eeg_blinks.utilities.zero_crossing import (_get_half_height,
                                                compute_fit_range, lines_intersection)
from eeg_blinks.vislab.base_left_right import create_left_right_base_vislab

logging.getLogger().setLevel(logging.INFO)

class FitBlinks:

    def __init__(self, data=None, df=None):
        self.data = data
        self.df = df
        self.frame_blinks=[]
        self.baseFraction = 0.1
        self.cols_half_height = ['leftZeroHalfHeight', 'rightZeroHalfHeight', 'leftBaseHalfHeight', 'rightBaseHalfHeight']
        self.cols_fit_range = ['xLeft', 'xRight', 'leftRange', 'rightRange',
                               'blinkBottomPoint_l_Y', 'blinkBottomPoint_l_X', 'blinkTopPoint_l_Y', 'blinkTopPoint_l_X',
                               'blinkBottomPoint_r_X', 'blinkBottomPoint_r_Y', 'blinkTopPoint_r_X', 'blinkTopPoint_r_Y']
        self.cols_lines_intesection = ['leftSlope', 'rightSlope', 'averLeftVelocity', 'averRightVelocity',
                                       'rightR2', 'leftR2', 'xIntersect', 'yIntersect', 'leftXIntercept',
                                       'rightXIntercept', 'xLineCross_l', 'yLineCross_l', 'xLineCross_r', 'yLineCross_r']
        self.fit()


    def fit(self):
        self.frame_blinks = create_left_right_base_vislab(self.data, self.df)
        self.frame_blinks[self.cols_half_height] = self.frame_blinks.apply(lambda x: _get_half_height(self.data, x['maxFrames'], x['leftZero'], x['rightZero'],
                                                                                       x['leftBase'], x['outerEnds']), axis=1,
                                                       result_type="expand")
        self.frame_blinks[self.cols_fit_range] = self.frame_blinks.apply(lambda x: compute_fit_range(self.data, x['maxFrames'], x['leftZero'], x['rightZero'],
                                                                                      self.baseFraction, top_bottom=True), axis=1,
                                                     result_type="expand")
        self.frame_blinks = self.frame_blinks.dropna()
        self.frame_blinks['nsize_xLeft'] = self.frame_blinks.apply(lambda x: x['xLeft'].size, axis=1)
        self.frame_blinks['nsize_xRight'] = self.frame_blinks.apply(lambda x: x['xRight'].size, axis=1)
        self.frame_blinks = self.frame_blinks[~(self.frame_blinks['nsize_xLeft'] <= 1) & ~(self.frame_blinks['nsize_xRight'] <= 1)]
        self.frame_blinks.reset_index(drop=True, inplace=True)
        self.frame_blinks[self.cols_lines_intesection] = self.frame_blinks.apply(lambda x: lines_intersection(xRight=x['xRight'], xLeft=x['xLeft'],
                                                                                          yRight=self.data[x['xRight']], yLeft=self.data[x['xLeft']],
                                                                                          dic_type=False), axis=1, result_type="expand")
