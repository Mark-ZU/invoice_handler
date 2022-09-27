#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import copy
from layout import Grid

class CompanyInfo:
    def __init__(self,a1="",a2="",a3="",a4="",*args):
        # 公司名称
        self.mingcheng = a1
        # 纳税人识别号
        self.shuihao = a2
        # 地址电话
        self.dizhidianhua = a3
        # 开户行及账号
        self.kaihuhang = a4
    def __str__(self):
        res = ""
        res += self.mingcheng+'\t'
        res += self.shuihao
        # res += self.shuihao+'\t'
        # res += self.dizhidianhua+'\t'
        # res += self.kaihuhang
        return res
class InvoiceInfo:
    def __init__(self,a1="",a2="",a3="",a4="",*args):
        # 发票代号
        self.fapiaodaihao = a1
        # 发票号码
        self.fapiaohaoma = a2
        # 开票日期
        self.kaipiaoriqi = a3
        # 检验码
        self.jiaoyanma = a4
    def __str__(self):
        res = ""
        res += self.fapiaodaihao+'\t'
        res += self.fapiaohaoma+'\t'
        res += self.kaipiaoriqi+'\t'
        res += self.jiaoyanma
        return res
class StuffInfo:
    def __init__(self):
        # 项目/货物/服务名称
        self.mingcheng = None
        # 规格型号
        self.guigexinghao = None
        # 单位
        self.danwei = None
        # 数量
        self.shuliang = None
        # 单价
        self.danjia = None
        # 金额
        self.jine = None
        # 税率
        self.shuilv = None
        # 税额
        self.shuie = None
    def __str__(self):
        res = ""
        res += str(self.mingcheng)+"\t"
        res += str(self.shuliang)+"\t"
        res += str(self.jine)+"\t"
        res += str(self.shuie)
        return res

class Info:
    def __init__(self):
        # 机器编号
        self.jiqibianhao = None
        # 基本信息
        self.jibenxinxi = InvoiceInfo()
        # 购买方
        self.goumaifang = CompanyInfo()
        # 密码区
        self.mimaqu = None
        # 项目/货物/服务 list of StuffInfo
        self.mingcheng = []
        # 合计
        self.heji = None
        # 销售方
        self.xiaoshoufang = CompanyInfo()
        # 备注
        self.beizhu = None
    def __str__(self):
        res = ""
        res += str(self.goumaifang)+"\t"
        res += str(self.xiaoshoufang)+"\t"
        res += str(self.jibenxinxi)+"\t"
        res += str(self.heji)
        for info in self.mingcheng:
            res += "\n\t" + str(info)
        return res

def connect(lists: list):
    res = ""
    for l in lists:
        res += l+'\n'
    return [res]

def filter(lists: list,regexes=[],SPLIT = True,*,MIN_LEN=0):
    res = []
    string = ""
    for l in lists:
        if type(l) == list:
            res += filter(l,regexes,SPLIT,MIN_LEN = MIN_LEN)
        elif type(l) == str:
            string += l
        else:
            print("type not support in filter func,type: ",type(l))

    for reg in regexes:
        regex = reg
        replace = ""
        if type(reg) == list:
            if len(reg) == 2:
                regex = reg[0]
                replace = reg[1]
            else:
                print("input arg for filter not support : ",reg)
        string = re.sub(regex,replace,string)
    temp = string.split("\n") if SPLIT else [re.sub('\n','',string)]
    temp_res = []
    for s in temp:
        if s != "":
            if len(s) >= MIN_LEN or len(temp_res) == 0:
                temp_res.append(s)
            else:
                temp_res[-1] += s
    res += temp_res
    return res

def split(lists: list,reg = []):
    res = []
    for l in lists:
        if type(l) == list:
            res.append(split(l,reg))
        elif type(l) == str:
            split_res = re.split(reg,l)
            if len(split_res) > 1:
                for s in split_res:
                    res.append([s])
            else:
                res += (split_res)
        else:
            print("type not support in split func,type: ",type(l))
    return res

