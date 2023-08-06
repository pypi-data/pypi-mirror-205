# -*- coding: utf-8 -*-

import numpy as np


def FT_qtor(q, soq, rho, r):
    # based heavily on deanFT above
    # Seems to work, at least produces something that resembles an FT.
    # The only thing is that the peak is in the wrong place.
    output = np.zeros(len(r))
    qhq = q * soq
    for i in range(0, len(r)):
        output[i] = (np.sin(q * r[i]) * qhq).sum()
    output = output * (q[3] - q[2]) * np.power(2.0 * np.square(np.pi) * rho * r, -1)

    return output


def FT_qtor_Lorch(q, soq, rho, r, Soper_Lorch_width):
    # based heavily on deanFT above
    # Seems to work, at least produces something that resembles an FT.
    # The only thing is that the peak is in the wrong place.
    output = np.zeros(len(r))
    qhq = q * soq
    QD = q * Soper_Lorch_width
    Lorch = 3 * np.power(QD, -3) * (np.sin(QD) - QD * np.cos(QD))
    Lorch[0] = 0
    for i in range(0, len(r)):
        output[i] = (np.sin(q * r[i]) * qhq * Lorch).sum()
    output = output * (q[3] - q[2]) * np.power(2.0 * np.square(np.pi) * rho * r, -1)

    return output


def FT_rtoq(r, gofr, rho, q):
    output = np.zeros(len(q))
    rhr = r * gofr
    for i in range(0, len(q)):
        output[i] = (np.sin(r * q[i]) * rhr).sum()
    output = output * (r[3] - r[2]) * 4 * np.pi * rho / q

    return output


def topHatConvolutionSubtraction(q, soq, top_hat_width_in_Q):
    """top hat sub some optimised"""
    # data should be one-dimensional for this correction to work.
    if len(soq.shape) != 1:
        for i in range(0, 10):
            print("this currently only works on 1D data")
    # find the number of points that corresponds to the top hat width
    step_size = q[1] - q[0]
    w = top_hat_width_in_Q / step_size
    intw = int((2 * np.round(w / 2)) + 1)  # do we need to make this an interger?
    # step through the points of the output array. We'll define the value of
    # each, one by one.
    result = np.zeros(len(soq))
    w = float(intw)
    intn = len(soq)

    soq_extended = np.append(soq, np.ones(intw + 1) * soq[-1])
    soq_extended = np.insert(soq_extended, 0, np.ones(intw + 1) * soq[0])
    # now we have w points extra on the start and the end.

    oneovertwowplus1cubed = np.power(2 * float(w) + 1, -3)

    for intr in range(intw, intn + intw):
        c_range = np.array([intr - intw, intr + intw])
        c_range = c_range.clip(0, 1000000).astype(int)

        r = float(intr)

        intc = np.arange(c_range[0], c_range[1] + 1)

        c = intc.astype("float")
        last_bit = (
            3
            * c
            * (4 * np.square(c) + 4 * np.square(r) - np.square(2 * w + 1) + 1)
            / 2
            / r
        )
        c_use = c > w - r  # is true for the long equation.

        prefactor = (2 - integerKroneckerDelta(c, 0.0)) * ~c_use + 1.0 * c_use

        weighting = (
            prefactor
            * (12 * np.square(c) - 1 - c_use * last_bit)
            * oneovertwowplus1cubed
        )

        try:
            result[intr - intw] = sum(weighting * soq_extended[intc - 1])
        except IndexError:
            print(intc)
            print(intr)
            print(intw)
            print(sum(weighting * soq_extended[intc - 1]))
    return result


def integerKroneckerDelta(i, j):
    """Kronecker delta function. first thing is an array. second is an int."""
    truth = i.round() == j
    return truth * 1.0
