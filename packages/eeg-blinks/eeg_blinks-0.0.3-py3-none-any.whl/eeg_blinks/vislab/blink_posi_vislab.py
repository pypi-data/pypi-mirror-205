import logging
import numpy as np
import pandas as pd
from eeg_blinks.vislab.getBlinkPositions_vislab import getBlinkPosition
from eeg_blinks.utilities.zero_crossing import left_right_zero_crossing

logging.basicConfig(level=logging.INFO)

class BlinkFrameValley:
    def __init__(self, data, sfreq, params, ch, srate):
        self.data = data
        self.sfreq = sfreq
        self.params = params
        self.ch = ch
        self.srate = srate
        self._get_blink_position()
        self._get_max_values()
        self._compute_duration()
        self._filter_duration()
        self._get_zero_crossing()

    def _get_blink_position(self):
        self.ch_data = getBlinkPosition(self.params, self.sfreq, blinkComp=self.data, ch=self.ch)
        self.startBlinks = self.ch_data['start_blink']
        self.endBlinks = self.ch_data['end_blink']

    def _get_max_frame(self, startBlinks, endBlinks):
        blinkRange = np.arange(startBlinks, endBlinks + 1)
        blink_frame = self.data[startBlinks:endBlinks + 1]
        maxValues = np.amax(blink_frame)
        maxFrames = blinkRange[np.argmax(blink_frame)]
        return maxValues, maxFrames

    def _get_max_values(self):
        maxValues, maxFrames = zip(*[self._get_max_frame(dstartBlinks, dendBlinks) for
                                     dstartBlinks, dendBlinks in zip(self.startBlinks, self.endBlinks)])
        self.maxFrames = np.array(maxFrames)
        self.maxValues = np.array(maxValues)
        self.outerStarts = np.append(0, self.maxFrames[0:-1])
        self.outerEnds = np.append(self.maxFrames[1:], self.data.size)

    def _compute_duration(self):
        self.blink_frame = pd.DataFrame(dict(maxFrames=self.maxFrames, maxValues=self.maxValues,
                                             startBlinks=self.startBlinks, endBlinks=self.endBlinks,
                                             outerStarts=self.outerStarts, outerEnds=self.outerEnds))
        self.blink_frame['blink_duration'] = (self.blink_frame['endBlinks'] - self.blink_frame['startBlinks']) / self.srate

    def _filter_duration(self):
        self.blink_frame = self.blink_frame[self.blink_frame.blink_duration.ge(0.05)].reset_index(drop=True)



    def _get_zero_crossing(self):
        self.blink_frame[['leftZero', 'rightZero']] = self.blink_frame.apply(lambda x: left_right_zero_crossing(self.data,x['maxFrames'], x['outerStarts'],
                                                                                        x['outerEnds']), axis=1,
                                                     result_type="expand")



