'''
该模型为数据源表
涂迅
2023/6/21
'''
from sqlalchemy import Column, Integer, String, DateTime, Float,DECIMAL,NUMERIC,INTEGER,CHAR,VARCHAR,DATETIME,INT,BINARY,SMALLINT
from sqlalchemy.ext.declarative import declarative_base

# 创建一个基类
Base = declarative_base()

class A01(Base):
    __tablename__ = 'a01'
    a0188 = Column(INTEGER,nullable=False,primary_key=True) # uid
    a0190 = Column(VARCHAR(20),nullable=True,index=True) #员工号
    a0101 = Column(VARCHAR(20),nullable=False,index=True) #姓名
    dept_1 = Column(VARCHAR(40),nullable=False) #一级机构
    dept_2 = Column(VARCHAR(40),nullable=False) #二级机构
    dept_code = Column(VARCHAR(200),nullable=False) #中心
    a0141 = Column(DATETIME(8),nullable=False) #入行时间
    a01145 = Column(DATETIME(8),nullable=True) #任现岗位时间
    a01686 = Column(VARCHAR(20),nullable=True) #行员等级
    e0101 = Column(VARCHAR(10),nullable=True) #岗位

    def __repr__(self):
        return f"<A01(a0190='{self.a0190}',a0101='{self.a0101}',dept_1='{self.dept_1}',dept_2='{self.dept_2}',dept_code='{self.dept_code}'" \
               f",a0141='{self.a0141}',a01145='{self.a01145}',a01686='{self.a01686}',e0101='{self.e0101}')>"

class A04(Base):
    __tablename__ = 'a04'
    recordid = Column(INTEGER,nullable=False,primary_key=True,autoincrement=True) # recordid
    a0447 = Column(VARCHAR(20), nullable=False)  # 教育类型
    endtime = Column(DATETIME(8), nullable=False)  # 终止时间
    a0431 = Column(VARCHAR(200), nullable=False)  # 学校
    a0429 = Column(VARCHAR(20), nullable=False)  # 学历
    a0440 = Column(VARCHAR(100), nullable=True)  # 学位
    fjo = Column(VARCHAR(1000), nullable=True)  # 学历附件
    fjt = Column(VARCHAR(1000), nullable=True)  # 学位附件
    fj3 = Column(VARCHAR(1000), nullable=True)  # 学信网在线验证报告

    def __repr__(self):
        return f"<A04(a0447='{self.a0447}',endtime='{self.endtime}',a0431='{self.a0431}',a0429='{self.a0429}',a0440='{self.a0440}',fjo='{self.fjo}',fjt='{self.fjt}',fj3='{self.fj3}')>"

class A8145(Base):
    __tablename__ = 'a8145'
    recordid = Column(INTEGER,nullable=False,primary_key=True,autoincrement=True) # record id
    a81452 = Column(DATETIME(8),nullable=True) #发现日期
    a81453 = Column(VARCHAR(20),nullable=True) #扣分

    def __repr__(self):
        return f"<A8145(a81452='{self.a81452}',a81453='{self.a81453}')>"

class A815(Base):
    __tablename__ = 'a815'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    a0188 = Column(INTEGER,nullable=False,index=True) # 员工号，姓名
    a81535 = Column(VARCHAR(5),nullable=True)# 表彰奖励年月

    def __repr__(self):
        return f"<A815(a0188='{self.a0188}',a81535='{self.a81535}')>"


class A8192(Base):
    __tablename__ = 'a8192'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    a0188 = Column(INTEGER,nullable=False) #姓名

    def __repr__(self):
        return f"<A8192(a0188='{self.a0188}')>"

class A832(Base):
    __tablename__ = 'a832'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    a83211 = Column(VARCHAR(100),nullable=False) #证书名称

    def __repr__(self):
        return f"<A832(a83211='{self.a83211}')>"

class A864(Base):
    __tablename__ = 'a864'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    a0188 = Column(INTEGER, nullable=False)  # 姓名
    a86412 = Column(VARCHAR(30), nullable=False)  # 与本人关系

    def __repr__(self):
        return f"<A864(a0188='{self.a0188}',a86412='{self.a86412}')>"

class A865(Base):
    __tablename__ = 'a865'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    a0188 = Column(INTEGER, nullable=False)  # 姓名

    def __repr__(self):
        return f"<A864(a0188='{self.a0188}')>"



class A866(Base):
    __tablename__ = 'a866'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    a8661 = Column(DATETIME(8),nullable=False) #起始时间
    a8662 = Column(DATETIME(8),nullable=True) #终止时间

    def __repr__(self):
        return f"<A866(a8661='{self.a8661}',a8662='{self.a8662}')>"

class A875(Base):
    __tablename__ = 'a875'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    gz_ym = Column(VARCHAR(6),nullable=False) # 年月
    a0188 = Column(INT(4),nullable=False,index=True) # 姓名

    def __repr__(self):
        return f"<A875(gz_ym='{self.gz_ym}',a0188='{self.a0188}')>"


class Bm_gxsjb(Base):
    __tablename__ = 'bm_gxsjb'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    sfsyl = Column(VARCHAR(20),nullable=True) #是否双一流
    sfjbw = Column(VARCHAR(20),nullable=True) #是否985
    sf = Column(VARCHAR(20),nullable=True) #是否211
    qs100 = Column(VARCHAR(20),nullable=True) #是否QS100
    sfqs2 = Column(VARCHAR(20),nullable=True) #是否QS200

    def __repr__(self):
        return f"<Bm_gxsjb(sfsyl='{self.sfsyl}',sfjbw='{self.sfjbw}',sf='{self.sf}',qs100='{self.qs100}',sfqs2='{self.sfqs2}')>"

# class Empat17(Base):
# __tablename__ = 'empat17'
#
#     def __repr__(self):
#         return f"<Empat17(
# class Empat18(Base):
# __tablename__ = 'empat18'
#
#     def __repr__(self):
#         return f"<Empat18(
# class Empat19(Base):
# __tablename__ = 'empat19'
#
#     def __repr__(self):
#         return f"<Empat19(
class Gxlygydjx(Base):
    __tablename__ = 'gxlygydjx'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    yjjxje = Column(NUMERIC(19,2),nullable=True) #月均绩效金额

    def __repr__(self):
        return f"<Gxlygydjx(yjjxje='{self.yjjxje}')>"

class K_month(Base):
    __tablename__ = 'k_month'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    gz_ym = Column(VARCHAR(6),nullable=False) #年月
    leave_time_11 = Column(NUMERIC(19,2),nullable=True) #事假天数
    leave_time_12 = Column(NUMERIC(19,2),nullable=True) #病假天数

    def __repr__(self):
        return f"<K_month(gz_ym='{self.gz_ym}',leave_time_11='{self.leave_time_11}',leave_time_12='{self.leave_time_12}')>"

class Tability(Base):
    __tablename__ = 'tability'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    totalscore = Column(DECIMAL(4,2),nullable=False) #总分

    def __repr__(self):
        return f"<Tability(totalscore='{self.totalscore}')>"

class Tpersonality(Base):
    __tablename__ = 'tpersonality'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    dominance = Column(INTEGER,nullable=False) #支配型
    influence = Column(INTEGER,nullable=False) #影响型
    steadiness = Column(INTEGER,nullable=False) #支持型
    compliance = Column(INTEGER,nullable=False) #思考型

    def __repr__(self):
        return f"<Tpersonality(dominance='{self.dominance}',influence='{self.influence}',steadiness='{self.steadiness}',compliance='{self.compliance}')>"


