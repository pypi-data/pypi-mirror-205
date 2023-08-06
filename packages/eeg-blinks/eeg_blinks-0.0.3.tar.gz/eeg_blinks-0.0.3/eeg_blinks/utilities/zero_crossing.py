import warnings

import numpy as np


def _get_interception_at_xaxis(xlist, ylist):
    domain = np.std(xlist) * np.arange(-1, 2, 2) + np.mean(xlist)
    p = np.polynomial.Polynomial.fit(xlist, ylist, 1, domain=domain)
    XIntercept = p.roots()[0]  # 6.336226562500000e+03
    return XIntercept, p


def get_xy_line_cross(line_eq):
    xLineCross = line_eq.roots()[0]
    yLineCross = line_eq(xLineCross)
    return xLineCross,yLineCross


def _get_tent_coord(xLeft, yLeft,xRight, yRight):
    ## Let get the tent point
    left_line = np.polynomial.Polynomial.fit(xLeft, yLeft, 1, domain=[-1, 1])
    right_line = np.polynomial.Polynomial.fit(xRight, yRight, 1, domain=[-1, 1])
    xIntersect = (left_line - right_line).roots()[0]  # x0 6.192071289062500e+03
    yIntersect = left_line(xIntersect)  # y0=9.931675910949707

    ## Important for plotting
    xLineCross_l,yLineCross_l=get_xy_line_cross(left_line)


    xLineCross_r,yLineCross_r=get_xy_line_cross(right_line)


    return xIntersect,yIntersect,xLineCross_l,yLineCross_l,xLineCross_r,yLineCross_r

def get_line_intersection_slope(xIntersect,yIntersect,leftXIntercept,rightXIntercept):
    leftSlope = yIntersect / (xIntersect - leftXIntercept)  # 0.36513907
    rightSlope = yIntersect / (xIntersect - rightXIntercept)  # -0.068895683
    return leftSlope,rightSlope

def get_average_velocity(pLeft,pRight,xLeft,xRight):
    averLeftVelocity = pLeft.coef[1] / np.std(xLeft)  # 0.36513701
    averRightVelocity = pRight.coef[1] / np.std(xRight)  # -0.068895057

    return averLeftVelocity,averRightVelocity
def  line_corrcoef(p,xlist,ylist):

    ffit = np.polyval(p.coef, xlist)

    R2 = np.corrcoef(ylist.flatten(), ffit.flatten())[0, 1]
    return R2


def lines_intersection(xRight=None, xLeft=None, yRight=None, yLeft=None, dic_type=True):
    """
    Source:
    https://stackoverflow.com/q/68182079/6446053

    I think tent is the top most point
    leftSlope
    The slope of the left tent line or NaN if the tent line doesn’t exist.

    rightSlope
    Slope of the right blink tent line or NaN if the tent line doesn’t exist.

    averLeftVelocity
    The velocity as estimated by the left tent line.

    averRightVelocity
    The velocity as estimated by the right tent line.

    leftR2
    The correlation of the left tent line with the 80% blink upstroke. [A numeric value or NaN if the tent line doesn’t exist.]

    rightR2
    The correlation of the right tent line with the 80% blink downstroke. [A numeric value or NaN if the tent line doesn’t exist.]

    xIntersect
    The x-coordinate of the intersection of the left and right tent line with the x-axis.
    [A numeric value or NaN if the tent line doesn’t exist.]

    yIntersect
    The y-coordinate of the intersection of the left and right tent line with the x-axis.
    [A numeric value or NaN if the tent line doesn’t exist.]

    leftXIntercept
    An integer giving the frame number of the intersection of the left tent line with the x-axis (or NaN if the tent line doesn’t exist).

    rightXIntercept
    An integer giving the frame number of the intersection of the right tent line with the x-axis (or NaN if the tent line doesn’t exist).


    """

    rightXIntercept, pRight = _get_interception_at_xaxis(xRight, yRight)
    leftXIntercept, pLeft = _get_interception_at_xaxis(xLeft, yLeft)



    # ## Let get the tent point
    xIntersect,yIntersect,xLineCross_l,yLineCross_l,xLineCross_r,yLineCross_r=_get_tent_coord(xLeft, yLeft,xRight, yRight)

    leftSlope,rightSlope=get_line_intersection_slope(xIntersect,yIntersect,leftXIntercept,rightXIntercept)

    averLeftVelocity,averRightVelocity=get_average_velocity(pLeft,pRight,xLeft,xRight)

    rightR2,leftR2 =line_corrcoef(pRight,xRight,yRight),line_corrcoef(pLeft,xLeft,yLeft)


    # from eeg_blinks.viz.viz_sanity import viz_line_intersection
    # viz_line_intersection(candidateSignal,xRight,xLeft,leftXIntercept,rightXIntercept,
    #                       xIntersect,yIntersect)

    if dic_type:
        d = dict(leftSlope=leftSlope, rightSlope=rightSlope, averLeftVelocity=averLeftVelocity,
                 averRightVelocity=averRightVelocity, rightR2=rightR2, leftR2=leftR2)
        return d
    else:
        return leftSlope, rightSlope, averLeftVelocity, averRightVelocity, \
               rightR2, leftR2, xIntersect, yIntersect, leftXIntercept, rightXIntercept, \
               xLineCross_l, yLineCross_l, xLineCross_r, yLineCross_r


