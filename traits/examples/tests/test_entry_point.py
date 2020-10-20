# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import os
import unittest

from traits.examples._entry_point import introduction
from traits.testing.optional_dependencies import requires_pkg_resources


@requires_pkg_resources
class TestExampleEntryPoint(unittest.TestCase):
    """ Test entry points contributed for etsdemo."""

    def test_file_exists(self):
        response = introduction({})
        self.assertTrue(
            os.path.exists(response["root"]),
            "Expected example files to exist."
        )