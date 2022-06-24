import sys
import invoice
from pdfminer.layout import *
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

import matplotlib.pyplot as plt
import os
from mplfonts import use_font

use_font('Noto Serif CJK SC')

def draw_rec(x1,y1,x2,y2,*args):
    pass
if __name__ == "__main__":
    if len(sys.argv) != 2:
        "script.py [dirname]"
    directory = sys.argv[1]
    count = 0
    print("file count : ",len(os.listdir(directory)))
    for filename in os.listdir(directory):
        if not filename.endswith('.pdf'):
            print(filename,"skip")
        print(count)
        count += 1
        if count > 1:
            break
        fp = open(os.path.join(directory,filename), 'rb')
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pages = PDFPage.get_pages(fp)

        texts = []
        xs = []
        ys = []
        for page in pages:
            page_box = page.mediabox
            print(page_box)
            interpreter.process_page(page)
            layout = device.get_result()
            for lobj in layout:
                if isinstance(lobj, LTTextBox):
                    x, y, text = lobj.bbox[0], lobj.bbox[1], lobj.get_text()
                    xx = x/page_box[2]
                    yy = y/page_box[3]
                    plt.text(xx,yy,text[:-1])
                    plt.plot(xx,yy,'r.')

                if isinstance(lobj, LTTextLineHorizontal):
                    x = lobj.bbox
                    print(x)
                    plt.plot([x[0]/page_box[2],x[1]/page_box[2]],[x[2]/page_box[3],x[3]/page_box[3]],'b-')
    plt.show()