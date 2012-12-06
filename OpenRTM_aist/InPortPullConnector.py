#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file InPortPullConnector.py
# @brief InPortPull type connector class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2009
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

from omniORB import *
from omniORB import any

import OpenRTM_aist


##
# @if jp
# @class InPortPullConnector
# @brief InPortPullConnector ���饹
#
# InPort �� pull ���ǡ����ե��Τ���� Connector ���饹�����Υ���
# �������Ȥϡ���³���� dataflow_type �� pull �����ꤵ�줿��硢
# InPort �ˤ�ä���������ͭ���졢OutPortPullConnector ���Фˤʤäơ�
# �ǡ����ݡ��Ȥ� pull ���Υǡ����ե���¸����롣��Ĥ���³���Ф��ơ�
# ��ĤΥǡ������ȥ꡼����󶡤���ͣ��� Connector ���б����롣
# Connector �� ��³������������� UUID ������ ID �ˤ����̤���롣
#
# InPortPullConnector �ϰʲ��λ��ĤΥ��֥������Ȥ��ͭ���������롣
#
# - InPortConsumer
# - Buffer
#
# OutPort �˽񤭹��ޤ줿�ǡ����� OutPortPullConnector::write() ����
# ���� Buffer �˽񤭹��ޤ�롣InPort::read(),
# InPortPullConnector::read() �Ϸ�̤Ȥ��ơ�OutPortConsumer::get()
# ��ƤӽФ���OutPortPullConnector �λ��ĥХåե�����ǡ������ɤ߽�
# ����InPortPullConnector �Τ�ĥХåե��˥ǡ�����񤭹��ࡣ
#
# @since 1.0.0
#
# @else
# @class InPortPullConnector
# @brief InPortPullConnector class
#
# Connector class of InPort for pull type dataflow. When "pull" is
# specified as dataflow_type at the time of establishing
# connection, this object is generated and owned by the InPort.
# This connector and InPortPullConnector make a pair and realize
# pull type dataflow of data ports. One connector corresponds to
# one connection which provides a data stream. Connector is
# distinguished by ID of the UUID that is generated at establishing
# connection.
#
# InPortPullConnector owns and manages the following objects.
#
# - InPortConsumer
# - Buffer
#
# Data written into the OutPort is passed to the
# OutPortPullConnector::write(), and is written into the buffer.
# Consequently, InPort::read() and InPortPullConnector::read() call
# OutPortConsumer::get(), and it reads data from the buffer of
# OutPortPullConnector.  Finally data would be written into the
# InPortPullConnector's buffer.
#
# @since 1.0.0
#
# @endif
#
class InPortPullConnector(OpenRTM_aist.InPortConnector):
  """
  """
    
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # InPortPullConnector �Υ��󥹥ȥ饯���ϥ��֥��������������˲���
  # ������ˤȤ롣ConnectorInfo ����³�����ޤߡ����ξ���˽����Х�
  # �ե������������롣OutPort ���󥿡��ե������Υץ�Х������֥�����
  # �ȤؤΥݥ��󥿤��ꡢ��ͭ������ĤΤǡ�InPortPullConnector ��
  # OutPortConsumer �β�����Ǥ����ġ��Ƽ磻�٥�Ȥ��Ф��륳����Х�
  # ���������󶡤��� ConnectorListeners �������Ŭ�ڤʥ����ߥ󥰤ǥ���
  # ��Хå���ƤӽФ����ǡ����Хåե����⤷ InPortBase �����󶡤�
  # �����Ϥ��Υݥ��󥿤��롣
  #
  # @param info ConnectorInfo
  # @param consumer OutPortConsumer
  # @param listeners ConnectorListeners ���Υꥹ�ʥ��֥������ȥꥹ��
  # @param buffer CdrBufferBase ���ΥХåե�
  #
  # @else
  # @brief Constructor
  #
  # InPortPullConnector's constructor is given the following
  # arguments.  According to ConnectorInfo which includes
  # connection information, a buffer is created.  It is also given
  # a pointer to the consumer object for the OutPort interface.
  # The owner-ship of the pointer is owned by this
  # OutPortPullConnector, it has responsibility to destruct the
  # OutPortConsumer.  OutPortPullConnector also has
  # ConnectorListeners to provide event callback mechanisms, and
  # they would be called at the proper timing.  If data buffer is
  # given by OutPortBase, the pointer to the buffer is also given
  # as arguments.
  #
  # @param info ConnectorInfo
  # @param consumer OutPortConsumer
  # @param listeners ConnectorListeners type lsitener object list
  # @param buffer CdrBufferBase type buffer
  #
  # @endif
  #
  # InPortPullConnector(ConnectorInfo info,
  #                     OutPortConsumer* consumer,
  #                     ConnectorListeners& listeners,
  #                     CdrBufferBase* buffer = 0);
  def __init__(self, info, consumer, listeners, buffer = 0):
    OpenRTM_aist.InPortConnector.__init__(self, info, buffer)
    self._consumer = consumer
    self._listeners = listeners
    if buffer == 0:
      self._buffer = self.createBuffer(self._profile)

    if self._buffer == 0 or not self._consumer:
      raise
        
    self._buffer.init(info.properties.getNode("buffer"))
    self._consumer.setBuffer(self._buffer)
    self._consumer.setListener(info, self._listeners)
    self.onConnect()
    return


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # disconnect() ���ƤФ졢consumer, publisher, buffer �����Ρ��������롣
  #
  # @else
  #
  # @brief Destructor
  #
  # This operation calls disconnect(), which destructs and deletes
  # the consumer, the publisher and the buffer.
  #
  # @endif
  #
  def __del__(self):
    return


  ##
  # @if jp
  # @brief read �ؿ�
  #
  # OutPortConsumer ����ǡ�����������롣������ɤ߽Ф�����硢���
  # �ͤ� PORT_OK �Ȥʤꡢdata ���ɤ߽Ф��줿�ǡ�������Ǽ����롣����
  # �ʳ��ξ��ˤϡ����顼�ͤȤ��� BUFFER_EMPTY, TIMEOUT,
  # PRECONDITION_NOT_MET, PORT_ERROR ���֤���롣
  #
  # @return PORT_OK              ���ｪλ
  #         BUFFER_EMPTY         �Хåե��϶��Ǥ���
  #         TIMEOUT              �����ॢ���Ȥ���
  #         PRECONDITION_NOT_MET ���������������ʤ�
  #         PORT_ERROR           ����¾�Υ��顼
  #
  # @else
  # @brief Destructor
  #
  # This function get data from OutPortConsumer.  If data is read
  # properly, this function will return PORT_OK return code. Except
  # normal return, BUFFER_EMPTY, TIMEOUT, PRECONDITION_NOT_MET and
  # PORT_ERROR will be returned as error codes.
  #  
  # @return PORT_OK              Normal return
  #         BUFFER_EMPTY         Buffer empty
  #         TIMEOUT              Timeout
  #         PRECONDITION_NOT_MET Preconditin not met
  #         PORT_ERROR           Other error
  #
  # @endif
  #
  # virtual ReturnCode read(cdrMemoryStream& data);
  def read(self, data):
    self._rtcout.RTC_TRACE("InPortPullConnector.read()")
    if not self._consumer:
      return self.PORT_ERROR

    cdr_data = [None]
    ret = self._consumer.get(cdr_data)

    if ret == self.PORT_OK:
      # CDR -> (conversion) -> data
      if self._endian is not None:
        data[0] = cdrUnmarshal(any.to_any(data[0]).typecode(),cdr_data[0],self._endian)

      else:
        self._rtcout.RTC_ERROR("unknown endian from connector")
        return OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET
    
    return ret


  ##
  # @if jp
  # @brief ��³����ؿ�
  #
  # Connector ���ݻ����Ƥ�����³��������
  #
  # @else
  # @brief Disconnect connection
  #
  # This operation disconnect this connection
  #
  # @endif
  #
  # virtual ReturnCode disconnect();
  def disconnect(self):
    self._rtcout.RTC_TRACE("disconnect()")
    self.onDisconnect()
    # delete consumer
    if self._consumer:
      OpenRTM_aist.OutPortConsumerFactory.instance().deleteObject(self._consumer)
    self._consumer = 0

    return self.PORT_OK
        
  ##
  # @if jp
  # @brief �����ƥ��ֲ�
  #
  # ���Υ��ͥ����򥢥��ƥ��ֲ�����
  #
  # @else
  #
  # @brief Connector activation
  #
  # This operation activates this connector
  #
  # @endif
  #
  # virtual void activate(){}; // do nothing
  def activate(self): # do nothing
    pass

  ##
  # @if jp
  # @brief �󥢥��ƥ��ֲ�
  #
  # ���Υ��ͥ������󥢥��ƥ��ֲ�����
  #
  # @else
  #
  # @brief Connector deactivation
  #
  # This operation deactivates this connector
  #
  # @endif
  #
  # virtual void deactivate(){}; // do nothing
  def deactivate(self): # do nothing
    pass
  
  ##
  # @if jp
  # @brief Buffer������
  #
  # Ϳ����줿��³����˴�Ť��Хåե����������롣
  #
  # @param info ��³����
  # @return �Хåե��ؤΥݥ���
  #
  # @else
  # @brief create buffer
  #
  # This function creates a buffer based on given information.
  #
  # @param info Connector information
  # @return The poitner to the buffer
  #
  # @endif
  #
  # CdrBufferBase* createBuffer(Profile& profile);
  def createBuffer(self, profile):
    buf_type = profile.properties.getProperty("buffer_type","ring_buffer")
    return OpenRTM_aist.CdrBufferFactory.instance().createObject(buf_type)
    
  ##
  # @if jp
  # @brief ��³��Ω���˥�����Хå���Ƥ�
  # @else
  # @brief Invoke callback when connection is established
  # @endif
  # void onConnect()
  def onConnect(self):
    if self._listeners and self._profile:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_CONNECT].notify(self._profile)
    return

  ##
  # @if jp
  # @brief ��³���ǻ��˥�����Хå���Ƥ�
  # @else
  # @brief Invoke callback when connection is destroied
  # @endif
  # void onDisconnect()
  def onDisconnect(self):
    if self._listeners and self._profile:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_DISCONNECT].notify(self._profile)
    return
