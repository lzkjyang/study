# -*- encode:utf8 -*-
'''
author： yangzhengwu
data:2020/02/15
dsc: search Keywords of taobao ,and download information
'''

import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from config import *

KEYWD = u'机床工作灯'

class Taobao(object):
    ''' ChromeBrowser do 'Login、search as keywords and dsc by user 、download infomaiton  for taobao  '''

    def __init__(self,*args,**kwargs):
        ''' init taobao CSSselector ,chromewebdriver,...'''
        self._tbrowser = webdriver.Chrome()
        self._wait = WebDriverWait(self._tbrowser , 15)
        self._searchtxt = '#q'
        self._searchbutton ="#J_TSearchForm > div.search-button > button"
        self._totalpagestxt = "#mainsrp-pager > div > div > div > div.total"
        self._localpagetxt = "#mainsrp-pager > div > div > div > div.form > input"
        self._pageitemactive = '#mainsrp-pager > div > '\
                                                     'div > div > ul > '\
                                                     'li.item.active > '\
                                                     'span'
        self._nextpagebutton = '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'
        self._itemlist = '#mainsrp-itemlist .items .item'
        self._sortselldesc = '#J_relative > div.sort-row > div > ul > li:nth-child(2) > a'
        self._sortcreditdesc = '#J_relative > div.sort-row > div > ul > li:nth-child(3) > a'
        # J_relative > div.sort-row > div > ul > li.sort.has-droplist.J_LaterHover > ul > li:nth-child(1) > a
        super(Taobao).__init__(*args,**kwargs)

    def _Login(self):
        """ login by chrome scan QC"""
        #self._browser = webdriver.Chrome()
        print("正在登录")
        # 需要用手机淘宝扫二维码登录才能搜索
        self._tbrowser.get(url='https://login.taobao.com')
        # 10s用来扫码登录
        self._tbrowser.implicitly_wait(10)

    def _Search(self,keyw =None,desc=None):
        ''' search kewords for taobao ,sort by user default None is  sortDefault'''
        print("正在查找",keyw)
        try:
            input = self._wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self._searchtxt))
            )
            submit = self._wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self._searchbutton))
            )
            input.send_keys(keyw)
            submit.click()
            self._total = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                        self._totalpagestxt)))
            self._Downinfo()
        except TimeoutError:
            raise "QC timeout"

    def _Downinfo(self):
        #self._flag = 0
        try:
            self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                       '#mainsrp-itemlist .items '
                                                       '.item')))
            html = self._tbrowser.page_source
            self._tdoc= pq(html)
            self._items = self._tdoc('#mainsrp-itemlist .items .item').items()
            #self._flag = 1
            #self._blockgoods()
        except:
            raise ("获取商品失败")

    def GetGoods(self,keyword=None,desc=None):
        ''' download goods for taoboo as kewords by user, iter for result'''
        # login taobao by QC
        self._Login()
        # search keywords return total pages
        self._Search(keyw=keyword,desc=desc)
        total = int(re.compile('(\d+)').search(str(self._total.text)).group(0))
        print(" Total pages :{0}".format(total))
        #self._Downinfo() # 后面加个判断 来做_blockgoods()
        #if self._flag:
        #    self._blockgoods()
        yield self._blockgoods()
        for i in range(2,total+1):
            if i%15 == 0:
                time.sleep(20)
            self._NextPage(i)
            yield self._blockgoods()



    def _blockgoods(self):
        res = []
        for item in self._items:
            self._goods = {
                'img': item.find('.pic .img').attr('data-src'),
                'price': item.find('.price').text(),
                'deal': item.find('.deal-cnt').text(),
                'title': item.find('.title').text(),
                'shop': item.find('.shop').text(),
                'location': item.find('.location').text()
            }
            #print(self._goods)
            res.append(self._goods)
        return res




    def _NextPage(self,page_number):
        ''' next page inner func'''
        print("正在换页", page_number)
        try:
            input = self._wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,self._localpagetxt))
            )
            submit = self._wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,self._nextpagebutton))
            )
            input.clear()
            input.send_keys(page_number)
            submit.click()
            self._wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,self._pageitemactive), str(page_number)))
            self._Downinfo()
        except Exception as e:
            raise(e)

if __name__ == '__main__':
    Myworker = Taobao()
    res = Myworker.GetGoods(keyword=KEYWD)
    for lres in res:
        for k,v in enumerate(lres):
            print("{0}:\t{1}".format(k,v))

