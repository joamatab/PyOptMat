# -*- coding: utf-8 -*-
from __future__ import division, print_function
import numpy as np
import riip


class Material(object):

    """A class defining the dielectric function for a material.

    Attributes:
        model: A string indicating the model of dielectric function.
    """

    def __init__(self, params):
        """Init Material class.

        Args:
            params: A dict whose keys are as follows.
                'model': A string indicating the model of dielectric function,
                    that must be 'dielectric', 'pec', 'rii',
                    'gold_d', 'gold_dl', 'silver_dl', 'aluminium_dl'
                    (default 'dielectric')
                'e' or 'RI': For 'dielectric'
                'shelf', 'book', 'page': For 'rii',
                    Use data from M. N. Polyanskiy,
                    "Refractive index database," https://refractiveindex.info.
                'im_factor': A float indicating the reduction factor for the
                    imaginary part of the dielectric constant
        """
        self.__w = None
        self.__eps = None
        self.params = params
        model = self.params.get('model', 'dielectric')
        self.model = model
        self.__im_factor = self.params.get('im_factor', 1.0)
        self.material = None
        if model == 'gold_dl':
            ri = riip.RiiDataFrame()
            idx = ri.catalog[
                (ri.catalog['shelf'] == 'DL') & (ri.catalog['book'] == 'Au') &
                (ri.catalog['page'] == 'Stewart')].index[0]
            self.material = ri.material(idx)
        elif model == 'silver_dl':
            ri = riip.RiiDataFrame()
            idx = ri.catalog[
                (ri.catalog['shelf'] == 'DL') & (ri.catalog['book'] == 'Ag') &
                (ri.catalog['page'] == 'Vial')].index[0]
            self.material = ri.material(idx)
        elif model == 'aluminium_dl':
            ri = riip.RiiDataFrame()
            idx = ri.catalog[
                (ri.catalog['shelf'] == 'DL') & (ri.catalog['book'] == 'Al') &
                (ri.catalog['page'] == 'Rakic')].index[0]
            self.material = ri.material(idx)
        elif model == 'gold_d':
            ri = riip.RiiDataFrame()
            idx = ri.catalog[
                (ri.catalog['shelf'] == 'Drude') &
                (ri.catalog['book'] == 'Au') &
                (ri.catalog['page'] == 'Vial')].index[0]
            self.material = ri.material(idx)
        elif model == 'rii':
            ri = riip.RiiDataFrame()
            idx = ri.catalog[
                (ri.catalog['shelf'] == self.params['shelf']) &
                (ri.catalog['book'] == self.params['book']) &
                (ri.catalog['page'] == self.params['page'])].index[0]
            self.material = ri.material(idx)
        elif model == 'dielectric':
            if 'RI' in self.params:
                if 'e' in self.params:
                    if self.params['e'] != self.params['RI'] ** 2:
                        raise ValueError("e must be RI ** 2.")
                else:
                    self.params['e'] = self.params['RI'] ** 2
            else:
                if 'e' not in self.params:
                    raise ValueError("'RI' or 'e' must be specified.")

    @property
    def im_factor(self):
        return self.__im_factor

    @im_factor.setter
    def im_factor(self, factor):
        self.__w = None
        self.__im_factor = factor

    def __call__(self, w):
        """Return a float indicating the permittivity.

        Args:
            w: A float indicating the angular frequency.

        Raises:
            ValueError: The model is not defined.
        """
        wr = w.real
        if self.__w is None or wr != self.__w:
            self.__w = wr
            model = self.model
            p = self.params
            if model == 'dielectric':
                self.__eps = p['e']
            elif model == 'pec':
                self.__eps = -1e8
            elif model in ['gold_d', 'gold_dl', 'silver_dl', 'aluminium_dl']:
                eps = self.material.eps(2 * np.pi / wr)
                self.__eps = eps.real + 1j * self.im_factor * eps.imag
                if self.__eps.imag < 1.0e-12:
                    self.__eps = self.__eps.real + 1.0e-12j
            elif model == 'rii':
                if (self.material.catalog['tabulated'] == 'f' and
                            int(self.material.catalog['formula']) <= 20):
                    self.__eps = self.material.n(2 * np.pi / wr) ** 2
                else:
                    eps = self.material.eps(2 * np.pi / wr)
                    self.__eps = eps.real + 1j * self.im_factor * eps.imag
                    if self.__eps.imag < 1.0e-12:
                        self.__eps = self.__eps.real + 1.0e-12j
            else:
                raise ValueError("The model is not defined.")
        return self.__eps
