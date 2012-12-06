#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file PortCallBack.py
# @brief PortCallBack class
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
 

#============================================================
# callback functor base classes
#

##
# @if jp
# @class ConnectCallback
# @brief connect/notify_connect() ���Υ�����Хå���ݥ��饹
#
# Port���Ф���connect/notify_connect() �����ƤӽФ������˸ƤӽФ����
# ������Хå��ե��󥯥��������� RTC::ConnectorProfile ���롣
#
# @param profile ConnectorProfile
#
# @since 1.0.0
#
# @else
# @class ConnectCallback
# @brief Callback functor abstract for connect/notify_connect() funcs
#
# This is the interface for callback functor for connect/notify_connect()
# invocation in Port. Argument is RTC::ConnectorProfile that is given
# these functions.
#
# @param profile ConnectorProfile
#
# @since 1.0.0
#
# @endif
#
class ConnectionCallback:
  """
  """

  ##
  # @if jp
  #
  # @brief ������Хå��ؿ�
  #
  # connect/notify_connect() �����ƤӽФ������˸ƤӽФ����
  # ������Хå��ؿ�
  #
  # @param self
  # @param profile ConnectorProfile
  #
  # @else
  #
  # @brief Callback method
  #
  # This is the callback method invoked when connect/notify_connect()
  # invocation in Port.
  #
  # @param self
  # @param profile ConnectorProfile
  #
  # @endif
  #
  # virtual void operator()(RTC::ConnectorProfile& profile) = 0;
  def __call__(self, profile):
    pass


##
# @if jp
# @class DisconnectCallback
# @brief disconnect/notify_disconnect() ���Υ�����Хå���ݥ��饹
#
# Port���Ф���disconnect/notify_disconnect() �����ƤӽФ������˸ƤӽФ����
# ������Хå��ե��󥯥�����������³ID���롣
#
# @since 1.0.0
#
# @else
# @class DisconnectCallback
# @brief Callback functor abstract for disconnect/notify_disconnect() funcs
#
# This is the interface for callback functor for 
# disconnect/notify_disconnect() invocation in Port.
# Argument is connector ID is given these functions.
#
# @since 1.0.0
#
# @endif
#
class DisconnectCallback:
  """
  """

  ##
  # @if jp
  #
  # @brief ������Хå��ؿ�
  #
  # disconnect/notify_disconnect() �����ƤӽФ������˸ƤӽФ����
  # ������Хå��ؿ�
  #
  # @param self
  # @param connector_id Connector ID
  #
  # @else
  #
  # @brief Callback method
  #
  # This is the callback method invoked when disconnect/notify_disconnect()
  # invocation in Port.
  #
  # @param self
  # @param connector_id Connector ID
  #
  # @endif
  #
  # virtual void operator()(const char* connector_id) = 0;
  def __call__(self, connector_id):
    pass


##
# @if jp
# @class OnWrite
# @brief write() ���Υ�����Хå����饹(���֥��饹������)
#
# DataPort�ΥХåե��˥ǡ�����write()�����ľ���˸ƤӽФ���륳����Хå���<BR>
# �����֥��饹�Ǥμ���������
#
# @since 0.4.0
#
# @else
# @class OnPut
# @brief OnPut abstract class
#
# @endif
class OnWrite:
  """
  """

  ##
  # @if jp
  #
  # @brief ������Хå��ؿ�
  #
  # �Хåե��˥ǡ������񤭹��ޤ��ľ���˸ƤӽФ���륳����Хå��ؿ�
  #
  # @param self
  # @param value �Хåե��˽񤭹��ޤ��ǡ���
  #
  # @else
  #
  # @brief Callback function
  #
  # This is the callback method invoked immediately before data is written
  # into the buffer.
  #
  # @param self
  # @param value Data that is written into the buffer
  #
  # @endif
  #
  def __call__(self, value):
    pass



##
# @if jp
# @class OnWriteConvert
# @brief write() ���Υǡ����Ѵ�������Хå����饹(���֥��饹������)
#
# InPort/OutPort�ΥХåե��˥ǡ����� write()�������˸ƤӽФ����<BR>
# �����֥��饹�Ǥμ���������
# ������Хå��ѥ��󥿡��ե�������
# ���Υ�����Хå�������ͤ��Хåե��˳�Ǽ����롣
#
# @since 0.4.0
#
# @else
# @class OnWriteConvert
# @brief OnWriteConvert abstract class
#
# @endif
class OnWriteConvert:
  """
  """

  ##
  # @if jp
  #
  # @brief ������Хå��ؿ�
  #
  # �Хåե��˥ǡ������񤭹��ޤ��ݤ˸ƤӽФ���륳����Хå��ؿ���
  #
  # @param self
  # @param value �Ѵ����ǡ���
  # @return �Ѵ���ǡ���
  #
  # @else
  #
  # @brief Callback function
  #
  # This is the callback function invoked when data is written into the
  # buffer.
  #
  # @param self
  # @param value Data to be converted
  # @return Converted data
  #
  # @endif
  #
  def __call__(self,value):
    pass



##
# @if jp
# @class OnRead
# @brief read() ���Υ�����Хå����饹(���֥��饹������)
#
# InPort/OutPort�ΥХåե�����ǡ����� read()�����ľ���˸ƤӽФ����
# ������Хå��ѥ��󥿡��ե�������<BR>
# �����֥��饹�Ǥμ���������
#
# @since 0.4.0
#
# @else
# @class OnRead
# @brief OnRead abstract class
#
# @endif
class OnRead:
  """
  """

  ##
  # @if jp
  #
  # @brief ������Хå��᥽�å�
  #
  # �Хåե�����ǡ������ɤ߽Ф����ľ���˸ƤӽФ���륳����Хå��ؿ���
  #
  # @else
  #
  # @brief Callback function
  #
  # This is the callback method invoked immediately before data is readout
  # from the buffer.
  #
  # @endif
  def __call__(self):
    pass



##
# @if jp
# @class OnReadConvert
# @brief read() ���Υǡ����Ѵ�������Хå����饹(���֥��饹������)
#
# InPort/OutPort�ΥХåե�����ǡ����� read()�����ݤ˸ƤӽФ����
# ������Хå��ѥ��󥿡��ե�������
# ���Υ�����Хå�������ͤ�read()������ͤȤʤ롣<BR>
# �����֥��饹�Ǥμ���������
#
# @since 0.4.0
#
# @else
# @class OnReadConvert
# @brief OnReadConvert abstract class
#
# @endif
class OnReadConvert:
  """
  """

  ##
  # @if jp
  #
  # @brief ������Хå��᥽�å�
  #
  # �Хåե�����ǡ������ɤ߽Ф����ݤ˸ƤӽФ���륳����Хå��ؿ�
  # �Ǥ��ꡢoperator()() ������ͤ� InPort �� read() ������ͤȤʤ롢
  # �ޤ��ϥǡ����ѿ��˳�Ǽ����롣
  #
  # @param self
  # @param value �Хåե������ɤߤ����줿�ǡ���
  # @return �Ѵ���Υǡ������ǡ����ݡ����ѿ��ˤϤ����ͤ���Ǽ����롣
  #
  # @else
  #
  # @brief Callback method
  #
  # This function is the callback function invoked when data is
  # readout from the buffer, and the return value of operator()()
  # is used as return value of InPort's read() or it is stored in
  # the InPort data variable.
  #
  # @param self
  # @param value Data that is readout from buffer
  # @return Converted data. These data are stored in the port's variable.
  #
  # @endif
  #
  def __call__(self,value):
    pass
