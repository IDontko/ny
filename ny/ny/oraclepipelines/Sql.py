import cx_Oracle
import ny.config


path = ny.config.username + '/' + ny.config.pwd + '@' + ny.config.port  # 数据库配置
conn = cx_Oracle.connect(path)
cursor =conn.cursor()
list_pro=[]
list_city=[]
class Sql:

    #从县和省的字典表，获取县和省的ID
    @classmethod
    def getList(cls):
        sql = "select AREAID,NAMECN from W_CITYCODE"#县id
        cursor.execute(sql)
        res=cursor.fetchall()
        for i in res:
            list_city.append(i[0])
            list_city.append(i[1])
        sql1="select CP_ID,CP_NAME from  CC_PROVICE"#省id
        cursor.execute(sql1)
        res1=cursor.fetchall()
        for j in res1:
            list_pro.append(j[0])
            list_pro.append(j[1])

    #有效成分
    @classmethod
    def insert_yxcf(cls,yxcfcn,yxcfen):
        sql='insert into NY_YXCFZDB ("NV_YXCFCN","NV_YXCFEN") VALUES (:1,:2)'
        value=[
            yxcfcn,
            yxcfen
        ]
        cursor.execute(sql,value)
        conn.commit()

    #通过有效成分查重
    @classmethod
    def select_name(cls,yxcfcn):
        sql = "select * from NY_YXCFZDB WHERE exists (SELECT 1 FROM NY_YXCFZDB WHERE NV_YXCFCN =:1)"
        value=[yxcfcn]
        cursor.execute(sql,value)
        # cursor.execute(sql)
        return cursor.fetchone()

    #剂型名称
    @classmethod
    def insert_JX(cls,jxmc):
        sql="insert into NY_JX (JXMC) VALUES (:1) "
        value=[
            jxmc
        ]
        cursor.execute(sql,value)
        conn.commit()

    @classmethod
    def select_JX(cls,jxmc):
        sql = "select * from NY_JX WHERE exists (SELECT 1 FROM NY_JX WHERE JXMC =:1)"
        value=[jxmc]
        cursor.execute(sql,value)
        # cursor.execute(sql)
        return cursor.fetchone()

    #病虫害名称
    @classmethod
    def insert_pest(cls,pestname):
        sql = "insert into NY_PEST (PESTNAME) VALUES (:1) "
        value = [
            pestname
        ]
        cursor.execute(sql, value)
        conn.commit()

    @classmethod
    def select_pest(cls, pestname):
        sql = "select * from NY_PEST WHERE exists (SELECT 1 FROM NY_PEST WHERE PESTNAME =:1)"
        value = [
            pestname
        ]
        cursor.execute(sql,value)
        # cursor.execute(sql)
        return cursor.fetchone()

    #农药类型字典表
    @classmethod
    def insert_type(cls,lxmc):
        sql = "insert into NY_TYPE (LXMC) VALUES (:1) "
        value = [
            lxmc
        ]
        cursor.execute(sql, value)
        conn.commit()

    @classmethod
    def select_type(cls, lxmc):
        sql = "select * from NY_TYPE WHERE exists (SELECT 1 FROM NY_TYPE WHERE LXMC =:1)"
        value = [
            lxmc
        ]
        cursor.execute(sql,value)
        # cursor.execute(sql)
        return cursor.fetchone()

    #企业信息
    @classmethod
    def insert_qyxx(cls,dwmc,province,gj,county,xzjd,yb,dh,fix,lxr,dwdz,email,dwlx):
        sql="insert into NY_QYXX (dwmc,province,gj,county,xzjd,yb,dh,fix,lxr,dwdz,email,dwlx)VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12)"
        value=[
            dwmc,
            province,
            gj,
            county,
            xzjd,
            yb,
            dh,
            fix,
            lxr,
            dwdz,
            email,
            dwlx
        ]
        cursor.execute(sql,value)
        conn.commit()

    @classmethod
    def select_dwmc(cls,dwmc):
        sql = "select * from NY_QYXX WHERE exists (SELECT 1 FROM NY_QYXX WHERE DWMC =:1)"
        value = [
            dwmc
        ]
        cursor.execute(sql,value)
        # cursor.execute(sql)
        return cursor.fetchone()

    #w_Citycode获得城市所对应的id
    # @classmethod
    # def getCityId(cls,cityname):
    #     sql = "select AREAID,NAMECN from W_CITYCODE"

    #获得省对应的id,如果存在省的id，返回该省所对应的id ，参数为省的名称
    @classmethod
    def getProId(cls,proName):
        if proName in list_pro:
            i=list_pro.index(proName)
            return list_pro[i-1]
        else:
            print('不存在该省名称')
            return -1
    @classmethod
    def getCityId(cls,cityName):
        newCityName=cityName.replace('县','')#为了与数据库匹配，去掉‘县’字
        if newCityName in list_city:
            i=list_city.index(newCityName)
            return list_city[i-1]
        else:
            print('不存在该县名称或者表中没有相关信息',newCityName)
            return -1

    #获得类型ID
    @classmethod
    def getTypeID(cls,lxmc):
        sql="select LXID from NY_TYPE WHERE exists (SELECT 1 FROM NY_TYPE WHERE LXMC=:1)"
        value=[
            lxmc
        ]
        cursor.execute(sql,value)
        return cursor.fetchone()

    #获得剂型ID
    @classmethod
    def getJxId(cls,jxmc):
        sql="select JXID from NY_JX WHERE exists (SELECT 1 FROM NY_JX WHERE JXMC=:1)"
        value=[
            jxmc
        ]
        cursor.execute(sql,value)
        return cursor.fetchone()

    #获得有效成分ID
    @classmethod
    def getYxcfId(cls,yxcfcn):
        sql="select NY_YZID from NY_YXCFZDB WHERE  NV_YXCFCN=:1 "
        value=[
            yxcfcn
        ]
        cursor.execute(sql,value)
        return cursor.fetchone()

    #插入有效成分含量表
    @classmethod
    def insert_yxcfhl(cls,djzh,yzid,yxcfhl,yxcfhldw):
        sql="insert into NY_YXCFHL (NY_DJZH,NY_YZID,NY_YXCFHL,NY_YXCFHL_DW)VALUES (:1,:2,:3,:4)"
        value=[
            djzh,
            yzid,
            yxcfhl,
            yxcfhldw
        ]
        cursor.execute(sql,value)
        conn.commit()

    #查询登记证号
    @classmethod
    def select_djzh(cls,djzh):
        sql="select * from NY_YXCFHL WHERE exists (SELECT 1 FROM NY_YXCFHL WHERE NY_DJZH=:1 )"
        value=[
            djzh
        ]
        cursor.execute(sql,value)
        return cursor.fetchone()
    #查询生产厂家id(企业ID）
    @classmethod
    def select_sccjId(cls,sccj):
        sql="select QYID from  NY_QYXX WHERE DWMC=:1 "
        value=[
            sccj
        ]
        cursor.execute(sql,value)
        return cursor.fetchone()
    #查询农药登记信息表该登记证号有没有数据
    @classmethod
    def select_NYdjzh(cls, djzh):
        sql = "select * from NY_NYDJXX WHERE exists (SELECT 1 FROM NY_NYDJXX WHERE NY_DJZH=:1 )"
        value = [
            djzh
        ]
        cursor.execute(sql, value)
        return cursor.fetchone()

    #农药登记信息表
    @classmethod
    def insert_nyxxdj(cls,djzh,djmc,jxmc,zhl,zhldw,yxqjzr,sccj,yxqqsr,gj,dx,bz):
        sql="insert into NY_NYDJXX(NY_DJZH,NY_DJMC,NY_JX,NY_ZHL,NY_ZHL_DW,NY_YXQJZR,NY_QY,NY_YXQQSR,NY_GJ,NY_DX,NY_BZ) VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11)"
        jxid=Sql.getJxId(jxmc)[0]
        sccjid=Sql.select_sccjId(sccj)[0]
        value=[
            djzh,
            djmc,
            jxid,
            zhl,
            zhldw,
            yxqjzr,
            sccjid,
            yxqqsr,
            gj,
            dx,
            bz
        ]
        cursor.execute(sql,value)
        conn.commit()
