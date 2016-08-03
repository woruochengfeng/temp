#!/usr/bin/env python3
# Author: Zhangxunan

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Index, Table
from sqlalchemy.orm import sessionmaker, relationship

# 创建基类，所有创建表的类都要继承这个基类
Base = declarative_base()


class HostToHostUser(Base):
    """
    关系表，多对多的关系，存账户和服务器的对应关系，一台服务器上可以有多个账户，一个账户可以登录多个服务器
    """
    __tablename__ = 'host2host_user'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    host_id = Column(Integer, ForeignKey('hosts.id'))
    host_user_id = Column(Integer, ForeignKey('host_users.id'))


class Host(Base):
    """
    服务器表
    hostname: 主机名
    port: ssh端口,默认22
    ip: IP地址
    host_user: 和host_users表通过第三张表host2host_user建立关系
    """
    __tablename__ = 'hosts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(32))
    port = Column(String(32), default='22')
    ip = Column(String(32))

    host_user = relationship('HostUser', secondary=lambda: HostToHostUser.__table__, backref='host')


class HostUser(Base):
    """
    服务器帐户表
    username: 用户名
    password: 密码
    user_profile: 和user_profile表建立关系
    audit_log: 和audit_log表建立关系
    """
    __tablename__ = 'host_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32))
    password = Column(String(32))

    user_profile = relationship('UserProfile', backref='hostuser', userlist=False)
    audit_log = relationship('AuditLog', backref='host_user')


class Group(Base):
    """
    组表，堡垒机用户组表
    group_name: 组名
    user_profile: 和user_profile表建立关系
    """
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(32))

    user_profile = relationship('UserProfile', backref='group')


class UserProfile(Base):
    """
    堡垒机账户表，一对多关系，一个用户只能属于一个组，一个组可以有多个用户
    username: 用户名
    password: 密码
    user_id: 服务器帐户的id
    group_id: 堡垒机用户组id
    audit_log: 和 audit_log表建立关系
    """
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    user_id = Column(Integer, ForeignKey('host_users.id'))
    group_id = Column(Integer, ForeignKey('group.id'))

    audit_log = relationship('AuditLog', backref='user_profile')


class AuditLog(Base):
    """
    日志审计表
    userprofile_id: 堡垒机用户id
    hostuser_id: 堡垒机用户对应的服务器帐户的id
    cmd: 执行的命令
    date: 执行命令的时间
    """
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    userprofile_id = Column(Integer, ForeignKey('user_profile.id'))
    cmd = Column(String(255))
    date = Column(DateTime)

