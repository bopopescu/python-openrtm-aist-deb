#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file OutPortPushConnector.py
# @brief Push type connector class
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
# @class OutPortPushConnector
# @brief OutPortPushConnector ���饹
#
# OutPort �� push ���ǡ����ե��Τ���� Connector ���饹�����Υ���
# �������Ȥϡ���³���� dataflow_type �� push �����ꤵ�줿��硢
# OutPort �ˤ�ä���������ͭ���졢InPortPushConnector ���Фˤʤäơ�
# �ǡ����ݡ��Ȥ� push ���Υǡ����ե���¸����롣��Ĥ���³���Ф��ơ�
# ��ĤΥǡ������ȥ꡼����󶡤���ͣ��� Connector ���б����롣
# Connector �� ��³������������� UUID ������ ID �ˤ����̤���롣
#
# OutPortPushConnector �ϰʲ��λ��ĤΥ��֥������Ȥ��ͭ���������롣
#
# - InPortConsumer
# - Buffer
# - Publisher
#
# OutPort �˽񤭹��ޤ줿�ǡ����� OutPortPushConnector::write() ����
# ���졢Connector �� Publisher �˥ǡ�����񤭹��ࡣPublisher �Ϥ���
# �����˽��äƥǡ����� Buffer ��������� InPortConsumer ���Ф���
# push ���뤳�Ȥ� InPort �˥ǡ�����ž������롣
#
# @since 1.0.0
#
# @else
# @class OutPortPushConnector
# @brief OutPortPushConnector class
#
# Connector class of OutPort for push type dataflow.  When "push"
# is specified as dataflow_type at the time of establishing
# connection, this object is generated and owned by the OutPort.
# This connector and InPortPushConnector make a pair and realize
# push type dataflow of data ports.  One connector corresponds to
# one connection which provides a data stream.  Connector is
# distinguished by ID of the UUID that is generated at establishing
# connection.
#
# OutPortPushConnector owns and manages the following objects.
#
# - InPortConsumer
# - Buffer
# - Publisher
#
# @since 1.0.0
#
# Data written into the OutPort is passed to
# OutPortPushConnector::write(), and the connector writes into the
# publisher.  The publisher gets data from the buffer based on the
# policy and it is transferred to InPort by pushing it into the
# InPortConsumer.
#
# @endif
#
class OutPortPushConnector(OpenRTM_aist.OutPortConnector):
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # OutPortPushConnector �Υ��󥹥ȥ饯���ϥ��֥��������������˲���
  # ������ˤȤ롣ConnectorInfo ����³�����ޤߡ����ξ���˽����ѥ�
  # ��å����Хåե������������롣InPort ���󥿡��ե��������Ф���
  # ���󥷥塼�ޥ��֥������ȤؤΥݥ��󥿤��ꡢ��ͭ������ĤΤǡ�
  # OutPortPushConnector �� InPortConsumer �β�����Ǥ����ġ��Ƽ磻
  # �٥�Ȥ��Ф��륳����Хå��������󶡤��� ConnectorListeners ���
  # ����Ŭ�ڤʥ����ߥ󥰤ǥ�����Хå���ƤӽФ����ǡ����Хåե�����
  # �� OutPortBase �����󶡤������Ϥ��Υݥ��󥿤��롣
  #
  # @param info ConnectorInfo
  # @param consumer InPortConsumer
  # @param listeners ConnectorListeners ���Υꥹ�ʥ��֥������ȥꥹ��
  # @param buffer CdrBufferBase ���ΥХåե�
  #
  # @else
  # @brief Constructor
  #
  # OutPortPushConnector's constructor is given the following
  # arguments.  According to ConnectorInfo which includes
  # connection information, a publisher and a buffer are created.
  # It is also given a pointer to the consumer object for the
  # InPort interface.  The owner-ship of the pointer is owned by
  # this OutPortPushConnector, it has responsibility to destruct
  # the InPortConsumer.  OutPortPushConnector also has
  # ConnectorListeners to provide event callback mechanisms, and
  # they would be called at the proper timing.  If data buffer is
  # given by OutPortBase, the pointer to the buffer is also given
  # as arguments.
  #
  # @param info ConnectorInfo
  # @param consumer InPortConsumer
  # @param listeners ConnectorListeners type lsitener object list
  # @param buffer CdrBufferBase type buffer
  #
  # @endif
  #
  # OutPortPushConnector(ConnectorInfo info,
  #                      InPortConsumer* consumer,
  #                      ConnectorListeners& listeners,
  #                      CdrBufferBase* buffer = 0);
  def __init__(self, info, consumer, listeners, buffer = 0):
    OpenRTM_aist.OutPortConnector.__init__(self, info)

    self._buffer = buffer
    self._consumer = consumer
    self._listeners = listeners

    # publisher/buffer creation. This may throw std::bad_alloc;
    self._publisher = self.createPublisher(info)
    if not self._buffer:
      self._buffer = self.createBuffer(info)


    if not self._publisher or not self._buffer or not self._consumer:
      raise

    if self._publisher.init(info.properties) != self.PORT_OK:
      raise
        
    if self._profile.properties.hasKey("serializer"):
      endian = self._profile.properties.getProperty("serializer.cdr.endian")
      if not endian:
        self._rtcout.RTC_ERROR("write(): endian is not set.")
        raise
        
      endian = OpenRTM_aist.split(endian, ",") # Maybe endian is ["little","big"]
      endian = OpenRTM_aist.normalize(endian) # Maybe self._endian is "little" or "big"
      if endian == "little":
        self._endian = True
      elif endian == "big":
        self._endian = False
      else:
        self._endian = None

    else:
      self._endian = True # little endian

    self._buffer.init(info.properties.getNode("buffer"))
    self._consumer.init(info.properties)
    self._publisher.setConsumer(self._consumer)
    self._publisher.setBuffer(self._buffer)
    self._publisher.setListener(self._profile, self._listeners)

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
  # @brief �ǡ����ν񤭹���
  #
  # Publisher���Ф��ƥǡ�����񤭹��ߡ�����ˤ���б�����InPort�إǡ�
  # ����ž������롣���ｪλ������� PORT_OK ���֤���롣����ʳ���
  # ��硢���顼�ͤȤ��ơ�CONNECTION_LOST, BUFFER_FULL,
  # BUFFER_ERROR, PORT_ERROR, BUFFER_TIMEOUT, PRECONDITION_NO_MET ��
  # �֤���롣
  #
  # @return PORT_OK              ���ｪλ
  #         CONNECTION_LOST      ��³�����Ȥ���
  #         BUFFER_FULL          �Хåե������դǤ���
  #         BUFFER_ERROR         �Хåե����顼
  #         BUFFER_TIMEOUT       �Хåե��ؤν񤭹��ߤ������ॢ���Ȥ���
  #         PRECONDITION_NOT_MET ���������������ʤ�
  #         PORT_ERROR           ����¾�Υ��顼
  #
  # @else
  #
  # @brief Writing data
  #
  # This operation writes data into publisher and then the data
  # will be transferred to correspondent InPort. If data is written
  # properly, this function will return PORT_OK return code. Except
  # normal return, CONNECTION_LOST, BUFFER_FULL, BUFFER_ERROR,
  # PORT_ERROR, BUFFER_TIMEOUT and PRECONDITION_NO_MET will be
  # returned as error codes.
  #  
  # @return PORT_OK              Normal return
  #         CONNECTION_LOST      Connectin lost
  #         BUFFER_FULL          Buffer full
  #         BUFFER_ERROR         Buffer error
  #         BUFFER_TIMEOUT       Timeout
  #         PRECONDITION_NOT_MET Precondition not met
  #         PORT_ERROR           Other error
  #
  # @endif
  #
  # template<class DataType>
  # virtual ReturnCode write(const DataType& data);
  def write(self, data):
    self._rtcout.RTC_TRACE("write()")

    # data -> (conversion) -> CDR stream
    cdr_data = None
    if self._endian is not None:
      cdr_data = cdrMarshal(any.to_any(data).typecode(), data, self._endian)
    else:
      self._rtcout.RTC_ERROR("write(): endian %s is not support.",self._endian)
      return self.UNKNOWN_ERROR

    return self._publisher.write(cdr_data, 0, 0)


  ##
  # @if jp
  # @brief ��³���
  #
  # consumer, publisher, buffer �����Ρ��������롣
  #
  # @else
  #
  # @brief disconnect
  #
  # This operation destruct and delete the consumer, the publisher
  # and the buffer.
  #
  # @endif
  #
  # virtual ReturnCode disconnect();
  def disconnect(self):
    self._rtcout.RTC_TRACE("disconnect()")
    self.onDisconnect()
    # delete publisher
    if self._publisher:
      self._rtcout.RTC_DEBUG("delete publisher")
      pfactory = OpenRTM_aist.PublisherFactory.instance()
      pfactory.deleteObject(self._publisher)

    self._publisher = 0
    
    # delete consumer
    if self._consumer:
      self._rtcout.RTC_DEBUG("delete consumer")
      cfactory = OpenRTM_aist.InPortConsumerFactory.instance()
      cfactory.deleteObject(self._consumer)

    self._consumer = 0

    # delete buffer
    if self._buffer:
      self._rtcout.RTC_DEBUG("delete buffer")
      bfactory = OpenRTM_aist.CdrBufferFactory.instance()
      bfactory.deleteObject(self._buffer)

    self._buffer = 0
    self._rtcout.RTC_TRACE("disconnect() done")

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
  # virtual void activate();
  def activate(self):
    self._publisher.activate()
    return


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
  # virtual void deactivate();
  def deactivate(self):
    self._publisher.deactivate()
    return

    
  ##
  # @if jp
  # @brief Buffer ���������
  #
  # Connector ���ݻ����Ƥ��� Buffer ���֤�
  #
  # @else
  # @brief Getting Buffer
  #
  # This operation returns this connector's buffer
  #
  # @endif
  #
  # virtual CdrBufferBase* getBuffer();
  def getBuffer(self):
    return self._buffer


  ##
  # @if jp
  # @brief Publisher������
  #
  # Ϳ����줿��³����˴�Ť��ѥ֥�å�����������롣
  #
  # @param info ��³����
  # @return �ѥ֥�å���ؤΥݥ���
  #
  # @else
  # @brief create buffer
  #
  # This function creates a publisher based on given information.
  #
  # @param info Connector information
  # @return The poitner to the publisher
  #
  # @endif
  #
  # virtual PublisherBase* createPublisher(ConnectorInfo& info);
  def createPublisher(self, info):
    pub_type = info.properties.getProperty("subscription_type","flush")
    pub_type = OpenRTM_aist.normalize([pub_type])
    return OpenRTM_aist.PublisherFactory.instance().createObject(pub_type)


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
  # virtual CdrBufferBase* createBuffer(ConnectorInfo& info);
  def createBuffer(self, info):
    buf_type = info.properties.getProperty("buffer_type",
                                           "ring_buffer")

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
