#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  PublisherNew.py
# @brief PublisherNew class
# @date  $Date: 2007/09/27 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
 
import threading

import OpenRTM_aist


##
# @if jp
# @class PublisherNew
# @brief PublisherNew ���饹
#
# �Хåե���˿����ǡ�������Ǽ���줿�����ߥ󥰤ǡ����ο����ǡ������������롣
# �ǡ������Х����ߥ󥰤��Ԥĥ��󥷥塼�ޤ����Ф���¦�Ȥϰۤʤ륹��åɤ�
# ư�������˻��ѡ�
# Publisher�ζ�ư�ϡ��ǡ������ФΥ����ߥ󥰤ˤʤ�ޤǥ֥�å����졢
# ���Х����ߥ󥰤����Τ������ȡ�¨�¤˥��󥷥塼�ޤ����н�����ƤӽФ���
#
# @else
# @class PublisherNew
# @brief PublisherNew class
#
# Send new data at timing of when it is stored into the buffer.
# This class is used when operating Consumer that waits for the data send
# timing in different thread from one of the send side.
# Publisher's driven is blocked until the data send timing reaches, if the
# send timing notification is received, the Consumer's send processing will
# be invoked immediately.
#
# @endif
class PublisherNew(OpenRTM_aist.PublisherBase):
  """
  """

  # Policy
  ALL  = 0
  FIFO = 1
  SKIP = 2
  NEW  = 3

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  # �� Publisher �ѿ�������åɤ��������롣
  #
  # @param self
  # @param consumer �ǡ������Ф��Ԥĥ��󥷥塼��
  # @param property ��Publisher�ζ�ư�����������ꤷ��Property���֥�������
  #                 (��Publisher�Ǥ�̤����)
  # @else
  # @brief Constructor
  # @endif
  def __init__(self):
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("PublisherNew")
    self._consumer = None
    self._buffer   = None
    self._task     = None
    self._retcode  = self.PORT_OK
    self._retmutex = threading.RLock()
    self._pushPolicy = self.NEW
    self._skipn      = 0
    self._active     = False
    self._leftskip   = 0
    self._profile    = None
    self._listeners  = None

  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
  #
  # @param self
  #
  # @else
  # @brief Destructor
  #
  # @endif
  def __del__(self):
    self._rtcout.RTC_TRACE("~PublisherNew()")
    if self._task:
      self._task.resume()
      self._task.finalize()

      OpenRTM_aist.PeriodicTaskFactory.instance().deleteObject(self._task)
      del self._task
      self._rtcout.RTC_PARANOID("task deleted.")

    # "consumer" should be deleted in the Connector
    self._consumer = 0
    # "buffer"   should be deleted in the Connector
    self._buffer = 0
    return

  ##
  # @if jp
  # @brief PushPolicy ������
  # @else
  # @brief Setting PushPolicy
  # @endif
  #
  #void PublisherNew::setPushPolicy(const coil::Properties& prop)
  def setPushPolicy(self, prop):
    push_policy = prop.getProperty("publisher.push_policy","new")
    self._rtcout.RTC_DEBUG("push_policy: %s", push_policy)

    push_policy = OpenRTM_aist.normalize([push_policy])

    if push_policy == "all":
      self._pushPolicy = self.ALL

    elif push_policy == "fifo":
      self._pushPolicy = self.FIFO

    elif push_policy == "skip":
      self._pushPolicy = self.SKIP

    elif push_policy == "new":
      self._pushPolicy = self.NEW

    else:
      self._rtcout.RTC_ERROR("invalid push_policy value: %s", push_policy)
      self._pushPolicy = self.NEW
  
    skip_count = prop.getProperty("publisher.skip_count","0")
    self._rtcout.RTC_DEBUG("skip_count: %s", skip_count)

    skipn = [self._skipn]
    ret = OpenRTM_aist.stringTo(skipn, skip_count)
    if ret:
      self._skipn = skipn[0]
    else:
      self._rtcout.RTC_ERROR("invalid skip_count value: %s", skip_count)
      self._skipn = 0

    if self._skipn < 0:
      self._rtcout.RTC_ERROR("invalid skip_count value: %d", self._skipn)
      self._skipn = 0

    return

  ##
  # @if jp
  # @brief Task ������
  # @else
  # @brief Setting Task
  # @endif
  #
  #bool PublisherNew::createTask(const coil::Properties& prop)
  def createTask(self, prop):
    factory = OpenRTM_aist.PeriodicTaskFactory.instance()

    th = factory.getIdentifiers()
    self._rtcout.RTC_DEBUG("available task types: %s", OpenRTM_aist.flatten(th))

    self._task = factory.createObject(prop.getProperty("thread_type", "default"))

    if not self._task:
      self._rtcout.RTC_ERROR("Task creation failed: %s",
                             prop.getProperty("thread_type", "default"))
      return self.INVALID_ARGS

    self._rtcout.RTC_PARANOID("Task creation succeeded.")

    mprop = prop.getNode("measurement")

    # setting task function
    self._task.setTask(self.svc)
    self._task.setPeriod(0.0)
    self._task.executionMeasure(OpenRTM_aist.toBool(mprop.getProperty("exec_time"),
                                                    "enable", "disable", True))
    ecount = [0]
    if OpenRTM_aist.stringTo(ecount, mprop.getProperty("exec_count")):
      self._task.executionMeasureCount(ecount[0])

    self._task.periodicMeasure(OpenRTM_aist.toBool(mprop.getProperty("period_time"),
                                                   "enable", "disable", True))
    pcount = [0]
    if OpenRTM_aist.stringTo(pcount, mprop.getProperty("period_count")):
      self._task.periodicMeasureCount(pcount[0])

    self._task.suspend()
    self._task.activate()
    self._task.suspend()

    return self.PORT_OK

  ##
  # @if jp
  # @brief �����
  #
  # ���Υ��饹�Υ��֥������Ȥ���Ѥ���Τ���Ω����ɬ�����δؿ���Ƥ�
  # �Ф�ɬ�פ����롣�����ˤϡ����Υ��֥������ȤγƼ���������ޤ�
  # Properties ��Ϳ���롣�ǡ�����ץå��夹��ݤΥݥꥷ���Ȥ���
  # publisher.push_policy �򥭡��Ȥ����ͤˡ�all, fifo, skip, new ��
  # �����줫��Ϳ���뤳�Ȥ��Ǥ��롣
  # 
  # �ʲ��Υ��ץ�����Ϳ���뤳�Ȥ��Ǥ��롣
  # 
  # - thread_type: ����åɤΥ����� (ʸ���󡢥ǥե����: default)
  # - publisher.push_policy: Push�ݥꥷ�� (all, fifo, skip, new)
  # - publisher.skip_count: �嵭�ݥꥷ�� skip �ΤȤ��Υ����å׿�
  # - measurement.exec_time: �������¹Ի��ַ�¬ (enable/disable)
  # - measurement.exec_count: �������ؿ��¹Ի��ַ�¬���� (����, ���)
  # - measurement.period_time: �������������ַ�¬ (enable/disable)
  # - measurement.period_count: �������������ַ�¬���� (����, ���)
  #
  # @param property ��Publisher�ζ�ư�����������ꤷ��Property���֥�������
  # @return ReturnCode PORT_OK ���ｪλ
  #                    INVALID_ARGS Properties ���������ͤ�ޤ�
  #
  # @else
  # @brief Initialization
  #
  # This function have to be called before using this class object.
  # Properties object that includes certain configuration
  # information should be given as an argument.  all, fifo, skip,
  # new can be given as a data push policy in a value of the key
  # "publisher.push_policy."
  #
  # The following options are available.
  # 
  # - thread_type: Thread type (string, default: default)
  # - publisher.push_policy: Push policy (all, fifo, skip, new)
  # - publisher.skip_count: The number of skip count in the "skip" policy
  # - measurement.exec_time: Task execution time measurement (enable/disable)
  # - measurement.exec_count: Task execution time measurement count
  #                           (numerical, number of times)
  # - measurement.period_time: Task period time measurement (enable/disable)
  # - measurement.period_count: Task period time measurement count 
  #                             (number, count)
  #
  # @param property Property objects that includes the control information
  #                 of this Publisher
  # @return ReturnCode PORT_OK normal return
  #                    INVALID_ARGS Properties with invalid values.
  # @endif
  #
  # PublisherBase::ReturnCode PublisherNew::init(coil::Properties& prop)
  def init(self, prop):
    self._rtcout.RTC_TRACE("init()")
    self.setPushPolicy(prop)
    return self.createTask(prop)

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
  # @endif
  #
  # PublisherBase::ReturnCode PublisherNew::setConsumer(InPortConsumer* consumer)
  def setConsumer(self, consumer):
    self._rtcout.RTC_TRACE("setConsumer()")
    
    if not consumer:
      self._rtcout.RTC_ERROR("setConsumer(consumer = 0): invalid argument.")
      return self.INVALID_ARGS

    self._consumer = consumer
    return self.PORT_OK

  ##
  # @if jp
  # @brief �Хåե��Υ��å�
  #
  # ���δؿ��Ǥϡ����� Publisher �˴�Ϣ�դ�����Хåե��򥻥åȤ��롣
  # �Хåե����֥������Ȥ��̥�ݥ��󥿤ξ�硢INVALID_ARGS���֤���롣
  # ����ʳ��ξ��ϡ�PORT_OK ���֤���롣
  #
  # @param buffer CDR buffer �ؤΥݥ���
  # @return ReturnCode PORT_OK ���ｪλ
  #                    INVALID_ARGS �������������ͤ��ޤޤ�Ƥ���
  #
  # @else
  # @brief Setting buffer pointer
  #
  # This operation sets a buffer that is associated with this
  # object. If the buffer object is NULL, INVALID_ARGS will be
  # returned.
  #
  # @param buffer A pointer to a CDR buffer object.
  # @return ReturnCode PORT_OK normal return
  #                    INVALID_ARGS given argument has invalid value
  #
  # @endif
  #
  # PublisherBase::ReturnCode PublisherNew::setBuffer(CdrBufferBase* buffer)
  def setBuffer(self, buffer):
    self._rtcout.RTC_TRACE("setBuffer()")

    if not buffer:
      self._rtcout.RTC_ERROR("setBuffer(buffer == 0): invalid argument")
      return self.INVALID_ARGS

    self._buffer = buffer
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
  # virtual ReturnCode setListener(ConnectorInfo& info,
  #                                ConnectorListeners* listeners);
  def setListener(self, info, listeners):
    self._rtcout.RTC_TRACE("setListener()")
    
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
  # Publisher ���ݻ�����Хåե����Ф��ƥǡ�����񤭹��ࡣ���󥷥塼
  # �ޡ��Хåե����ꥹ������Ŭ�ڤ����ꤵ��Ƥ��ʤ�����Publisher ����
  # �������Ȥ����������������Ƥ��ʤ���硢���δؿ���ƤӽФ��ȥ��顼
  # ������ PRECONDITION_NOT_MET ���֤��졢�Хåե��ؤν񤭹���������
  # ��ϰ��ڹԤ��ʤ���
  #
  # �Хåե��ؤν񤭹��ߤȡ�InPort�ؤΥǡ�������������Ʊ��Ū�˹Ԥ��
  # �뤿�ᡢ���δؿ��ϡ�InPort�ؤΥǡ��������η�̤򼨤���
  # CONNECTION_LOST, BUFFER_FULL �ʤɤΥ꥿���󥳡��ɤ��֤����Ȥ���
  # �롣���ξ�硢�ǡ����ΥХåե��ؤν񤭹��ߤϹԤ��ʤ���
  #
  # �Хåե��ؤν񤭹��ߤ��Ф��ơ��Хåե����ե���֡��Хåե��Υ�
  # �顼���Хåե��ؤν񤭹��ߤ������ॢ���Ȥ�����硢�Хåե��λ���
  # ��郎��������ʤ����ˤϤ��줾�졢���顼������ BUFFER_FULL,
  # BUFFER_ERROR, BUFFER_TIMEOUT, PRECONDITION_NOT_MET ���֤���롣
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
  #         CONNECTION_LOST     ��³�����Ǥ��줿���Ȥ��Τ�����
  #         BUFFER_FULL         �Хåե����ե���֤Ǥ��롣
  #         BUFFER_ERROR        �Хåե��˲��餫�Υ��顼����������硣
  #         NOT_SUPPORTED       ���ݡ��Ȥ���ʤ����Ԥ�줿��
  #         TIMEOUT             �����ॢ���Ȥ�����
  #
  # @else
  # @brief Write data 
  #
  # This function writes data into the buffer associated with this
  # Publisher.  If a Publisher object calls this function, without
  # initializing correctly such as a consumer, a buffer, listeners,
  # etc., error code PRECONDITION_NOT_MET will be returned and no
  # operation of the writing to a buffer etc. will be performed.
  #
  # Since writing into the buffer and sending data to InPort are
  # performed asynchronously, occasionally this function returns
  # return-codes such as CONNECTION_LOST and BUFFER_FULL that
  # indicate the result of sending data to InPort. In this case,
  # writing data into buffer will not be performed.
  #
  # When publisher writes data to the buffer, if the buffer is
  # filled, returns error, is returned with timeout and returns
  # precondition error, error codes BUFFER_FULL, BUFFER_ERROR,
  # BUFFER_TIMEOUT and PRECONDITION_NOT_MET will be returned
  # respectively.
  #
  # In other cases, PROT_ERROR will be returned.
  #
  # @param data Data to be wrote to the buffer
  # @param sec Timeout time in unit seconds
  # @param nsec Timeout time in unit nano-seconds
  # @return PORT_OK             Normal return
  #         PRECONDITION_NO_MET Precondition does not met. A consumer,
  #                             a buffer, listenes are not set properly.
  #         CONNECTION_LOST     detected that the connection has been lost
  #         BUFFER_FULL         The buffer is full status.
  #         BUFFER_ERROR        Some kind of error occurred in the buffer.
  #         NOT_SUPPORTED       Some kind of operation that is not supported
  #                             has been performed.
  #         TIMEOUT             Timeout occurred when writing to the buffer.
  #
  # @endif
  #
  # PublisherBase::ReturnCode PublisherNew::write(const cdrMemoryStream& data,
  #                                               unsigned long sec,
  #                                               unsigned long usec)
  def write(self, data, sec, usec):
    self._rtcout.RTC_PARANOID("write()")
    
    if not self._consumer or not self._buffer or not self._listeners:
      return self.PRECONDITION_NOT_MET

    if self._retcode == self.CONNECTION_LOST:
      self._rtcout.RTC_DEBUG("write(): connection lost.")
      return self._retcode

    if self._retcode == self.SEND_FULL:
      self._rtcout.RTC_DEBUG("write(): InPort buffer is full.")
      ret = self._buffer.write(data, sec, usec)
      self._task.signal()
      return self.BUFFER_FULL

    # why?
    assert(self._buffer != 0)

    self.onBufferWrite(data)
    ret = self._buffer.write(data, sec, usec)

    self._task.signal()
    self._rtcout.RTC_DEBUG("%s = write()", OpenRTM_aist.DataPortStatus.toString(ret))

    return self.convertReturn(ret, data)

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
  # bool PublisherNew::isActive()
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
  # PublisherBase::ReturnCode PublisherNew::activate()
  def activate(self):
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
  # PublisherBase::ReturnCode PublisherNew::deactivate()
  def deactivate(self):
    self._active = False;
    return self.PORT_OK

  ##
  # @if jp
  # @brief ����åɼ¹Դؿ�
  #
  # coil::PeriodicTask �ˤ������¹Ԥ���륿�����¹Դؿ���
  #
  # @else
  # @brief Thread execution function
  #
  # A task execution function to be executed by coil::PeriodicTask.
  #
  # @endif
  #
  # int PublisherNew::svc(void)
  def svc(self):
    guard = OpenRTM_aist.ScopedLock(self._retmutex)

    if self._pushPolicy == self.ALL:
      self._retcode = self.pushAll()
      return 0
    elif self._pushPolicy == self.FIFO:
      self._retcode = self.pushFifo()
      return 0
    elif self._pushPolicy == self.SKIP:
      self._retcode = self.pushSkip()
      return 0
    elif self._pushPolicy == self.NEW:
      self._retcode = self.pushNew()
      return 0
    else:
      self._retcode = self.pushNew()

    return 0

  ##
  # @brief push all policy
  #
  # PublisherNew::ReturnCode PublisherNew::pushAll()
  def pushAll(self):
    self._rtcout.RTC_TRACE("pushAll()")
    try:

      while self._buffer.readable() > 0:
        cdr = self._buffer.get()
        self.onBufferRead(cdr)

        self.onSend(cdr)
        ret = self._consumer.put(cdr)
            
        if ret != self.PORT_OK:
          self._rtcout.RTC_DEBUG("%s = consumer.put()", OpenRTM_aist.DataPortStatus.toString(ret))
          return self.invokeListener(ret, cdr)
        self.onReceived(cdr)

        self._buffer.advanceRptr()

      return self.PORT_OK
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      return self.CONNECTION_LOST

    return self.PORT_ERROR

  ##
  # @brief push "fifo" policy
  #
  # PublisherNew::ReturnCode PublisherNew::pushFifo()
  def pushFifo(self):
    self._rtcout.RTC_TRACE("pushFifo()")

    try:
      cdr = self._buffer.get()
      self.onBufferRead(cdr)

      self.onSend(cdr)
      ret = self._consumer.put(cdr)

      if ret != self.PORT_OK:
        self._rtcout.RTC_DEBUG("%s = consumer.put()", OpenRTM_aist.DataPortStatus.toString(ret))
        return self.invokeListener(ret, cdr)
      self.onReceived(cdr)
        
      self._buffer.advanceRptr()
        
      return self.PORT_OK
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      return self.CONNECTION_LOST

    return self.PORT_ERROR

  ##
  # @brief push "skip" policy
  #
  # PublisherNew::ReturnCode PublisherNew::pushSkip()
  def pushSkip(self):
    self._rtcout.RTC_TRACE("pushSkip()")
    try:
      ret = self.PORT_OK
      preskip = self._buffer.readable() + self._leftskip
      loopcnt = preskip/(self._skipn+1)
      postskip = self._skipn - self._leftskip

      for i in range(loopcnt):
        self._buffer.advanceRptr(postskip)
        cdr = self._buffer.get()
        self.onBufferRead(cdr)

        self.onSend(cdr)
        ret = self._consumer.put(cdr)
        if ret != self.PORT_OK:
          self._buffer.advanceRptr(-postskip)
          self._rtcout.RTC_DEBUG("%s = consumer.put()", OpenRTM_aist.DataPortStatus.toString(ret))
          return self.invokeListener(ret, cdr)

        self.onReceived(cdr)
        postskip = self._skipn + 1

      self._buffer.advanceRptr(self._buffer.readable())

      if loopcnt == 0:
        # Not put
        self._leftskip = preskip % (self._skipn + 1)
      else:
        if self._retcode != self.PORT_OK:
          # put Error after
          self._leftskip = 0
        else:
          # put OK after
          self._leftskip = preskip % (self._skipn + 1)

      return ret

    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      return self.CONNECTION_LOST

    return self.PORT_ERROR

  ##
  # @brief push "new" policy
  #
  # PublisherNew::ReturnCode PublisherNew::pushNew()
  def pushNew(self):
    self._rtcout.RTC_TRACE("pushNew()")
    try:
      self._buffer.advanceRptr(self._buffer.readable() - 1)
        
      cdr = self._buffer.get()
      self.onBufferRead(cdr)

      self.onSend(cdr)
      ret = self._consumer.put(cdr)

      if ret != self.PORT_OK:
        self._rtcout.RTC_DEBUG("%s = consumer.put()", OpenRTM_aist.DataPortStatus.toString(ret))
        return self.invokeListener(ret, cdr)

      self.onReceived(cdr)
      self._buffer.advanceRptr()

      return self.PORT_OK

    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      return self.CONNECTION_LOST

    return self.PORT_ERROR

  ##
  # @if jp
  # @brief BufferStatus ���� DataPortStatus �ؤ��Ѵ�
  #
  # �Хåե����������ͤ� DataPortStatus::Enum �����Ѵ�����ؿ�����
  # �줾�졢�ʲ��Τ褦���Ѵ�����롣�Ѵ����˥�����Хå���Ƥ־�硢
  # ������Х��ؿ����յ����롣
  # 
  # - BUFFER_OK: PORT_OK
  #  - None
  # - BUFFER_ERROR: BUFFER_ERROR
  #  - None
  # - BUFFER_FULL: BUFFER_FULL
  #  - onBufferFull()
  # - NOT_SUPPORTED: PORT_ERROR
  #  - None
  # - TIMEOUT: BUFFER_TIMEOUT
  #  - onBufferWriteTimeout()
  # - PRECONDITION_NOT_MET: PRECONDITION_NOT_MET
  #  - None
  # - other: PORT_ERROR
  #  - None
  #
  # @param status BufferStatus
  # @param data cdrMemoryStream
  # @return DataPortStatu ���Υ꥿���󥳡���
  #
  # @else
  # @brief Convertion from BufferStatus to DataPortStatus
  # 
  # This function converts return value from the buffer to
  # DataPortStatus::Enum typed return value. The conversion rule is
  # as follows. Callback functions are also shown, if it exists.
  # 
  # - BUFFER_OK: PORT_OK
  #  - None
  # - BUFFER_ERROR: BUFFER_ERROR
  #  - None
  # - BUFFER_FULL: BUFFER_FULL
  #  - onBufferFull()
  # - NOT_SUPPORTED: PORT_ERROR
  #  - None
  # - TIMEOUT: BUFFER_TIMEOUT
  #  - onBufferWriteTimeout()
  # - PRECONDITION_NOT_MET: PRECONDITION_NOT_MET
  #  - None
  # - other: PORT_ERROR
  #  - None
  #
  # @param status BufferStatus
  # @param data cdrMemoryStream
  # @return DataPortStatus typed return code
  #
  # @endif
  #
  # PublisherBase::ReturnCode
  # PublisherNew::convertReturn(BufferStatus::Enum status,
  #                             const cdrMemoryStream& data)
  def convertReturn(self, status, data):
    ##
    # BufferStatus -> DataPortStatus
    #
    # BUFFER_OK     -> PORT_OK
    # BUFFER_ERROR  -> BUFFER_ERROR
    # BUFFER_FULL   -> BUFFER_FULL
    # NOT_SUPPORTED -> PORT_ERROR
    # TIMEOUT       -> BUFFER_TIMEOUT
    # PRECONDITION_NOT_MET -> PRECONDITION_NOT_MET
    ##
    if status == OpenRTM_aist.BufferStatus.BUFFER_OK:
      return self.PORT_OK
    
    elif status == OpenRTM_aist.BufferStatus.BUFFER_ERROR:
      return self.BUFFER_ERROR

    elif status == OpenRTM_aist.BufferStatus.BUFFER_FULL:
      self.onBufferFull(data)
      return self.BUFFER_FULL

    elif status == OpenRTM_aist.BufferStatus.NOT_SUPPORTED:
      return self.PORT_ERROR

    elif status == OpenRTM_aist.BufferStatus.TIMEOUT:
      self.onBufferWriteTimeout(data)
      return self.BUFFER_TIMEOUT

    elif status == OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET:
      return self.PRECONDITION_NOT_MET

    else:
      return self.PORT_ERROR

  ##
  # @if jp
  # @brief DataPortStatus�˽��äƥꥹ�ʤ����Τ���ؿ���ƤӽФ���
  #
  # @param status DataPortStatus
  # @param data cdrMemoryStream
  # @return �꥿���󥳡���
  #
  # @else
  # @brief Call listeners according to the DataPortStatus
  #
  # @param status DataPortStatus
  # @param data cdrMemoryStream
  # @return Return code
  #
  # @endif
  #
  # PublisherNew::ReturnCode
  # PublisherNew::invokeListener(DataPortStatus::Enum status,
  #                              const cdrMemoryStream& data)
  def invokeListener(self, status, data):
    # ret:
    # PORT_OK, PORT_ERROR, SEND_FULL, SEND_TIMEOUT, CONNECTION_LOST,
    # UNKNOWN_ERROR
    if status == self.PORT_ERROR:
      self.onReceiverError(data)
      return self.PORT_ERROR
        
    elif status == self.SEND_FULL:
      self.onReceiverFull(data)
      return self.SEND_FULL
        
    elif status == self.SEND_TIMEOUT:
      self.onReceiverTimeout(data)
      return self.SEND_TIMEOUT
        
    elif status == self.CONNECTION_LOST:
      self.onReceiverError(data)
      return self.CONNECTION_LOST
        
    elif status == self.UNKNOWN_ERROR:
      self.onReceiverError(data)
      return self.UNKNOWN_ERROR
        
    else:
      self.onReceiverError(data)
      return self.PORT_ERROR

  ##
  # @if jp
  # @brief ON_BUFFER_WRITE�Υꥹ�ʤ����Τ��롣 
  # @param data cdrMemoryStream
  # @else
  # @brief Notify an ON_BUFFER_WRITE event to listeners
  # @param data cdrMemoryStream
  # @endif
  #
  # inline void onBufferWrite(const cdrMemoryStream& data)
  def onBufferWrite(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE].notify(self._profile, data)
    return

  ##
  # @if jp
  # @brief ON_BUFFER_FULL�ꥹ�ʤإ��٥�Ȥ����Τ��롣 
  # @param data cdrMemoryStream
  # @else
  # @brief Notify an ON_BUFFER_FULL event to listeners
  # @param data cdrMemoryStream
  # @endif
  #
  # inline void onBufferFull(const cdrMemoryStream& data)
  def onBufferFull(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_FULL].notify(self._profile, data)
    return

  ##
  # @if jp
  # @brief ON_BUFFER_WRITE_TIMEOUT�Υꥹ�ʤ����Τ��롣 
  # @param data cdrMemoryStream
  # @else
  # @brief Notify an ON_BUFFER_WRITE_TIMEOUT event to listeners
  # @param data cdrMemoryStream
  # @endif
  #
  # inline void onBufferWriteTimeout(const cdrMemoryStream& data)
  def onBufferWriteTimeout(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE_TIMEOUT].notify(self._profile, data)
    return

  ##
  # @if jp
  # @brief ON_BUFFER_OVERWRITE�Υꥹ�ʤ����Τ��롣 
  # @param data cdrMemoryStream
  # @else
  # @brief Notify an ON_BUFFER_OVERWRITE event to listeners
  # @param data cdrMemoryStream
  # @endif
  #
  # inline void onBufferWriteOverwrite(const cdrMemoryStream& data)
  def onBufferWriteOverwrite(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_OVERWRITE].notify(self._profile, data)
    return

  ##
  # @if jp
  # @brief ON_BUFFER_READ�Υꥹ�ʤ����Τ��롣 
  # @param data cdrMemoryStream
  # @else
  # @brief Notify an ON_BUFFER_READ event to listeners
  # @param data cdrMemoryStream
  # @endif
  #
  # inline void onBufferRead(const cdrMemoryStream& data)
  def onBufferRead(self, data):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connectorData_[OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_READ].notify(self._profile, data)
    return

  ##
  # @if jp
  # @brief ON_SEND�Υꥹ�ʤ����Τ��롣 
  # @param data cdrMemoryStream
  # @else
  # @brief Notify an ON_SEND event to listners
  # @param data cdrMemoryStream
  # @endif
  #
  #inline void onSend(const cdrMemoryStream& data)
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

  ##
  # @if jp
  # @brief ON_SENDER_ERROR�Υꥹ�ʤ����Τ��롣 
  # @param data cdrMemoryStream
  # @else
  # @brief Notify an ON_SENDER_ERROR event to listeners
  # @param data cdrMemoryStream
  # @endif
  #
  # inline void onSenderError()
  def onSenderError(self):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_SENDER_ERROR].notify(self._profile)
    return



def PublisherNewInit():
  OpenRTM_aist.PublisherFactory.instance().addFactory("new",
                                                      OpenRTM_aist.PublisherNew,
                                                      OpenRTM_aist.Delete)
