# SQLALCHEMY

- SQLAlchemy、Peewee、Django ORM

## 为什么使用ORM

-  sql拼接- 注入漏洞
-  模型定义甚至与数据库无关，便于后续数据库的切换（可能存在兼容性稳定）


## 模型定义

    # coding=utf-8
    from __future__ import unicode_literals, absolute_import
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer, String, DateTime
    ModelBase = declarative_base() #<-元类
    
    class User(ModelBase):
        __tablename__ = "auth_user"
    
        id = Column(Integer, primary_key=True)
        date_joined = Column(DateTime)
        username = Column(String(length=30))
        password = Column(String(length=128))
        
## 增

with get_session() as session:
    session.add(User(username="asd", password="asd"))
    session.add(User(username="qwe", password="qwe"))
    session.commit()
    
##　查

with get_session() as session:
    # <class 'sqlalchemy.orm.query.Query'>
    session.query(User)
    
    