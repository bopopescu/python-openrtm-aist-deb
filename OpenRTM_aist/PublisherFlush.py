#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  PublisherFlush.py
# @brief PublisherFlush class
# @date  $Date: 2007/09/06$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import OpenRTM_aist


##
# @if jp
# @class PublisherFlush
# @brief PublisherFlush ���饹
#
# Flush �� Publisher ���饹
# �Хåե���˳�Ǽ����Ƥ���̤�����ǡ������������롣
# �ǡ������Ф��Ԥĥ��󥷥塼�ޤ����Ф���¦��Ʊ������åɤ�ư����롣
#
# @else
# @class PublisherFlush
# @brief PublisherFlush class
# @endif
class PublisherFlush(OpenRTM_aist.PublisherBase):
  """
  """



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param consumer �ǡ������Ф��Ԥĥ��󥷥塼��
  # @param property ��Publisher�ζ�ư�����������ꤷ��Property���֥�������
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self):
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("PublisherFlush")
    self._consumer  = None
    self._active    = False
    self._profile   = None # ConnectorInfo
    self._listeners = None # ConnectorListeners
    self._retcode   = self.PORT_OK

  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
  # ����Publisher���˴�����ݤˡ�PublisherFactory�ˤ��ƤӽФ���롣
  #
  # @param self
  #
  # @else
  # @brief Destructor
  # @endif
  def __del__(self):
    # "consumer" should be deleted in the Connector
    self._rtcout.RTC_TRACE("~PublisherFlush()")
    self._consumer = None
    return

  ##
  # @if jp
  # @brief �����
  #
  # ���Υ��饹�Υ��֥������Ȥ���Ѥ���Τ���Ω����ɬ�����δؿ���Ƥ�
  # �Ф�ɬ�פ����롣������������ PublisherFlush �ϸ����ǽ���������
  # ��᡼��������ʤ���
  #    
  # @param property ��Publisher�ζ�ư�����������ꤷ��Property���֥�������
  # @return ReturnCode PORT_OK ���ｪλ
  #                    INVALID_ARGS Properties ���������ͤ�ޤ�
  #
  # @else
  # @brief initialization
  #
  # This function have to be called before using this class object.
  # However, this PublisherFlush class has no parameters to be initialized.
  #
  # @param property Property objects that includes the control information
  #                 of this Publisher
  # @return ReturnCode PORT_OK normal return
  #                    INVALID_ARGS Properties with invalid values.
  # @endif
  #
  # virtual ReturnCode init(coil::Properties& prop);
  def init(self, prop):
    self._rtcout.RTC_TRACE("init()")
    return self.PORT_OK;

  ##
  # @if jp
  # @brief InPort���󥷥塼�ޤΥ��å�
  #
  # ���δؿ��Ǥϡ����� Publisher �˴�Ϣ�դ����륳�󥷥塼�ޤ򥻥åȤ��롣
  # ���󥷥塼�ޥ��֥������Ȥ��̥�ݥ��󥿤ξ�硢INVALID_ARGS���֤���롣
  # ����ʳ��ξ��ϡ�PORT_OK ���֤���롣
  #
  # @param consumer Consumer �ؤΥݥ���
  # @return ReturnCode PORT_OK ���ｪλ
  #                    INVALID_ARGS �������������ͤ��ޤޤ�Ƥ���
  #
  # @else
  # @brief Store InPort consumer
  #
  # This operation sets a consumer that is associated with this
  # object. If the consumer object is NULL, INVALID_ARGS will be
  # returned.
  #
  # @param consumer A pointer to a consumer object.
  # @return ReturnCode PORT_OK normal return
  #                    INVALID_ARGS given argument has invalid value
  #
  # PublisherFlush::setConsumer(InPortConsumer* consumer)
  def setConsumer(self, consumer):
    self._rtcout.RTC_TRACE("setConsumer()")
    if not consumer:
      return self.INVALID_ARGS

    self._consumer = consumer

    return self.PORT_OK

  ##
  # @if jp
  # @brief �Хåե��Υ��å�
  # 
  # PublisherFlush�Ǥϡ��Хåե�����Ѥ��ʤ����ᡢ�����ʤ����
  # PORT_OK ���֤���
  #
  # @param buffer CDR�Хåե�
  # @return PORT_OK ���ｪλ
  #
  # @else
  # @brief Setting buffer pointer
  #
  # Since PublisherFlush does not use any buffers, This function
  # always returns PORT_OK.
  #
  # @param buffer CDR buffer
  # @return PORT_OK
  #
  # @endif
  #
  # PublisherBase::ReturnCode PublisherFlush::setBuffer(CdrBufferBase* buffer)
  def setBuffer(self, buffer):
    self._rtcout.RTC_TRACE("setBuffer()")
    return self.PORT_OK

  ##
  # @if jp
  # @brief �ꥹ�ʤ����ꤹ�롣
  #
  # Publisher ���Ф��ƥꥹ�ʥ��֥������� ConnectorListeners �����ꤹ�롣
  # �Ƽ�ꥹ�ʥ��֥������Ȥ�ޤ� ConnectorListeners �򥻥åȤ��뤳�Ȥǡ�
  # �Хåե����ɤ߽񤭡��ǡ��������������ˤ����Υꥹ�ʤ򥳡��뤹�롣
  # ConnectorListeners ���֥������Ȥν�ͭ���ϥݡ��Ȥޤ��� RTObject ������
  # Publisher ������� ConnectorListeners �Ϻ������뤳�ȤϤʤ���
  # ConnectorListeners ���̥�ݥ��󥿤ξ�� INVALID_ARGS ���֤���
  #
  # @param info ConnectorProfile ������벽�������֥������� ConnectorInfo
  # @param listeners �ꥹ�ʤ�¿���ݻ����� ConnectorListeners ���֥�������
  # @return PORT_OK      ���ｪλ
  #         INVALID_ARGS �����ʰ���
  # @else
  # @brief Set the listener. 
  #
  # This function sets ConnectorListeners listener object to the
  # Publisher. By setting ConnectorListeners containing various
  # listeners objects, these listeners are called at the time of
  # reading and writing of a buffer, and transmission of data
  # etc. Since the ownership of the ConnectorListeners object is
  # owned by Port or RTObject, the Publisher never deletes the
  # ConnectorListeners object. If the given ConnectorListeners'
  # pointer is NULL, this function returns INVALID_ARGS.
  #
  # @param info ConnectorInfo that is localized object of ConnectorProfile
  # @param listeners ConnectorListeners that holds various listeners
  # @return PORT_OK      Normal return
  #         INVALID_ARGS Invalid arguments
  # @endif
  #
  # virtual ::RTC::DataPortStatus::Enum
  # setListener(ConnectorInfo& info,
  #             RTC::ConnectorListeners* listeners);
  def setListener(self, info, listeners):
    self._rtcout.RTC_TRACE("setListeners()")
    
    if not listeners:
      self._rtcout.RTC_ERROR("setListeners(listeners == 0): invalid argument")
      return self.INVALID_ARGS

    self._profile = info
    self._listeners = listeners

    return self.PORT_OK

  ##
  # @if jp
  # @brief �ǡ�����񤭹���
  #
  # Publisher ���ݻ����륳�󥷥塼�ޤ��Ф��ƥǡ�����񤭹��ࡣ����
  # ���塼�ޡ��ꥹ������Ŭ�ڤ����ꤵ��Ƥ��ʤ�����Publisher ���֥���
  # ���Ȥ����������������Ƥ��ʤ���硢���δؿ���ƤӽФ��ȥ��顼����
  # �� PRECONDITION_NOT_MET ���֤��졢���󥷥塼�ޤؤν񤭹���������
  # ��ϰ��ڹԤ��ʤ���
  #
  # ���󥷥塼�ޤؤν񤭹��ߤ��Ф��ơ����󥷥塼�ޤ��ե���֡�����
  # ���塼�ޤΥ��顼�����󥷥塼�ޤؤν񤭹��ߤ������ॢ���Ȥ������
  # �ˤϤ��줾�졢���顼������ SEND_FULL, SEND_ERROR, SEND_TIMEOUT
  # ���֤���롣
  #
  # �����ʳ��Υ��顼�ξ�硢PORT_ERROR ���֤���롣
  # 
  #
  # @param data �񤭹���ǡ��� 
  # @param sec �����ॢ���Ȼ���
  # @param nsec �����ॢ���Ȼ���
  #
  # @return PORT_OK             ���ｪλ
  #         PRECONDITION_NO_MET consumer, buffer, listener����Ŭ�ڤ�����
  #                             ����Ƥ��ʤ��������Υ��֥������Ȥλ������
  #                             ���������ʤ���硣
  #         SEND_FULL           �����褬�ե����
  #         SEND_TIMEOUT        �����褬�����ॢ���Ȥ���
  #         CONNECTION_LOST     ��³�����Ǥ��줿���Ȥ��Τ�����
  #
  # @else
  # @brief Write data 
  #
  # This function writes data into the consumer associated with
  # this Publisher. If this function is called without initializing
  # correctly such as a consumer, listeners, etc., error code
  # PRECONDITION_NOT_MET will be returned and no operation of the
  # writing to the consumer etc. will be performed.
  #
  # When publisher writes data to the buffer, if the consumer
  # returns full-status, returns error, is returned with timeout,
  # error codes BUFFER_FULL, BUFFER_ERROR and BUFFER_TIMEOUT will
  # be returned respectively.
  #
  # In other cases, PROT_ERROR will be returned.
  #
  # @param data Data to be wrote to the buffer
  # @param sec Timeout time in unit seconds
  # @param nsec Timeout time in unit nano-seconds
  # @return PORT_OK             Normal return
  #         PRECONDITION_NO_MET Precondition does not met. A consumer,
  #                             a buffer, listenes are not set properly.
  #         SEND_FULL           Data was sent but full-status returned
  #         SEND_TIMEOUT        Data was sent but timeout occurred
  #         CONNECTION_LOST     detected that the connection has been lost
  #
  # @endif
  #
  ## PublisherBase::ReturnCode PublisherFlush::write(const cdrMemoryStream& data,
  ##                                                 unsigned long sec,
  ##                                                 unsigned long usec)
  def write(self, data, sec, usec):
    self._rtcout.RTC_PARANOID("write()")
    if not self._consumer or not self._listeners:
      return self.PRECONDITION_NOT_MET

    if self._retcode == self.CONNECTION_LOST:
      self._rtcout.RTC_DEBUG("write(): connection lost.")
      return self._retcode

    self.onSend(data)

    self._retcode = self._consumer.put(data)

    if self._retcode == self.PORT_OK:
      self.onReceived(data)
      return self._retcode
    elif self._retcode == self.PORT_ERROR:
      self.onReceiverError(data)
      return self._retcode
    elif self._retcode == self.SEND_FULL:
      self.onReceiverFull(data)
      return self._retcode
    elif self._retcode == self.SEND_TIMEOUT:
      self.onReceiverTimeout(data)
      return self._retcode
    elif self._retcode == self.CONNECTION_LOST:
      self.onReceiverTimeout(data)
      return self._retcode
    elif self._retcode == self.UNKNOWN_ERROR:
      self.onReceiverError(data)
      return self._retcode
    else:
      self.onReceiverError(data)
      return self._retcode

    return self._retcode


  ##
  # @if jp
  #
  # @brief �����ƥ��ֲ���ǧ
  # 
  # Publisher �ϥǡ����ݡ��Ȥ�Ʊ������ activate/deactivate ����롣
  # activate() / deactivate() �ؿ��ˤ�äơ������ƥ��־��֤��󥢥��ƥ�
  # �־��֤��ڤ��ؤ�롣���δؿ��ˤ�ꡢ���ߥ����ƥ��־��֤����󥢥�
  # �ƥ��־��֤����ǧ���뤳�Ȥ��Ǥ��롣
  #
  # @return ���ֳ�ǧ���(�����ƥ��־���:true���󥢥��ƥ��־���:false)
  #
  # @else
  #
  # @brief If publisher is active state
  # 
  # A Publisher can be activated/deactivated synchronized with the
  # data port.  The active state and the non-active state are made
  # transition by the "activate()" and the "deactivate()" functions
  # respectively. This function confirms if the publisher is in
  # active state.
  #
  # @return Result of state confirmation
  #         (Active state:true, Inactive state:false)
  #
  # @endif
  #
  ## bool PublisherFlush::isActive()
  def isActive(self):
    return self._active


  ##
  # @if jp
  # @brief �����ƥ��ֲ�����
  #
  # Publisher �򥢥��ƥ��ֲ����롣���δؿ���ƤӽФ����Ȥˤ�ꡢ
  # Publisher�����ġ��ǡ������������륹��åɤ�ư��򳫻Ϥ��롣���
  # �����Ԥ��Ƥ��ʤ��ʤɤˤ�ꡢ���������������ʤ���硢���顼����
  # �� PRECONDITION_NOT_MET ���֤���
  #
  # @return PORT_OK ���ｪλ
  #         PRECONDITION_NOT_MET ���������������ʤ�
  #
  # @else
  # @brief activation
  #
  # This function activates the publisher. By calling this
  # function, this publisher starts the thread that pushes data to
  # InPort. If precondition such as initialization process and so
  # on is not met, the error code PRECONDITION_NOT_MET is returned.
  #
  # @return PORT_OK normal return
  #         PRECONDITION_NOT_MET precondition is not met
  #
  # @endif
  #
  ## PublisherBase::ReturnCode PublisherFlush::activate()
  def activate(self):
    if self._active:
      return self.PRECONDITION_NOT_MET

    self._active = True

    return self.PORT_OK

  ##
  # @if jp
  # @brief �󥢥��ƥ��ֲ�����
  #
  # Publisher ���󥢥��ƥ��ֲ����롣���δؿ���ƤӽФ����Ȥˤ�ꡢ
  # Publisher�����ġ��ǡ������������륹��åɤ�ư�����ߤ��롣���
  # �����Ԥ��Ƥ��ʤ��ʤɤˤ�ꡢ���������������ʤ���硢���顼����
  # �� PRECONDITION_NOT_MET ���֤���
  #
  # @return PORT_OK ���ｪλ
  #         PRECONDITION_NOT_MET ���������������ʤ�
  #
  # @else
  # @brief deactivation
  #
  # This function deactivates the publisher. By calling this
  # function, this publisher stops the thread that pushes data to
  # InPort. If precondition such as initialization process and so
  # on is not met, the error code PRECONDITION_NOT_MET is returned.
  #
  # @return PORT_OK normal return
  #         PRECONDITION_NOT_MET precondition is not met
  #
  # @endif
  #
  ## PublisherBase::ReturnCode PublisherFlush::deactivate()
  def deactivate(self):
    if not self._active:
      return self.PRECONDITION_NOT_MET

    self._active = False

    return self.PORT_OK

  ##
  # @if jp
  # @brief ON_SEND�Υꥹ�ʤ����Τ��롣 
  # @param data cdrMemoryStream
  # @else
  # @brief Notify an ON_SEND event to listners
  # @param data cdrMemoryStream
  # @endif
  #
  # inline void onSend(const cdrMemoryStream& data)
  def onSend(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_SEND].notify(self._profile, data)
    return

  ##
  # @if jp
  # @brief ON_RECEIVED�Υꥹ�ʤ����Τ��롣 
  # @param data cdrMemoryStream
  # @else
  # @brief Notify an ON_RECEIVED event to listeners
  # @param data cdrMemoryStream
  # @endif
  #
  # inline void onReceived(const cdrMemoryStream& data)
  def onReceived(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED].notify(self._profile, data)
    return

  ##
  # @if jp
  # @brief ON_RECEIVER_FULL�Υꥹ�ʤ����Τ��롣 
  # @param data cdrMemoryStream
  # @else
  # @brief Notify an ON_RECEIVER_FULL event to listeners
  # @param data cdrMemoryStream
  # @endif
  #
  # inline void onReceiverFull(const cdrMemoryStream& data)
  def onReceiverFull(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_FULL].notify(self._profile, data)
    return

  ##
  # @if jp
  # @brief ON_RECEIVER_TIMEOUT�Υꥹ�ʤ����Τ��롣 
  # @param data cdrMemoryStream
  # @else
  # @brief Notify an ON_RECEIVER_TIMEOUT event to listeners
  # @param data cdrMemoryStream
  # @endif
  #
  # inline void onReceiverTimeout(const cdrMemoryStream& data)
  def onReceiverTimeout(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_TIMEOUT].notify(self._profile, data)
    return

  ##
  # @if jp
  # @brief ON_RECEIVER_ERROR�Υꥹ�ʤ����Τ��롣 
  # @param data cdrMemoryStream
  # @else
  # @brief Notify an ON_RECEIVER_ERROR event to listeners
  # @param data cdrMemoryStream
  # @endif
  #
  # inline void onReceiverError(const cdrMemoryStream& data)
  def onReceiverError(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVER_ERROR].notify(self._profile, data)
    return
  

def PublisherFlushInit():
  OpenRTM_aist.PublisherFactory.instance().addFactory("flush",
                                                      OpenRTM_aist.PublisherFlush,
                                                      OpenRTM_aist.Delete)
