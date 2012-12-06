#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-


##
# \file CorbaNaming.py
# \brief CORBA naming service helper class
# \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import omniORB.CORBA as CORBA
import CosNaming
import string

##
# @if jp
# @class CorbaNaming
# @brief CORBA Naming Service ���妭���妾�⎯�㎩�⎹
#
# ���墰�⎯�㎩�⎹�Ꭿ�ࡤosNaming::NamingContext �Ꭻ걎�������㎩�����㎼�⎯�㎩�⎹�Ꭷ�������
# CosNaming::NamingContext �����Ꭴ�⎪���妮�㎼�⎷�㎧�㎳�Ꭸ�Ꮋ�Ꮌ������ꦿ�Ꭾ
# �⎪���妮�㎼�⎷�㎧�㎳������������墪�Ꭸ��墭�����㎼�㎠�⎳�㎳���妾��妵�� CosNaming::Name
# �Ꭾ轎������Ꭻ���玭����Ꭻ��������𣎨���������掻�����夬���妮�㎼�⎷�㎧�㎳�����������倂
#
# �⎪���夺�⎧�⎯��墱��������倢�������Ꭿ������������墭 CORBA ��妾�㎠�⎵�㎼���墭�����
# 轎����倢���Ꭾ��妾�㎠�⎵�㎼���墰�㎫�㎼��夵�㎳��夯�⎹��墭걎����墨���墰�⎪���妮�㎼�⎷�㎧�㎳
# ���箨������倂
# 칎������곎��Ꭾ��妾���妵�⎰�⎳�㎳��夯�⎹��墰������夬���夺�⎧�⎯��墰���夦�㎳��墭�����Ꭶ���
# ���掸���Ꭾ�⎳�㎳��夯�⎹�������ت���墬��玠����墩��倢玼���莶���墭�⎳�㎳��夯�⎹�������夦�㎳��
# ����ְ���墰�⎳�㎳��夯�⎹�����⎪���夺�⎧�⎯��墰���夦�㎳����������墪��墩�������
#
# @since 0.4.0
#
# @else
# @class CorbaNaming
# @brief CORBA Naming Service helper class
#
# This class is a wrapper class of CosNaming::NamingContext.
# Almost the same operations which CosNaming::NamingContext has are
# provided, and some operation allows string naming representation of
# context and object instead of CosNaming::Name.
#
# The object of the class would connect to a CORBA naming server at
# the instantiation or immediately after instantiation.
# After that the object invokes operations to the root context of it.
# This class realizes forced binding to deep NamingContext, without binding
# intermediate NamingContexts explicitly.
#
# @since 0.4.0
#
# @endif
class CorbaNaming:
  """
  """



  ##
  # @if jp
  #
  # @brief �⎳�㎳�⎹��妫�⎯�⎿
  #
  # @param self
  # @param orb ORB
  # @param name_server ��妾�㎠�⎵�㎼���墰��鎧��(�����⎩�㎫��瀎�:None)
  #
  # @else
  #
  # @brief Consructor
  #
  # @endif
  def __init__(self, orb, name_server=None):
    self._orb = orb
    self._nameServer = ""
    self._rootContext = CosNaming.NamingContext._nil
    self._blLength = 100

    if name_server:
      self._nameServer = "corbaloc::" + name_server + "/NameService"
      try:
        obj = orb.string_to_object(self._nameServer)
        self._rootContext = obj._narrow(CosNaming.NamingContext)
        if CORBA.is_nil(self._rootContext):
          print "CorbaNaming: Failed to narrow the root naming context."

      except CORBA.ORB.InvalidName:
        print "Service required is invalid [does not exist]."

    return
  

  ##
  # @if jp
  #
  # @brief ��夻��妫�⎯�⎿
  # 
  # @param self
  # 
  # @else
  # 
  # @brief destructor
  # 
  # @endif
  def __del__(self):
    return


  ##
  # @if jp
  #
  # @brief ��妾���妵�⎰�⎵�㎼���夻�Ꭾ����ء��
  # 
  # ��玮�����墡��妾�㎠�⎵�㎼���掸�墰��妾���妵�⎰�⎵�㎼���夻������������������倂
  # 
  # @param self
  # @param name_server ��妾�㎠�⎵�㎼���墰��鎧��
  # 
  # @else
  # 
  # @endif
  def init(self, name_server):
    self._nameServer = "corbaloc::" + name_server + "/NameService"
    obj = self._orb.string_to_object(self._nameServer)
    self._rootContext = obj._narrow(CosNaming.NamingContext)
    if CORBA.is_nil(self._rootContext):
      raise MemoryError

    return


  ##
  # @if jp
  #
  # @brief Object �� bind �����
  #
  # CosNaming::bind() �Ꭸ�Ꮋ�Ꮌ��鎭�墰���������������玸���Ꭻ躼������������㎼�㎠�⎵�㎼���墰
  # �㎫�㎼��夵�㎳��夯�⎹��墭걎����墨bind()���¾�Ꮃ�玺�������餻���ʲ�Ꭺ��倂
  #
  # Name <name> �Ꭸ Object <obj> ���玽�ꎩ�� NamingContext 躴墭���夦�㎳������倂
  # c_n �� n ���������Ꭾ NameComponent ������������墪������Ꭸ���
  # name �� n ��墰 NameComponent ����������Ꭸ��倢掻��躶墰�����Ꭻ�鎱������倂
  #
  # cxt->bind(<c_1, c_2, ... c_n>, obj) �Ꭿ轎�躶墰��掽�墪��鎭�墩�������
  # cxt->resolve(<c_1, ... c_(n-1)>)->bind(<c_n>, obj)
  #
  # ���墬��墣���1������������n-1���������Ꭾ�⎳�㎳��夯�⎹����𩎣쳎����倡�-1���������Ꭾ�⎳�㎳��夯�⎹��
  # 躴墭 name <n> �Ꭸ���墨���obj �� bind ��������
  # ����𩎣쳎��Ꭻ��索����� <c_1, ... c_(n-1)> �Ꭾ NemingContext �Ꭿ���
  # bindContext() �� rebindContext() �Ꭷ�����Ꭻ���夦�㎳��莸����Ꭷ�Ꭺ������Ꮀ�Ꭺ��墬��倂
  # ���� <c_1, ... c_(n-1)> �Ꭾ NamingContext ��玭��ت���墬��玠����墭�Ꭿ���
  # NotFound ���玤��������������倂
  #
  # ���墢���倢玼���莶���夦�㎳�����㎩�⎰ force �� true �Ꭾ���墱���<c_1, ... c_(n-1)>
  # ��玭��ت���墬��玠����墭��倢��꺎����墭�⎳�㎳��夯�⎹�������夦�㎳�����Ꭺ�������
  # �������Ꭻ obj ������� name <c_n> �Ꭻ���夦�㎳������倂
  #
  # ������墰ꢎ���墩��倡�-1���������Ꭾ�⎳�㎳��夯�⎹��掸�墭 name<n> �Ꭾ�⎪���夺�⎧�⎯��
  # (Object ������墱 �⎳�㎳��夯�⎹��) �����⎤�㎳������墨�����Ꮀ
  # AlreadyBound ���玤��������������倂
  #
  # @param self
  # @param name_list �⎪���夺�⎧�⎯��墭����������墰 NameComponent
  # @param obj ������������������ Object
  # @param force true�Ꭾꢎ���倢��掸���Ꭾ�⎳�㎳��夯�⎹����꾎��莶���墭���夦�㎳������
  #              (�����⎩�㎫��瀎�:None)
  #
  # @exception NotFound ���掸���Ꭾ <c_1, c_2, ..., c_(n-1)> ��玭��ت���墬��倂
  # @exception CannotProceed ������墰���ȳ�Ꭷ�玦������鎶�墩��墬��倂
  # @exception InvalidName ���ʲ name_list �Ꭾ������掸�莭�����
  # @exception AlreadyBound name <c_n> �Ꭾ Object �����Ꭷ�Ꭻ���夦�㎳������墨�������
  #
  # @else
  #
  # @brief
  #
  # @endif
  def bind(self, name_list, obj, force=None):
    if force is None :
      force = True

    try:
      self._rootContext.bind(name_list, obj)
    except CosNaming.NamingContext.NotFound:
      if force:
        self.bindRecursive(self._rootContext, name_list, obj)
      else:
        raise
    except CosNaming.NamingContext.CannotProceed, err:
      if force:
        self.bindRecursive(err.cxt, err.rest_of_name, obj)
      else:
        raise
    except CosNaming.NamingContext.AlreadyBound:
      self._rootContext.rebind(name_list, obj)


  ##
  # @if jp
  #
  # @brief Object �� bind �����
  #
  # Object �� bind ��������墭躼�������������玭���𣎨��Ꭷ�������墪轎���墱���ind()
  # �Ꭸ�����Ꭷ�������ind(toName(string_name), obj) �Ꭸ掾�����
  #
  # @param self
  # @param string_name �⎪���夺�⎧�⎯��墭����������墰���玭���𣎨�
  # @param obj ������������������夬���夺�⎧�⎯��
  # @param force true�Ꭾꢎ���倢��掸���Ꭾ�⎳�㎳��夯�⎹����꾎��莶���墭���夦�㎳������
  #              (�����⎩�㎫��瀎�:true)
  #
  # @exception NotFound ���掸���Ꭾ <c_1, c_2, ..., c_(n-1)> ��玭��ت���墬��倂
  # @exception CannotProceed ������墰���ȳ�Ꭷ�玦������鎶�墩��墬��倂
  # @exception InvalidName ���ʲ string_name �Ꭾ������掸�莭�����
  # @exception AlreadyBound name <n> �Ꭾ Object �����Ꭷ�Ꭻ���夦�㎳������墨�������
  #
  # @else
  #
  # @brief
  #
  # @endif
  def bindByString(self, string_name, obj, force=True):
    self.bind(self.toName(string_name), obj, force)


  ##
  # @if jp
  #
  # @brief ���掸���Ꭾ�⎳�㎳��夯�⎹���� bind ���墬���� Object �� bind �����
  #
  # context �Ꭷ躼�������� NamingContext �Ꭻ걎����墨���ame �Ꭷ��玮�����墡
  # ��妾�㎠�⎳�㎳���妾��妵�� <c_1, ... c_(n-1)> �� NamingContext �Ꭸ���墨
  # 𩎣쳎����墬���������� <c_n> �Ꭻ걎����墨 obj �� bind ��������
  # �������<c_1, ... c_(n-1)> �Ꭻ걎�������� NamingContext ��墬��玠����墭�Ꭿ
  # �������墬 NamingContext ������⎤�㎳������倂
  #
  # �������Ꭻ <c_1, c_2, ..., c_(n-1)> �Ꭻ걎�������� NamingContext ���ȡ��
  # �Ꮎ���墱𩎣쳎���������掸�墩�ࡤosNaming::bind(<c_n>, object) ���¾�Ꮃ�玺�������倂
  # ���墰�Ꭸ��倢���Ꭷ�Ꭻ���夦�㎳��夥�㎳�⎰��玭��ت������Ꮀ AlreadyBound���玤��������������倂
  #
  # ���掸���Ꭾ�⎳�㎳��夯�⎹����𩎣쳎��������鎨�墩��ꎧ��쳎��������墪������⎳�㎳��夯�⎹��墪
  # ���������Ꭾ NamingContext �Ꭷ�Ꭿ�Ꭺ�� Binding ��玭��ت�����ꢎ���倁
  # CannotProceed ���玤�������������玦����躎�쯎���������
  #
  # @param self
  # @param context bind ������ꩶ����倀NamingContext
  # @param name_list �⎪���夺�⎧�⎯��墭����������墰��妾�㎠�⎳�㎳���妾��妵��
  # @param obj ������������������夬���夺�⎧�⎯��
  #
  # @exception CannotProceed <c_1, ..., c_(n-1)> �Ꭻ걎�������� NamingContext 
  #            �Ꭾ��墣�Ꮂ�Ꭸ�Ꭴ��倢���Ꭷ�Ꭻ NamingContext 轎���墰 object �Ꭻ���夦�㎳��
  #            ������Ꭶ������箨������鎶�墩��墬��倂
  # @exception InvalidName ���� name_list ��掸�莭��
  # @exception AlreadyBound name <c_n> �Ꭻ���墩�Ꭻ������墰 object �����⎤�㎳��
  #            ������Ꭶ�������
  # @else
  #
  # @brief
  #
  # @endif
  def bindRecursive(self, context, name_list, obj):
    length = len(name_list)
    cxt = context
    for i in range(length):
      if i == length -1:
        try:
          cxt.bind(self.subName(name_list, i, i), obj)
        except CosNaming.NamingContext.AlreadyBound:
          cxt.rebind(self.subName(name_list, i, i), obj)
        return
      else:
        if self.objIsNamingContext(cxt):
          cxt = self.bindOrResolveContext(cxt,self.subName(name_list, i, i))
        else:
          raise CosNaming.NamingContext.CannotProceed(cxt, self.subName(name_list, i))
    return


  ##
  # @if jp
  #
  # @brief Object �� rebind �����
  #
  # name_list �Ꭷ��玮�����墡 Binding �����Ꭷ�Ꭻ���ت�����ꢎ�����������墨 bind() �Ꭸ����
  # �Ꭷ���������⎤�㎳��夥�㎳�⎰�����Ꭷ�Ꭻ���ت�����ꢎ���墭�Ꭿ���̲��������夦�㎳��夥�㎳�⎰�Ꭻ
  # ����������������
  #
  # @param self
  # @param name_list �⎪���夺�⎧�⎯��墭����������墰 NameComponent
  # @param obj ������������������夬���夺�⎧�⎯��
  # @param force true�Ꭾꢎ���倢��掸���Ꭾ�⎳�㎳��夯�⎹����꾎��莶���墭���夦�㎳������
  #              (�����⎩�㎫��瀎�:true)
  #
  # @exception NotFound ���掸���Ꭾ <c_1, c_2, ..., c_(n-1)> ��玭��ت���墬��倂
  # @exception CannotProceed ������墰���ȳ�Ꭷ�玦������鎶�墩��墬��倂
  # @exception InvalidName ���� name_list ��掸�莭��
  #
  # @else
  #
  # @brief
  #
  # @endif
  def rebind(self, name_list, obj, force=True):
    if force is None:
      force = True
      
    try:
      self._rootContext.rebind(name_list, obj)

    except CosNaming.NamingContext.NotFound:
      if force:
        self.rebindRecursive(self._rootContext, name_list, obj)
      else:
        raise

    except CosNaming.NamingContext.CannotProceed, err:
      if force:
        self.rebindRecursive(err.cxt, err,rest_of_name, obj)
      else:
        raise
      
    return


  ##
  # @if jp
  #
  # @brief Object �� rebind �����
  #
  # Object �� rebind ��������墭躼�������������玭���𣎨��Ꭷ�������墪轎���墱 rebind()
  # �Ꭸ�����Ꭷ�������ebind(toName(string_name), obj) �Ꭸ掾�����
  #
  # @param self
  # @param string_name �⎪���夺�⎧�⎯��墭����������墰���玭���𣎨�
  # @param obj ������������������夬���夺�⎧�⎯��
  # @param force true�Ꭾꢎ���倢��掸���Ꭾ�⎳�㎳��夯�⎹����꾎��莶���墭���夦�㎳������
  #              (�����⎩�㎫��瀎�:true)
  #
  # @exception NotFound ���掸���Ꭾ <c_1, c_2, ..., c_(n-1)> ��玭��ت���墬��倂
  # @exception CannotProceed ������墰���ȳ�Ꭷ�玦������鎶�墩��墬��倂
  # @exception InvalidName ���ʲ string_name �Ꭾ������掸�莭�����
  #
  # @else
  #
  # @brief
  #
  # @endif
  def rebindByString(self, string_name, obj, force=True):
    self.rebind(self.toName(string_name), obj, force)

    return


  ##
  # @if jp
  #
  # @brief ���掸���Ꭾ�⎳�㎳��夯�⎹���� bind ���墬���� Object �� rebind �����
  #
  # name_list <c_n> �Ꭷ��玮�����墡 NamingContext ������墱 Object �����Ꭷ�Ꭻ���ت�����
  # ꢎ�����������墨 bindRecursive() �Ꭸ�����Ꭷ�������
  #
  # name_list <c_n> �Ꭷ��玮�����墡���夦�㎳��夥�㎳�⎰�����Ꭷ�Ꭻ���ت�����ꢎ���墭�Ꭿ���
  # ������������夦�㎳��夥�㎳�⎰�Ꭻ����������������
  #
  # @param self
  # @param context bind ������ꩶ����倀NamingContext
  # @param name_list �⎪���夺�⎧�⎯��墭����������墰 NameComponent
  # @param obj ������������������夬���夺�⎧�⎯��
  #
  # @exception CannotProceed ���掸���Ꭾ�⎳�㎳��夯�⎹����𩎣쳎��Ꭷ��墬��倂
  # @exception InvalidName 躼�������� name_list ��掸�莭�����
  #
  # @else
  #
  # @brief
  #
  # @endif
  def rebindRecursive(self, context, name_list, obj):
    length = len(name_list)
    for i in range(length):
      if i == length - 1:
        context.rebind(self.subName(name_list, i, i), obj)
        return
      else:
        if self.objIsNamingContext(context):
          try:
            context = context.bind_new_context(self.subName(name_list, i, i))
          except CosNaming.NamingContext.AlreadyBound:
            obj_ = context.resolve(self.subName(name_list, i, i))
            context = obj_._narrow(CosNaming.NamingContext)
        else:
          raise CosNaming.NamingContext.CannotProceed(context, self.subName(name_list, i))
    return


  ##
  # @if jp
  #
  # @brief NamingContext �� bind �����
  #
  # bind 걎�𳎡�Ꭸ���墨��玮�����墡���ʲ name ����������Ꭾꢎ���墱 bindByString() �Ꭸ���
  # �����轎���墰ꢎ���墱 bind() �Ꭸ�����Ꭷ�������
  #
  # @param self
  # @param name �⎪���夺�⎧�⎯��墭����������
  # @param name_cxt ������������������ NamingContext
  # @param force true�Ꭾꢎ���倢��掸���Ꭾ�⎳�㎳��夯�⎹����꾎��莶���墭���夦�㎳������
  #              (�����⎩�㎫��瀎�:True)
  #
  # @exception NotFound ���掸���Ꭾ <c_1, c_2, ..., c_(n-1)> ��玭��ت���墬��倂
  # @exception CannotProceed ������墰���ȳ�Ꭷ�玦������鎶�墩��墬��倂
  # @exception InvalidName ���ʲ name �Ꭾ������掸�莭�����
  # @exception AlreadyBound name <c_n> �Ꭾ Object �����Ꭷ�Ꭻ���夦�㎳������墨�������
  #
  # @else
  #
  # @brief
  #
  # @endif
  def bindContext(self, name, name_cxt, force=True):
    if isinstance(name, basestring):
      self.bind(self.toName(name), name_cxt, force)
    else:
      self.bind(name, name_cxt, force)
    return


  ##
  # @if jp
  #
  # @brief NamingContext �� bind �����
  #
  # bind �������夬���夺�⎧�⎯���� NamingContext �Ꭷ�������墪����Ҧ��墨
  # bindRecursive() �Ꭸ�����Ꭷ�������
  #
  # @param self
  # @param context bind ������ꩶ����倀NamingContext
  # @param name_list �⎪���夺�⎧�⎯��墭����������墰��妾�㎠�⎳�㎳���妾��妵��
  # @param name_cxt ������������������ NamingContext
  #
  # @else
  #
  # @brief
  #
  # @endif
  def bindContextRecursive(self, context, name_list, name_cxt):
    self.bindRecursive(context, name_list, name_cxt)
    return


  ##
  # @if jp
  #
  # @brief NamingContext �� rebind �����
  #
  # bind 걎�𳎡�Ꭸ���墨��玮�����墡���ʲ name ����������Ꭾꢎ���墱 rebindByString() �Ꭸ���
  # �����轎���墰ꢎ���墱 rebind() �Ꭸ�����Ꭷ�������
  # �Ꭹ�Ꭱ��墰ꢎ��������夦�㎳��夥�㎳�⎰�����Ꭷ�Ꭻ���ت�����ꢎ���墭�Ꭿ���
  # ������������夦�㎳��夥�㎳�⎰�Ꭻ����������������
  #
  # @param self
  # @param name �⎪���夺�⎧�⎯��墭����������墰��妾�㎠�⎳�㎳���妾��妵��
  # @param name_cxt ������������������ NamingContext
  # @param force true�Ꭾꢎ���倢��掸���Ꭾ�⎳�㎳��夯�⎹����꾎��莶���墭���夦�㎳������
  #              (�����⎩�㎫��瀎�:true)
  #
  # @exception NotFound ���掸���Ꭾ <c_1, c_2, ..., c_(n-1)> ��玭��ت���墬��倂
  # @exception CannotProceed ������墰���ȳ�Ꭷ�玦������鎶�墩��墬��倂
  # @exception InvalidName ���ʲ name �Ꭾ������掸�莭�����
  #
  # @else
  #
  # @endif
  def rebindContext(self, name, name_cxt, force=True):
    if isinstance(name, basestring):
      self.rebind(self.toName(name), name_cxt, force)
    else:
      self.rebind(name, name_cxt, force)
    return


  ##
  # @if jp
  #
  # @brief ���掸���Ꭾ�⎳�㎳��夯�⎹������玸�����墭 rebind �� NamingContext �� rebind �����    #
  # bind �������夬���夺�⎧�⎯���� NamingContext �Ꭷ�������墪����Ҧ��墨
  # rebindRecursive() �Ꭸ�����Ꭷ�������
  #
  # @param self
  # @param context bind ������ꩶ����倀NamingContext
  # @param name_list �⎪���夺�⎧�⎯��墭����������墰 NameComponent
  # @param name_cxt ������������������ NamingContext
  #
  # @else
  #
  # @brief
  #
  # @endif
  def rebindContextRecursive(self, context, name_list, name_cxt):
    self.rebindRecursive(context, name_list, name_cxt)
    return


  ##
  # @if jp
  #
  # @brief Object �� name ����𩎣쳎������
  #
  # name �Ꭻ bind ������Ꭶ�����⎪���夺�⎧�⎯�����厧���ꎿ������
  # ��妾�㎠�⎳�㎳���妾��妵�� <c_1, c_2, ... c_n> �Ꭿ��玸�����墭𩎣쳎��������倂
  # 
  # ���ʲ name �Ꭻ躼���������瀎�����������Ꭾꢎ���墭�Ꭿ�Ꮎ���������墭 toName() �Ꭻ��墥�Ꭶ
  # NameComponent �Ꭻꦲ���������倂
  # 
  # CosNaming::resolve() �Ꭸ�Ꮋ�Ꮌ��鎭�墰���������������玸���Ꭻ躼��������
  # ��妾�㎠�⎵�㎼���墰�㎫�㎼��夵�㎳��夯�⎹��墭걎����墨 resolve() ���¾�Ꮃ�玺�������餻��
  # �����Ꭺ��倂
  #
  # @param self
  # @param name 𩎣쳎����墻��夬���夺�⎧�⎯��墰�����Ꭾ��妾�㎠�⎳�㎳���妾��妵��
  #
  # @return 𩎣쳎���������夬���夺�⎧�⎯�����厧
  #
  # @exception NotFound ���掸���Ꭾ <c_1, c_2, ..., c_(n-1)> ��玭��ت���墬��倂
  # @exception CannotProceed ������墰���ȳ�Ꭷ�玦������鎶�墩��墬��倂
  # @exception InvalidName ���ʲ name �Ꭾ������掸�莭�����
  #
  # @else
  #
  # @endif
  def resolve(self, name):
    if isinstance(name, basestring):
      name_ = self.toName(name)
    else:
      name_ = name
      
    try:
      obj = self._rootContext.resolve(name_)
      return obj
    except CosNaming.NamingContext.NotFound, ex:
      return None


  ##
  # @if jp
  #
  # @brief ��玮�����墡�����Ꭾ�⎪���夺�⎧�⎯��墰 bind ���ꎧ�����������
  #
  # name �Ꭻ bind ������Ꭶ�����⎪���夺�⎧�⎯�����厧���ꎧ��������������
  # ��妾�㎠�⎳�㎳���妾��妵�� <c_1, c_2, ... c_n> �Ꭿ��玸�����墭𩎣쳎��������倂
  # 
  # ���ʲ name �Ꭻ躼���������瀎�����������Ꭾꢎ���墭�Ꭿ�Ꮎ���������墭 toName() �Ꭻ��墥�Ꭶ
  # NameComponent �Ꭻꦲ���������倂
  # 
  # CosNaming::unbind() �Ꭸ�Ꮋ�Ꮌ��鎭�墰���������������玸���Ꭻ躼��������
  # ��妾�㎠�⎵�㎼���墰�㎫�㎼��夵�㎳��夯�⎹��墭걎����墨 unbind() ���¾�Ꮃ�玺�������餻��
  # �����Ꭺ��倂
  #
  # @param self
  # @param name ���Ҧ������⎪���夺�⎧�⎯��墰��妾�㎠�⎳�㎳���妾��妵��
  #
  # @exception NotFound ���掸���Ꭾ <c_1, c_2, ..., c_(n-1)> ��玭��ت���墬��倂
  # @exception CannotProceed ������墰���ȳ�Ꭷ�玦������鎶�墩��墬��倂
  # @exception InvalidName ���ʲ name �Ꭾ������掸�莭�����
  #
  # @else
  #
  # @endif
  # void unbind(const CosNaming::Name& name)
  #   throw(NotFound, CannotProceed, InvalidName);
  def unbind(self, name):
    if isinstance(name, basestring):
      name_ = self.toName(name)
    else:
      name_ = name

    self._rootContext.unbind(name_)
    return


  ##
  # @if jp
  #
  # @brief ����������⎳�㎳��夯�⎹��������������
  #
  # 躼������������㎼�㎠�⎵�㎼���掸�墩������������ NamingContext ���ꎿ������
  # �������墡 NamingContext �Ꭿ bind ������Ꭶ��墬��倂
  # 
  # @param self
  # 
  # @return ��������������̲����� NamingContext
  #
  # @else
  #
  # @endif
  def newContext(self):
    return self._rootContext.new_context()


  ##
  # @if jp
  #
  # @brief ����������⎳�㎳��夯�⎹���� bind �����
  #
  # 躼�������� name �Ꭻ걎����墨����������⎳�㎳��夯�⎹�������夦�㎳������倂
  # �������������倀NamingContext �Ꭿ��妾�㎠�⎵�㎼���掸�墩����������������Ꭾ�Ꭷ�������
  # 
  # ���ʲ name �Ꭻ躼���������瀎�����������Ꭾꢎ���墭�Ꭿ�Ꮎ���������墭 toName() �Ꭻ��墥�Ꭶ
  # NameComponent �Ꭻꦲ���������倂
  # 
  # @param self
  # @param name NamingContext�Ꭻ����������墰��妾�㎠�⎳�㎳���妾��妵��
  # @param force true�Ꭾꢎ���倢��掸���Ꭾ�⎳�㎳��夯�⎹����꾎��莶���墭���夦�㎳������
  #              (�����⎩�㎫��瀎�:true)
  #
  # @return ��������������̲����� NamingContext
  #
  # @exception NotFound ���掸���Ꭾ <c_1, c_2, ..., c_(n-1)> ��玭��ت���墬��倂
  # @exception CannotProceed ������墰���ȳ�Ꭷ�玦������鎶�墩��墬��倂
  # @exception InvalidName ���ʲ name �Ꭾ������掸�莭�����
  # @exception AlreadyBound name <n> �Ꭾ Object �����Ꭷ�Ꭻ���夦�㎳������墨�������
  #
  # @else
  #
  # @endif
  def bindNewContext(self, name, force=True):
    if force is None:
      force = True
      
    if isinstance(name, basestring):
      name_ = self.toName(name)
    else:
      name_ = name

    try:
      return self._rootContext.bind_new_context(name_)
    except CosNaming.NamingContext.NotFound:
      if force:
        self.bindRecursive(self._rootContext, name_, self.newContext())
      else:
        raise
    except CosNaming.NamingContext.CannotProceed, err:
      if force:
        self.bindRecursive(err.cxt, err.rest_of_name, self.newContext())
      else:
        raise
    return None


  ##
  # @if jp
  #
  # @brief NamingContext �������⎢�⎯��夥����������
  #
  # context �Ꭷ��玮�����墡 NamingContext �������⎢�⎯��夥�������������
  # context �Ꭻ��墰�⎳�㎳��夯�⎹�������夦�㎳������墨����ꢎ���墱 NotEmpty ���玤���
  # �����������倂
  # 
  # @param self
  # @param context ���夤�⎯��夥���������� NamingContext
  #
  # @exception NotEmpty 걎�𳎡context �Ꭻ��墰�⎳�㎳��夯�⎹�������夦�㎳������墨�������
  #
  # @else
  #
  # @else
  #
  # @brief Destroy the naming context
  #
  # Delete the specified naming context.
  # any bindings should be <unbind> in which the given context is bound to
  # some names before invoking <destroy> operation on it. 
  #
  # @param context NamingContext which is destroied.
  #     
  # @exception NotEmpty 
  #
  # @else
  #
  # @endif
  def destroy(self, context):
    context.destroy()


  ##
  # @if jp
  # @brief NamingContext �����꺎����墭躶墥�Ꭶ���夤�⎯��夥����������
  #
  # context �Ꭷ躼�������� NamingContext �Ꭻ걎����墨���ame �Ꭷ��玮�����墡
  # ��妾�㎠�⎳�㎳���妾��妵�� <c_1, ... c_(n-1)> �� NamingContext �Ꭸ���墨
  # 𩎣쳎����墬���������� <c_n> �Ꭻ걎����墨 ���夤�⎯��夥��������ꎡ������
  #
  # @param self
  # @param context ���夤�⎯��夥���������� NamingContext
  #
  # @exception NotEmpty 걎�𳎡context �Ꭻ��墰�⎳�㎳��夯�⎹�������夦�㎳������墨�������
  # @exception NotFound ���掸���Ꭾ <c_1, c_2, ..., c_(n-1)> ��玭��ت���墬��倂
  # @exception CannotProceed ������墰���ȳ�Ꭷ�玦������鎶�墩��墬��倂
  # @exception InvalidName ���ʲ name �Ꭾ������掸�莭�����
  #
  # @else
  # @brief Destroy the naming context recursively
  # @endif
  def destroyRecursive(self, context):
    cont = True
    bl = []
    bi = 0
    bl, bi = context.list(self._blLength)
    while cont:
      for i in range(len(bl)):
        if bl[i].binding_type == CosNaming.ncontext:
          obj = context.resolve(bl[i].binding_name)
          next_context = obj._narrow(CosNaming.NamingContext)

          self.destroyRecursive(next_context)
          context.unbind(bl[i].binding_name)
          next_context.destroy()
        elif bl[i].binding_type == CosNaming.nobject:
          context.unbind(bl[i].binding_name)
        else:
          assert(0)
      if CORBA.is_nil(bi):
        cont = False
      else:
        bi.next_n(self._blLength, bl)

    if not (CORBA.is_nil(bi)):
      bi.destroy()
    return


  ##
  # @if jp
  # @brief ���墻�Ꭶ�Ꭾ Binding ��������������
  #
  # �����쎲������Ꭶ�����厨�Ꭶ�ᎮBinding �����������������
  #
  # @param self
  #
  # @else
  # @brief Destroy all binding
  # @endif
  def clearAll(self):
    self.destroyRecursive(self._rootContext)
    return


  ##
  # @if jp
  # @brief 躼�������� NamingContext �Ꭾ Binding ������������
  #
  # ��玮�����墡 NamingContext �Ꭾ Binding ������������倂
  #
  # @param self
  # @param name_cxt Binding ���玾�环��𳎡 NamingContext
  # @param how_many Binding ���������������곎��Ꭾ칎���
  # @param rbl ���玾����� Binding ���掿�����������妭��
  # @param rbi ���玾����� Binding ���墡�Ꭹ��墡��墰�⎤��妮�㎼�⎿
  #
  # @else
  # @endif
  def list(self, name_cxt, how_many, rbl, rbi):
    bl, bi = name_cxt.list(how_many)

    for i in bl:
      rbl.append(bl)

    rbi.append(bi)
  

  #============================================================
  # interface of NamingContext
  #============================================================

  ##
  # @if jp
  # @brief 躼�������� NameComponent �Ꭾ���玭���𣎨����ꎿ���
  #
  # ��玮�����墡 NameComponent ��������墭ꦲ����������
  #
  # @param self
  # @param name_list ꦲ��걎�𳎡 NameComponent
  #
  # @return ���玭���ꦲ�������
  #
  # @exception InvalidName ���ʲ name_list �Ꭾ������掸�莭�����
  #
  # @else
  # @brief Get string representation of given NameComponent
  # @endif
  def toString(self, name_list):
    if len(name_list) == 0:
      raise CosNaming.NamingContext.InvalidName

    slen = self.getNameLength(name_list)
    string_name = [""]
    self.nameToString(name_list, string_name, slen)

    return string_name


  ##
  # @if jp
  # @brief 躼����������������𣎨��� NameComponent �Ꭻ��ꎧ�������
  #
  # ��玮�����墡���玭����� NameComponent �Ꭻꦲ����������
  #
  # @param self
  # @param sname ꦲ��걎�𳎡���玭���
  #
  # @return NameComponent ꦲ�������
  #
  # @exception InvalidName ���ʲ sname ��掸�莭�����
  #
  # @else
  # @brief Get NameComponent from gien string name representation
  # @endif
  def toName(self, sname):
    if not sname:
      raise CosNaming.NamingContext.InvalidName

    string_name = sname
    name_comps = []

    nc_length = 0
    nc_length = self.split(string_name, "/", name_comps)
    if not (nc_length > 0):
      raise CosNaming.NamingContext.InvalidName

    name_list = [CosNaming.NameComponent("","") for i in range(nc_length)]

    for i in range(nc_length):
      pos = string.rfind(name_comps[i][0:],".")
      if pos == -1:
        name_list[i].id   = name_comps[i]
        name_list[i].kind = ""
      else:
        name_list[i].id   = name_comps[i][0:pos]
        name_list[i].kind = name_comps[i][(pos+1):]

    return name_list


  ##
  # @if jp
  # @brief 躼�������� addr �Ꭸ string_name ���� URL𣎨�������������
  #
  # ��玮�����墡�⎢��妮�⎹�Ꭸ��鎧����öRL�Ꭻꦲ����������
  #
  # @param self
  # @param addr ꦲ��걎�𳎡�⎢��妮�⎹
  # @param string_name ꦲ��걎�𳎡��鎧��
  #
  # @return URL ꦲ�������
  #
  # @exception InvalidAddress ���ʲ addr ��掸�莭�����
  # @exception InvalidName ���ʲ string_name ��掸�莭�����
  #
  # @else
  # @brief Get URL representation from given addr and string_name
  # @endif
  def toUrl(self, addr, string_name):
    return self._rootContext.to_url(addr, string_name)


  ##
  # @if jp
  # @brief 躼����������������𣎨��� resolve ���夬���夺�⎧�⎯���������
  #
  # ��玮�����墡���玭���𣎨�����esolve���񎼸夬���夺�⎧�⎯�������玾�����倂
  #
  # @param self
  # @param string_name ���玾�环��𳎡�⎪���夺�⎧�⎯���������𣎨�
  #
  # @return 𩎣쳎���������夬���夺�⎧�⎯��
  #
  # @exception NotFound ���掸���Ꭾ <c_1, c_2, ..., c_(n-1)> ��玭��ت���墬��倂
  # @exception CannotProceed ������墰���ȳ�Ꭷ�玦������鎶�墩��墬��倂
  # @exception InvalidName ���ʲ name �Ꭾ������掸�莭�����
  # @exception AlreadyBound name <n> �Ꭾ Object �����Ꭷ�Ꭻ���夦�㎳������墨�������
  #
  # @else
  # @brief Resolve from name of string representation and get object 
  # @endif
  def resolveStr(self, string_name):
    return self.resolve(self.toName(string_name))


  #============================================================
  # Find functions
  #============================================================

  ##
  # @if jp
  #
  # @brief �⎪���夺�⎧�⎯��墰����������⎤�㎳�������墱𩎣쳎������
  #
  # ��玮�����墡�⎳�㎳��夯�⎹��墭걎����墨�⎪���夺�⎧�⎯���� NameComponent �Ꭷ��玮�����墡
  # 迺鎽���Ꭻ���夦�㎳������倂
  # ��掸����Ꭻ�����Ꭻ��墰�鎴�������⎤�㎳��莸����Ꭾꢎ���墱���Τ��墰���夦�㎳��莸����鎴����
  # ���玾�����倂
  #
  # @param self
  # @param context bind ������墱 resole 걎�𳎡�⎳�㎳��夯�⎹��
  # @param name_list �⎪���夺�⎧�⎯��墭����������墰 NameComponent
  # @param obj ������������������ Object
  #
  # @return NameComponent �Ꭷ��玮�����墡迺鎽���Ꭻ���夦�㎳������墨�����⎪���夺�⎧�⎯��
  #
  # @else
  # @brief Bind of resolve the given name component
  # @endif
  def bindOrResolve(self, context, name_list, obj):
    try:
      context.bind_context(name_list, obj)
      return obj
    except CosNaming.NamingContext.AlreadyBound:
      obj = context.resolve(name_list)
      return obj
    return CORBA.Object._nil


  ##
  # @if jp
  #
  # @brief �⎳�㎳��夯�⎹��墰����������⎤�㎳�������墱𩎣쳎������
  #
  # ��玮�����墡�⎳�㎳��夯�⎹��墭걎����墨 Context�� NameComponent �Ꭷ��玮�����墡迺鎽���Ꭻ
  # ���夦�㎳������倂
  # Context ��鎩���Ꭾꢎ���墱�����夵�㎳��夯�⎹������������墨���夦�㎳������倂
  # ��掸����Ꭻ�����Ꭻ��墰�鎴�������⎤�㎳��莸����Ꭾꢎ���墱���Τ��墰���夦�㎳��莸����鎴����
  # ���玾�����倂
  #
  # @param self
  # @param context bind ������墱 resole 걎�𳎡�⎳�㎳��夯�⎹��
  # @param name_list �⎳�㎳��夯�⎹��墭����������墰 NameComponent
  # @param new_context ������������������ Context(�����⎩�㎫��瀎�:None)
  #
  # @return NameComponent �Ꭷ��玮�����墡迺鎽���Ꭻ���夦�㎳������墨����Context
  #
  # @else
  # @brief Bind of resolve the given name component
  # @endif
  def bindOrResolveContext(self, context, name_list, new_context=None):
    if new_context is None:
      new_cxt = self.newContext()
    else:
      new_cxt = new_context

    obj = self.bindOrResolve(context, name_list, new_cxt)
    return obj._narrow(CosNaming.NamingContext)


  ##
  # @if jp
  # @brief ��妾�㎠�⎵�㎼���墰����������������
  #
  # 𪎭����������㎼�㎠�⎵�㎼���墰����������������倂
  #
  # @param self
  #
  # @return ��妾�㎠�⎵�㎼���墰����
  #
  # @else
  # @brief Get the name of naming server
  # @endif
  def getNameServer(self):
    return self._nameServer


  ##
  # @if jp
  # @brief �㎫�㎼��夵�㎳��夯�⎹�������玾�����
  #
  # 𪎭����������㎼�㎠�⎵�㎼���墰�㎫�㎼��夵�㎳��夯�⎹�������玾�����倂
  #
  # @param self
  #
  # @return ��妾�㎠�⎵�㎼���墰�㎫�㎼��夵�㎳��夯�⎹��
  #
  # @else
  # @brief Get the root context
  # @endif
  def getRootContext(self):
    return self._rootContext


  ##
  # @if jp
  # @brief �⎪���夺�⎧�⎯������妾���妵�⎰�⎳�㎳��夯�⎹�����莤�莥�����
  #
  # ��玮������ꎦ�鎴�������㎼���妵�⎰�⎳�㎳��夯�⎹�����莤�莥�����
  #
  # @param self
  # @param obj �莤�莥걎�𳎡�鎴��
  #
  # @return �莤�莥�����(��妾���妵�⎰�⎳�㎳��夯�⎹��:true������掻��ꦖ:false)
  #
  # @else
  # @brief Whether the object is NamingContext
  # @endif
  def objIsNamingContext(self, obj):
    nc = obj._narrow(CosNaming.NamingContext)
    if CORBA.is_nil(nc):
      return False
    else:
      return True


  ##
  # @if jp
  # @brief 躼�����������������妾���妵�⎰�⎳�㎳��夯�⎹�����Ꭹ�����莤�莥�����
  #
  # NameComponent ������墱���玭����Ꭷ��玮������ꎦ�鎴�������㎼���妵�⎰�⎳�㎳��夯�⎹����
  # �莤�莥�����
  #
  # @param self
  # @param name_list �莤�莥걎�𳎡
  #
  # @return �莤�莥�����(��妾���妵�⎰�⎳�㎳��夯�⎹��:true������掻��ꦖ:false)
  #
  # @else
  # @brief Whether the given name component is NamingContext
  # @endif
  def nameIsNamingContext(self, name_list):
    return self.objIsNamingContext(self.resolve(name_list))


  ##
  # @if jp
  # @brief ��妾�㎠�⎳�㎳���妾��妵��墰�㎨���������
  #
  # ��玮�����墡�ִ�Ꭾ��妾�㎠�⎳�㎳���妾��妵�������玾�����倂
  # 掺�掽�鎽������������墨��墬��玠����墱��������墰�鎴������Ҧ��墡��妾�㎠�⎳�㎳���妾��妵��
  # ���ꎿ������
  #
  # @param self
  # @param name_list ��鎴��걎�𳎡NameComponent
  # @param begin ���玾�鎯��ִ���玧�掽�鎽��
  # @param end ���玾�鎯��ִ掺�掽�鎽��(�����⎩�㎫��瀎�:None)
  #
  # @return NameComponent ���玾�鎵����
  #
  # @else
  # @brief Get subset of given name component
  # @endif
  def subName(self, name_list, begin, end = None):
    if end is None or end < 0:
      end = len(name_list) - 1

    sub_len = end - (begin -1)
    objId = ""
    kind  = ""
    
    sub_name = []
    for i in range(sub_len):
      sub_name.append(name_list[begin + i])

    return sub_name


  ##
  # @if jp
  # @brief ��妾�㎠�⎳�㎳���妾��妵��墰���玭���𣎨�������������
  #
  # ��玮������鎯��ִ�Ꭾ��妾�㎠�⎳�㎳���妾��妵��墰���玭���𣎨�������������倂
  # ���玭���𣎨��Ꭿ�࡯ameComponent�Ꭾ쩶�����Nc[0],Nc[1],Nc[2]������������}�Ꭾꢎ���倁
  #   Nc[0]id.Nc[0].kind/Nc[1]id.Nc[1].kind/Nc[2].id/Nc[2].kind������������
  # �Ꭸ����꿎�꾾墩���玾�墩�������
  # ���玾��������������Ꭾ�����������玮�������ʹ���掻��躴墰ꢎ���墱���
  # ��玮�������ʹ���墩�����펨�Ꭶ������倂
  #
  # @param self
  # @param name_list ���玾�环��𳎡NameComponent
  # @param string_name ���玾�鎵�������玭���
  # @param slen ���玾�环��𳎡���玭������ꦎ�����
  #
  # @else
  # @brief Get string representation of name component
  # @endif
  def nameToString(self, name_list, string_name, slen):
    for i in range(len(name_list)):
      for id_ in name_list[i].id:
        if id_ == "/" or id_ == "." or id_ == "\\":
          string_name[0] += "\\"
        string_name[0] += id_

      if name_list[i].id == "" or name_list[i].kind != "":
        string_name[0] += "."

      for kind_ in name_list[i].kind:
        if kind_ == "/" or kind_ == "." or kind_ == "\\":
          string_name[0] += "\\"
        string_name[0] += kind_

      string_name[0] += "/"


  ##
  # @if jp
  # @brief ��妾�㎠�⎳�㎳���妾��妵��墰���玭���𣎨����墰���玭��ʹ������������
  #
  # ��玮���������㎼�㎠�⎳�㎳���妾��妵�������玭����Ꭷ𣎨����墡ꢎ���墰������������玾�����倂
  # ���玭���𣎨��Ꭿ�࡯ameComponent�Ꭾ쩶�����Nc[0],Nc[1],Nc[2]�㎻�㎻�㎻}�Ꭾꢎ���倁
  #   Nc[0]id.Nc[0].kind/Nc[1]id.Nc[1].kind/Nc[2].id/Nc[2].kind�㎻�㎻�㎻
  # �Ꭸ����꿎�꾾墩���玾�墩�������
  #
  # @param self
  # @param name_list ���玾�环��𳎡NameComponent
  #
  # @return ��玮���������㎼�㎠�⎳�㎳���妾��妵��墰���玭���������
  #
  # @else
  # @brief Get string length of the name component's string representation
  # @endif
  def getNameLength(self, name_list):
    slen = 0

    for i in range(len(name_list)):
      for id_ in name_list[i].id:
        if id_ == "/" or id_ == "." or id_ == "\\":
          slen += 1
        slen += 1
      if name_list[i].id == "" or name_list[i].kind == "":
        slen += 1

      for kind_ in name_list[i].kind:
        if kind_ == "/" or kind_ == "." or kind_ == "\\":
          slen += 1
        slen += 1

      slen += 1

    return slen


  ##
  # @if jp
  # @brief ���玭����Ꭾ��粴
  #
  # ���玭������������������㎪������Ꭷ��粴��������
  #
  # @param self
  # @param input ��粴걎�𳎡���玭���
  # @param delimiter ��粴����妬�����
  # @param results ��粴�����
  #
  # @return ��粴���墡���玭����Ꭾ�鎴������
  #
  # @else
  # @brief Split of string
  # @endif
  def split(self, input, delimiter, results):
    delim_size = len(delimiter)
    found_pos = begin_pos = pre_pos = substr_size = 0

    if input[0:delim_size] == delimiter:
      begin_pos = pre_pos = delim_size

    while 1:
      found_pos = string.find(input[begin_pos:],delimiter)
      
      if found_pos == -1:
        results.append(input[pre_pos:])
        break

      if found_pos > 0 and input[found_pos - 1] == "\\":
        begin_pos += found_pos + delim_size
      else:
        substr_size = found_pos + (begin_pos - pre_pos)
        if substr_size > 0:
          results.append(input[pre_pos:(pre_pos+substr_size)])
        begin_pos += found_pos + delim_size
        pre_pos   = begin_pos

    return len(results)
