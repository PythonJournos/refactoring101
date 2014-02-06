#!/usr/bin/env python
from unittest import TestCase

from elex4.lib.analysis import percent


class TestPercentFunc(TestCase):

    def test_percent(self):
        "test_percent returns percentage as string"
        self.assertEquals(percent(50, 100), '50')
