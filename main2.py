import sys
import invoice
from pdfminer.layout import *
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

import matplotlib.pyplot as plt
import os
import numpy as np
from mplfonts import use_font

use_font('Noto Serif CJK SC')

replacements = [
    ["\n\n","\n"],
    [" ",""],
    ["\t",""],
    ["\u3000",""],
    ["\n",""]
]
keywords = [
    "购","买","方",
    "销","售",
    "密","码","区",
    "名称","纳税人识别号","地址、电话","开户行及账号",
]
key = "纳税人识别号"
def pure(text):
    for r in replacements:
        text = text.replace(*r)
    return text

def draw_box(b,arg):
    plt.plot([b[0],b[0],b[2],b[2],b[0]],[b[1],b[3],b[3],b[1],b[1]],arg)
if __name__ == "__main__":
    if len(sys.argv) != 2:
        "script.py [dirname]"
    directory = sys.argv[1]
    count = 0
    print("file count : ",len(os.listdir(directory)))
    for filename in os.listdir(directory):
        if not filename.endswith('.pdf'):
            print(filename,"skip")
        count += 1
        if count > 3:
            break
        print(count,filename)
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
            print(page_box)
            interpreter.process_page(page)
            layout = device.get_result()
            h_line = []
            v_line = []
            for o in layout:
                if isinstance(o, LTTextBox):
                    x, y, text = o.bbox[0], o.bbox[1], o.get_text()
                    # print(o.bbox,text)
                    text = pure(text)
                    arg = "r."
                    if key in text:
                        print("found key ! ",text,x/w,y/h)
                        arg = "r*"
                    plt.text(x/w,y/h,text)
                    plt.plot(x/w,y/h,arg)
                if isinstance(o, LTLine):
                    b = np.array(o.bbox)/[w,h,w,h]
                    draw_box(b,'y')
                    if b[0] != b[2] and b[1] != b[3]:
                        print(b)
                    pass
                if isinstance(o, LTRect):
                    b = np.array(o.bbox)/[w,h,w,h]
                    draw_box(b,'b')
                    pass
        plt.show()