#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
class Lines:
    SAME = 0.015
    def __init__(self):
        self.l = np.empty(shape=(0,))
    def add(self,v: float):
        ind = np.where(np.logical_and(self.l<v+Lines.SAME,self.l>v-Lines.SAME))[0]
        if ind.size >0:
            if ind.size > 1:
                print("maybe 'SAME' threshold value too large")
            return
        self.l = np.append(self.l,v)
        self.l = np.sort(self.l)


if __name__ == "__main__":
    def t1():
        ls = Lines()
        ls.SAME = 0.1
        for i in range(6):
            v = np.random.rand()
            print("insert ",v)
            ls.add(v)
            print(ls.l)
    t1()