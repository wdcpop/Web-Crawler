#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import random

class Proxyer(object):
    def __init__(self, list=None):
        self.list = list

    def get_random_one(self):
        if self.list:
            return random.choice(self.list)
        return None
