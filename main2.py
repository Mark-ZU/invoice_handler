#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
from pdfminer.layout import *
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

from mplfonts import use_font
import matplotlib.pyplot as plt

import numpy as np
import invoice
import layout as L

plt.rcParams.update({'font.size': 10})
use_font('Noto Serif CJK SC')

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

replacements = [
    ["\n\n","\n"],
    [" ",""],
    ["\t",""],
    ["\u3000",""],
    # ["\n",""]
]
keywords = [
    "购","买","方",
    "销","售",
    "密","码","区",
    "名称","纳税人识别号","地址、电话","开户行及账号",
]
key = "浙江大学"
keys = [
    key,
    "增值税电子普通发票"
]
vlines = []
hlines = []
vlines_layout = L.Lines()
hlines_layout = L.Lines()
def pure(text):
    for r in replacements:
        text = text.replace(*r)
    return text

def draw_box(ax,b,arg):
    ax.plot(b[[0,0,2,2,0]],b[[1,3,3,1,1]],arg,linewidth=3.0)

if __name__ == "__main__":
    count = 1
    start = np.random.randint(0,10,1)
    # start = 0
    end = start + count
    if len(sys.argv) != 2:
        "script.py [dirname[default=invoice]]"
    directory = sys.argv[1] if len(sys.argv) >= 2 else "invoice"
    _count = -1
    print("file count : ",len(os.listdir(directory)))
    for filename in os.listdir(directory):
        if not filename.endswith('.pdf'):
            print(filename,"skip")
        _count += 1
        if _count < start:
            continue
        if _count >= end:
            break
        fig, axs = plt.subplots(1,1,figsize=(20,12))
        plt.setp(axs, xlim=(0,1), ylim=(0,1))
        plt.tight_layout()
        ax = axs
        bx = ax#axs[0,0]
        cx = ax#axs[0,0]
        dx = ax#axs[0,0]
        print(_count,filename)
        fp = open(os.path.join(directory,filename), 'rb')
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pages = PDFPage.get_pages(fp)

        for page in pages:
            page_box = page.mediabox
            w = page_box[2]
            h = page_box[3]
            # print(page_box)
            interpreter.process_page(page)
            layout = device.get_result()
            for o in layout:
                if isinstance(o, LTTextBox):
                    b = np.array(o.bbox)/[w,h,w,h]
                    x, y, text = o.bbox[0], o.bbox[1], o.get_text()
                    text = pure(text)
                    color = "g"
                    if key in text:
                        print("found key ! ",text,x/w,y/h)
                        color = "r"
                    ax.text(b[0],b[3],text,horizontalalignment='left',verticalalignment='top')
                    ax.plot(b[0],b[3],color+".")
                    b = np.array(o.bbox)/[w,h,w,h]
                    hlines.append(b[[0,1,0,3]])
                    vlines.append(b[[0,3,2,3]])
                    vlines_layout.add(b[0])
                    hlines_layout.add(b[3])
                    pass
        for vline in vlines:
            draw_box(bx,vline,"y")
        for hline in hlines:
            draw_box(bx,hline,"b")
        for v in vlines_layout.l:
            cx.plot([v,v],[0,1],"b")
            dx.plot([v,v],[0,1],"b")
        for v in hlines_layout.l:
            cx.plot([0,1],[v,v],"y")
            dx.plot([0,1],[v,v],"y")
        plt.show()