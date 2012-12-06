#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file InPort.py
# @brief InPort template class
# @date $Date: 2007/09/20 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2003-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

from omniORB import *
from omniORB import any
import sys
import copy
import time

import OpenRTM_aist

##
# @if jp
#
# @class InPort
#
# @brief InPort ���饹
# 
# InPort �μ������饹��
# InPort �������˥�󥰥Хåե�����������������������줿�ǡ�����缡
# ���Υ�󥰥Хåե��˳�Ǽ���롣��󥰥Хåե��Υ������ϥǥե���Ȥ�64��
# �ʤäƤ��뤬�����󥹥ȥ饯�������ˤ�ꥵ��������ꤹ�뤳�Ȥ��Ǥ��롣
# �ǡ����ϥե饰�ˤ�ä�̤�ɡ����ɾ��֤��������졢isNew(), getNewDataLen()
# getNewList(), getNewListReverse() ���Υ᥽�åɤˤ��ϥ�ɥ�󥰤��뤳�Ȥ�
# �Ǥ��롣
#
# @since 0.2.0
#
# @else
#
# @class InPort
#
# @brief InPort template class
#
# This class template provides interfaces to input port.
# Component developer can define input value, which act as input
# port from other components, using this template.
# This is class template. This class have to be incarnated class as port
# value types. This value types are previously define RtComponent IDL.
# ex. type T: TimedFload, TimedLong etc... 
#
# @since 0.2.0
#
# @endif
class InPort(OpenRTM_aist.InPortBase):
  """
  """



  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯����
  #
  # @param self
  # @param name InPort ̾��InPortBase:name() �ˤ�껲�Ȥ���롣
  # @param value ���� InPort �˥Х���ɤ�����ѿ�
  # @param read_block �ɹ��֥�å��ե饰��
  #        �ǡ����ɹ�����̤�ɥǡ������ʤ���硢���Υǡ��������ޤǥ֥�å�����
  #        ���ɤ���������(�ǥե������:False)
  # @param write_block ����֥�å��ե饰��
  #        �ǡ���������˥Хåե����ե�Ǥ��ä���硢�Хåե��˶������Ǥ���
  #        �ޤǥ֥�å����뤫�ɤ���������(�ǥե������:False)
  # @param read_timeout �ɹ��֥�å�����ꤷ�Ƥ��ʤ����Ρ��ǡ����ɼ西����
  #        �����Ȼ���(�ߥ���)(�ǥե������:0)
  # @param write_timeout ����֥�å�����ꤷ�Ƥ��ʤ����Ρ��ǡ������������
  #        �����Ȼ���(�ߥ���)(�ǥե������:0)
  #
  # @else
  #
  # @brief A constructor.
  #
  # Setting channel name and registering channel value.
  #
  # @param self
  # @param name A name of the InPort. This name is referred by
  #             InPortBase::name().
  # @param value A channel value related with the channel.
  # @param read_block
  # @param write_block
  # @param read_timeout
  # @param write_timeout
  #
  # @endif
  def __init__(self, name, value, buffer=None,
               read_block=False, write_block=False,
               read_timeout=0, write_timeout = 0):
    OpenRTM_aist.InPortBase.__init__(self, name, OpenRTM_aist.toTypename(value))
    self._name           = name
    self._value          = value
    self._OnRead         = None
    self._OnReadConvert  = None


  def __del__(self, InPortBase=OpenRTM_aist.InPortBase):
    InPortBase.__del__(self)
    return

  ##
  # @if jp
  # @brief �ݡ���̾�Τ�������롣
  #
  # �ݡ���̾�Τ�������롣
  #
  # @param self
  #
  # @return �ݡ���̾��
  #
  # @else
  #
  # @endif
  #
  # const char* name()
  def name(self):
    return self._name


  ##
  # @if jp
  # @brief �ǿ��ǡ�������ǧ
  #
  # ���ߤΥХåե����֤˳�Ǽ����Ƥ���ǡ������ǿ��ǡ�������ǧ���롣
  #
  # @param self
  #
  # @return �ǿ��ǡ�����ǧ���
  #            ( true:�ǿ��ǡ������ǡ����Ϥޤ��ɤ߽Ф���Ƥ��ʤ�
  #             false:���Υǡ������ǡ����ϴ����ɤ߽Ф���Ƥ���)
  #
  # @else
  #
  # @endif
  #
  # bool isNew()
  def isNew(self):
    self._rtcout.RTC_TRACE("isNew()")

    if len(self._connectors) == 0:
      self._rtcout.RTC_DEBUG("no connectors")
      return False

    r = self._connectors[0].getBuffer().readable()
    if r > 0:
      self._rtcout.RTC_DEBUG("isNew() = True, readable data: %d",r)
      return True

    self._rtcout.RTC_DEBUG("isNew() = False, no readable data")
    return False


  ##
  # @if jp
  #
  # @brief �Хåե��������ɤ�����ǧ����
  # 
  # InPort�ΥХåե��������ɤ����� bool �ͤ��֤���
  # ���ξ��� true, ̤�ɥǡ������������ false ���֤���
  #
  # @return true  �Хåե��϶�
  #         false �Хåե���̤�ɥǡ���������
  # 
  # @else
  #
  # @brief Check whether the data is newest
  # 
  # Check whether the data stored at a current buffer position is newest.
  #
  # @return Newest data check result
  #         ( true:Newest data. Data has not been readout yet.
  #          false:Past data��Data has already been readout.)
  # 
  # @endif
  #
  # bool isEmpty()
  def isEmpty(self):
    self._rtcout.RTC_TRACE("isEmpty()")

    if len(self._connectors) == 0:
      self._rtcout.RTC_DEBUG("no connectors")
      return True

    r = self._connectors[0].getBuffer().readable()
    if r == 0:
      self._rtcout.RTC_DEBUG("isEmpty() = true, buffer is empty")
      return True
      
    self._rtcout.RTC_DEBUG("isEmpty() = false, data exists in the buffer")
    return False


  ##
  # @if jp
  #
  # @brief DataPort �����ͤ��ɤ߽Ф�
  #
  # InPort�˽񤭹��ޤ줿�ǡ������ɤߤ�������³����0���ޤ��ϥХåե���
  # �ǡ������񤭹��ޤ�Ƥ��ʤ����֤��ɤߤ�������������ͤ�����Ǥ��롣
  # �Хåե������ξ��֤ΤȤ���
  # ���������ꤵ�줿�⡼�� (readback, do_nothing, block) �˱����ơ�
  # �ʲ��Τ褦��ư��򤹤롣
  #
  # - readback: �Ǹ���ͤ��ɤߤʤ�����
  #
  # - do_nothing: ���⤷�ʤ�
  #
  # - block: �֥�å����롣�����ॢ���Ȥ����ꤵ��Ƥ�����ϡ�
  #       �����ॢ���Ȥ���ޤ��Ԥġ�
  #
  # �Хåե������ξ��֤Ǥϡ�InPort�˥Х���ɤ��줿�ѿ����ͤ��֤���롣
  # �������äơ�����ɤ߽Ф����ˤ������ͤ��֤���ǽ�������롣
  # ���δؿ������Ѥ���ݤˤϡ�
  #
  # - isNew(), isEmpty() ��ʻ�Ѥ��������˥Хåե����֤�����å����롣
  # 
  # - ����ɤ߽Ф����������ͤ��֤��ʤ��褦�˥Х�����ѿ�������˽��������
  # 
  #
  # �ƥ�����Хå��ؿ��ϰʲ��Τ褦�˸ƤӽФ���롣
  # - OnRead: read() �ؿ����ƤФ��ݤ�ɬ���ƤФ�롣
  # 
  # - OnReadConvert: �ǡ������ɤ߽Ф�������������硢�ɤߤ������ǡ�����
  #       �����Ȥ���OnReadConvert���ƤӽФ��졢����ͤ�read()�������
  #       �Ȥ����֤���
  #
  # - OnEmpty: �Хåե������Τ���ǡ������ɤ߽Ф��˼��Ԥ������ƤӽФ���롣
  #        OnEmpty ������ͤ� read() ������ͤȤ����֤���
  #
  # - OnBufferTimeout: �ǡ����ե�����Push���ξ��ˡ��ɤ߽Ф�
  #        �����ॢ���ȤΤ���˥ǡ������ɤ߽Ф��˼��Ԥ������˸ƤФ�롣
  #
  # - OnRecvTimeout: �ǡ����ե�����Pull���ξ��ˡ��ɤ߽Ф������ॢ����
  #        �Τ���˥ǡ����ɤ߽Ф��˼��Ԥ������˸ƤФ�롣
  #
  # - OnReadError: �嵭�ʳ�����ͳ���ɤߤ����˼��Ԥ������˸ƤФ�롣
  #        ��ͳ�Ȥ��Ƥϡ��Хåե�����������硢�㳰��ȯ���ʤɤ��ͤ�����
  #        ���̾�ϵ����ꤨ�ʤ�����Х��β�ǽ�������롣
  #
  # @return �ɤ߽Ф����ǡ���
  #
  # @else
  #
  # @brief Readout the value from DataPort
  #
  # Readout the value from DataPort
  #
  # - When Callback functor OnRead is already set, OnRead will be invoked
  #   before reading from the buffer held by DataPort.
  # - When the buffer held by DataPort can detect the underflow,
  #   and when it detected the underflow at reading, callback functor
  #   OnUnderflow will be invoked.
  # - When callback functor OnReadConvert is already set, the return value of
  #   operator() of OnReadConvert will be the return value of read().
  # - When timeout of reading is already set by setReadTimeout(),
  #   it waits for only timeout time until the state of the buffer underflow
  #   is reset, and if OnUnderflow is already set, this will be invoked to 
  #   return.
  #
  # @return Readout data
  #
  # @endif
  #
  #  DataType read()
  def read(self):
    self._rtcout.RTC_TRACE("DataType read()")

    if self._OnRead is not None:
      self._OnRead()
      self._rtcout.RTC_TRACE("OnRead called")

    if len(self._connectors) == 0:
      self._rtcout.RTC_DEBUG("no connectors")
      return self._value

    _val = copy.deepcopy(self._value)
    cdr = [_val]
    ret = self._connectors[0].read(cdr)


    if ret == OpenRTM_aist.DataPortStatus.PORT_OK:
      self._rtcout.RTC_DEBUG("data read succeeded")
      self._value = cdr[0]

      if self._OnReadConvert is not None:
        self._value = self._OnReadConvert(self._value)
        self._rtcout.RTC_DEBUG("OnReadConvert called")
        return self._value
      return self._value

    elif ret == OpenRTM_aist.DataPortStatus.BUFFER_EMPTY:
      self._rtcout.RTC_WARN("buffer empty")
      return self._value

    elif ret == OpenRTM_aist.DataPortStatus.BUFFER_TIMEOUT:
      self._rtcout.RTC_WARN("buffer read timeout")
      return self._value

    self._rtcout.RTC_ERROR("unknown retern value from buffer.read()")
    return self._value


  ##
  # @if jp
  #
  # @brief �Х���ɤ��줿�ѿ��� InPort �Хåե��κǿ��ͤ��ɤ߹���
  #
  # �Х���ɤ��줿�ǡ����� InPort �κǿ��ͤ��ɤ߹��ࡣ
  # ���󥹥ȥ饯�����ѿ��� InPort ���Х���ɤ���Ƥ��ʤ���Фʤ�ʤ���
  # ���Υ᥽�åɤϥݥ�⡼�ե��å��˻��Ѥ�����������Ȥ��Ƥ��뤿�ᡢ
  # ���˰�¸���ʤ�����������ͤȤʤäƤ��롣
  #
  # @param self
  #
  # @else
  #
  # @brief Read into bound T-type data from current InPort
  #
  # @endif
  def update(self):
    self.read()


  ##
  # @if jp
  #
  # @brief InPort �Хåե��إǡ����ɤ߹��߻��Υ�����Хå�������
  #
  # InPort �����ĥХåե�����ǡ������ɤ߹��ޤ��ľ���˸ƤФ�륳����Хå�
  # ���֥������Ȥ����ꤹ�롣
  # 
  # @param self
  # @param on_read �����оݥ�����Хå����֥�������
  #
  # @else
  #
  # @endif
  def setOnRead(self, on_read):
    self._OnRead = on_read


  ##
  # @if jp
  #
  # @brief InPort �Хåե��إǡ����ɤ߽Ф����Υ�����Хå�������
  #
  # InPort �����ĥХåե�����ǡ������ɤ߽Ф����ݤ˸ƤФ�륳����Хå�
  # ���֥������Ȥ����ꤹ�롣������Хå����֥������Ȥ�����ͤ�read()�᥽�å�
  # �θƽз�̤Ȥʤ롣
  # 
  # @param self
  # @param on_rconvert �����оݥ�����Хå����֥�������
  #
  # @else
  #
  # @endif
  def setOnReadConvert(self, on_rconvert):
    self._OnReadConvert = on_rconvert
