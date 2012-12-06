#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file OutPort.py
# @brief OutPort class
# @date $Date: 2007/09/19$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


from omniORB import *
from omniORB import any

import OpenRTM_aist


##
# @if jp
# @brief �ǡ����˥����ॹ����פ򥻥åȤ���
#
# �ǡ����ݡ��ȤΥǡ������Ф��ƥ����ॹ����פ򥻥åȤ��롣�ǡ����ݡ���
# �Υǡ����Ϲ�¤�ΤΥ��С��Ȥ��� tm.sec, tm.nsec �����ɬ�פ����롣
#
# @param data �����ॹ����פ򥻥åȤ���ǡ������¹Ը�¹Ի��Υ����ॹ
#             ����פ����åȤ����
#
# @else
# @brief Setting timestamp to data
#
# This function sets timestamp to data of data port. This data should
# have tm.sec, tm.nsec as members of the structure.
#
# @param data Data to be set timestamp. After executing this
#             function, current timestamp is set to the data.
#
# @endif
# template <class DataType>
# void setTimestamp(DataType& data)
def setTimestamp(data):
  # set timestamp
  tm = OpenRTM_aist.Time()
  data.tm.sec  = tm.sec
  data.tm.nsec = tm.usec * 1000


##
# @if jp
#
# @class OutPort
#
# @brief OutPort ���饹
# 
# OutPort �ѥ��饹
#
# @since 0.2.0
#
# @else
# 
# @endif
class OutPort(OpenRTM_aist.OutPortBase):
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
  # @param name �ݡ���̾
  # @param value ���Υݡ��Ȥ˥Х���ɤ����ǡ����ѿ�
  # @param buffer_ �Хåե�
  #
  # @else
  #
  # @brief Constructor
  #
  # @endif
  def __init__(self, name, value, buffer=None):
    OpenRTM_aist.OutPortBase.__init__(self, name, OpenRTM_aist.toTypename(value))
    self._value          = value
    #self._timeoutTick    = 1000 # timeout tick: 1ms
    #self._writeBlock     = False
    #self._writeTimeout   = 0
    self._OnWrite        = None
    self._OnWriteConvert = None
    #self._OnOverflow     = None
    #self._OnUnderflow    = None
    #self._OnConnect      = None
    #self._OnDisconnect   = None
    

  def __del__(self, OutPortBase=OpenRTM_aist.OutPortBase):
    OutPortBase.__del__(self)
    return

  ##
  # @if jp
  #
  # @brief �ǡ����񤭹���
  #
  # �ݡ��Ȥإǡ�����񤭹��ࡣ
  #
  # - ������Хå��ե��󥯥� OnWrite �����åȤ���Ƥ����硢
  #   OutPort ���ݻ�����Хåե��˽񤭹������� OnWrite ���ƤФ�롣
  # - OutPort ���ݻ�����Хåե��������С��ե��򸡽ФǤ���Хåե��Ǥ��ꡢ
  #   ���ġ��񤭹���ݤ˥Хåե��������С��ե��򸡽Ф�����硢
  #   ������Хå��ե��󥯥� OnOverflow ���ƤФ�롣
  # - ������Хå��ե��󥯥� OnWriteConvert �����åȤ���Ƥ����硢
  #   �Хåե��񤭹��߻��ˡ� OnWriteConvert �� operator() ������ͤ�
  #   �Хåե��˽񤭹��ޤ�롣
  #
  # @param self
  # @param value �񤭹����оݥǡ���
  #
  # @return �񤭹��߽������(�񤭹�������:true���񤭹��߼���:false)
  #
  # @else
  #
  # @brief Write data
  #
  # @endif
  # virtual bool write(const DataType& value)
  ##
  # @if jp
  #
  # @brief �ǡ����񤭹���
  #
  # �ݡ��Ȥإǡ�����񤭹��ࡣ
  # ���ꤵ�줿�ͤ�ݡ��Ȥ˽񤭹��ࡣ
  #
  # @param self
  # @param value �񤭹����оݥǡ���
  #
  # @return �񤭹��߽������(�񤭹�������:true���񤭹��߼���:false)
  #
  # @else
  #
  # @endif
  # bool operator<<(DataType& value)
  def write(self, value=None):
    if not value:
      value=self._value

    
    if self._OnWrite:
      self._OnWrite(value)

    # check number of connectors
    conn_size = len(self._connectors)
    if not conn_size > 0:
      return True
  
    # set timestamp
    #tm = Time()
    #value.tm.sec  = tm.sec
    #value.tm.nsec = tm.usec * 1000

    #tm_pre = Time()

    if self._OnWriteConvert:
      value = self._OnWriteConvert(value)
      
    result = True

    guard = OpenRTM_aist.ScopedLock(self._connector_mutex)
    for con in self._connectors:
      ret = con.write(value)
      if ret != self.PORT_OK:
        result = False
        if ret == self.CONNECTION_LOST:
          self.disconnect(con.id())

    return result


  ##
  # @if jp
  #
  # @brief �ǡ����񤭹��߽����Υ֥�å��⡼�ɤ�����
  #
  # �񤭹��߽������Ф��ƥ֥�å��⡼�ɤ����ꤹ�롣
  # �֥�å��⡼�ɤ���ꤷ����硢�Хåե��˽񤭹����ΰ褬�Ǥ��뤫
  # �����ॢ���Ȥ�ȯ������ޤ� write() �᥽�åɤθƤӤ������֥�å�����롣
  #
  # @param self
  # @param block �֥�å��⡼�ɥե饰
  #
  # @else
  #
  # @brief Set read() block mode
  #
  # @endif
  #def setWriteBlock(self, block):
  #  self._writeBlock = block


  ##
  # @if jp
  #
  # @brief �񤭹��߽����Υ����ॢ���Ȼ��֤�����
  # 
  # write() �Υ����ॢ���Ȼ��֤� usec �����ꤹ�롣
  # write() �ϥ֥�å��⡼�ɤǤʤ���Фʤ�ʤ���
  #
  # @param self
  # @param timeout �����ॢ���Ȼ��� [usec]
  #
  # @else
  #
  # @brief Set write() timeout
  #
  # @endif
  #def setWriteTimeout(self, timeout):
  #  self._writeTimeout = timeout


  ##
  # @if jp
  #
  # @brief OnWrite ������Хå�������
  #
  # �ǡ����񤭹���ľ���˸ƤФ�� OnWrite ������Хå��ե��󥯥������ꤹ�롣
  #
  # @param self
  # @param on_write OnWrite ������Хå��ե��󥯥�
  #
  # @else
  #
  # @brief Set OnWrite callback
  #
  # @endif
  def setOnWrite(self, on_write):
    self._OnWrite = on_write


  ##
  # @if jp
  #
  # @brief OnWriteConvert ������Хå�������
  #
  # �ǡ����񤭹��߻��˸ƤФ�� OnWriteConvert ������Хå��ե��󥯥�������
  # ���롣
  # ���Υ�����Хå��ؿ��ν�����̤��񤭹��ޤ�롣
  # ���Τ���񤭹��ߥǡ����Υե��륿��󥰤���ǽ�Ȥʤ롣
  #
  # @param self
  # @param on_wconvert OnWriteConvert ������Хå��ե��󥯥�
  #
  # @else
  #
  # @brief Set OnWriteConvert callback
  #
  # @endif
  def setOnWriteConvert(self, on_wconvert):
    self._OnWriteConvert = on_wconvert


  ##
  # @if jp
  #
  # @brief �ǡ�����̾�����ѥ᥽�å�
  #
  # �ǡ����η�̾��������뤿�ᡢInPortCorbaProvider����ƤФ�롣
  # 
  # @param self
  #
  # @return �Хåե������ꤵ��Ƥ���ǡ����η�̾
  #
  # @else
  #
  # @endif
  def getPortDataType(self):
    val = any.to_any(self._value)
    return str(val.typecode().name())



  class subscribe:
    def __init__(self, prof, subs = None):
      if subs:
        self._prof = subs._prof
        self._consumer = subs._consumer
        return

      self._prof = prof
      self._consumer = None
      

    def __call__(self, cons):
      if cons.subscribeInterface(self._prof.properties):
        self._consumer = cons
