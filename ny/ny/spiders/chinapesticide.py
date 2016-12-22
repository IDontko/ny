import scrapy
from bs4 import BeautifulSoup
import subprocess
import datetime
import time
from lxml import etree
from scrapy.http import Request
from selenium import webdriver
from scrapy.selector import Selector
from ny.items import infoitem
from ny.items import lxitem
from ny.items import Qyitem
from selenium.webdriver.common.keys import Keys
import ny.config
from ny.oraclepipelines.Sql import Sql
from scrapy.selector import HtmlXPathSelector
import selenium

# 自己的spider文件


class myspider(scrapy.Spider):
    name = 'pesticide'
    allow_domains = ['chinapesticide.gov.cn']
    start_urls = ['http://www.chinapesticide.gov.cn/myquery/queryselect']
    # base_url='http://www.chinapesticide.gov.cn/myquery/queryselect'

    def __init__(self):
        self.htmlList = []  # 用来存储所有的网页源码
        self.driver = webdriver.PhantomJS()
        self.driver.maximize_window()
        self.driver.get(self.start_urls[0])
        ele = self.driver.find_element_by_xpath(
            '//input[@class="Wdate"]')  # 获取有效日期的输入框
        # 原生JS移除readonly属性
        js = "document.getElementById('yxqs_start').removeAttribute('readonly')"
        self.driver.execute_script(js)  # 执行JS
        ele.send_keys(ny.config.YxDate)  # 输入有效日期
        time.sleep(3)  # 为了让输入有效日期
        ele.send_keys(Keys.RETURN)
        ele_btn = self.driver.find_element_by_id('btnSubmit')  # 找到查询按钮
        ele_btn.click()

    def nextPage(self):
        next_page = self.driver.find_element_by_xpath(
            '//div[@class="pagination"]/ul/li[last()-1]/a')
        print('正在翻页。。。')
        next_page.click()

    def parse(self, response):
        # yield Request(url=self.start_urls[0],callback=self.getJboxHtmlList)
        yield Request(url=self.start_urls[0], callback=self.getAllinfo)
        # yield Request(url=self.start_urls[0],callback=self.getlxmc)

    # 获得农药类型 这个类的功能
    # def getlxmc(self,response):
    #     item1 = lxitem()
    #     page=1
    #     while page<3:
    #         lxmc = self.driver.find_elements_by_xpath('//*[@class="t4"]/span')
    #         j = 1
    #         while j < len(lxmc):
    #             print('类型名称：', lxmc[j].text)
    #             item1['lxmc'] = lxmc[j].text
    #             j += 6
    #             yield item1
    #         self.nextPage()
    #         page += 1

    def request(self):  # 请求农药查询网址
        # ele_btn.send_keys(Keys.RETURN)#单击回车
        elet3 = self.driver.find_elements_by_xpath(
            '//td[@class="t3"]/span/a')  # elet3为所有class="t3"的td标签的值，返回一个list
        return elet3

    # 这个类的功能也集成到下面了
    # def getJboxHtmlList(self,response):  # JBoxHTMLLIST
    #     page=1
    #     while page<3:
    #         elements = self.request()
    #     # print(type(elements))
    #         for i in elements:
    #             i.click()  # 点击该标签。
    #             # print(self.driver.page_source)
    #             html = etree.HTML(self.driver.page_source)
    #             result = html.xpath('//div[@id="jbox-content"]/iframe/@src')
    #             Jboxsrc = 'http://www.chinapesticide.gov.cn' + result[0]
    #             yield Request(Jboxsrc, callback=self.getInformation)  # 弹出页的html
    #             eletJboxClose = self.driver.find_element_by_xpath('//a[@class="jbox-close"]')  # 找到弹出窗口的关闭按钮
    #             eletJboxClose.click()  # 点击关闭
    #         self.nextPage()
    #         page+=1

    # 获得农药相关信息
    def getInformation(self, response):
        item = infoitem()
        # jxitem1=jxitem()
        # 登记证号
        djzh = Selector(text=response.text).xpath(
            '//div[@class="web_ser_body_right_main_search"]/table[1]/tr[2]/td[2]/text()').extract()
        item['djzh'] = str(djzh[0]).replace('\r', '').replace(
            '\n', '').replace('\t', '').strip()
        # 登记名称
        djmc = Selector(text=response.text).xpath(
            '//div[@class="web_ser_body_right_main_search"]/table[1]/tr[3]/td[2]/text()').extract()
        item['djmc'] = str(djmc[0])
        # 总含量
        zhl = Selector(text=response.text).xpath(
            '//div[@class="web_ser_body_right_main_search"]/table[1]/tr[5]/td[2]/text()').extract()
        # 总含量保留后两位小数
        if '克/升' not in zhl[0]:
            zhll = '%.2f' % float(str(zhl[0]).replace('%', ''))
            item['zhl'] = zhll
            item['zhldw'] = ''
        else:
            item['zhl'] = zhl[0].split('克/升')[0]
            item['zhldw'] = '克/升'

        # 有效起始日
        yxqqsr = Selector(text=response.text).xpath(
            '//div[@class="web_ser_body_right_main_search"]/table[1]/tr[2]/td[4]/text()').extract()
        # 转换为日期格式

        # datetime = datetime.datetime.strptime('Dec 29, 2011', '%b %d, %Y').date()
        item['yxqqsr'] = datetime.datetime.strptime(
            yxqqsr[0], '%b %d, %Y').date()  # str转日期类型

        # 有效日期截止日
        yxqjzr = Selector(text=response.text).xpath(
            '//div[@class="web_ser_body_right_main_search"]/table[1]/tr[2]/td[6]/text()').extract()
        item['yxqjzr'] = datetime.datetime.strptime(
            yxqjzr[0], '%b %d, %Y').date()  # str转日期类型
        # 国家
        gj = Selector(text=response.text).xpath(
            '//div[@class="web_ser_body_right_main_search"]/table[1]/tr[4]/td[4]/text()').extract()
        item['gj'] = gj[0]
        # 生产厂家
        sccj = Selector(text=response.text).xpath(
            '//div[@class="web_ser_body_right_main_search"]/table[1]/tr[4]/td[2]/a/text()').extract()
        item['sccj'] = sccj[0].replace('\r', '').replace(
            '\n', '').replace('\t', '').strip()
        # 毒性
        dx = Selector(text=response.text).xpath(
            '//div[@class="web_ser_body_right_main_search"]/table[1]/tr[3]/td[4]/text()').extract()
        item['dx'] = dx[0]
        # 备注
        bz = Selector(text=response.text).xpath(
            '//div[@class="web_ser_body_right_main_search"]/table[1]/tr[6]/td[2]/text()').extract()
        if bz:
            item['bz'] = bz[0]
        else:
            item['bz'] = '空'
        # 有效成分
        yxcf = Selector(text=response.text).xpath(
            '//div[@class="web_ser_body_right_main_search"]/table[3]/tr[3]/td[1]/text()').extract()
        YXCFinfo = yxcf[0].split('/')
        print('有效成分中文名称:', YXCFinfo[0])
        print('有效成分英文名称:', YXCFinfo[1])
        item['yxcfcn'] = str(YXCFinfo[0]).replace('/', '')
        item['yxcfen'] = str(YXCFinfo[1]).replace('/', '')
        # 有效成分含量
        yxcfhl = Selector(text=response.text).xpath(
            '//div[@class="web_ser_body_right_main_search"]/table[3]/tr[3]/td[2]/text()').extract()
        if '克/升' not in zhl[0]:
            yxcfhl = '%.2f' % float(str(yxcfhl[0]).replace('%', ''))
            item['yxcfhl'] = yxcfhl
            item['yxcfhldw'] = ''
        else:
            item['yxcfhl'] = yxcfhl[0].split('克/升')[0]
            item['yxcfhldw'] = '克/升'
        # 剂型
        jx = Selector(text=response.text).xpath(
            '//div[@class="web_ser_body_right_main_search"]/table[1]/tr[3]/td[6]/text()').extract()
        print('剂型信息:', jx)
        item['jxmc'] = jx[0]
        # 病虫害
        pest = Selector(text=response.text).xpath(
            '//div[@class="web_ser_body_right_main_search"]/table[4]/tr[3]/td[2]/text()').extract()
        print('病虫害信息:', pest)
        if pest:
            item['pest'] = pest[0]
        else:
            item['pest'] = None
        yield item

        # 企业信息列表
    def qyxx(self):
        elet4 = self.driver.find_elements_by_xpath('//td[@class="t4"]/span/a')
        return elet4

    def getAllinfo(self, response):
        # print('企业信息')
        page = 1
        while page < ny.config.pagecount:
            qyxx = self.qyxx()
            for j in qyxx:
                j.click()
                html = etree.HTML(self.driver.page_source)
                result = html.xpath('//div[@id="jbox-content"]/iframe/@src')
                # 这个是生产企业想信息的url
                Jboxsrc = 'http://www.chinapesticide.gov.cn' + result[0]
                yield Request(Jboxsrc, callback=self.getQyxxInfo)
                eletJboxClose = self.driver.find_element_by_xpath(
                    '//a[@class="jbox-close"]')  # 找到弹出窗口的关闭按钮
                eletJboxClose.click()

            item1 = lxitem()
            lxmc = self.driver.find_elements_by_xpath('//*[@class="t4"]/span')
            j = 1
            while j < len(lxmc):
                print('类型名称：', lxmc[j].text)
                item1['lxmc'] = lxmc[j].text
                j += 6
                yield item1

            elements = self.request()
            # print(type(elements))
            for i in elements:
                i.click()  # 点击该标签。
                # print(self.driver.page_source)
                html = etree.HTML(self.driver.page_source)
                result = html.xpath('//div[@id="jbox-content"]/iframe/@src')
                Jboxsrc = 'http://www.chinapesticide.gov.cn' + result[0]
                # 弹出页的html
                yield Request(Jboxsrc, callback=self.getInformation)
                eletJboxClose = self.driver.find_element_by_xpath(
                    '//a[@class="jbox-close"]')  # 找到弹出窗口的关闭按钮
                eletJboxClose.click()  # 点击关闭
            self.nextPage()
            page += 1

    # 农药企业信息表
    def getQyxxInfo(self, response):
        qyxx = Qyitem()
        # print(response.text)
        dwmc = Selector(text=response.text).xpath(
            '//div/table[1]/tr[2]/td[2]/a/text()').extract()
        qyxx['dwmc'] = dwmc[0].replace('\r', '').replace(
            '\n', '').replace('\t', '').strip()
        province = Selector(text=response.text).xpath(
            '//div/table[1]/tr[2]/td[4]/text()').extract()
        qyxx['province'] = province[0]
        gj = Selector(text=response.text).xpath(
            '//div/table[1]/tr[2]/td[last()]/text()').extract()
        qyxx['gj'] = gj[0]
        county = Selector(text=response.text).xpath(
            '// div/table[1]/tr[3]/td[2]/text()').extract()
        if county:
            qyxx['county'] = county[0]
        else:
            qyxx['county'] = '空'
        xzjd = Selector(text=response.text).xpath(
            '//div/table[1]/tr[3]/td[4]/text()').extract()
        qyxx['xzjd'] = xzjd[0]
        yb = Selector(text=response.text).xpath(
            '//div/table[1]/tr[3]/td[6]/text()').extract()
        qyxx['yb'] = yb[0]
        dh = Selector(text=response.text).xpath(
            '//div/table[1]/tr[4]/td[2]/text()').extract()
        qyxx['dh'] = dh[0]
        fix = Selector(text=response.text).xpath(
            '//div/table[1]/tr[4]/td[4]/text()').extract()
        qyxx['fix'] = fix[0]
        lxr = Selector(text=response.text).xpath(
            '//div/table[1]/tr[4]/td[6]/text()').extract()
        qyxx['lxr'] = lxr[0]
        dwdz = Selector(text=response.text).xpath(
            '//div/table[1]/tr[5]/td[2]/text()').extract()
        qyxx['dwdz'] = dwdz[0]
        email = Selector(text=response.text).xpath(
            '//div/table[1]/tr[5]/td[4]/text()').extract()
        if email:
            qyxx['email'] = email[0]
        else:
            qyxx['email'] = '空'
        dwlx = Selector(text=response.text).xpath(
            '//div/table[1]/tr[5]/td[6]/text()').extract()
        qyxx['dwlx'] = dwlx[0]
        print(dwmc)
        # return qyitem
        yield qyxx
