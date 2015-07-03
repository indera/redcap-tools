###############################################################################
# Copyright 2014-2015 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's ADRC Forms project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

"""
Helper class for collectiong stats about test performed
@see ConfigurableTestCase#run_test()

@author Andrei Sura
"""

from action import Action
from collections import defaultdict

class ActionStatistic(object):

    def __init__(self, target):
        self.target = target
        self.counts = {
                'num' : 0,
                'num_skipped' : 0,
                'by_type' : defaultdict(int)
        }

    def update(self, action, was_executed):
        if was_executed:
            self.counts['num'] += 1
            self.counts['by_type'][action.ftype] += 1
        else:
            self.counts['num_skipped'] += 1


    def to_string(self):
        string = "# === {} statistics:".format(self.target)
        string += "\n# \t Total values entered: {}".format(self.counts['num'])
        string += "\n# \t Total values skipped: {}".format(self.counts['num_skipped'])

        by_type = self.counts['by_type']
        for name in by_type:
            string += "\n# \t Variable '{}' values entered: {}".format(name, by_type[name])

        return string
