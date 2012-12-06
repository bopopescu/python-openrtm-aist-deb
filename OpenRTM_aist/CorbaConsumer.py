#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
#
# @file CorbaConsumer.py
# @brief CORBA Consumer class
# @date $Date: 2007/09/20 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


from omniORB import CORBA

##
# @if jp
# @class CorbaConsumerBase
#
# @brief ���֥������ȥ�ե���󥹤��ݻ�����ץ졼���ۥ�����쥯�饹
#
# �̿����ʤȤ��� CORBA �����򤷤����Υ��󥷥塼�޼����Τ���δ��쥯�饹
#
# @since 0.4.0
#
# @else
# @class ConsumerBase
# @brief Placeholder base class to hold remote object reference.
# @endif
class CorbaConsumerBase:
  """
  """



  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  # 
  # @param self 
  # @param consumer ���ԡ�����CorbaConsumerBase���֥�������
  #
  # @else
  #
  # @brief Consructor
  #
  # @param self 
  #
  # @endif
  def __init__(self, consumer=None):
    if consumer:
      self._objref = consumer._objref
    else:
      self._objref = None


  ##
  # @if jp
  # 
  # @brief �����黻��
  # 
  # @param self 
  # @param consumer ������
  # 
  # @return �������
  # 
  # @else
  # 
  # @brief Assignment operator
  # 
  # @param self 
  # @param consumer Copy source.
  # 
  # @endif
  def equal(self, consumer):
    self._objref = consumer._objref
    return self


  ##
  # @if jp
  #
  # @brief CORBA���֥������Ȥ򥻥åȤ���
  #
  # Ϳ����줿���֥������ȥ�ե���󥹤ϡ�ConsumerBase ���֥����������
  # CORBA::Object_var ���Ȥ����ݻ�����롣 
  #
  # @param self
  # @param obj CORBA ���֥������ȤΥ�ե����
  #
  # @return obj �� nil ��ե���󥹤ξ�� false ���֤���
  #
  # @else
  #
  # @brief Set CORBA Object
  #
  # The given CORBA Object is held as CORBA::Object_var type
  #
  # @param self
  # @param obj Object reference of CORBA object
  #
  # @return If obj is nil reference, it returns false.
  #
  # @endif
  def setObject(self, obj):
    if CORBA.is_nil(obj):
      return False

    self._objref = obj
    return True


  ##
  # @if jp
  #
  # @brief CORBA���֥������Ȥ��������
  #
  # ConsumerBase ���֥���������� CORBA::Object_var ���Ȥ����ݻ�����Ƥ���
  # ���֥������ȥ�ե���󥹤�������롣 
  #
  # @param self
  #
  # @return obj CORBA ���֥������ȤΥ�ե����
  #
  # @else
  #
  # @brief Get CORBA Object
  #
  # @param self
  #
  # @return Object reference of CORBA object
  #
  # @endif
  def getObject(self):
    return self._objref


  ##
  # @if jp
  #
  # @brief CORBA���֥������Ȥ�����򥯥ꥢ����
  #
  # ���ꤵ��Ƥ��� CORBA ���֥������Ȥ򥯥ꥢ���롣
  # CORBA���֥������Ȥ��Τ�Τ��Ф��Ƥϲ������ʤ���
  #
  # @param self
  #
  # @else
  #
  # @endif
  def releaseObject(self):
    self._objref = CORBA.Object._nil



