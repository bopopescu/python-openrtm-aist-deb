#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  PublisherPeriodic.py
# @brief PublisherPeriodic class
# @date  $Date: 2007/09/28 $
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
from omniORB import any

import OpenRTM_aist


##
# @if jp
# @class PublisherPeriodic
# @brief PublisherPeriodic ���饹
#
# ����Ū�˥ǡ������������뤿��� Publisher ���饹�����Υ��饹�ϡ���
# �� Connector ��ˤ��äơ��Хåե�����ӥ��󥷥塼�ޤ˴�Ϣ�դ����
# �롣����������Ȥ˥Хåե�����ǡ�������Ф����󥷥塼�ޤ��Ф���
# �ǡ��������Ф��롣
#
# @else
# @class PublisherPeriodic
# @brief PublisherPeriodic class
#
# Publisher for periodic data transmitting. Usually this class
# object exists in a Connector object, and it is associated with a
# buffer and a consumer. This publisher periodically gets data from
# the buffer and publish it into the consumer.
#
# @endif
#
class PublisherPeriodic(OpenRTM_aist.PublisherBase):
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
  # ���н����θƤӽФ��ֳ֤�Property���֥������Ȥ�dataport.push_rate����
  # �����ꤷ�Ƥ���ɬ�פ����롣���дֳ֤ϡ�Hzñ�̤���ư����ʸ����ǻ��ꡣ
  # ���Ȥ��С�1000.0Hz�ξ��ϡ���1000.0�פ����ꡣ
  # �嵭�ץ�ѥƥ���̤����ξ��ϡ���1000Hz�פ����ꡣ
  #
  # @param self
  # @param consumer �ǡ������Ф��Ԥĥ��󥷥塼��
  # @param property ��Publisher�ζ�ư�����������ꤷ��Property���֥�������
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self):
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("PublisherPeriodic")
    self._consumer   = None
    self._buffer     = None
    self._task       = None
    self._retcode    = self.PORT_OK
    self._retmutex   = threading.RLock()
    self._pushPolicy = self.NEW
    self._skipn      = 0
    self._active     = False
    self._readback   = False
    self._leftskip   = 0
    self._profile    = None
    self._listeners  = None

    return

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
  # @endif
  def __del__(self):
    self._rtcout.RTC_TRACE("~PublisherPeriodic()")
    if self._task:
      self._task.resume()
      self._task.finalize()
      self._rtcout.RTC_PARANOID("task finalized.")

      OpenRTM_aist.PeriodicTaskFactory.instance().deleteObject(self._task)
      del self._task
      self._rtcout.RTC_PARANOID("task deleted.")

    # "consumer" should be deleted in the Connector
    self._consumer = None
    # "buffer"   should be deleted in the Connector
    self._buffer = None
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

    # setting task function
    self._task.setTask(self.svc)

    # Task execution rate
    rate = prop.getProperty("publisher.push_rate")

    if rate != "":
      hz = float(rate)
      if hz == 0:
        hz = 1000.0
      self._rtcout.RTC_DEBUG("Task period %f [Hz]", hz)
    else:
      hz = 1000.0

    self._task.setPeriod(1.0/hz)
    
    # Measurement setting
    mprop = prop.getNode("measurement")

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

    # Start task in suspended mode
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
  # Properties ��Ϳ���롣���ʤ��Ȥ⡢���н����θƤӽФ�������ñ��
  # Hz �ο��ͤȤ��� Property���֥������Ȥ� publisher.push_rate �򥭡�
  # �Ȥ������Ǥ����ꤹ��ɬ�פ����롣���� 5ms ���ʤ����200Hz�ξ�硢
  # 200.0 �����ꤹ�롣 dataport.publisher.push_rate ��̤����ξ�硢
  # false ���֤���롣�ǡ�����ץå��夹��ݤΥݥꥷ���Ȥ���
  # publisher.push_policy �򥭡��Ȥ����ͤˡ�all, fifo, skip, new ��
  # �����줫��Ϳ���뤳�Ȥ��Ǥ��롣
  # 
  # �ʲ��Υ��ץ�����Ϳ���뤳�Ȥ��Ǥ��롣
  # 
  # - publisher.thread_type: ����åɤΥ����� (ʸ���󡢥ǥե����: default)
  # - publisher.push_rate: Publisher���������� (����)
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
  # information should be given as an argument.  At least, a
  # numerical value of unit of Hz with the key of
  # "dataport.publisher.push_rate" has to be set to the Properties
  # object of argument.  The value is the invocation cycle of data
  # sending process.  In case of 5 ms period or 200 Hz, the value
  # should be set as 200.0. False will be returned, if there is no
  # value with the key of "dataport.publisher.push_rate".
  #
  # The following options are available.
  # 
  # - publisher.thread_type: Thread type (string, default: default)
  # - publisher.push_rate: Publisher sending period (numberical)
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
  # PublisherBase::ReturnCode PublisherPeriodic::init(coil::Properties& prop)
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
  # PublisherBase::ReturnCode
  # PublisherPeriodic::setConsumer(InPortConsumer* consumer)
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
  # PublisherBase::ReturnCode PublisherPeriodic::setBuffer(CdrBufferBase* buffer)
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
  #PublisherBase::ReturnCode
  #PublisherPeriodic::setListener(ConnectorInfo& info,
  #                               ConnectorListeners* listeners)
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
  # PublisherBase::ReturnCode
  # PublisherPeriodic::write(const cdrMemoryStream& data,
  #                          unsigned long sec,
  #                          unsigned long usec)
  def write(self, data, sec, usec):
    self._rtcout.RTC_PARANOID("write()")

    if not self._consumer or not self._buffer or not self._listeners:
      return self.PRECONDITION_NOT_MET

    if self._retcode == self.CONNECTION_LOST:
      self._rtcout.RTC_DEBUG("write(): connection lost.")
      return self._retcode

    if self._retcode == self.SEND_FULL:
      self._rtcout.RTC_DEBUG("write(): InPort buffer is full.")
      self._buffer.write(data,sec,usec)
      return self.BUFFER_FULL

    self.onBufferWrite(data)
    ret = self._buffer.write(data, sec, usec)
    self._rtcout.RTC_DEBUG("%s = write()", OpenRTM_aist.DataPortStatus.toString(ret))
    self._task.resume()
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
  # bool PublisherPeriodic::isActive()
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
  # PublisherBase::ReturnCode PublisherPeriodic::activate()
  def activate(self):
    if not self._task or not self._buffer:
      return self.PRECONDITION_NOT_MET
    self._active = True
    self._task.resume()
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
  # PublisherBase::ReturnCode PublisherPeriodic::deactivate()
  def deactivate(self):
    if not self._task:
      return self.PRECONDITION_NOT_MET
    self._active = False
    self._task.suspend()
    return self.PORT_OK

  ##
  # @if jp
  # @brief ����åɼ¹Դؿ�
  # @else
  # @brief Thread execution function
  # A task execution function to be executed by coil::PeriodicTask.
  # @endif
  #
  # int PublisherPeriodic::svc(void)
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
  # PublisherBase::ReturnCode PublisherPeriodic::pushAll()
  def pushAll(self):
    self._rtcout.RTC_TRACE("pushAll()")

    if not self._buffer:
      return self.PRECONDITION_NOT_MET      

    if self.bufferIsEmpty():
      return self.BUFFER_EMPTY

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


  ##
  # @brief push "fifo" policy
  #
  # PublisherBase::ReturnCode PublisherPeriodic::pushFifo()
  def pushFifo(self):
    self._rtcout.RTC_TRACE("pushFifo()")
    if not self._buffer:
      return self.PRECONDITION_NOT_MET      

    if self.bufferIsEmpty():
      return self.BUFFER_EMPTY

    cdr = self._buffer.get()
    self.onBufferRead(cdr)

    self.onSend(cdr)
    ret = self._consumer.put(cdr)

    if ret != self.PORT_OK:
      self._rtcout.RTC_DEBUG("%s = consumer.put()",OpenRTM_aist.DataPortStatus.toString(ret))
      return self.invokeListener(ret, cdr)

    self.onReceived(cdr)
    self._buffer.advanceRptr()
    
    return self.PORT_OK


  ##
  # @brief push "skip" policy
  #
  # PublisherBase::ReturnCode PublisherPeriodic::pushSkip()
  def pushSkip(self):
    self._rtcout.RTC_TRACE("pushSkip()")
    if not self._buffer:
      return self.PRECONDITION_NOT_MET      

    if self.bufferIsEmpty():
      return self.BUFFER_EMPTY

    ret = self.PORT_OK
    preskip  = self._buffer.readable() + self._leftskip
    loopcnt  = preskip / (self._skipn + 1)
    postskip = self._skipn - self._leftskip
    for i in range(loopcnt):
      self._buffer.advanceRptr(postskip)
      cdr = self._buffer.get()
      self.onBufferRead(cdr)

      self.onSend(cdr)
      ret = self._consumer.put(cdr)
      if ret != self.PORT_OK:
        self._buffer.advanceRptr(-postskip)
        self._rtcout.RTC_DEBUG("%s = consumer.put()",OpenRTM_aist.DataPortStatus.toString(ret))
        return self.invokeListener(ret, cdr)
      self.onReceived(cdr)
      postskip = self._skipn + 1

    self._buffer.advanceRptr(self._buffer.readable())
    self._leftskip = preskip % (self._skipn + 1)
    
    return ret


  ##
  # @brief push "new" policy
  #
  # PublisherBase::ReturnCode PublisherPeriodic::pushNew()
  def pushNew(self):
    self._rtcout.RTC_TRACE("pushNew()")
    if not self._buffer:
      return self.PRECONDITION_NOT_MET      

    if self.bufferIsEmpty():
      return self.BUFFER_EMPTY

    # In case of the periodic/push_new policy, the buffer should
    # allow readback. But, readback flag should be set as "true"
    # after written at least one datum into the buffer.
    self._readback = True

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
  # PublisherBase::ReturnCodea
  # PublisherPeriodic::convertReturn(BufferStatus::Enum status,
  #                                  const cdrMemoryStream& data)
  def convertReturn(self, status, data):
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
  # PublisherPeriodic::ReturnCode
  # PublisherPeriodic::invokeListener(DataPortStatus::Enum status,
  #                                   const cdrMemoryStream& data)
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
  # @brief ON_BUFFER_READ�Υꥹ�ʤ����Τ��롣 
  # @param data cdrMemoryStream
  # @else
  # @brief Notify an ON_BUFFER_READ event to listeners
  # @param data cdrMemoryStream
  # @endif
  #
  #  inline void onBufferRead(const cdrMemoryStream& data)
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


  ##
  # @if jp
  # @brief ON_BUFFER_EMPTY�Υꥹ�ʤ����Τ��롣 
  # @else
  # @brief Notify an ON_BUFFER_EMPTY event to listeners
  # @endif
  #
  #inline void onBufferEmpty()
  def onBufferEmpty(self):
    if self._listeners is not None and self._profile is not None:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_BUFFER_EMPTY].notify(self._profile)
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
    if self._listeners is not None and self._profile is not None:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_SENDER_EMPTY].notify(self._profile)
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
    if self._listeners is not None and self._profile is not None:
      self._listeners.connector_[OpenRTM_aist.ConnectorListenerType.ON_SENDER_ERROR].notify(self._profile)
    return


  ##
  # @if jp
  # @brief �Хåե��������ɤ���������å����롣x
  # @else
  # @brief Whether a buffer is empty.
  # @endif
  #
  # bool bufferIsEmpty()
  def bufferIsEmpty(self):
    if self._buffer and self._buffer.empty() and  not self._readback:
      self._rtcout.RTC_DEBUG("buffer empty")
      self.onBufferEmpty()
      self.onSenderEmpty()
      return True

    return False



def PublisherPeriodicInit():
  OpenRTM_aist.PublisherFactory.instance().addFactory("periodic",
                                                      OpenRTM_aist.PublisherPeriodic,
                                                      OpenRTM_aist.Delete)
