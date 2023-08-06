import logging

import numpy as np
from tqdm import tqdm

from eeg_blinks.utilities.misc import mad_matlab

logging.getLogger().setLevel(logging.INFO)


def getBlinkPosition(params, sfreq, blinkComp=None, ch='No_channel'):
    """

    % Parameters:
    %    blinkComp       independent component (IC) of eye-related
    %                    activations derived from EEG.  This component should
    %                    be "upright"
    %    srate:         sample rate at which the EEG data was taken
    %    stdTreshold    number of standard deviations above threshold for blink
    %    blinkPositions (output) 2 x n array with start and end frames of blinks
        :param params:
        :param sfreq:
        :param signal_eeg:
        :param ch:
        :return:
    """


    # Ensure 1D array
    assert blinkComp.ndim == 1
    # blinkComp = signal_eeg
    mu = np.mean(blinkComp, dtype=np.float64)

    mad_val = mad_matlab(blinkComp)
    robustStdDev = 1.4826 * mad_val

    minBlink = params['minEventLen'] * sfreq  # minimum blink frames
    threshold = mu + params['stdThreshold'] * robustStdDev  # actual threshold

    '''
    % The return structure.  Initially there is room for an event at every time
    % tick, to be trimmed later
    '''

    inBlink = False
    startBlinks = []
    endBlinks = []
    # kk=blinkComp.size
    for index in tqdm(range(blinkComp.size), desc=f"Get blink start and end for channel {ch}"):
        Drule = ~inBlink and (blinkComp[index] > threshold)
        if Drule:
            start = index
            inBlink = np.ones((1), dtype=bool)

        # if previous point was in a blink and signal retreats below threshold and duration greater than discard
        # threshold
        krule = (inBlink == True) and (blinkComp[index] < threshold)
        if krule:
            if (index - start) > minBlink:
                startBlinks.append(start)  # t_up
                endBlinks.append(index)  # t_dn

            inBlink = False

    arr_startBlinks = np.array(startBlinks)
    arr_endBlinks = np.array(endBlinks)

    # Now remove blinks that aren't separated
    positionMask = np.ones(arr_endBlinks.size, dtype=bool)

    x = (arr_startBlinks[1:] - arr_endBlinks[:-1]) / sfreq  # Calculate the blink duration
    y = np.argwhere(x <= 0.05)  # Index where blink duration is less than 0.05 sec
    positionMask[y] = np.zeros((1), dtype=bool)
    positionMask[y + 1] = np.zeros((1), dtype=bool)
    # v=arr_startBlinks[positionMask]
    blink_position = {'start_blink': arr_startBlinks[positionMask],
                      'end_blink': arr_endBlinks[positionMask],
                      'ch': ch}

    return blink_position
