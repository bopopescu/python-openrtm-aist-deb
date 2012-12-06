#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file PeriodicExecutionContext.py
# @brief PeriodicExecutionContext class
# @date $Date: 2007/08/29$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import sys
import copy
import threading
import time
from omniORB import CORBA, PortableServer

import OpenRTM_aist
import OpenRTM
import RTC

DEFAULT_PERIOD = 0.000001

##
# @if jp
# @class PeriodicExecutionContext
# @brief PeriodicExecutionContext ���饹
#
# Periodic Sampled Data Processing(�����¹���)ExecutionContext���饹��
#
# @since 0.4.0
#
# @else
# @class PeriodicExecutionContext
# @brief PeriodicExecutionContext class
# @endif
class PeriodicExecutionContext(OpenRTM_aist.ExecutionContextBase,
                               OpenRTM_aist.Task):
  """
  """



  ##
  # @if jp
  # @class DFP
  # @brief DFP ���饹
  #
  # ���üԥꥹ�Ȥ���Ͽ���줿 DataFlowParticipant �δؿ���ư���뤿���
  # �������饹��
  #
  # @param Object �����оݥ���ݡ��ͥ�Ȥη�
  #
  # @else
  #
  # @endif
  class DFP:
    """
    """

    ##
    # @if jp
    # @brief �ǥե���ȥ��󥹥ȥ饯��
    #
    # �ǥե���ȥ��󥹥ȥ饯��
    #
    # @param self
    # @param obj �����оݥ���ݡ��ͥ��
    # @param id_ ��°���� ExecutionContext ��ID
    #
    # @else
    # @brief Constructor
    # @endif
    def __init__(self, obj, id_):
      self._obj = obj
      self._active = True
      self.ec_id = id_
      self._sm = OpenRTM_aist.StateMachine(4)
      self._sm.setListener(self)
      self._sm.setEntryAction (RTC.ACTIVE_STATE,
                               self.on_activated)
      self._sm.setDoAction    (RTC.ACTIVE_STATE,
                               self.on_execute)
      self._sm.setPostDoAction(RTC.ACTIVE_STATE,
                               self.on_state_update)
      self._sm.setExitAction  (RTC.ACTIVE_STATE,
                               self.on_deactivated)
      self._sm.setEntryAction (RTC.ERROR_STATE,
                               self.on_aborting)
      self._sm.setDoAction    (RTC.ERROR_STATE,
                               self.on_error)
      self._sm.setExitAction  (RTC.ERROR_STATE,
                               self.on_reset)
      st = OpenRTM_aist.StateHolder()
      st.prev = RTC.INACTIVE_STATE
      st.curr = RTC.INACTIVE_STATE
      st.next = RTC.INACTIVE_STATE
      self._sm.setStartState(st)
      self._sm.goTo(RTC.INACTIVE_STATE)


    ##
    # @if jp
    # @brief ExecutionContext �¹Գ��ϻ��˸ƤФ��ؿ�
    #
    # ���ä��Ƥ��� ExecutionContext ���¹Ԥ򳫻Ϥ����(Running���֤����ܻ�)
    # �ˡ������оݥ���ݡ��ͥ�Ȥ� on_startup ��ƤӤ�����
    #
    # @param self
    #
    # @else
    #
    # @brief
    #
    # @endif
    def on_startup(self):
      return self._obj.on_startup(self.ec_id)


    ##
    # @if jp
    # @brief ExecutionContext ��߻��˸ƤФ��ؿ�
    #
    # ���ä��Ƥ��� ExecutionContext ���¹Ԥ���ߤ����(Stopped���֤����ܻ�)
    # �ˡ������оݥ���ݡ��ͥ�Ȥ� on_shutdown ��ƤӤ�����
    #
    # @param self
    #
    # @else
    #
    # @endif
    def on_shutdown(self):
      return self._obj.on_shutdown(self.ec_id)


    ##
    # @if jp
    # @brief RT����ݡ��ͥ�Ȥ������ƥ��ֲ����줿���˸ƤФ��ؿ�
    #
    # �����оݤ�RT����ݡ��ͥ�Ȥ������ƥ��ֲ����줿��(Active���֤����ܻ�)
    # �ˡ������оݥ���ݡ��ͥ�Ȥ� on_activated ��ƤӤ�����
    # �����оݥ���ݡ��ͥ�ȤΥ����ƥ��ֲ������Ԥ������ˤϡ����ơ��ȥޥ���
    # �� Error ���֤����ܤ����롣
    #
    # @param self
    # @param st �о�RT����ݡ��ͥ�Ȥθ��ߤξ���
    #
    # @else
    #
    # @endif
    def on_activated(self, st):
      if self._obj.on_activated(self.ec_id) != RTC.RTC_OK:
        self._sm.goTo(RTC.ERROR_STATE)
        return
      return


    ##
    # @if jp
    # @brief RT����ݡ��ͥ�Ȥ��󥢥��ƥ��ֲ����줿���˸ƤФ��ؿ�
    #
    # �����оݤ�RT����ݡ��ͥ�Ȥ��󥢥��ƥ��ֲ����줿��
    # (Deactive���֤����ܻ�)�ˡ������оݥ���ݡ��ͥ�Ȥ� on_deactivated ��
    # �ƤӤ�����
    #
    # @param self
    # @param st �о�RT����ݡ��ͥ�Ȥθ��ߤξ���
    #
    # @else
    #
    # @endif
    def on_deactivated(self, st):
      self._obj.on_deactivated(self.ec_id)


    ##
    # @if jp
    # @brief RT����ݡ��ͥ�Ȥǥ��顼��ȯ���������˸ƤФ��ؿ�
    #
    # �����оݤ�RT����ݡ��ͥ�Ȥ˥��顼��ȯ��������(Error���֤����ܻ�)
    # �˴����оݥ���ݡ��ͥ�Ȥ� on_aborting ��ƤӤ�����
    #
    # @param self
    # @param st �о�RT����ݡ��ͥ�Ȥθ��ߤξ���
    #
    # @else
    #
    # @brief
    #
    # @endif
    def on_aborting(self, st):
      self._obj.on_aborting(self.ec_id)


    ##
    # @if jp
    # @brief RT����ݡ��ͥ�Ȥ����顼���֤λ��˸ƤФ��ؿ�
    #
    # �����оݤ�RT����ݡ��ͥ�Ȥ����顼���֤ˤ���֡� 
    # �����оݥ���ݡ��ͥ�Ȥ� on_error �����Ū�˸ƤӤ�����
    #
    # @param self
    # @param st �о�RT����ݡ��ͥ�Ȥθ��ߤξ���
    #
    # @else
    #
    # @brief
    #
    # @endif
    def on_error(self, st):
      self._obj.on_error(self.ec_id)


    ##
    # @if jp
    # @brief RT����ݡ��ͥ�Ȥ�ꥻ�åȤ�����˸ƤФ��ؿ�
    #
    # �����оݤ�RT����ݡ��ͥ�Ȥ�ꥻ�åȤ���ݤˡ������оݥ���ݡ��ͥ��
    # �� on_reset ��ƤӤ�����
    #
    # @param self
    # @param st �о�RT����ݡ��ͥ�Ȥθ��ߤξ���
    #
    # @else
    #
    # @endif
    def on_reset(self, st):
      if self._obj.on_reset(self.ec_id) != RTC.RTC_OK:
        self._sm.goTo(RTC.ERROR_STATE)
        return
      return


    ##
    # @if jp
    # @brief RT����ݡ��ͥ�ȼ¹Ի������Ū�˸ƤФ��ؿ�
    #
    # �����оݤ�RT����ݡ��ͥ�Ȥ� Active ���֤Ǥ���ȤȤ�ˡ�
    # ExecutionContext �� Running ���֤ξ��ˡ����ꤵ�줿ư����������Ū��
    # �����оݥ���ݡ��ͥ�Ȥ� on_execute ��ƤӤ�����
    # �ؿ��μ¹Ԥ˼��Ԥ������(���ͤ� RTC_OK �ʳ�)�������оݥ���ݡ��ͥ�Ȥ�
    # ���֤� Error ���֤����ܤ����롣
    #
    # @param self
    # @param st �о�RT����ݡ��ͥ�Ȥθ��ߤξ���
    #
    # @else
    #
    # @endif
    def on_execute(self, st):
      if self._obj.on_execute(self.ec_id) != RTC.RTC_OK:
        self._sm.goTo(RTC.ERROR_STATE)
        return
      return


    ##
    # @if jp
    # @brief RT����ݡ��ͥ�ȼ¹Ի������Ū�˸ƤФ��ؿ�
    #
    # �����оݤ�RT����ݡ��ͥ�Ȥ� Active ���֤Ǥ���ȤȤ�ˡ�
    # ExecutionContext �� Running ���֤ξ��ˡ����ꤵ�줿ư����������Ū��
    # �����оݥ���ݡ��ͥ�Ȥ� on_state_update ��ƤӤ�����
    # �ؿ��μ¹Ԥ˼��Ԥ������(���ͤ� RTC_OK �ʳ�)�������оݥ���ݡ��ͥ�Ȥ�
    # ���֤� Error ���֤����ܤ����롣
    #
    # @param self
    # @param st �о�RT����ݡ��ͥ�Ȥθ��ߤξ���
    #
    # @else
    #
    # @endif
    def on_state_update(self, st):
      if self._obj.on_state_update(self.ec_id) != RTC.RTC_OK:
        self._sm.goTo(RTC.ERROR_STATE)
        return
      return


    ##
    # @if jp
    # @brief ExecutionContext �μ¹Լ����ѹ����˸ƤФ��ؿ�
    #
    # ���ä��Ƥ��� ExecutionContext �μ¹Լ������ѹ��Ȥʤä����ˡ�
    # �����оݥ���ݡ��ͥ�Ȥ� on_rate_changed ��ƤӤ�����
    #
    # @param self
    #
    # @else
    #
    # @endif
    def on_rate_changed(self):
      self._obj.on_rate_changed(self.ec_id)


    ##
    # @if jp
    # @brief �������ܤ�¹Ԥ����������������
    #
    # �����о�RT����ݡ��ͥ�Ȥξ������ܤ�¹Ԥ���������������롣
    #
    # @param self
    #
    # @return �����
    #
    # @else
    #
    # @brief
    #
    # @endif
    def worker(self):
      return self._sm.worker()


    ##
    # @if jp
    # @brief ���ߤξ��֤��������
    #
    # �����о�RT����ݡ��ͥ�Ȥθ��ߤξ��֤�������롣
    #
    # @param self
    #
    # @return ���߾���
    #
    # @else
    #
    # @brief
    #
    # @endif
    def get_state(self):
      return self._sm.getState()


  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  # ���ꤵ�줿�ͤ�ץ�ե���������ꤹ�롣
  #
  # @param self
  # @param owner ���� Executioncontext �� owner(�ǥե������:None)
  # @param rate ư�����(Hz)(�ǥե������:None)
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, owner=None, rate=None):
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("rtobject.periodic_ec")
    self._rtcout.RTC_TRACE("PeriodicExecutionContext()")

    OpenRTM_aist.Task.__init__(self)

    self._nowait = False
    self._running = False

    self._worker = self.Worker()

    global DEFAULT_PERIOD

    if rate is None:
      self._period = OpenRTM_aist.TimeValue(DEFAULT_PERIOD)
    else:
      if rate == 0:
        rate = 1.0 / DEFAULT_PERIOD
      self._period = OpenRTM_aist.TimeValue(1.0 / rate)

      if self._period.sec() == 0  and self._period.usec() < 0.000001:
        self._nowait = True

    self._rtcout.RTC_DEBUG("Actual rate: %d [sec], %d [usec]",
                           (self._period.sec(), self._period.usec()))    

    self._comps = []
    self._profile = RTC.ExecutionContextProfile(RTC.PERIODIC, (1.0/self._period.toDouble()), None, [], [])
    self._ref = self._this()
    self._mutex_del = threading.RLock()
    return


  def __del__(self, Task=OpenRTM_aist.Task):
    self._rtcout.RTC_TRACE("~PeriodicExecutionContext()")
    self._worker._cond.acquire()
    self._worker._running = True
    self._worker._cond.notify()
    self._worker._cond.release()
    self._running = False
    #self.wait()

    self._profile.owner = None
    self._profile.paarticipants = []
    self._profile.properties = []
    guard = OpenRTM_aist.ScopedLock(self._mutex_del)
    Task.__del__(self)
    del guard

  ##
  # @if jp
  # @brief CORBA ���֥������Ȼ��Ȥμ���
  #
  # �ܥ��֥������Ȥ� ExecutioncontextService �Ȥ��Ƥ� CORBA ���֥������Ȼ���
  # ��������롣
  #
  # @return CORBA ���֥������Ȼ���
  #
  # @param self
  #
  # @else
  #
  # @endif
  def getObjRef(self):
    return self._ref


  ##
  # @if jp
  # @brief ����ݡ��ͥ�ȤΥ����ƥ��ӥƥ�����åɴؿ�
  #
  # ����ݡ��ͥ�Ȥ����������ƥ��ӥƥ�����åɤμ¹Դؿ���
  # ACE_Task �����ӥ����饹�᥽�åɤΥ����С��饤�ɡ�
  #
  # @else
  #
  # @brief Create internal activity thread
  #
  # Run by a daemon thread to handle deferred processing.
  # ACE_Task class method override.
  #
  # @endif
  def svc(self):
    self._rtcout.RTC_TRACE("svc()")
    flag = True
    count_ = 0
    
    guard = OpenRTM_aist.ScopedLock(self._mutex_del)
    while flag:
      self._worker._cond.acquire()
      while not self._worker._running:
        self._worker._cond.wait()

      t0_ = OpenRTM_aist.Time()

      if self._worker._running:
        for comp in self._comps:
          comp._sm.worker()

      self._worker._cond.release()

      t1_ = OpenRTM_aist.Time()

      if count_ > 1000:
        exctm_ = (t1_ - t0_).getTime().toDouble()
        slptm_ = self._period.toDouble() - exctm_
        self._rtcout.RTC_PARANOID("Period:    %f [s]", self._period.toDouble())
        self._rtcout.RTC_PARANOID("Execution: %f [s]", exctm_)
        self._rtcout.RTC_PARANOID("Sleep:     %f [s]", slptm_)

      t2_ = OpenRTM_aist.Time()

      if not self._nowait and self._period.toDouble() > ((t1_ - t0_).getTime().toDouble()):
        if count_ > 1000:
          self._rtcout.RTC_PARANOID("sleeping...")
        slptm_ = self._period.toDouble() - (t1_ - t0_).getTime().toDouble()
        time.sleep(slptm_)

      if count_ > 1000:
        t3_ = OpenRTM_aist.Time()
        self._rtcout.RTC_PARANOID("Slept:     %f [s]", (t3_ - t2_).getTime().toDouble())
        count_ = 0
      count_ += 1
      flag = self._running
    del guard
    return 0


  ##
  # @if jp
  # @brief ExecutionContext �ѤΥ���åɼ¹Դؿ�
  #
  # ExecutionContext �ѤΥ���åɽ�λ���˸ƤФ�롣
  # ����ݡ��ͥ�ȥ��֥������Ȥ��󥢥��ƥ��ֲ����ޥ͡�����ؤ����Τ�Ԥ���
  # ����� ACE_Task �����ӥ����饹�᥽�åɤΥ����С��饤�ɡ�
  #
  # @param self
  # @param flags ��λ�����ե饰
  #
  # @return ��λ�������
  #
  # @else
  #
  # @brief Close activity thread
  #
  # close() method is called when activity thread svc() is returned.
  # This method deactivate this object and notify it to manager.
  # ACE_Task class method override.
  #
  # @endif
  def close(self, flags):
    self._rtcout.RTC_TRACE("close()")
    return 0


  ##
  # @if jp
  # @brief ExecutionContext �¹Ծ��ֳ�ǧ�ؿ�
  #
  # �������� ExecutionContext �� Runnning ���֤ξ��� true ���֤���
  # Executioncontext �� Running �δ֡����� Executioncontext �˻��ä��Ƥ���
  # ���ƤΥ����ƥ���RT����ݡ��ͥ�Ȥ��� ExecutionContext �μ¹Լ���˱�����
  # �¹Ԥ���롣
  #
  # @param self
  #
  # @return ���ֳ�ǧ�ؿ�(ư����:true�������:false)
  #
  # @else
  #
  # @brief Check for ExecutionContext running state
  #
  # This operation shall return true if the context is in the Running state.
  # While the context is Running, all Active RTCs participating
  # in the context shall be executed according to the context��s execution
  # kind.
  #
  # @endif
  def is_running(self):
    self._rtcout.RTC_TRACE("is_running()")
    return self._running


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Ԥ򳫻�
  #
  # ExecutionContext �μ¹Ծ��֤� Runnning �Ȥ��뤿��Υꥯ�����Ȥ�ȯ�Ԥ��롣
  # ExecutionContext �ξ��֤����ܤ���� ComponentAction::on_startup ��
  # �ƤӽФ���롣
  # ���ä��Ƥ���RT����ݡ��ͥ�Ȥ�������������ޤ� ExecutionContext �򳫻�
  # ���뤳�ȤϤǤ��ʤ���
  # ExecutionContext ��ʣ���󳫻�/��ߤ򷫤��֤����Ȥ��Ǥ��롣
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Start ExecutionContext
  #
  # Request that the context enter the Running state. 
  # Once the state transition occurs, the ComponentAction::on_startup 
  # operation will be invoked.
  # An execution context may not be started until the RT components that
  # participate in it have been initialized.
  # An execution context may be started and stopped multiple times.
  #
  # @endif
  def start(self):
    self._rtcout.RTC_TRACE("start()")
    if self._running:
      return RTC.PRECONDITION_NOT_MET

    for comp in self._comps:
      comp._sm.on_startup()

    self._running = True

    self._worker._cond.acquire()
    self._worker._running = True
    self._worker._cond.notify()
    self._worker._cond.release()

    try:
      self.activate()
    except:
      self._running = False

      self._worker._cond.acquire()
      self._worker._running = False
      self._worker._cond.notify()
      self._worker._cond.release()
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    return RTC.RTC_OK


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Ԥ����
  #
  # ExecutionContext �ξ��֤� Stopped �Ȥ��뤿��Υꥯ�����Ȥ�ȯ�Ԥ��롣
  # ���ܤ�ȯ���������ϡ� ComponentAction::on_shutdown ���ƤӽФ���롣
  # ���ä��Ƥ���RT����ݡ��ͥ�Ȥ���λ�������� ExecutionContext ����ߤ���
  # ɬ�פ����롣
  # ExecutionContext ��ʣ���󳫻�/��ߤ򷫤��֤����Ȥ��Ǥ��롣
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Stop ExecutionContext
  #
  # Request that the context enter the Stopped state. 
  # Once the transition occurs, the ComponentAction::on_shutdown operation
  # will be invoked.
  # An execution context must be stopped before the RT components that
  # participate in it are finalized.
  # An execution context may be started and stopped multiple times.
  #
  # @endif
  def stop(self):
    self._rtcout.RTC_TRACE("stop()")
    if not self._running:
      return RTC.PRECONDITION_NOT_MET

    self._running = False
    self._worker._cond.acquire()
    self._worker._running = False
    self._worker._cond.release()

    for comp in self._comps:
      comp._sm.on_shutdown()

    #self.wait()
    return RTC.RTC_OK


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Լ���(Hz)���������
  #
  # Active ���֤ˤ�RT����ݡ��ͥ�Ȥ��¹Ԥ�������(ñ��:Hz)��������롣
  #
  # @param self
  #
  # @return ��������(ñ��:Hz)
  #
  # @else
  #
  # @brief Get ExecutionRate
  #
  # This operation shall return the rate (in hertz) at which its Active
  # participating RTCs are being invoked.
  #
  # @endif
  def get_rate(self):
    self._rtcout.RTC_TRACE("get_rate()")
    return self._profile.rate


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Լ���(Hz)�����ꤹ��
  #
  # Active ���֤ˤ�RT����ݡ��ͥ�Ȥ��¹Ԥ�������(ñ��:Hz)�����ꤹ�롣
  # �¹Լ������ѹ��ϡ� DataFlowComponentAction �� on_rate_changed �ˤ�ä�
  # ��RT����ݡ��ͥ�Ȥ���ã����롣
  #
  # @param self
  # @param rate ��������(ñ��:Hz)
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Set ExecutionRate
  #
  # This operation shall set the rate (in hertz) at which this context��s 
  # Active participating RTCs are being called.
  # If the execution kind of the context is PERIODIC, a rate change shall
  # result in the invocation of on_rate_changed on any RTCs realizing
  # DataFlowComponentAction that are registered with any RTCs participating
  # in the context.
  #
  # @endif
  def set_rate(self, rate):
    self._rtcout.RTC_TRACE("set_rate(%f)", rate)
    if rate > 0.0:
      self._profile.rate = rate
      self._period.set_time(1.0/rate)
      if self._period.toDouble() == 0.0:
        self._nowait = True

      for comp in self._comps:
        comp._sm.on_rate_changed()
      return RTC.RTC_OK
    return RTC.BAD_PARAMETER


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ򥢥��ƥ��ֲ�����
  #
  # Inactive ���֤ˤ���RT����ݡ��ͥ�Ȥ�Active �����ܤ����������ƥ��ֲ����롣
  # �������ƤФ줿��̡� on_activate ���ƤӽФ���롣
  # ���ꤷ��RT����ݡ��ͥ�Ȥ����üԥꥹ�Ȥ˴ޤޤ�ʤ����ϡ� BAD_PARAMETER 
  # ���֤���롣
  # ���ꤷ��RT����ݡ��ͥ�Ȥξ��֤� Inactive �ʳ��ξ��ϡ�
  #  PRECONDITION_NOT_MET ���֤���롣
  #
  # @param self
  # @param comp �����ƥ��ֲ��о�RT����ݡ��ͥ��
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Activate a RT-component
  #
  # The given participant RTC is Inactive and is therefore not being invoked
  # according to the execution context��s execution kind. This operation
  # shall cause the RTC to transition to the Active state such that it may
  # subsequently be invoked in this execution context.
  # The callback on_activate shall be called as a result of calling this
  # operation. This operation shall not return until the callback has
  # returned, and shall result in an error if the callback does.
  #
  # @endif
  def activate_component(self, comp):
    self._rtcout.RTC_TRACE("activate_component()")
    for compIn in self._comps:
      if compIn._ref._is_equivalent(comp):
        if not compIn._sm._sm.isIn(RTC.INACTIVE_STATE):
          return RTC.PRECONDITION_NOT_MET
        compIn._sm._sm.goTo(RTC.ACTIVE_STATE)
        return RTC.RTC_OK

    return RTC.BAD_PARAMETER


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ��󥢥��ƥ��ֲ�����
  #
  # Inactive ���֤ˤ���RT����ݡ��ͥ�Ȥ��󥢥��ƥ��ֲ�����
  # Inactive �����ܤ����롣
  # �������ƤФ줿��̡� on_deactivate ���ƤӽФ���롣
  # ���ꤷ��RT����ݡ��ͥ�Ȥ����üԥꥹ�Ȥ˴ޤޤ�ʤ����ϡ� BAD_PARAMETER 
  # ���֤���롣
  # ���ꤷ��RT����ݡ��ͥ�Ȥξ��֤� Active �ʳ��ξ��ϡ�
  # PRECONDITION_NOT_MET ���֤���롣
  #
  # @param self
  # @param comp �󥢥��ƥ��ֲ��о�RT����ݡ��ͥ��
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Deactivate a RT-component
  #
  # The given RTC is Active in the execution context. Cause it to transition 
  # to the Inactive state such that it will not be subsequently invoked from
  # the context unless and until it is activated again.
  # The callback on_deactivate shall be called as a result of calling this
  # operation. This operation shall not return until the callback has 
  # returned, and shall result in an error if the callback does.
  #
  # @endif
  def deactivate_component(self, comp):
    self._rtcout.RTC_TRACE("deactivate_component()")
    for compIn in self._comps:
      if compIn._ref._is_equivalent(comp):
        if not compIn._sm._sm.isIn(RTC.ACTIVE_STATE):
          return RTC.PRECONDITION_NOT_MET
        compIn._sm._sm.goTo(RTC.INACTIVE_STATE)
        count_ = 0
        usec_per_sec_ = 1.0e6
        sleeptime_ = 10.0 * usec_per_sec_ / float(self.get_rate())
        self._rtcout.RTC_PARANOID("Sleep time is %f [us]", sleeptime_)
        while compIn._sm._sm.isIn(RTC.ACTIVE_STATE):
          self._rtcout.RTC_TRACE("Waiting to be the INACTIVE state %d %f", (count_, float(time.time())))
          time.sleep(sleeptime_/usec_per_sec_)
          if count_ > 1000:
            self._rtcout.RTC_ERROR("The component is not responding.")
            break
          count_ += 1
        if compIn._sm._sm.isIn(RTC.INACTIVE_STATE):
          self._rtcout.RTC_TRACE("The component has been properly deactivated.")
          return RTC.RTC_OK
        self._rtcout.RTC_ERROR("The component could not be deactivated.")
        return RTC.RTC_ERROR

    return RTC.BAD_PARAMETER


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ�ꥻ�åȤ���
  #
  # Error ���֤�RT����ݡ��ͥ�Ȥ��������ߤ롣
  # �������ƤФ줿��̡� on_reset ���ƤӽФ���롣
  # ���ꤷ��RT����ݡ��ͥ�Ȥ����üԥꥹ�Ȥ˴ޤޤ�ʤ����ϡ� BAD_PARAMETER
  # ���֤���롣
  # ���ꤷ��RT����ݡ��ͥ�Ȥξ��֤� Error �ʳ��ξ��ϡ� PRECONDITION_NOT_MET
  # ���֤���롣
  #
  # @param self
  # @param comp �ꥻ�å��о�RT����ݡ��ͥ��
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Reset a RT-component
  #
  # Attempt to recover the RTC when it is in Error.
  # The ComponentAction::on_reset callback shall be invoked. This operation
  # shall not return until the callback has returned, and shall result in an
  # error if the callback does. If possible, the RTC developer should
  # implement that callback such that the RTC may be returned to a valid
  # state.
  #
  # @endif
  def reset_component(self, comp):
    self._rtcout.RTC_TRACE("reset_component()")
    for compIn in self._comps:
      if compIn._ref._is_equivalent(comp):
        if not compIn._sm._sm.isIn(RTC.ERROR_STATE):
          return RTC.PRECONDITION_NOT_MET
        compIn._sm._sm.goTo(RTC.INACTIVE_STATE)
        return RTC.RTC_OK

    return RTC.BAD_PARAMETER


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥξ��֤��������
  #
  # ���ꤷ��RT����ݡ��ͥ�Ȥξ���(LifeCycleState)��������롣
  # ���ꤷ��RT����ݡ��ͥ�Ȥ����üԥꥹ�Ȥ˴ޤޤ�ʤ����ϡ� CREATED_STATE 
  # ���֤���롣
  #
  # @param self
  # @param comp ���ּ����о�RT����ݡ��ͥ��
  #
  # @return ���ߤξ���(LifeCycleState)
  #
  # @else
  #
  # @brief Get RT-component's state
  #
  # This operation shall report the LifeCycleState of the given participant
  # RTC.
  #
  # @endif
  def get_component_state(self, comp):
    self._rtcout.RTC_TRACE("get_component_state()")
    for compIn in self._comps:
      if compIn._ref._is_equivalent(comp):
        return compIn._sm._sm.getState()

    return RTC.CREATED_STATE


  ##
  # @if jp
  # @brief ExecutionKind ���������
  #
  # �� ExecutionContext �� ExecutionKind ���������
  #
  # @param self
  #
  # @return ExecutionKind
  #
  # @else
  #
  # @brief Get the ExecutionKind
  #
  # This operation shall report the execution kind of the execution context.
  #
  # @endif
  def get_kind(self):
    self._rtcout.RTC_TRACE("get_kind()")
    return self._profile.kind


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ��ɲä���
  #
  # ���ꤷ��RT����ݡ��ͥ�Ȥ򻲲üԥꥹ�Ȥ��ɲä��롣
  # �ɲä��줿RT����ݡ��ͥ�Ȥ� attach_context ���ƤФ졢Inactive ���֤�����
  # ���롣
  # ���ꤵ�줿RT����ݡ��ͥ�Ȥ�null�ξ��ϡ�BAD_PARAMETER ���֤���롣
  # ���ꤵ�줿RT����ݡ��ͥ�Ȥ� DataFlowComponent �ʳ��ξ��ϡ�
  # BAD_PARAMETER ���֤���롣
  #
  # @param self
  # @param comp �ɲ��о�RT����ݡ��ͥ��
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Add a RT-component
  #
  # The operation causes the given RTC to begin participating in the
  # execution context.
  # The newly added RTC will receive a call to 
  # LightweightRTComponent::attach_context and then enter the Inactive state.
  #
  # @endif
  def add_component(self, comp):
    self._rtcout.RTC_TRACE("add_component()")
    if CORBA.is_nil(comp):
      return RTC.BAD_PARAMETER
    try:
      dfp_  = comp._narrow(OpenRTM.DataFlowComponent)
      rtc_  = comp._narrow(RTC.RTObject)
      if CORBA.is_nil(dfp_) or CORBA.is_nil(rtc_):
        return RTC.BAD_PARAMETER

      id_   = dfp_.attach_context(self._ref)
      comp_ = self.Comp(ref=comp, dfp=dfp_, id=id_)
      self._comps.append(comp_)
      self._profile.participants.append(rtc_)
      return RTC.RTC_OK
    except CORBA.Exception:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      return RTC.BAD_PARAMETER

    return RTC.RTC_OK


  def bindComponent(self, rtc):
    self._rtcout.RTC_TRACE("bindComponent()")
    if rtc is None:
      return RTC.BAD_PARAMETER

    comp_ = rtc.getObjRef()
    dfp_  = comp_._narrow(OpenRTM.DataFlowComponent)
    id_   = rtc.bindContext(self._ref)
    if id_ < 0 or id_ > OpenRTM_aist.ECOTHER_OFFSET:
      self._rtcout.RTC_ERROR("bindContext returns invalid id: %d", id_)
      return RTC.RTC_ERROR

    self._rtcout.RTC_DEBUG("bindContext returns id = %d", id_)
    # rtc is owner of this EC
    self._comps.append(self.Comp(ref=comp_, dfp=dfp_, id=id_))
    self._profile.owner = dfp_
    return RTC.RTC_OK


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ򻲲üԥꥹ�Ȥ���������
  #
  # ���ꤷ��RT����ݡ��ͥ�Ȥ򻲲üԥꥹ�Ȥ��������롣
  # ������줿RT����ݡ��ͥ�Ȥ� detach_context ���ƤФ�롣
  # ���ꤵ�줿RT����ݡ��ͥ�Ȥ����üԥꥹ�Ȥ���Ͽ����Ƥ��ʤ����ϡ�
  # BAD_PARAMETER ���֤���롣
  #
  # @param self
  # @param comp ����о�RT����ݡ��ͥ��
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Remove the RT-component from participant list
  #
  # This operation causes a participant RTC to stop participating in the
  # execution context.
  # The removed RTC will receive a call to
  # LightweightRTComponent::detach_context.
  #
  # @endif
  def remove_component(self, comp):
    self._rtcout.RTC_TRACE("remove_component()")
    len_ = len(self._comps)
    for i in range(len_):
      idx = (len_ - 1) - i
      if self._comps[idx]._ref._is_equivalent(comp):
        self._comps[idx]._ref.detach_context(self._comps[idx]._sm.ec_id)
        del self._comps[idx]
        rtcomp = comp._narrow(RTC.RTObject)
        if CORBA.is_nil(rtcomp):
          self._rtcout.RTC_ERROR("Invalid object reference.")
          return RTC.RTC_ERROR
        OpenRTM_aist.CORBA_SeqUtil.erase_if(self._profile.participants,
                                            self.find_participant(rtcomp))
        return RTC.RTC_OK

    return RTC.BAD_PARAMETER


  ##
  # @if jp
  # @brief ExecutionContextProfile ���������
  #
  # �� ExecutionContext �Υץ�ե������������롣
  #
  # @param self
  #
  # @return ExecutionContextProfile
  #
  # @else
  #
  # @brief Get the ExecutionContextProfile
  #
  # This operation provides a profile ��descriptor�� for the execution 
  # context.
  #
  # @endif
  def get_profile(self):
    self._rtcout.RTC_TRACE("get_profile()")
    return self._profile


  class find_participant:
    def __init__(self, comp):
      self._comp = comp
      return

    def __call__(self, comp):
      return self._comp._is_equivalent(comp)

      
  ##
  # @if jp
  # @class Comp
  # @brief ����ݡ��ͥ�ȴ������������饹
  # @else
  # @endif
  class Comp:
    def __init__(self, ref=None, dfp=None, id=None, comp=None):
      if comp is None:
        self._ref = ref
        self._sm = PeriodicExecutionContext.DFP(dfp,id)
      else:
        self._ref = comp._ref
        self._sm  = PeriodicExecutionContext.DFP(comp._sm._obj,comp._sm.ec_id)

  ##
  # @if jp
  # @class Worker
  # @brief ExecutionContext ��ư���饹
  #
  # �¹Խ����˴ؤ�����¾����ʤɡ��ºݤν�����ƻ롦���椹�뤿��Υ��饹��
  #
  # @since 0.4.0
  #
  # @else
  #
  # @endif
  class Worker:
    
    ##
    # @if jp
    # @brief ���󥹥ȥ饯��
    #
    # ���󥹥ȥ饯��
    #
    # @param self
    #
    # @else
    # @brief Constructor
    # @endif
    def __init__(self):
      self._mutex = threading.RLock()
      self._cond = threading.Condition(self._mutex)
      self._running = False

##
# @if jp
# @brief ExecutionContext ����������
#
# ExecutionContext ��ư�ѥե����ȥ����Ͽ���롣
#
# @param manager �ޥ͡����㥪�֥�������
#
# @else
#
# @endif
def PeriodicExecutionContextInit(manager):
  manager.registerECFactory("PeriodicExecutionContext",
                            OpenRTM_aist.PeriodicExecutionContext,
                            OpenRTM_aist.ECDelete)
