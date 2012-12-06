#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ObjectManager.py
# @brief Object management class
# @date $Date: $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2003-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import sys
import string
import threading

import OpenRTM_aist



##
# @if jp
#
# @brief ���֥������ȴ����ѥ��饹
#
# �Ƽ索�֥������Ȥ�������뤿��Υ��饹��
#
# @since 0.4.0
#
# @else
#
# @endif
class ObjectManager:
  """
  """

  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  # 
  # ���󥹥ȥ饯��
  # 
  # @param self
  # @param predicate ���֥������ȸ����ѥե��󥯥�
  # 
  # @else
  #
  # @endif
  def __init__(self, predicate):
    self._objects = self.Objects()
    self._predicate = predicate



  ##
  # @if jp
  # @class Objects
  # @brief ���֥������ȴ������������饹
  # @endif
  class Objects:
    def __init__(self):
      self._mutex = threading.RLock()
      self._obj = []


  ##
  # @if jp
  #
  # @brief ���ꤷ�����֥������Ȥ���Ͽ����
  # 
  # ���ꤷ�����֥������Ȥ���Ͽ���롣
  # Ʊ�쥪�֥������Ȥ���Ͽ�Ѥߤξ��ϡ�����Ԥ�ʤ���
  #
  # @param self
  # @param obj ��Ͽ�оݥ��֥�������
  #
  # @return ��Ͽ�������(���֥������Ȥ���Ͽ��������true)
  # 
  # @else
  #
  # @endif
  def registerObject(self, obj):
    guard = OpenRTM_aist.ScopedLock(self._objects._mutex)
    predi = self._predicate(factory=obj)

    for _obj in self._objects._obj:
      if predi(_obj):
        return False

    self._objects._obj.append(obj)
    return True


  ##
  # @if jp
  #
  # @brief ���ꤷ�����֥������Ȥ���Ͽ�������
  # 
  # ���ꤷ�����֥������Ȥ���Ͽ���������������롣
  # ���ꤷ�����֥������Ȥ���Ͽ����Ƥ��ʤ����ˤ�NULL���֤���
  #
  # @param self
  # @param id ��Ͽ����оݥ��֥������Ȥ�ID
  #
  # @return ��Ͽ������줿���֥�������
  # 
  # @else
  #
  # @endif
  def unregisterObject(self, id):
    guard = OpenRTM_aist.ScopedLock(self._objects._mutex)
    predi = self._predicate(name=id)
    i = 0
    for _obj in self._objects._obj:
      if predi(_obj):
        ret = _obj
        del self._objects._obj[i]
        return ret
      i+=1
      
    return None


  ##
  # @if jp
  #
  # @brief ���֥������Ȥ򸡺�����
  # 
  # ��Ͽ����Ƥ��륪�֥������Ȥ��椫����ꤷ�����˹��פ��륪�֥������Ȥ򸡺�
  # ���Ƽ������롣
  # ���ꤷ�����˹��פ��륪�֥������Ȥ���Ͽ����Ƥ��ʤ����ˤ�NULL���֤���
  #
  # @param self
  # @param id �����оݥ��֥������Ȥ�ID
  #
  # @return ���֥������Ȥθ������
  # 
  # @else
  #
  # @endif
  def find(self, id):
    guard = OpenRTM_aist.ScopedLock(self._objects._mutex)
    if isinstance(id,str):
      predi = self._predicate(name=id)
    else:
      predi = self._predicate(prop=id)

    for _obj in self._objects._obj:
      if predi(_obj):
        return _obj
      
    return None


  ##
  # @if jp
  #
  # @brief ��Ͽ����Ƥ��륪�֥������ȤΥꥹ�Ȥ��������
  # 
  # ��Ͽ����Ƥ��륪�֥������ȤΥꥹ�Ȥ�������롣
  #
  # @param self
  #
  # @return ��Ͽ����Ƥ��륪�֥������ȡ��ꥹ��
  # 
  # @else
  #
  # @endif
  def getObjects(self):
    guard = OpenRTM_aist.ScopedLock(self._objects._mutex)
    return self._objects._obj


  ##
  # @if jp
  # @brief ���֥������Ȥ򸡺�����
  #
  # ���ꤵ�줿���˹��פ��륪�֥������Ȥ򸡺����롣
  #
  # @param self
  # @param p ���֥������ȸ����ѥե��󥯥�
  #
  # @else
  #
  # @endif
  def for_each(self,p):
    guard = OpenRTM_aist.ScopedLock(self._objects._mutex)
    predi = p()

    for _obj in self._objects._obj:
      predi(_obj)

    return predi

