#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import copy

SAME_ = [0.016,0.015]
class Lines:
    SAME = 0.013
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
    class Dir:
        LEFTRIGHT = 0
        UPDOWN = 1
        LEFTORUP = 0
        RIGHTORDOWN = 1
    class Node:
        def __init__(self,text,v):
            self.neigh = [[None,None],[None,None]]
            self.text = text
            self.v = v
        def dir(self,c = 1,dir=[0,0]):
            node = self
            for _ in range(c):
                node = node.neigh[dir[0]][dir[1]]
                if node is None:
                    break
            return node
        def right(self,c = 1):
            return self.dir(c,[Grid.Dir.LEFTRIGHT,Grid.Dir.RIGHTORDOWN])
        def left(self,c = 1):
            return self.dir(c,[Grid.Dir.LEFTRIGHT,Grid.Dir.LEFTORUP])
        def up(self,c = 1):
            return self.dir(c,[Grid.Dir.UPDOWN,Grid.Dir.LEFTORUP])
        def down(self,c = 1):
            return self.dir(c,[Grid.Dir.UPDOWN,Grid.Dir.RIGHTORDOWN])
        def downTo(self,v=1.0,append_node=False):
            res = []
            node = self
            while node is not None and node.v[Grid.Dir.UPDOWN] < v:
                res.append(node if append_node else node.text)
                node = node.down()
            return res
        def rightTo(self,v=1.0,append_node=False):
            res = []
            node = self
            while node is not None and node.v[Grid.Dir.LEFTRIGHT] < v:
                res.append(node if append_node else node.text)
                node = node.right()
            return res
        def downRightTo(self,*,rv=1.0,dv=1.0):
            starts = self.downTo(dv,True)
            res = []
            for n in starts:
                res.append(n.rightTo(rv))
            return res
        def rightDownTo(self,*,rv=1.0,dv=1.0):
            pass
        def __str__(self):
            return "m:{}-{},n:{}".format(hex(id(self)),str(self.text),self.neigh)
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
        def getFirst(self,v):
            node = None
            min_v = 1
            for n in self.nodes:
                if n.v[self.IND] > v and n.v[self.IND] < min_v:
                    node = n
                    min_v = n.v[self.IND]
            return node
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
            line = None
            dist = 9999
            for l in self.lists:
                if l.v[self.IND] < node.v[self.IND] - SAME_[self.IND]:
                    ind += 1
                    left = l
                elif l.v[self.IND] > node.v[self.IND] + SAME_[self.IND]:
                    right = l
                    break
                else:
                    temp_dist = np.abs(l.v[self.IND] - node.v[self.IND])
                    if line is None or temp_dist < dist:
                        dist = temp_dist
                        line = l
            if line is not None:
                line.add(node)
                return
            v = [0.0,0.0]
            v[self.IND] = node.v[self.IND]
            l = Grid.NodeList(v,1-self.IND)
            self.lists.insert(ind,l)
            l.add(node)
        def getFirstNode(self,v,vside):
            list = None
            near_v = 1
            for l in self.lists:
                if l.v[self.IND] > v and l.v[self.IND] < near_v:
                    list = l
                    near_v = l.v[self.IND]
            if list is not None:
                return list.getFirst(vside)
            else:
                return None
        def __str__(self):
            repo = "RootList:"
            for l in self.lists:
                repo += "\n{}".format(l)
            return repo
    def __init__(self):
        self.vIndex = self.__class__.RootList(0)
        self.hIndex = self.__class__.RootList(1)
        self.nodes = []
    def add(self,v,text):
        assert(len(v)>=2)
        node = self.__class__.Node(text,v)
        self.vIndex.add(node)
        self.hIndex.add(node)
        self.nodes.append(node)
    def search(self,text,*,xl=[0.0,1.0],yl=[0.0,1.0]):
        return self.searchSeq([text],xl=xl,yl=yl)
    def searchSeq(self,texts,*,dir=Dir.LEFTRIGHT,xl = [0.0,1.0],yl = [0.0,1.0],startswith = True):
        start_res = []
        for n in self.nodes:
            if texts[0] in n.text:
                x,y = n.v
                if x>xl[0] and x<xl[1] and y>yl[0] and y<yl[1]:
                    start_res.append(n)
        final_res = copy.copy(start_res)
        for n in start_res:
            node = n
            for t in texts:
                if node is None:
                    final_res.remove(n)
                    break
                if node.text.startswith(t) or (startswith==False and t in node.text):
                    node = node.neigh[dir][1]
                else:
                    final_res.remove(n)
                    break
        return_res = []
        for n in final_res:
            return_res.append(n.dir(len(texts)-1,[dir,Grid.Dir.RIGHTORDOWN]))
        return return_res
    def searchMultiSeq(self,multi_texts,*,dir=Dir.LEFTRIGHT,xl = [0.0,1.0],yl = [0.0,1.0],startswith = True):
        res = []
        for texts in multi_texts:
            res += self.searchSeq(texts,dir=dir,xl=xl,yl=yl,startswith = startswith)
        return res
    def getFirstNode(self,xv,yv):
        return self.hIndex.getFirstNode(yv,xv)
    def normalization(self,x_range=[0.0,1.0],y_range = [0.0,1.0]):
        #TODO
        pass
    def __str__(self):
        repo = "Grid:"
        for n in self.nodes:
            repo += "\n"+str(n)
        return repo


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
    def t4():
        class A:
            def __init__(self):
                self.a = 1
                pass
            def f(self):
                node = self
                return node.a
        a = A()
        print(a.f())
    # t1()
    # t2()
    # t3()
    t4()
