# -*- coding:utf-8 -*-
port='192.168.1.114:1521/orcl_backups'#数据库所在地址及其端口

username='bigdata'#数据库登录用户名

pwd='bigdata'#数据库登录密码

pagecount=1777#你要爬取的页数

YxDate='2011-11-01' #农药的有效日期，根据该字段来查询有效日期之后的信息。 格式必须是 Y-M-D


# tableName='CC_PRICE'#数据库表名


#要爬取的地址列表，一定要用中括号将URL包裹，地址分别为新发地市场的蔬菜，水果和粮油地址
#原地址为http://www.xinfadi.com.cn/marketanalysis/1/list/1.sthml，后面的1.shtml就是页号，代码中进行了循环处理，只需要制定页码就可以了

