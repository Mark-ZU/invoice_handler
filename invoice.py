#!/usr/bin/env python
# -*- coding: utf-8 -*-
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