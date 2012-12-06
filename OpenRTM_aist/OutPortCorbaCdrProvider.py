#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  OutPortCorbaProvider.py
# @brief OutPortCorbaProvider class
# @date  $Date: 2008-01-14 07:52:40 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2009
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

import sys
from omniORB import *
from omniORB import any

import OpenRTM_aist
import OpenRTM__POA,OpenRTM

##
# @if jp
# @class OutPortCorbaCdrProvider
# @brief OutPortCorbaCdrProvider ���饹
#
# OutPortProvider 
#
# �ǡ���ž���� CORBA �� OpenRTM::OutPortCdr ���󥿡��ե����������Ѥ�
# ����pull ���ǡ����ե�����¸����� OutPort �ץ�Х������饹��
#
# @since 0.4.0
#
# @else
# @class OutPortCorbaCdrProvider
# @brief OutPortCorbaCdrProvider class
#
# The OutPort provider class which uses the OpenRTM::OutPortCdr
# interface in CORBA for data transfer and realizes a pull-type
# dataflow.
#
# @since 0.4.0
#
# @endif
#
class OutPortCorbaCdrProvider(OpenRTM_aist.OutPortProvider,
                              OpenRTM__POA.OutPortCdr):
  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param buffer �����ץ�Х����˳�����Ƥ�Хåե����֥�������
  #
  # @else
  # @brief Constructor
  #
  # Constructor
  #
  # @param buffer Buffer object that is assigned to this provider
  #
  # @endif
  #
  def __init__(self):
    OpenRTM_aist.OutPortProvider.__init__(self)
    self.setInterfaceType("corba_cdr")

    # ConnectorProfile setting
    self._objref = self._this()
    
    self._buffer = None

    # set outPort's reference
    orb = OpenRTM_aist.Manager.instance().getORB()

    self._properties.append(OpenRTM_aist.NVUtil.newNV("dataport.corba_cdr.outport_ior",
                                                      orb.object_to_string(self._objref)))
    self._properties.append(OpenRTM_aist.NVUtil.newNV("dataport.corba_cdr.outport_ref",
                                                      self._objref))

    self._listeners = None
    self._connector = None
    self._profile   = None
    return


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
  #
  # @else
  # @brief Destructor
  #
  # Destructor
  #
  # @endif
  #
  def __del__(self):
    oid = self._default_POA().servant_to_id(self)
    self._default_POA().deactivate_object(oid)
    return


  ##
  # @if jp
  # @brief ��������
  #
  # InPortConsumer�γƼ������Ԥ����������饹�Ǥϡ�Ϳ����줿
  # Properties����ɬ�פʾ����������ƳƼ������Ԥ������� init() ��
  # ���ϡ�OutPortProvider����ľ�太��ӡ���³���ˤ��줾��ƤФ���
  # ǽ�������롣�������äơ����δؿ���ʣ����ƤФ�뤳�Ȥ����ꤷ�Ƶ�
  # �Ҥ����٤��Ǥ��롣
  # 
  # @param prop �������
  #
  # @else
  #
  # @brief Initializing configuration
  #
  # This operation would be called to configure in initialization.
  # In the concrete class, configuration should be performed
  # getting appropriate information from the given Properties data.
  # This function might be called right after instantiation and
  # connection sequence respectivly.  Therefore, this function
  # should be implemented assuming multiple call.
  #
  # @param prop Configuration information
  #
  # @endif
  #
  # virtual void init(coil::Properties& prop);
  def init(self, prop):
    pass


  ##
  # @if jp
  # @brief �Хåե��򥻥åȤ���
  #
  # OutPortProvider���ǡ�������Ф��Хåե��򥻥åȤ��롣
  # ���Ǥ˥��åȤ��줿�Хåե��������硢�����ΥХåե��ؤ�
  # �ݥ��󥿤��Ф��ƾ�񤭤���롣
  # OutPortProvider�ϥХåե��ν�ͭ�����ꤷ�Ƥ��ʤ��Τǡ�
  # �Хåե��κ���ϥ桼������Ǥ�ǹԤ�ʤ���Фʤ�ʤ���
  #
  # @param buffer OutPortProvider���ǡ�������Ф��Хåե��ؤΥݥ���
  #
  # @else
  # @brief Setting outside buffer's pointer
  #
  # A pointer to a buffer from which OutPortProvider retrieve data.
  # If already buffer is set, previous buffer's pointer will be
  # overwritten by the given pointer to a buffer.  Since
  # OutPortProvider does not assume ownership of the buffer
  # pointer, destructor of the buffer should be done by user.
  # 
  # @param buffer A pointer to a data buffer to be used by OutPortProvider
  #
  # @endif
  #
  # virtual void setBuffer(BufferBase<cdrMemoryStream>* buffer);
  def setBuffer(self, buffer):
    self._buffer = buffer
    return


  ##
  # @if jp
  # @brief �ꥹ�ʤ����ꤹ�롣
  #
  # OutPort �ϥǡ������������ˤ�����Ƽ磻�٥�Ȥ��Ф�������Υꥹ��
  # ���֥������Ȥ򥳡��뤹�륳����Хå��������󶡤��롣�ܺ٤�
  # ConnectorListener.h �� ConnectorDataListener, ConnectorListener
  # ���򻲾ȤΤ��ȡ�OutPortCorbaCdrProvider �Ǥϡ��ʲ��Υ�����Хå�
  # ���󶡤���롣
  # 
  # - ON_BUFFER_READ
  # - ON_SEND
  # - ON_BUFFER_EMPTY
  # - ON_BUFFER_READ_TIMEOUT
  # - ON_SENDER_EMPTY
  # - ON_SENDER_TIMEOUT
  # - ON_SENDER_ERROR
  #
  # @param info ��³����
  # @param listeners �ꥹ�ʥ��֥�������
  #
  # @else
  # @brief Set the listener. 
  #
  # OutPort provides callback functionality that calls specific
  # listener objects according to the events in the data publishing
  # process. For details, see documentation of
  # ConnectorDataListener class and ConnectorListener class in
  # ConnectorListener.h. In this OutPortCorbaCdrProvider provides
  # the following callbacks.
  # 
  # - ON_BUFFER_READ
  # - ON_SEND
  # - ON_BUFFER_EMPTY
  # - ON_BUFFER_READ_TIMEOUT
  # - ON_SENDER_EMPTY
  # - ON_SENDER_TIMEOUT
  # - ON_SENDER_ERROR
  #
  # @param info Connector information
  # @param listeners Listener objects
  #
  # @endif
  #
  # virtual void setListener(ConnectorInfo& info,
  #                          ConnectorListeners* listeners);
  def setListener(self, info, listeners):
    self._profile = info
    self._listeners = listeners
    return


  ##
  # @if jp
  # @brief Connector�����ꤹ�롣
  #
  # OutPort ����³��Ω���� OutPortConnector ���֥������Ȥ�����������
  # ���������֥������ȤΥݥ��󥿤ȶ��ˤ��δؿ���ƤӽФ�����ͭ����
  # OutPort ���ݻ�����Τ� OutPortProvider �� OutPortConnector ���
  # �����ƤϤ����ʤ���
  #
  # @param connector OutPortConnector
  #
  # @else
  # @brief set Connector
  #
  # OutPort creates OutPortConnector object when it establishes
  # connection between OutPort and InPort, and it calls this
  # function with a pointer to the connector object. Since the
  # OutPort has the ownership of this connector, OutPortProvider
  # should not delete it.
  #
  # @param connector OutPortConnector
  #
  # @endif
  #
  # virtual void setConnector(OutPortConnector* connector);
  def setConnector(self, connector):
    self._connector = connector
    return


  ##
  # @if jp
  # @brief [CORBA interface] �Хåե�����ǡ������������
  #
  # ���ꤵ�줿�����Хåե�����ǡ�����������롣
  #
  # @return �����ǡ���
  #
  # @else
  # @brief [CORBA interface] Get data from the buffer
  #
  # Get data from the internal buffer.
  #
  # @return Data got from the buffer.
  #
  # @endif
  #
  # virtual ::OpenRTM::PortStatus get(::OpenRTM::CdrData_out data);
  def get(self):
    self._rtcout.RTC_PARANOID("OutPortCorbaCdrProvider.get()")
    if not self._buffer:
      self.onSenderError()
      return (OpenRTM.UNKNOWN_ERROR, None)

    try:
      if self._buffer.empty():
        self._rtcout.RTC_ERROR("buffer is empty.")
        return (OpenRTM.BUFFER_EMPTY, None)

      cdr = [None]
      ret = self._buffer.read(cdr)

      if ret == OpenRTM_aist.BufferStatus.BUFFER_OK:
        if not cdr:
          self._rtcout.RTC_ERROR("buffer is empty.")
          return (OpenRTM.BUFFER_EMPTY, None)
      
    except:
      self._rtcout.RTC_TRACE(OpenRTM_aist.Logger.print_exception())
      return (OpenRTM.UNKNOWN_ERROR, None)

    return self.convertReturn(ret, cdr[0])
    
  ##
  # @if jp
  # @brief ON_BUFFER_READ �Υꥹ�ʤ����Τ��롣 
  # @param data cdrMemoryStream
  # @else
  # @brief Notify an ON_BUFFER_READ event to listeners
  # @param data cdrMemoryStream
  # @endif
  #
  # inline void onBufferRead(const cdrMemoryStream& data)
  def onBufferRead(self, data):
    if self._listeners and self._profile:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_READ].notify(self._profile, data)
    return

  ##
  # @if jp
  # @brief ON_SEND �Υꥹ�ʤ����Τ��롣 
  # @param data cdrMemoryStream
  # @else
  # @brief Notify an ON_SEND event to listeners
  # @param data cdrMemoryStream
  # @endif
  #
  # inline void onSend(const cdrMemoryStream& data)
  def onSend(self, data):
    if self._listeners and self._profile:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_SEND].notify(self._profile, data)
    return

  ##
  # @if jp
  # @brief ON_BUFFER_EMPTY�Υꥹ�ʤ����Τ��롣 
  # @else
  # @brief Notify an ON_BUFFER_EMPTY event to listeners
  # @endif
  #
  # inline void onBufferEmpty()
  def onBufferEmpty(self):
    if self._listeners and self._profile:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_BUFFER_EMPTY].notify(self._profile)
    return

  ##
  # @if jp
  # @brief ON_BUFFER_READ_TIMEOUT �Υꥹ�ʤ����Τ��롣 
  # @else
  # @brief Notify an ON_BUFFER_READ_TIMEOUT event to listeners
  # @endif
  #
  # inline void onBufferReadTimeout()
  def onBufferReadTimeout(self):
    if self._listeners and self._profile:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_BUFFER_READ_TIMEOUT].notify(self._profile)
    return

  ##
  # @if jp
  # @brief ON_SENDER_EMPTY�Υꥹ�ʤ����Τ��롣 
  # @else
  # @brief Notify an ON_SENDER_EMPTY event to listeners
  # @endif
  #
  # inline void onSenderEmpty()
  def onSenderEmpty(self):
    if self._listeners and self._profile:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_SENDER_EMPTY].notify(self._profile)
    return

  ##
  # @if jp
  # @brief ON_SENDER_TIMEOUT �Υꥹ�ʤ����Τ��롣 
  # @else
  # @brief Notify an ON_SENDER_TIMEOUT event to listeners
  # @endif
  #
  # inline void onSenderTimeout()
  def onSenderTimeout(self):
    if self._listeners and self._profile:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_SENDER_TIMEOUT].notify(self._profile)
    return

  ##
  # @if jp
  # @brief ON_SENDER_ERROR�Υꥹ�ʤ����Τ��롣 
  # @else
  # @brief Notify an ON_SENDER_ERROR event to listeners
  # @endif
  #
  # inline void onSenderError()
  def onSenderError(self):
    if self._listeners and self._profile:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_SENDER_ERROR].notify(self._profile)
    return


  ##
  # @if jp
  # @brief �꥿���󥳡����Ѵ�
  # @else
  # @brief Return codes conversion
  # @endif
  #
  # ::OpenRTM::PortStatus convertReturn(BufferStatus::Enum status,
  #                                     const cdrMemoryStream& data);
  def convertReturn(self, status, data):
    if status == OpenRTM_aist.BufferStatus.BUFFER_OK:
      self.onBufferRead(data)
      self.onSend(data)
      return (OpenRTM.PORT_OK, data)
    
    elif status == OpenRTM_aist.BufferStatus.BUFFER_ERROR:
      self.onSenderError()
      return (OpenRTM.PORT_ERROR, data)
    
    elif status == OpenRTM_aist.BufferStatus.BUFFER_FULL:
      # never come here
      return (OpenRTM.BUFFER_FULL, data)

    elif status == OpenRTM_aist.BufferStatus.BUFFER_EMPTY:
      self.onBufferEmpty()
      self.onSenderEmpty()
      return (OpenRTM.BUFFER_EMPTY, data)

    elif status == OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET:
      self.onSenderError()
      return (OpenRTM.PORT_ERROR, data)
    
    elif status == OpenRTM_aist.BufferStatus.TIMEOUT:
      self.onBufferReadTimeout()
      self.onSenderTimeout()
      return (OpenRTM.BUFFER_TIMEOUT, data)
    
    else:
      return (OpenRTM.UNKNOWN_ERROR, data)
    
    self.onSenderError()
    return (OpenRTM.UNKNOWN_ERROR, data)


def OutPortCorbaCdrProviderInit():
  factory = OpenRTM_aist.OutPortProviderFactory.instance()
  factory.addFactory("corba_cdr",
                     OpenRTM_aist.OutPortCorbaCdrProvider,
                     OpenRTM_aist.Delete)
