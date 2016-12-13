#!/usr/bin/env python
# -*- coding: utf-8 -*-
from numpy.testing import assert_allclose


def test_rakic():
    import numpy as np
    from pyoptmat import Material
    al = Material({'model': 'aluminium_rak'})
    rak = al._rakic
    assert_allclose(np.vectorize(al)(rak.ws), rak(rak.ws))
    al_dl = Material({'model': 'aluminium_dl'})
    assert_allclose(np.vectorize(al_dl)(rak.ws), rak(rak.ws), rtol=0.05)
    # import matplotlib.pyplot as plt
    # plt.plot(rak.ws, np.vectorize(al_dl)(rak.ws).real -
    #          np.vectorize(al)(rak.ws).real)
    # plt.plot(rak.ws, np.vectorize(al_dl)(rak.ws).imag -
    #          np.vectorize(al)(rak.ws).imag)
    # plt.show()
