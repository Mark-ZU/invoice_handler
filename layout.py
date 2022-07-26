#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import copy

SAME = 0.015
class Lines:
    def __init__(self):
        self.l = np.empty(shape=(0,))
    def add(self,v: float):
        ind = np.where(np.logical_and(self.l<v+SAME,self.l>v-SAME))[0]
        if ind.size >0:
            if ind.size > 1:
                print("maybe 'SAME' threshold value too large")
            return
        self.l = np.append(self.l,v)
        self.l = np.sort(self.l)

class Grid:
    class Node:
        def __init__(self,model,v):
            self.neigh = [[None,None],[None,None]]
            self.model = model
            self.v = v
        def __str__(self):
            return "m:{}-{},n:{}".format(hex(id(self)),str(self.model),self.neigh)
    class NodeList:
        def __init__(self,v,IND):
            self.v = v
            self.nodes = []
            self.IND = IND
        def add(self,node):
            ind = 0
            left,right = None,None
            for n in self.nodes:
                if n.v[self.IND] < node.v[self.IND]:
                    ind += 1
                    left = n
                else:
                    right = n
                    break
            if left is not None:
                left.neigh[self.IND][1] = node
            if right is not None:
                right.neigh[self.IND][0] = node
            node.neigh[self.IND][0] = left
            node.neigh[self.IND][1] = right
            self.nodes.insert(ind,node)
        def __str__(self):
            repo = "NodeList: v={}".format(self.v)
            for n in self.nodes:
                repo += "\n{}".format(n)
            return repo
    class RootList:
        def __init__(self,IND):
            self.IND = IND
            self.lists = []
        def add(self,node):
            ind = 0
            left,right = None,None
            for l in self.lists:
                if l.v[self.IND] < node.v[self.IND] - SAME:
                    ind += 1
                    left = l
                elif l.v[self.IND] > node.v[self.IND] + SAME:
                    right = l
                    break
                else:
                    l.add(node)
                    return
            v = [0.0,0.0]
            v[self.IND] = node.v[self.IND]
            l = Grid.NodeList(v,1-self.IND)
            self.lists.insert(ind,l)
            l.add(node)
        def __str__(self):
            repo = "RootList:"
            for l in self.lists:
                repo += "\n{}".format(l)
            return repo
    def __init__(self):
        self.vIndex = self.__class__.RootList(0)
        self.hIndex = self.__class__.RootList(1)
        self.nodes = []
    def add(self,v,model):
        assert(len(v)>=2)
        node = self.__class__.Node(model,v)
        self.vIndex.add(node)
        self.hIndex.add(node)
        self.nodes.append(node)

if __name__ == "__main__":
    def t1():
        ls = Lines()
        ls.SAME = 0.1
        for i in range(6):
            v = np.random.rand()
            print("insert ",v)
            ls.add(v)
            print(ls.l)
    def t2():
        import random
        l = Grid.NodeList(0,1)
        for i in range(4):
            v = random.random()
            n = Grid.Node("v={}".format(v),[0,v])
            l.add(n)
            # print(n)
        print(l)
    def t3():
        import random
        l = Grid.RootList(0)
        r = Grid.RootList(1)
        for i in range(4):
            v1 = random.random()/10.0
            v2 = random.random()/10.0
            n = Grid.Node("v={},{}".format(v1,v2),[v1,v2])
            l.add(n)
            r.add(n)
        print(l)
    # t1()
    # t2()
    t3()