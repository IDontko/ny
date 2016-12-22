# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class infoitem(scrapy.Item):
    #登记证号
    djzh=scrapy.Field()
    #登记名称
    djmc=scrapy.Field()
    #总含量
    zhl=scrapy.Field()
    #总含量单位
    zhldw=scrapy.Field()
    #有效期截止日
    yxqjzr=scrapy.Field()
    #有效期起始日
    yxqqsr=scrapy.Field()
    #生产厂家
    sccj=scrapy.Field()
    #国家
    gj=scrapy.Field()
    #毒性
    dx=scrapy.Field()
    #备注
    bz=scrapy.Field()

    #有效成分中文名
    yxcfcn=scrapy.Field()
    #有效成分英文名
    yxcfen=scrapy.Field()
    # 剂型名称
    jxmc = scrapy.Field()
    #病虫害名称
    pest=scrapy.Field()
    #有效成分含量
    yxcfhl=scrapy.Field()
    #有效成分含量单位
    yxcfhldw=scrapy.Field()

class lxitem(scrapy.Item):
    # 类型名称
    lxmc=scrapy.Field()
# class jxitem(scrapy.Item):

class Qyitem(scrapy.Item):
    #单位名称
    dwmc=scrapy.Field()
    #省
    province=scrapy.Field()
    #国家
    gj=scrapy.Field()
    #县
    county=scrapy.Field()
    #乡镇街道
    xzjd=scrapy.Field()
    #邮编
    yb=scrapy.Field()
    #电话
    dh=scrapy.Field()
    #传真
    fix=scrapy.Field()
    #联系人
    lxr=scrapy.Field()
    #单位地址
    dwdz=scrapy.Field()
    #email
    email=scrapy.Field()
    #单位类型
    dwlx=scrapy.Field()


