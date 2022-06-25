#!/usr/bin/env python
# -*- coding: utf-8 -*-
class TextNode:
    def __init__(self,text,box):
        self.text = text
        self.box = box
class VLine:
    def __init__(self,box):
        self.box = box
        pass
class HLine:
    def __init__(self,box):
        self.box = box
        pass
class Layout:
    ROW = 1
    COLUMN = 2
    def __init__(self,box,type):
        self.box = box
        self.items = [[]]
        self.line_count = 0
        self.type = type
    def addText(self,textnode):
        if isinstance(textnode,TextNode):
            pass
        else:
            raise Exception("TypeError in addText")
    def addLine(self,line):
        if self.type == self.ROW and isinstance(line,HLine):
            pass
        elif self.type == self.COLUMN and isinstance(line,VLine):
            pass
        else:
            raise Exception("TypeError in addLine")

class CompanyInfo:
    def __init__(self):
        # 公司名称
        self.mingcheng = None
        # 纳税人识别号
        self.shuihao = None
        # 地址电话
        self.dizhidianhua = None
        # 开户行及账号
        self.kaihuhang = None

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

class Info:
    def __init__(self):
        # 机器编号
        self.jiqibianhao = None
        # 发票代号
        self.fapiaodaihao = None
        # 发票号码
        self.fapiaohaoma = None
        # 开票日期
        self.kaipiaoriqi = None
        # 检验码
        self.jiaoyanma = None
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