def left_right_zero_crossing(candidateSignal, maxFrame, outerStarts, outerEnds):
    ### Latest as of 29 April 2022 which is more efficient
    theRange = np.arange(int(outerStarts), int(maxFrame))
    sInd_leftZero = np.flatnonzero(candidateSignal[theRange] < 0)

    if (sInd_leftZero.size != 0):
        leftZero = theRange[sInd_leftZero[-1]]

    else:
        extreme_outerStartss = np.arange(0, maxFrame)
        extreme_outerStartss = extreme_outerStartss.astype(int)
        sInd_rightZero_ex = np.flatnonzero(candidateSignal[extreme_outerStartss] < 0)[-1]
        leftZero = extreme_outerStartss[sInd_rightZero_ex]

    theRange = np.arange(int(maxFrame), int(outerEnds))
    sInd_rightZero = np.flatnonzero(candidateSignal[theRange] < 0)

    if (sInd_rightZero.size != 0):
        rightZero = theRange[sInd_rightZero[0]]
    else:
        """
        We take extreme remedy by extending the outerEnds to the maximum
        """
        extreme_outerEns = np.arange(maxFrame, candidateSignal.shape)
        extreme_outerEns = extreme_outerEns.astype(int)
        sInd_rightZero_ex_s = np.flatnonzero(candidateSignal[extreme_outerEns] < 0)

        if (sInd_rightZero_ex_s.size != 0):
            # This usually happen for end of signal
            sInd_rightZero_ex = sInd_rightZero_ex_s[0]
            rightZero = extreme_outerEns[sInd_rightZero_ex]
        else:
            return leftZero, None

    if leftZero > maxFrame:
        raise ValueError('something is not right')

    if maxFrame > rightZero:
        raise ValueError('something is not right')

    # from eeg_blinks.viz.viz_sanity import _viz_sanity_zero_crossing
    # _viz_sanity_zero_crossing(leftZero, rightZero, maxFrame, candidateSignal, 'Zero_Crossing')

    return leftZero, rightZero


def get_up_down_stroke(maxFrame, leftZero, rightZero):
    upStroke = np.arange(leftZero, maxFrame)
    downStroke = np.arange(maxFrame, rightZero)
    return upStroke, downStroke


def _maxPosVelFrame(blinkVelocity, maxFrame, leftZero, rightZero):
    maxFrame, leftZero, rightZero = int(maxFrame), int(leftZero), int(rightZero)
    upStroke, downStroke = get_up_down_stroke(maxFrame, leftZero, rightZero)
    maxPosVelFrame = np.argmax(blinkVelocity[upStroke])
    maxPosVelFrame = maxPosVelFrame + upStroke[0]

    if len(blinkVelocity[downStroke])>0:
        maxNegVelFrame = np.argmin(blinkVelocity[downStroke])
        maxNegVelFrame = maxNegVelFrame + downStroke[0]
    else:
        warnings.warn('Force nan but require further invesitigation why happen like this')
        maxNegVelFrame=np.nan


    return maxPosVelFrame, maxNegVelFrame


