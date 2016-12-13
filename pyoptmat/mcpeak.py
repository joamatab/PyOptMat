# -*- coding: utf-8 -*-
import os
import numpy as np
from scipy.constants import c
from scipy.interpolate import interp1d


class McPeak():

    """A class defining the dielectric function for alminium according to
    K. M. McPeak, S. V. Jayanti, S. J. P. Kress, S. Meyer, S. Iotti,
    A. Rossinelli, and D. J. Norris, ACS Photonics 2, 326-333 (2015).

    Attributes:
        ws: 1D array of floats indicating the angular frequencys.
        ns: 1D array of floats indicating the real part of RIs.
        ks: 1D array of floats indicating the imaginary part of RIs.
    """

    def __init__(self, kind='cubic'):
        self.num = 2048
        dirname = os.path.dirname(__file__)
        dirname = os.path.join(dirname, "McPeak")
        filename = os.path.join(dirname, "McPeak_k.npy")
        data_k = np.load(filename)
        filename = os.path.join(dirname, "McPeak_n.npy")
        data_n = np.load(filename)
        self.ws = 2 * np.pi / data_n[::-1, 0]
        self.ns = data_n[::-1, 1]
        self.ks = data_k[::-1, 1]
        self.n_func = interp1d(self.ws, self.ns, kind=kind, copy=False,
                               assume_sorted=True)
        self.k_func = interp1d(self.ws, self.ks, kind=kind, copy=False,
                               assume_sorted=True)

    def __call__(self, w):
        n = self.n_func(w) + 1j * self.k_func(w)
        return n ** 2
