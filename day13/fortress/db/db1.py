#!/usr/bin/env python3
# Author: Zhangxunan
from sqlalchemy import create_engine, and_, or_, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import sessionmaker, relationship

# 生成一个SqlORM 基类
Base = declarative_base()


# 服务器用户和组
class HostUser2Group(Base):
    __tablename__ = 'host_user_2_group'
    id = Column(Integer, primary_key=True)
    host_user_id = Column(Integer, ForeignKey('host_users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))


# 用户和组关系表，用户可以属于多个组，一个组可以有多个人
class UserProfile2Group(Base):
    __tablename__ = 'user_profile_2_group'
    id = Column(Integer, primary_key=True)
    user_profile_id = Column(Integer, ForeignKey('user_profile.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))


# 程序登陆用户和服务器账户，一个人可以有多个服务器账号，一个服务器账号可以给多个人用
class UserProfile2HostUser(Base):
    __tablename__ = 'user_profile_2_host_user'
    id = Column(Integer, primary_key=True)
    user_profile_id = Column(Integer, ForeignKey('user_profile.id'))
    host_user_id = Column(Integer, ForeignKey('host_users.id'))


class Host(Base):
    __tablename__ = 'hosts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(64), unique=True, nullable=False)
    ip_address = Column(String(128), unique=True, nullable=False)
    port = Column(Integer, default=22)

    def __repr__(self):
        return "<id=%s,hostname=%s, ip_address=%s>" % (self.id, self.hostname, self.ip_addr)


class HostUser(Base):
    __tablename__ = 'host_users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(255))

    host_id = Column(Integer, ForeignKey('hosts.id'))

    groups = relationship('Group', secondary=lambda: HostUser2Group.__table__, backref='host_list')

    __table_args__ = (UniqueConstraint('host_id', 'username', name='_host_username_uc'),)

    def __repr__(self):
        return "<id=%s,name=%s>" % (self.id, self.username)


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)

    def __repr__(self):
        return "<id=%s,name=%s>" % (self.id, self.name)


class UserProfile(Base):
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    host_list = relationship('HostUser', secondary=lambda: UserProfile2HostUser.__table__, backref='user_profile')
    groups = relationship('Group', secondary=lambda: UserProfile2Group.__table__, backref='user_profile')

    def __repr__(self):
        return "<id=%s,name=%s>" % (self.id, self.username)


class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    user_profile_id = Column(Integer, ForeignKey('user_profile.id'))
    host_user_id = Column(Integer, ForeignKey('host_users.id'))
    cmd = Column(String(255))
    date = Column(DateTime)

    user_profile = relationship("UserProfile", backref='audit_log')
    host_user = relationship("HostUser", backref='audit_log')


engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/fortress", max_overflow=5)
Base.metadata.create_all(engine)