def _get_left_base(blinkVelocity, leftOuter, maxPosVelFrame):
    leftOuter, maxPosVelFrame = int(leftOuter), int(maxPosVelFrame)
    leftBase = np.arange(leftOuter, maxPosVelFrame)

    leftBaseVelocity = np.flip(blinkVelocity[leftBase])

    leftBaseIndex = np.argmax(leftBaseVelocity <= 0)

    leftBase = maxPosVelFrame - leftBaseIndex

    return leftBase


def _get_right_base(candidateSignal, blinkVelocity, rightOuter, maxNegVelFrame):
    # Start Line 102 Matlab
    rightOuter, maxNegVelFrame = int(rightOuter), int(maxNegVelFrame)
    a_tend = np.minimum(rightOuter, candidateSignal.size)

    if maxNegVelFrame > a_tend:
        # warnings.warn(
        #     'Failed to fit blink %s but due to MaxNegVelFrame: %s larger than a_tend: %s .For now I will skip this file'
        #     % (number, maxNegVelFrame, a_tend))
        return None

    rightBase = np.arange(maxNegVelFrame, a_tend)  # Line 102 matlab

    # hh=blinkVelocity.size
    # nn=np.max(rightBase)

    if rightBase.size == 0:
        return None

    if np.max(rightBase) >= blinkVelocity.size:
        # For some reason, the original rightBase has index value greate than blinkVelocity which cause index error.
        # To address this issue, we remove some value
        rightBase = rightBase[:-1]
        if np.max(rightBase) >= blinkVelocity.size:
            raise ValueError('Please strategise how to address this')

    rightBaseVelocity = blinkVelocity[rightBase]  #

    '''
    if rightBaseIndex.size == 0:  # Line 108 Matlab
        rightBaseIndex = 0
    '''
    rightBaseIndex = np.argmax(rightBaseVelocity >= 0)
    # try:
    #     rightBaseIndex = np.argwhere(rightBaseVelocity >= 0)[0]
    # except IndexError:  # Line 108 Matlab
    #     rightBaseIndex = 0

    rightBase = maxNegVelFrame + rightBaseIndex
    # rightBase_t = rightBase / srate

    return rightBase


def _get_half_height(candidateSignal, maxFrame, leftZero, rightZero, leftBase, rightOuter):
    ####
    """
    leftBaseHalfHeight
    The coordinate of the signal halfway (in height) between the blink maximum and the left base value. [A positive numeric value.]

    rightBaseHalfHeight
    The coordinate of the signal halfway (in height) between the blink maximum and the right base value.
    [A positive numeric value.]
    """

    maxFrame, leftZero, rightZero, leftBase, rightOuter = int(maxFrame), int(leftZero), int(rightZero), int(
        leftBase), int(rightOuter)

    ryy = candidateSignal[maxFrame] - candidateSignal[leftBase]
    blinkHalfHeight = candidateSignal[maxFrame] - (0.5 * (ryy))

    leftHalfBase = np.arange(leftBase, maxFrame)
    leftBaseHalfHeight = leftBase + np.argmax(candidateSignal[leftHalfBase] >= blinkHalfHeight)

    warnings.warn(
        'Need to double check this line:To confirm whether it is correct to used rightOuter instead of rightBase?')
    ## WIP : To confirm whether it is correct to used rightOuter instead of rightBase?
    rightHalfBase = np.arange(maxFrame, rightOuter)
    rightBaseHalfHeight = np.minimum(rightOuter,
                                     np.argmax(candidateSignal[rightHalfBase] <= blinkHalfHeight) + maxFrame)

    # Compute the left and right half-height frames from zero
    leftHalfBase = np.arange(leftZero, maxFrame)
    blinkHalfHeight = 0.5 * candidateSignal[maxFrame]  # with_val 4.3747134

    """
    leftZeroHalfHeight
    The coordinate of the signal halfway (in height) between the blink maximum and the left zero value.
    """
    leftZeroHalfHeight = np.argmax(candidateSignal[leftHalfBase] >= blinkHalfHeight) + leftZero

    rightHalfBase = np.arange(maxFrame, rightZero)

    """
    rightZeroHalfHeight
    The coordinate of the signal halfway (in height) between the blink maximum and the right zero value.
    """
    rightZeroHalfHeight = np.minimum(rightOuter, maxFrame +
                                     np.argmax(candidateSignal[rightHalfBase] <= blinkHalfHeight))

    return leftZeroHalfHeight, rightZeroHalfHeight, leftBaseHalfHeight, rightBaseHalfHeight


