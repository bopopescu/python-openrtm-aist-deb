#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ExtTrigExecutionContext.py
# @brief ExtTrigExecutionContext class
# @date $Date: 2007/09/06$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2007-2008
#    Task-intelligence Research Group,
#    Intelligent Systems Research Institute,
#    National Institute of
#        Advanced Industrial Science and Technology (AIST), Japan
#    All rights reserved.



import threading
import time

import OpenRTM_aist



##
# @if jp
# @class ExtTrigExecutionContext
# @brief ���ƥå׼¹Ԥ���ǽ�� ExecutionContext ���饹
#
# ��������μ¹Ԥ���ǽ��Periodic Sampled Data Processing(�����¹���)
# ExecutionContext���饹��
# ��������Υ᥽�åɸƤӤ����ˤ�äƻ��֤򣱼����ŤĿʤ�뤳�Ȥ��Ǥ��롣
#
# @since 0.4.0
#
# @else
# @class ExtTrigExecutionContext
# @endif
class ExtTrigExecutionContext(OpenRTM_aist.PeriodicExecutionContext):
  """
  """


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
    OpenRTM_aist.PeriodicExecutionContext.__init__(self)
    self._worker = self.Worker()
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("rtobject.exttrig_ec")

  ##
  # @if jp
  # @brief �����򣱥��ƥå׿ʤ��
  #
  # ExecutionContext�ν����򣱼���ʬ�ʤ�롣
  #
  # @param self
  #
  # @else
  #
  # @endif
  def tick(self):
    self._rtcout.RTC_TRACE("tick()")
    if not self._worker._cond.acquire():
      return
    self._worker._called = True
    self._worker._cond.notify()
    self._worker._cond.release()
    return

  ##
  # @if jp
  # @brief �� Component �ν�����ƤӽФ���
  # 
  # ExecutionContext �� attach ����Ƥ���� Component �ν�����ƤӽФ���
  # �� Component �ν�����ƤӽФ����塢���θƽФ�ȯ������ޤǵٻߤ��롣
  # 
  # @param self
  # 
  # @else
  # 
  # @endif
  # 
  def svc(self):
    self._rtcout.RTC_TRACE("svc()")
    flag = True

    while flag:
      sec_ = float(self._period.usec())/1000000.0
      self._worker._cond.acquire()
      while not self._worker._called and self._running:
        self._worker._cond.wait()
      if self._worker._called:
        self._worker._called = False
        for comp in self._comps:
          comp._sm.worker()

      self._worker._cond.release()
      flag = self._running

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
    """
    """
    
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
      self._called = False



##
# @if jp
# @brief ���� ExecutionContext ��Factory���饹����Ͽ��
#
# ����ExecutionContext����������Factory���饹��
# ExecutionContext������ObjectManager����Ͽ���롣
#
# @else
#
# @endif
def ExtTrigExecutionContextInit(manager):
  manager.registerECFactory("ExtTrigExecutionContext",
                            OpenRTM_aist.ExtTrigExecutionContext,
                            OpenRTM_aist.ECDelete)
