#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
#
# @file InPortPushConnector.py
# @brief Push type connector class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara.
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
# @class InPortPushConnector
# @brief InPortPushConnector ���饹
#
# InPort �� push ���ǡ����ե��Τ���� Connector ���饹�����Υ���
# �������Ȥϡ���³���� dataflow_type �� push �����ꤵ�줿��硢
# InPort �ˤ�ä���������ͭ���졢OutPortPushConnector ���Фˤʤäơ�
# �ǡ����ݡ��Ȥ� push ���Υǡ����ե���¸����롣��Ĥ���³���Ф��ơ�
# ��ĤΥǡ������ȥ꡼����󶡤���ͣ��� Connector ���б����롣
# Connector �� ��³������������� UUID ������ ID �ˤ����̤���롣
#
# InPortPushConnector �ϰʲ��λ��ĤΥ��֥������Ȥ��ͭ���������롣
#
# - InPortProvider
# - Buffer
#
# OutPort �˽񤭹��ޤ줿�ǡ����ϡ�OutPortConnector �ˤ�ä�
# InPortProvider::put() �˥ǡ������Ϥ���롣�񤭹��ޤ줿�ǡ�����
# Connector ��� Buffer �˥ǡ������񤭹��ޤ�롣
#
# @since 1.0.0
#
# @else
# @class InPortPushConnector
# @brief InPortPushConnector class
#
# Connector class of InPort for push type dataflow.  When "push"
# is specified as dataflow_type at the time of establishing
# connection, this object is generated and owned by the InPort.
# This connector and OutPortPushConnector make a pair and realize
# push type dataflow of data ports.  One connector corresponds to
# one connection which provides a data stream.  Connector is
# distinguished by ID of the UUID that is generated at establishing
# connection.
#
# InPortPushConnector owns and manages the following objects.
#
# - OutPortConsumer
# - Buffer
#
# Data written into the OutPort are passed to the
# InPortProvider::put() by OutPortConnector.  The data is written
# into the buffer in the connector.
#
# @since 1.0.0
#
# @endif
#
class InPortPushConnector(OpenRTM_aist.InPortConnector):
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # InPortPushConnector �Υ��󥹥ȥ饯���ϥ��֥��������������˲�����
  # �����ˤȤ롣ConnectorInfo ����³�����ޤߡ����ξ���˽����Хåե�
  # �����������롣InPort ���󥿡��ե������Υץ�Х������֥������Ȥ�
  # �Υݥ��󥿤��ꡢ��ͭ������ĤΤǡ�InPortPushConnector ��
  # InPortProvider �β�����Ǥ����ġ��Ƽ磻�٥�Ȥ��Ф��륳����Х�
  # ���������󶡤��� ConnectorListeners �������Ŭ�ڤʥ����ߥ󥰤ǥ���
  # ��Хå���ƤӽФ����ǡ����Хåե����⤷ InPortBase �����󶡤���
  # ����Ϥ��Υݥ��󥿤��롣
  #
  # @param info ConnectorInfo
  # @param provider InPortProvider
  # @param listeners ConnectorListeners ���Υꥹ�ʥ��֥������ȥꥹ��
  # @param buffer CdrBufferBase ���ΥХåե�
  #
  # @elsek
  # @brief Constructor
  #
  # InPortPushConnector's constructor is given the following
  # arguments.  According to ConnectorInfo which includes
  # connection information, a buffer is created.
  # It is also given a pointer to the provider object for the
  # InPort interface.  The owner-ship of the pointer is owned by
  # this InPortPushConnector, it has responsibility to destruct
  # the InPortProvider.  InPortPushConnector also has
  # ConnectorListeners to provide event callback mechanisms, and
  # they would be called at the proper timing.  If data buffer is
  # given by InPortBase, the pointer to the buffer is also given
  # as arguments.
  #
  # @param info ConnectorInfo
  # @param provider InPortProvider
  # @param listeners ConnectorListeners type lsitener object list
  # @param buffer CdrBufferBase type buffer
  #
  # @endif
  #
  # InPortPushConnector(ConnectorInfo info, InPortProvider* provider,
  #                    ConnectorListeners listeners, CdrBufferBase* buffer = 0);
  def __init__(self, info, provider, listeners, buffer = 0):
    OpenRTM_aist.InPortConnector.__init__(self, info, buffer)
    self._provider = provider
    self._listeners = listeners

    if buffer:
      self._deleteBuffer = True
    else:
      self._deleteBuffer = False

    if self._buffer == 0:
      self._buffer = self.createBuffer(info)

    if self._buffer == 0 or not self._provider:
      raise

    self._buffer.init(info.properties.getNode("buffer"))
    self._provider.init(info.properties)
    self._provider.setBuffer(self._buffer)
    self._provider.setListener(info, self._listeners)
    
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
  # @brief �ǡ������ɤ߽Ф�
  #
  # �Хåե�����ǡ������ɤ߽Ф���������ɤ߽Ф�����硢����ͤ�
  # PORT_OK �Ȥʤꡢdata ���ɤ߽Ф��줿�ǡ�������Ǽ����롣����ʳ�
  # �ξ��ˤϡ����顼�ͤȤ��� BUFFER_EMPTY, TIMEOUT,
  # PRECONDITION_NOT_MET, PORT_ERROR ���֤���롣
  #
  # @return PORT_OK              ���ｪλ
  #         BUFFER_EMPTY         �Хåե��϶��Ǥ���
  #         TIMEOUT              �����ॢ���Ȥ���
  #         PRECONDITION_NOT_MET ���������������ʤ�
  #         PORT_ERROR           ����¾�Υ��顼
  #
  # @else
  #
  # @brief Reading data
  #
  # This function reads data from the buffer. If data is read
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
    self._rtcout.RTC_TRACE("read()")

    ##
    # buffer returns
    #   BUFFER_OK
    #   BUFFER_EMPTY
    #   TIMEOUT
    #   PRECONDITION_NOT_MET
    #
    if not self._buffer:
      return self.PRECONDITION_NOT_MET

    if type(data) == list:
      ret = self._buffer.read(data)
    else:
      tmp = [data]
      ret = self._buffer.read(tmp)
            
            
    if ret == OpenRTM_aist.BufferStatus.BUFFER_OK:
      return self.PORT_OK

    elif ret == OpenRTM_aist.BufferStatus.BUFFER_EMPTY:
      return self.BUFFER_EMPTY

    elif ret == OpenRTM_aist.BufferStatus.TIMEOUT:
      return self.BUFFER_TIMEOUT

    elif ret == OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET:
      return self.PRECONDITION_NOT_MET
    
    return self.PORT_ERROR
        

  ##
  # @if jp
  # @brief ��³���
  #
  # consumer, publisher, buffer �����Ρ��������롣
  #
  # @return PORT_OK
  #
  # @else
  #
  # @brief disconnect
  #
  # This operation destruct and delete the consumer, the publisher
  # and the buffer.
  #
  # @return PORT_OK
  #
  # @endif
  #
  # virtual ReturnCode disconnect();
  def disconnect(self):
    self._rtcout.RTC_TRACE("disconnect()")
    self.onDisconnect()
    # delete consumer
    if self._provider:
      cfactory = OpenRTM_aist.InPortProviderFactory.instance()
      cfactory.deleteObject(self._provider)

    self._provider = 0

    # delete buffer
    if self._buffer and self._deleteBuffer == True:
      bfactory = OpenRTM_aist.CdrBufferFactory.instance()
      bfactory.deleteObject(self._buffer)
    
    self._buffer = 0
    
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
  def deactivate(self):  # do nothing
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
  # virtual CdrBufferBase* createBuffer(Profile& profile);
  def createBuffer(self, profile):
    buf_type = profile.properties.getProperty("buffer_type","ring_buffer")
    return OpenRTM_aist.CdrBufferFactory.instance().createObject(buf_type)


  ##
  # @if jp
  # @brief �ǡ����ν񤭽Ф�
  #
  # �Хåե��˥ǡ�����񤭽Ф�������˽񤭽Ф�����硢����ͤ�
  # BUFFER_OK �Ȥʤ롣����ʳ��ξ��ˤϡ����顼�ͤȤ��� BUFFER_FULL,TIMEOUT
  # PRECONDITION_NOT_MET, BUFFER_ERROR ���֤���롣
  #
  # @return BUFFER_OK              ���ｪλ
  #         BUFFER_FULL         �Хåե��Ϥ��äѤ��Ǥ���
  #         TIMEOUT              �����ॢ���Ȥ���
  #         PRECONDITION_NOT_MET ���������������ʤ�
  #         BUFFER_ERROR           ����¾�Υ��顼
  #
  # @else
  #
  # @brief Reading data
  #
  # This function write data to the buffer. If data is write
  # properly, this function will return BUFFER_OK return code. Except
  # normal return, BUFFER_FULL, TIMEOUT, PRECONDITION_NOT_MET and
  # BUFFER_ERROR will be returned as error codes.
  #  
  # @return BUFFER_OK            Normal return
  #         BUFFER_FULL          Buffer full
  #         TIMEOUT              Timeout
  #         PRECONDITION_NOT_MET Preconditin not met
  #         BUFFER_ERROR           Other error
  #
  # @endif
  #
  # ReturnCode write(const OpenRTM::CdrData& data);
  def write(self, data):
    if not self._dataType:
      return OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET

    _data = None
    # CDR -> (conversion) -> data
    if self._endian is not None:
      _data = cdrUnmarshal(any.to_any(self._dataType).typecode(),data,self._endian)

    else:
      self._rtcout.RTC_ERROR("unknown endian from connector")
      return OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET

    return self._buffer.write(_data)
        
    
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
