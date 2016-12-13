#!/usr/bin/env python
# -*- coding: utf-8 -*-
from nose.tools import assert_equal, assert_true


def test_mcpeak():
    import numpy as np
    from pyoptmat import Material
    al = Material({'model': 'aluminium_mcp'})
    mcp = al._mcpeak
    assert_true(np.allclose(np.vectorize(al)(mcp.ws), mcp(mcp.ws)))