def compute_fit_range(candidateSignal, maxFrame, leftZero, rightZero, baseFraction, top_bottom=None):
    maxFrame, leftZero, rightZero = int(maxFrame), int(leftZero), int(rightZero)
    # Compute fit ranges
    blinkHeight = candidateSignal[maxFrame] - candidateSignal[leftZero]  # ?? 8.8286028

    blinkTop = candidateSignal[maxFrame] - baseFraction * blinkHeight  # ?? 7.8665667
    blinkBottom = candidateSignal[leftZero] + baseFraction * blinkHeight  # ?? 0.80368418

    blinkRange_l = np.arange(leftZero, maxFrame + 1, dtype=int)


    blinkTopPoint_l = np.argmin(candidateSignal[blinkRange_l] < blinkTop)
    blinkTopPoint_l_X = blinkRange_l[blinkTopPoint_l]
    blinkTopPoint_l_Y = candidateSignal[blinkTopPoint_l_X]

    blinkBottomPoint_l = np.argmax(candidateSignal[blinkRange_l] > blinkBottom)
    blinkBottomPoint_l_X = blinkRange_l[blinkBottomPoint_l]
    blinkBottomPoint_l_Y = candidateSignal[blinkBottomPoint_l_X]


    leftRange = [blinkRange_l[blinkBottomPoint_l], blinkRange_l[blinkTopPoint_l]]


    blinkRange_r = np.arange(maxFrame, rightZero + 1, dtype=int)
    blinkTopPoint_r = np.argmax(candidateSignal[blinkRange_r] < blinkTop)
    blinkTopPoint_r_X = blinkRange_r[blinkTopPoint_r]
    blinkTopPoint_r_Y = candidateSignal[blinkTopPoint_r_X]

    blinkBottomPoint_r = np.argmin(candidateSignal[blinkRange_r] > blinkBottom)
    blinkBottomPoint_r_X = blinkRange_r[blinkBottomPoint_r]
    blinkBottomPoint_r_Y = candidateSignal[blinkBottomPoint_r_X]

    rightRange = [blinkRange_r[blinkTopPoint_r], blinkRange_r[blinkBottomPoint_r]]
    # use this to visualise
    # from eeg_blinks.viz.viz_sanity import viz_blink_top_buttom_point
    # viz_blink_top_buttom_point(candidateSignal,blinkRange,blinkTop,blinkBottom,maxFrame,rightZero,leftRange,rightRange)

    xLeft = np.arange(leftRange[0], leftRange[1] + 1, dtype=int)  # THe +1 to ensure we include the last frame
    xRight = np.arange(rightRange[0], rightRange[1] + 1, dtype=int)



    if blinkBottomPoint_l_X == blinkTopPoint_l_X:
        warnings.warn('same value for left top_blink and left bottom_blink')

    if blinkBottomPoint_r_X == blinkTopPoint_r_X:
        warnings.warn('same value for right top_blink and right bottom_blink')

    if xLeft.size == 0:
        xLeft = np.nan

    if xRight.size == 0:
        xRight = np.nan

    if top_bottom is None:
        warnings.warn('To modify this so that all function return the top_bottom point')
        return xLeft, xRight, leftRange, rightRange
    else:
        return xLeft, xRight, leftRange, rightRange, \
               blinkBottomPoint_l_Y,blinkBottomPoint_l_X,blinkTopPoint_l_Y,blinkTopPoint_l_X,\
               blinkBottomPoint_r_X,blinkBottomPoint_r_Y,blinkTopPoint_r_X,blinkTopPoint_r_Y