def filt_details(grid):
    details_up = grid.searchMultiSeq([["货物或应税劳务"],["项目名称"]])[0].v[Grid.Dir.UPDOWN]+0.01
    details_down = grid.searchMultiSeq([["合计"],["合","计"]])[0].v[Grid.Dir.UPDOWN]-0.01
    details_first = grid.getFirstNode(xv = 0,yv=details_up)
    if details_first.v[1]>0.3:
        raise Exception("get details failed")
    details = details_first.downTo(details_down-0.01)
    details = filter(split(connect(details),r"\n\*"),[r'\*',r'\n'],SPLIT=False)
    
    pos = grid.searchMultiSeq([["数量"],["数","量"]])[0]
    pos_x = pos.v[0]-0.03
    pos_y = pos.v[1]+0.01
    counts = grid.getFirstNode(xv = pos_x,yv = pos_y).downTo(details_down-0.01)
    print("counts : ",counts)

    pos = grid.searchMultiSeq([["金额"],["金","额"]])[0]
    pos_x = pos.v[0]-0.06
    pos_y = pos.v[1]+0.01
    prices = grid.getFirstNode(xv = pos_x,yv = pos_y).downRightTo(dv=details_down)
    temp = [[],[]]
    for p in prices:
        if len(p) == 3:
            p = [p[0],p[2]]
        for i,pp in enumerate(p):
            ppp = filter(split([pp],r'\n'))
            temp[i]+=ppp
    prices = []
    for p in zip(*temp):
        prices.append(p)
    
    # print("ddd111 ",details)
    # print("ddd222 ",prices)

    if len(details) != len(prices):
        raise Exception("details parse failed, length not equal1111:{}-{}-{}".format(len(details),len(prices),len(counts)))
    if len(details) != len(counts):
        raise Exception("details parse failed, length not equal2222:{}-{}-{}".format(len(details),len(prices),len(counts)))
    
    cs = []
    for c in counts:
        cs.append(int(c))
    p1s = []
    p2s = []
    for i,price in enumerate(prices):
        if len(price) == 3:
            strs = price[0],price[2]
        elif len(price) == 2:
            strs = price[0],price[1]
        else:
            raise Exception("details parse failed, prices length not correct")
        p1 = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)",strs[0])[0])
        try:
            p2 = float(strs[1])
        except ValueError:
            p2 = 0
        p1s.append(p1)
        p2s.append(p2)

    res = []
    for a,b,c,d in zip(details,cs,p1s,p2s):
        info = StuffInfo()
        info.mingcheng = a
        info.shuliang = b
        info.jine = c
        info.shuie = d
        res.append(info)
    return res

def parse_info(grid: Grid,DEBUG=False):
    info = Info()
    buyer = grid.searchMultiSeq([["名称"],["名","称"],["名\n称"]],yl=[0.0,0.5])[0].right().downRightTo(rv=0.4,dv=0.5)
    seller = grid.searchMultiSeq([["名称"],["名","称"],["名\n称"]],yl=[0.5,1.0])[0].right().downRightTo(rv=0.4,dv=1.0)
    basics = grid.searchMultiSeq([["发票代码"],["发","票","代","码"]],xl=[0.6,1.0],yl=[0.0,0.3])[0].right().downRightTo(dv=0.22)
    total = grid.searchMultiSeq([["合计"],["合","计"]])[0].right().rightTo(0.8)

    details = filt_details(grid)
    a = filter(buyer,MIN_LEN=5)
    b = filter(seller,MIN_LEN=5)
    c = filter(split(basics,r'(^[0-9]{8}\n)'),['月','日','年','：'],SPLIT=False,MIN_LEN=3)
    d = filter(total,['¥','￥'])
    
    if len(b) > 4:
        b = [b[0],b[1],"".join(b[2:-1]),b[-1]]
    if DEBUG:
        # print(buyer,a)
        # print(seller,b)
        # print(basics,c)
        # print(details)
        pass
    info.goumaifang = CompanyInfo(*a)
    info.xiaoshoufang = CompanyInfo(*b)
    info.jibenxinxi = InvoiceInfo(*c)
    info.heji = d[0]
    info.mingcheng = details
    return info

if __name__ == "__main__":
    def t1(s,regs = [],spliters = []):
        # print("dd00 ",s)
        s = split(s,spliters)
        # print("dd11 ",s)
        res = filter(s,regs,SPLIT=False)
        print("dd22",res)
        print('\n')

    reg = ['月','日','年','：']
    spliter = r'^([0-9]{8}\n)'
    t1([['032002100611\n'], ['37580317\n2022年04月15日\n'], ['16233843081290786408\n']],reg,spliter)
    t1([['044032100111'], ['45345710'], ['2021', '年月日\n', '08', '31'], ['16637705180042044351']],reg,spliter)