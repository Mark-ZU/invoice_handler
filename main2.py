#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os,shutil,re,copy,math
import traceback
from pdfminer.layout import *
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

from mplfonts import use_font
import matplotlib.pyplot as plt

import numpy as np
import invoice as I
import layout as L

DEBUG_SHOW = False

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

def pure(text):
    for r in replacements:
        text = text.replace(*r)
    return text

def draw_box(ax,b,arg):
    ax.plot(b[[0,0,2,2,0]],b[[1,3,3,1,1]],arg,linewidth=3.0)

# FILENAME = None
FILENAME = "加工880.pdf"

DEBUG = DEBUG_SHOW or FILENAME is not None

if __name__ == "__main__":
    count = -1
    if FILENAME is not None:
        count = 1
    if len(sys.argv) != 2:
        "script.py [dirname[default=invoice]]"
    directory = sys.argv[1] if len(sys.argv) >= 2 else "invoice"
    _count = -1
    print("file count : ",len(os.listdir(directory)))
    failed_dir = os.path.join(directory,"failed")
    os.makedirs(failed_dir,exist_ok=True)
    all_infos = {}
    
    num = 0
    success = 0
    failed = 0
    for filename in os.listdir(directory):
        if not filename.lower().endswith('.pdf'):
            print(filename,"skip")
            continue
        _count += 1
        if count > 0 and _count > count:
            break
        if FILENAME is not None:
            filename = FILENAME
        
        num += 1
        grid = L.Grid()
        vlines = []
        hlines = []
        fig, axs = plt.subplots(1,1,figsize=(20,12))
        plt.setp(axs, xlim=(0,1), ylim=(0,1))
        plt.tight_layout()
        ax = axs
        ax.invert_yaxis()
        print(_count,filename)
        fp = open(os.path.join(directory,filename), 'rb')
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pages = PDFPage.get_pages(fp)

        def deal(o,page_box,tt=None):
            pb = copy.deepcopy(page_box)
            w = pb[2]-pb[0]
            h = pb[3]-pb[1]
            if h > w:
                h = w*400/600.0
                pb[1] = pb[3] - h
            b = (np.array(o.bbox) - [pb[0],pb[1]]*2)/(2*[w,h])
            text = o.get_text() if tt is None else tt
            text = pure(text)
            if len(text) == 0:
                return
            ax.text(b[0],1-b[3],text,horizontalalignment='left',verticalalignment='top')
            ax.plot(b[0],1-b[3],".")
            hlines.append(np.array([b[0],1-b[1],b[0],1-b[3]]))
            vlines.append(np.array([b[0],1-b[3],b[2],1-b[3]]))
            grid.add([b[0],1-b[3]],text)

        page_count = 0
        for page in pages:
            page_count += 1
            if page_count != 1:
                print("{} page count not equal to 1".format(filename))
                break
            page_box = page.cropbox
            pbox = copy.deepcopy(page_box)
            bb = np.array([9999,9999,0,0],dtype=float)
            # s_x = page_box[0]
            # s_y = page_box[1]
            # w = page_box[2] - s_x
            # h = page_box[3] - s_y
            # print("debugsize : ",page_box)
            interpreter.process_page(page)
            layout = device.get_result()
            for o in layout:
                # if isinstance(o, LTTextBox):
                if isinstance(o, LTText) or isinstance(o, LTFigure):
                    bb[0] = min(bb[0],o.bbox[0])
                    bb[1] = min(bb[1],o.bbox[3])
                    bb[2] = max(bb[2],o.bbox[0])
                    bb[3] = max(bb[3],o.bbox[3])
            w = bb[2] - bb[0]
            h = bb[3] - bb[1]
            page_box = bb + np.array([-w,-h,w,h])*0.01
            for o in layout:
                # if isinstance(o, LTTextBox):
                if isinstance(o, LTText):
                    deal(o,page_box)
                elif isinstance(o, LTFigure):
                    text = ""
                    for e in o:
                        if isinstance(e,LTChar):
                            text += e.get_text()
                    deal(o,page_box,text)

        try:
            res = I.parse_info(grid,DEBUG)
            print("res : ",res)
            all_infos[filename] = (res)
            if DEBUG:
                for vline in vlines:
                    draw_box(ax,vline,"y")
                for hline in hlines:
                    draw_box(ax,hline,"b")
                for n in grid.vIndex.lists:
                    ax.plot([n.v[0],n.v[0]],[0,1],"b")
                    ax.plot([n.v[0],n.v[0]],[0,1],"b")
                for n in grid.hIndex.lists:
                    ax.plot([0,1],[n.v[1],n.v[1]],"y")
                    ax.plot([0,1],[n.v[1],n.v[1]],"y")
                plt.show()
        except Exception as e:
            print("\n\n-----------------\n{} analyze failed,skip,{}\n------------------\n\n".format(filename,e))
            traceback.print_exc()
            origin_path = os.path.join(directory,filename)
            new_path = os.path.join(failed_dir,filename)
            shutil.copyfile(origin_path,new_path)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
            failed += 1


            # for vline in vlines:
            #     draw_box(ax,vline,"y")
            # for hline in hlines:
            #     draw_box(ax,hline,"b")
            # for n in grid.vIndex.lists:
            #     ax.plot([n.v[0],n.v[0]],[0,1],"b")
            #     ax.plot([n.v[0],n.v[0]],[0,1],"b")
            # for n in grid.hIndex.lists:
            #     ax.plot([0,1],[n.v[1],n.v[1]],"y")
            #     ax.plot([0,1],[n.v[1],n.v[1]],"y")
            # plt.show()

            plt.close(fig)
            continue
        
        # plt.show()
        plt.close(fig)

        # input("press enter to continue")
        success += 1

    with open("infos.txt",'w') as f:
        for name,info in all_infos.items():
            f.write(name + "\t" + str(info)+"\n")
    print("total : {},success : {},failed : {}".format(num,success,failed))
