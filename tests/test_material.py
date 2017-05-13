#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from numpy.testing import assert_allclose

result_gold_d = (-42.438315881875219 + 3.1544052539392413j)
result_gold_dl = (-46.553004128210638 + 3.3266566828613278j)
result_silver_dl = (-48.058582927757783 + 2.9917315082144231j)
result_aluminium_dl = (-83.979985579914157 + 27.440127505777991j)
result_GaN = 5.4598374108551901
result_W = (-2.8490661174276219 + 21.023779631594959j)


def test_material():
    from pyoptmat import Material
    air = Material({'model': 'dielectric', 'RI': 1.0})
    water = Material({'model': 'dielectric', 'RI': 1.333})
    gold_d = Material({'model': 'gold_d'})
    gold_dl = Material({'model': 'gold_dl'})
    silver_dl = Material({'model': 'silver_dl'})
    aluminium_dl = Material({'model': 'aluminium_dl'})
    aluminium_dl_low_loss = Material({'model': 'aluminium_dl',
                                      'im_factor': 0.1})
    GaN = Material({'model': 'rii', 'shelf': 'main',
                    'book': 'GaN (Experimental data)',
                    'page': 'Barker-o'})
    W = Material({'model': 'rii', 'shelf': 'DL', 'book': 'W',
                  'page': 'Rakic'})
    w = 2.0 * np.pi
    assert_allclose(air(w), 1.0)
    assert_allclose(water(w), 1.333 ** 2)
    assert_allclose(gold_d(w), result_gold_d)
    assert_allclose(gold_dl(w), result_gold_dl)
    assert_allclose(silver_dl(w), result_silver_dl)
    assert_allclose(aluminium_dl(w), result_aluminium_dl)
    assert_allclose(
        aluminium_dl_low_loss(w),
        result_aluminium_dl.real + 0.1j * result_aluminium_dl.imag)
    assert_allclose(GaN(w), result_GaN)
    assert_allclose(W(w), result_W)