def get_zero_crossing_pd(number, maxFrame, maxValue, leftOuter, rightOuter, candidateSignal, blinkVelocity,
                         baseFraction):
    """

    number
    The number of the potential blink within the corresponding blinks structure. [A positive numeric value.]

    maxFrame
    The frame number of the first maximum amplitude of this blink. [A positive numeric value.]

    maxValue
    A numeric value giving the maximum value of the blink.

    leftOuter
    The frame number of the left outer reach of the blink
    (defined as the largest of 1 or the frame of the previous blink maximum).

    rightOuter
    The frame number of the right outer reach of the blink (defined as the smallest of the last
    frame or the frame of the next blink maximum).

    leftZero
    The frame number of the left zero crossing of the blink. [A positive numeric value.]

    rightZero
    The frame number of the right zero crossing of the blink. [A positive numeric value.]
    """


    leftZero, rightZero = left_right_zero_crossing(candidateSignal, maxFrame,
                                                   leftOuter, rightOuter)

    if (leftZero is None) or (rightZero is None):
        # This usually happen for end of signal
        return None
    ## Compute the place of maximum positive and negative velocities
    ## START FROM LINE 87 MATLAB

    """
    
    upStroke is the interval between leftZero and maxFrame, 
    downStroke is the interval between maxFrame and rightZero`.
    """

    maxPosVelFrame, maxNegVelFrame = _maxPosVelFrame(blinkVelocity, maxFrame, leftZero, rightZero)

    assert maxNegVelFrame.size == 1

    # Compute the left and right base frames

    if leftOuter > maxPosVelFrame:
        warnings.warn(
            'Failed to fit blink %s due to leftOuter :%s  larger than maxPosVelFrame : %s. For now I will skip this file'
            % (number, leftOuter, maxPosVelFrame))
        return

    """
    
    leftBase
    The frame number of the left local minimum of the blink. [A positive numeric value.]
    
    rightBase
    The frame number of the right local minimum of the blink. [A positive numeric value.]
    """

    leftBase = _get_left_base(blinkVelocity, leftOuter, maxPosVelFrame)

    rightBase = _get_right_base(candidateSignal, blinkVelocity, rightOuter, maxNegVelFrame)

    leftZeroHalfHeight, rightZeroHalfHeight, leftBaseHalfHeight, rightBaseHalfHeight = _get_half_height(candidateSignal,
                                                                                                        maxFrame,
                                                                                                        leftZero,
                                                                                                        rightZero,
                                                                                                        leftBase,
                                                                                                        rightOuter)

    """
    I am just curios why they dont simply define xLeft  and xRight simply as
    
    xLeft=np.arange(leftZero, maxFrame)
    xRight=np.arange(maxFrame,rightZero)
    """
    xLeft, xRight, leftRange, rightRange = compute_fit_range(candidateSignal, maxFrame, leftZero, rightZero,
                                                             baseFraction)

    if (xLeft.size <= 1) or (xRight.size <= 1):
        # To avoid ValueError: On entry to DLASCL parameter number 4 had an illegal value
        return None

    # Below and above for types
    if (xLeft.size != 0) and (xRight.size != 0):
        # There should be multiple x,y coordinate to perform the math operation

        ds_lines = lines_intersection(xRight=xRight, xLeft=xLeft,
                                      yRight=candidateSignal[xRight], yLeft=candidateSignal[xLeft])

        data_blink = dict(leftRange=leftRange, rightRange=rightRange,
                          rightBaseHalfHeight=rightBaseHalfHeight, leftBaseHalfHeight=leftBaseHalfHeight,
                          leftZero=leftZero, rightZero=rightZero,
                          leftBase=leftBase, rightBase=rightBase,
                          rightZeroHalfHeight=rightZeroHalfHeight, leftZeroHalfHeight=leftZeroHalfHeight,
                          rightOuter=rightOuter, leftOuter=leftOuter,
                          maxFrame=maxFrame, number=number, maxValues=maxValue)

        data_blink.update(ds_lines)

        return data_blink

    else:

        if (xLeft.size == 0) and (xRight.size == 0):
            warnings.warn('Failed to fit blink %s due to xLeft or xRight less than 1: xleft size:%s and xRIght size: %s'
                          % (number, len(xLeft), len(xRight)))
            return None

        else:
            warnings.warn(
                'Failed to fit blink %s but due to imbalance xLeft or xRight less than 1: xleft size:%s and xRIght size: %s. '
                'For now I will skip this file'
                % (number, len(xLeft), len(xRight)))

            return None
