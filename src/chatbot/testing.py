# -*- coding: utf-8 -*-

"""
Testing handler

"""

import dispatch

@dispatch.handler("testing")
def testing_handler(*args, **kwargs):
    return u"testing one two three"

