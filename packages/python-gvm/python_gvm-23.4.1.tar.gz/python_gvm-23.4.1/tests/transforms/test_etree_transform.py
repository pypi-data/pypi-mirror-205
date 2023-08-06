# -*- coding: utf-8 -*-
# Copyright (C) 2018-2022 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from lxml import etree

from gvm.transforms import EtreeTransform


class EtreeTransformTestCase(unittest.TestCase):
    def test_transform_response(self):
        transform = EtreeTransform()
        result = transform("<foo/>")

        self.assertTrue(etree.iselement(result))

    def test_transform_more_complex_response(self):
        transform = EtreeTransform()
        result = transform('<foo id="bar"><lorem/><ipsum/></foo>')

        self.assertTrue(etree.iselement(result))
        self.assertEqual(result.tag, "foo")
        self.assertEqual(result.get("id"), "bar")
        self.assertEqual(len(result), 2)
