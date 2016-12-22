from .Sql import Sql
from twisted.internet.threads import deferToThread
from ny.items import infoitem
from ny.items import lxitem
from ny.items import Qyitem
# from ny.items import DingdianItem

class nypipelines(object):
    # def __init__(self):
    #     Sql.__init__()

    def process_item(self,item,spider):
        if isinstance(item, lxitem):
            lxmc = item['lxmc']
            ret = Sql.select_type(lxmc)
            if ret:
                print('已经存在农药类型名称')
                pass
            else:
                Sql.insert_type(lxmc)
                print('开始存农药类型')
        if isinstance(item,infoitem):
            yxcfcn = item['yxcfcn']
            ret=Sql.select_name(yxcfcn)
            # if ret[0]==1:
            if ret:#如果存在该条信息
                print('已经存在该条有效成分信息')
                pass
            else:
                yxcfen=item['yxcfen']
                Sql.insert_yxcf(yxcfcn,yxcfen)
                print('开始存有效成分',yxcfcn)
        if isinstance(item,infoitem):
            jxmc=item['jxmc']
            ret=Sql.select_JX(jxmc)
            if ret:
                print('已经存在该条剂型信息')
                pass
            else:
                Sql.insert_JX(jxmc)
                print('开始存剂型信息',jxmc)
        if isinstance(item,infoitem):
            pestname=item['pest']
            if pestname:
                ret=Sql.select_pest(pestname)
                if ret:
                    print('已经存在该条病虫害信息',pestname)
                    pass
                else:
                    Sql.insert_pest(pestname)
                    print('开始存病虫害信息',pestname)
        if isinstance(item,infoitem):
            djzh=item['djzh']
            yxcfcn=item['yxcfcn']
            yzid=Sql.getYxcfId(yxcfcn)[0]
            yxcfhl=item['yxcfhl']
            yxcfhldw=item['yxcfhldw']
            ret=Sql.select_djzh(djzh)
            if ret:
                print('已经存在该农药有效成分含量',yxcfcn)
                pass
            else:
                Sql.insert_yxcfhl(djzh,yzid,yxcfhl,yxcfhldw)
                print('开始存农药有效成分含量',yxcfcn)
        if isinstance(item,infoitem):
            #djzh,djmc,lxmc,jxmc,zhl,yxqjzr,qyid,yxqqsr,gj,dx,bz
            djzh=item['djzh']
            djmc=item['djmc']
            jxmc=item['jxmc']
            zhl=item['zhl']
            zhldw=item['zhldw']
            yxqjzr=item['yxqjzr']
            sccj=item['sccj']
            yxqqsr=item['yxqqsr']
            gj=item['gj']
            dx=item['dx']
            bz=item['bz']
            ret=Sql.select_NYdjzh(djzh)
            if ret:
                print('该农药信息已经被登记')
                pass
            else:
                Sql.insert_nyxxdj(djzh,djmc,jxmc,zhl,zhldw,yxqjzr,sccj,yxqqsr,gj,dx,bz)
                print('正在存储该条农药信息')

        if isinstance(item,Qyitem):
            dwmc=item['dwmc']
            proName=item['province']
            province =Sql.getProId(proName)
            gj=item['gj']
            countyName=item['county']
            county=Sql.getCityId(countyName)
            xzjd=item['xzjd']
            yb=item['yb']
            dh=item['dh']
            fix=item['fix']
            lxr=item['lxr']
            dwdz=item['dwdz']
            email=item['email']
            dwlx=item['dwlx']
            ret=Sql.select_dwmc(dwmc)
            if ret:
                print(dwmc,'企业信息已经存在')
                pass
            else:
                Sql.insert_qyxx(dwmc=dwmc,province=province,gj=gj,county=county,xzjd=xzjd,yb=yb,dh=dh,fix=fix,lxr=lxr,dwdz=dwdz,email=email,dwlx=dwlx)
                print('开始存企业信息',dwmc)
# # class nyType(object):
# #     def process_item(self,item1,spider):
#     if isinstance(item, lxitem):
#         lxmc = item['lxmc']
#         ret = Sql.select_type(lxmc)
#         if ret:
#             print('已经存在农药类型名称')
#             pass
#         else:
#             Sql.insert_type(lxmc)
#             print('开始存农药类型')
#
#
# class qyxx(object):
#     Sql.getList()
#     def process_item(self,qyxx,spider):
#         if isinstance(qyxx,Qyitem):
#             dwmc=qyxx['dwmc']
#             proName=qyxx['province']
#             province =Sql.getProId(proName)
#             gj=qyxx['gj']
#             countyName=qyxx['county']
#             county=Sql.getCityId(countyName)
#             xzjd=qyxx['xzjd']
#             yb=qyxx['yb']
#             dh=qyxx['dh']
#             fix=qyxx['fix']
#             lxr=qyxx['lxr']
#             dwdz=qyxx['dwdz']
#             email=qyxx['email']
#             dwlx=qyxx['dwlx']
#             ret=Sql.select_dwmc(dwmc)
#             if ret:
#                 print(dwmc,'企业信息已经存在')
#                 pass
#             else:
#                 Sql.insert_qyxx(dwmc=dwmc,province=province,gj=gj,county=county,xzjd=xzjd,yb=yb,dh=dh,fix=fix,lxr=lxr,dwdz=dwdz,email=email,dwlx=dwlx)
#                 print('开始存企业信息',dwmc)