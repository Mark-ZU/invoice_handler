from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import sys, os, re, random
from mplfonts import use_font
import matplotlib.pyplot as plt
import numpy as np
import invoice as I
import layout as L
import traceback

show=True

DEBUG_COUNT = 0

replacements = [
    ["\n\n","\n"],
    [" ",""],
    ["\t",""],
    ["\u3000",""],
    # ["\n",""]
]
plt.rcParams.update({'font.size': 10})
use_font('Noto Serif CJK SC')

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def pure(text):
    for r in replacements:
        text = text.replace(*r)
    return text

class Dealer(object):
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.pdf_urls = []
        self.r = r"[-+]?(?:\d*\.\d+|\d+)"

        self.driver = self._set_driver(show)
        self.driver.delete_all_cookies()

        self.success = 0
        self.num = 0
        self.failed = 0
        self.failed_urls = []
    def run(self):
        self._get_all_pdf_url()
        random.shuffle(self.pdf_urls)
        count = 0
        for url in self.pdf_urls:
            print("url : ",url)
            self.num += 1
            self._deal(url)
            count += 1
            if DEBUG_COUNT > 0 and count >= DEBUG_COUNT:
                break
        print("total : {},success : {},failed : {}".format(self.num,self.success,self.failed))
        print("urls : {}".format(self.failed_urls))
    def _get_all_pdf_url(self):
        self.driver.get(self.base_url)
        all_a = self.driver.find_elements(By.XPATH,"//a")
        for a in all_a:
            self.pdf_urls.append(a.get_attribute("href"))
    def _deal(self,url):
        fig, ax = plt.subplots(1,1,figsize=(20,12))
        ax.invert_yaxis()
        grid = L.Grid()
        self.driver.get(url)
        self.driver.implicitly_wait(7)
        page = self.driver.find_element(By.XPATH,"//div[@class='textLayer']")
        width = float(re.findall(self.r,page.value_of_css_property('width'))[0])
        height = float(re.findall(self.r,page.value_of_css_property('height'))[0])
        elements = page.find_elements(By.XPATH,"./span")

        bb = np.array([9999,9999,0,0])
        for e in elements:
            try:
                text = pure(e.text)
                if len(text) == 0:
                    continue
                left_re = e.value_of_css_property('left')
                top_re = e.value_of_css_property('top')
                left = float(re.findall(self.r,left_re)[0])
                top = float(re.findall(self.r,top_re)[0])
                bb[0] = min(bb[0],left)
                bb[1] = min(bb[1],top)
                bb[2] = max(bb[2],left)
                bb[3] = max(bb[3],top)
            except Exception as ex:
                pass

        w = bb[2] - bb[0]
        h = bb[3] - bb[1]
        pb = bb + np.array([-w,-h,w,h])*0.01
        width = pb[2] - pb[0]
        height = pb[3] - pb[1]
        for e in elements:
            try:
                text = pure(e.text)
                if len(text) == 0:
                    continue
                left_re = e.value_of_css_property('left')
                top_re = e.value_of_css_property('top')
                left = (float(re.findall(self.r,left_re)[0]) - pb[0])/width
                top = (float(re.findall(self.r,top_re)[0]) - pb[1])/height
                grid.add([left,top],text)
            except Exception as ex:
                pass
        try:
            res = I.parse_info(grid)
            self.success += 1
        except BaseException as e:
            self.failed += 1
            self.failed_urls.append(url)
            # print("----------------------------\n",grid,"---------------------------------")
            print(str(e))
            traceback.print_exc()

            # for n in grid.nodes:
            #     ax.text(n.v[0],n.v[1],n.text,horizontalalignment='left',verticalalignment='top')
            #     ax.plot(n.v[0],n.v[1],".")
            # for n in grid.vIndex.lists:
            #     ax.plot([n.v[0],n.v[0]],[0,1],"b")
            # for n in grid.hIndex.lists:
            #     ax.plot([0,1],[n.v[1],n.v[1]],"y")
            # plt.show()
        plt.close(fig)

    def _set_driver(self,need_display=False):
        options = Options()
        profile = webdriver.FirefoxProfile("/home/mark/firefoxautoprofile")
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False) 
        profile.set_preference("geo.prompt.testing", True)
        profile.set_preference("geo.prompt.testing.allow", True)
        profile.set_preference("geo.provider.network.url",'data:application/json,{"status": "OK","accuracy": 10.0,"location":{"lat": 30.265,"lng":120.125,"latitude":30.265,"longitude":120.125,"accuracy":10}}')
        if not need_display:
            options.add_argument('--headless')
        return webdriver.Firefox(firefox_profile=profile,options=options)

test_urls = None
# test_urls = [
#     "http://localhost:8000/%E8%81%94%E8%BD%B4%E5%99%A866.pdf",
#     "http://localhost:8000/%E6%B8%85%E6%B4%97%E6%9C%BA649.pdf"
# ]
if __name__ == '__main__':
    if test_urls is None:
        dealer = Dealer()
        dealer.run()
    else:
        dealer = Dealer()
        for url in test_urls:
            dealer._deal(url)