##
# @if jp
#
# @class CorbaConsumer
# @brief ���֥������ȥ�ե���󥹤��ݻ�����ץ졼���ۥ�����饹
# 
# ������Ϳ����줿����CORBA���֥������Ȥ��ݻ����롣
# ���֥������Ȥ����åȤ��줿�Ȥ��ˡ�Ϳ����줿���� narrow �����Τǡ�
# _ptr() �Ǽ��������ե���󥹤ϡ�narrow �ѤߤΥ�ե���󥹤Ǥ��롣
#
# @since 0.4.0
#
# @else
#
# @class Consumer.CorbaConsumer
# @brief Placeholder class to hold remote object reference.
#
# This class holds a type of object that given by parameter.
# For internal use, _ptr type and _var type should be given as parameter.
#
# @since 0.4.0
#
# @endif
class CorbaConsumer(CorbaConsumerBase):
  """
  """



  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # @param self
  # @param interfaceType ���Υۥ�����ݻ����륪�֥������Ȥη�
  #                      (�ǥե������;None)
  # @param consumer ���Υۥ�����ݻ����륪�֥�������(�ǥե������;None)
  #
  # @else
  #
  # @brief Consructor
  #
  # @endif
  def __init__(self, interfaceType=None, consumer=None):
    if interfaceType:
      self._interfaceType = interfaceType
    else:
      self._interfaceType = None

    if consumer:
      CorbaConsumerBase.__init__(self, consumer)
      self._var = consumer._var
    else:
      CorbaConsumerBase.__init__(self)
      self._var = None


  ##
  # @if jp
  # 
  # @brief �����黻��
  # 
  # @param self 
  # @param consumer ������
  # 
  # @return �������
  # 
  # @else
  # 
  # @brief Assignment operator
  # 
  # @param self 
  # @param consumer Copy source.
  # 
  # @endif
  def equal(self, consumer):
    self._var = consumer._var


  def __del__(self):
    self.releaseObject()


  ##
  # @if jp
  # @brief ���֥������Ȥ򥻥åȤ���
  #
  # ConsumerBase �Υ����С��饤�ɡ�CORBA::Object_var �˥��֥������Ȥ򥻥å�
  # ����ȤȤ�ˡ��ѥ�᡼���η��� narrow �������֥������Ȥ��ݻ����롣
  #
  # @param self
  # @param obj CORBA Objecct
  #
  # @return ���֥�������������
  #         �����оݥ��֥������Ȥ� null �ξ��� false ���֤äƤ���
  # 
  # @else
  # @brief Set Object
  #
  # Override function of ConsumerBase. This operation set an Object to 
  # CORBA:Object_var in the class, and this object is narrowed to
  # given parameter and stored in.
  #
  # @param self
  # @param obj CORBA Objecct
  #
  # @endif
  def setObject(self, obj):
    if not CorbaConsumerBase.setObject(self, obj):
      self.releaseObject()
      return False

    if self._interfaceType:
      self._var = obj._narrow(self._interfaceType)
    else:
      self._var = self._objref

    if not CORBA.is_nil(self._var):
      return True

    self.releaseObject()
    return False


  ##
  # @if jp
  # @brief ObjectType ���Υ��֥������ȤΥ�ե���󥹤����
  #
  # ObjectType �� narrow�ѤߤΥ��֥������ȤΥ�ե���󥹤�������롣
  # ���֥������ȥ�ե���󥹤���Ѥ���ˤϡ�setObject() �ǥ��åȺѤߤ�
  # �ʤ���Фʤ�ʤ���
  # ���֥������Ȥ����åȤ���Ƥ��ʤ���С�nil ���֥������ȥ�ե���󥹤�
  # �֤���롣
  #
  # @param self
  #
  # @return ObjectType �� narrow �ѤߤΥ��֥������ȤΥ�ե����
  # 
  # @else
  # @brief Get Object reference narrowed as ObjectType
  #
  # This operation returns object reference narrowed as ObjectType.
  # To use the returned object reference, reference have to be set by
  # setObject().
  # If object is not set, this operation returns nil object reference.
  #
  # @return The object reference narrowed as ObjectType
  #
  # @endif
  def _ptr(self):
    return self._var


  ##
  # @if jp
  #
  # @brief CORBA���֥������Ȥ�����򥯥ꥢ����
  #
  # ���ꤵ��Ƥ��� CORBA ���֥������Ȥ򥯥ꥢ���롣
  # CORBA���֥������Ȥ��Τ�Τ��Ф��Ƥϲ������ʤ���
  #
  # @param self
  #
  # @else
  #
  # @endif
  def releaseObject(self):
    CorbaConsumerBase.releaseObject(self)
    self._var = CORBA.Object._nil
