#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file PeriodicTask.py
# @brief Periodic task template class
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

import threading
import time
import OpenRTM_aist

##
# @if jp
# @class ��������������åɼ¹ԥ��饹
#
# ����δؿ�������¹Ԥ��뤿��Υ���åɥ��֥������Ȥ�¸����롣
# ���Ѽ��ϰʲ����̤ꡣ
#
# task; // ���󥹥�������
# task.setTask(TaskFuncBase(obj, mem_func)); // �¹Ԥ���ؿ���Ϳ����
# task.activate(); // ����åɤ򥹥����Ȥ�����
#
# task.suspend(); // �����¹Ԥ�ߤ��
# task.signal(); // 1���������¹�
# task.resume(); // �����¹Ԥ�Ƴ�
#
# task.finalize(); // ��������λ������
# 
# @else
# @brief
#
# @endif
#
class PeriodicTask(OpenRTM_aist.Task):
  """
  """

  ##
  # @if jp
  # @brief ctor
  # @else
  # @brief ctor
  # @endif
  #
  def __init__(self):
    OpenRTM_aist.Task.__init__(self)
    self._period         = OpenRTM_aist.TimeValue(0.0)
    self._nowait         = False
    self._func           = 0
    self._deleteInDtor   = True
    self._alive          = self.alive_t(False)
    self._suspend        = self.suspend_t(False)

    # variables for execution time measurement
    self._execMeasure    = False
    self._execCount      = 0
    self._execCountMax   = 10
    self._execStat       = self.statistics_t()
    self._execTime       = OpenRTM_aist.TimeMeasure()

    # variables for period time measurement
    self._periodMeasure  = False
    self._periodCount    = 0
    self._periodCountMax = 10
    self._periodStat     = self.statistics_t()
    self._periodTime     = OpenRTM_aist.TimeMeasure()

    return

    
  ##
  # @if jp
  # @brief dtor
  # @else
  # @brief dtor
  # @endif
  #
  def __del__(self, Task=OpenRTM_aist.Task):
    self.finalize()
    self.wait()
    Task.__del__(self)
    return
  
    
  ##
  # @if jp
  # @brief �������¹Ԥ򳫻Ϥ���
  #
  # �������μ¹Ԥ򳫻Ϥ��뤿��˥���åɤ򥹥����Ȥ����롣  ��������
  # ����˳��Ϥ��줿���� true ���֤ꡢ���Ǥ˥����������ϺѤߡ��ޤ�
  # �ϼ¹Ԥ��륿���������ꤵ��Ƥ��ʤ���� false ���֤���
  #
  # @return true: ���ﳫ�ϡ�false: ����åɺѤߤ���������̤����Ǥ��롣
  #
  # @else
  # @brief Starting the task
  #
  # Starting a thread to execute a task.  If the task/thread is
  # started properly, it will return 'TRUE'.  if the task/thread
  # are already started or task function object is not set, 'FALSE'
  # will be returned.
  #
  # @return true: normal start, false: already started  or task is not set
  #
  # @endif
  #
  # virtual void activate();
  def activate(self):
    guard = OpenRTM_aist.ScopedLock(self._alive.mutex)
    if not self._func:
      return

    if self._alive.value:
      return

    self._alive.value = True
    OpenRTM_aist.Task.activate(self)
    return


  ##
  # @if jp
  # @brief �������¹Ԥ�λ����
  #
  # �¹���Υ�������λ���롣
  #
  # @else
  # @brief Finalizing the task
  #
  # Finalizing the task running.
  #
  # @endif
  #
  # virtual void finalize();
  def finalize(self):
    guard = OpenRTM_aist.ScopedLock(self._alive.mutex)
    self._alive.value = False

    self._suspend.cond.acquire()
    self._suspend.suspend = False
    self._suspend.cond.notify()
    self._suspend.cond.release()
    return


  ##
  # @if jp
  # @brief �������¹Ԥ����Ǥ���
  #
  # �¹���Υ����������Ǥ��롣
  #
  # @else
  # @brief Suspending the task
  #
  # Suspending the task running.
  #
  # @endif
  #
  # virtual int suspend(void);
  def suspend(self):
    self._suspend.cond.acquire()
    self._suspend.suspend = True
    self._suspend.cond.release()
    return 0
    

  ##
  # @if jp
  # @brief ���Ǥ���Ƥ��륿������Ƴ�����
  #
  # ���Ǥ���Ƥ��륿������Ƴ�����
  #
  # @else
  # @brief Resuming the suspended task
  #
  # Resuming the suspended task
  #
  # @endif
  #
  # virtual int resume(void);
  def resume(self):
    self._periodTime.reset()
    self._execTime.reset()
    self._suspend.cond.acquire()
    self._suspend.suspend = False
    self._suspend.cond.notify()
    self._suspend.cond.release()
    return 0


  ##
  # @if jp
  # @brief ���Ǥ���Ƥ��륿������1���������¹Ԥ���
  #
  # ���Ǥ���Ƥ��륿������1���������¹Ԥ���
  #
  # @else
  # @brief Executing the suspended task one tick
  #
  # Executing the suspended task one tick
  #
  # @endif
  #
  # virtual void signal();
  def signal(self):
    self._suspend.cond.acquire()
    self._suspend.cond.notify()
    self._suspend.cond.release()
    return


  ##
  # @if jp
  # @brief �������¹Դؿ��򥻥åȤ���
  #
  # @param func int (*)() ���δؿ��ݥ���
  #
  # @else
  # @brief Setting task execution function
  #
  # @param func Set int (*)() type function pointer
  #
  # @endif
  #
  # virtual bool setTask(TaskFuncBase* func, bool delete_in_dtor = true);
  def setTask(self, func, delete_in_dtor = True):
    if not func:
      return False

    self._deleteInDtor = delete_in_dtor
    self._func = func
    return True

  
  ##
  # @if jp
  # @brief �������¹Լ����򥻥åȤ���
  #
  # @param period �¹Լ��� [sec]
  #
  # @else
  # @brief Setting task execution period
  #
  # @param period Execution period [sec]
  #
  # @endif
  #
  # virtual void setPeriod(double period);
  # virtual void setPeriod(TimeValue& period);
  def setPeriod(self, period):
    if type(period) == float:
      self._period = OpenRTM_aist.TimeValue(period)
    else:
      self._period = period
    
    if self._period.sec() == 0 and self._period.usec() == 0:
      self._nowait = True
      return

    self._nowait = False
    return


  ##
  # @if jp
  # @brief �������ؿ��¹Ի��ַ�¬��ͭ���ˤ��뤫
  # @else
  # @brief 
  # @endif
  #
  # virtual void executionMeasure(bool value);
  def executionMeasure(self, value):
    self._execMeasure = value
    return

    
  ##
  # @if jp
  # @brief �������ؿ��¹Ի��ַ�¬����
  # @else
  # @brief 
  # @endif
  #
  # virtual void executionMeasureCount(int n);
  def executionMeasureCount(self, n):
    self._execCountMax = n
    return
    

  ##
  # @if jp
  # @brief �������������ַ�¬��ͭ���ˤ��뤫
  # @else
  # @brief 
  # @endif
  #
  # virtual void periodicMeasure(bool value);
  def periodicMeasure(self, value):
    self._periodMeasure = value
    return

  ##
  # @if jp
  # @brief �������������ַ�¬����
  # @else
  # @brief 
  # @endif
  #
  # virtual void periodicMeasureCount(int n);
  def periodicMeasureCount(self, n):
    self._periodCountMax = n
    return


  ##
  # @if jp
  # @brief �������ؿ��¹Ի��ַ�¬��̤����
  # @else
  # @brief 
  # @endif
  #
  # virtual TimeMeasure::Statistics getExecStat();
  def getExecStat(self):
    guard = OpenRTM_aist.ScopedLock(self._execStat.mutex)
    return self._execStat.stat
    
    
  ##
  # @if jp
  # @brief �������������ַ�¬��̤����
  # @else
  # @brief 
  # @endif
  #
  # virtual TimeMeasure::Statistics getPeriodStat();
  def getPeriodStat(self):
    guard = OpenRTM_aist.ScopedLock(self._periodStat.mutex)
    return self._periodStat.stat
    

  ## virtual int svc();
  def svc(self):

    while self._alive.value: # needs lock?
      if self._periodMeasure:
        self._periodTime.tack()
        
      # wait if suspended
      self._suspend.cond.acquire()
      if self._suspend.suspend:
        self._suspend.cond.wait()
        # break if finalized
        if not self._alive.value:
          self._suspend.cond.release()
          return 0
      self._suspend.cond.release()
          
      if self._periodMeasure:
        self._periodTime.tick()

      # task execution
      if self._execMeasure:
        self._execTime.tick()

      self._func()
      if self._execMeasure:
        self._execTime.tack()

      # wait for next period
      self.updateExecStat()
      self.sleep()
      self.updatePeriodStat()


    return 0
        
        
  ## virtual void sleep();
  def sleep(self):
    if self._nowait:
      return

    sleep_sec = self._period - self._execTime.interval()

    if sleep_sec.toDouble() < 0:
      return

    time.sleep(sleep_sec.toDouble())
    return


  ## virtual void updateExecStat();
  def updateExecStat(self):
    if self._execCount > self._execCountMax:
      guard = OpenRTM_aist.ScopedLock(self._execStat.mutex)
      self._execStat.stat = self._execTime.getStatistics()
      self._execCount = 0

    self._execCount += 1
    return


  ## virtual void updatePeriodStat();
  def updatePeriodStat(self):
    if self._periodCount > self._periodCountMax:
      guard = OpenRTM_aist.ScopedLock(self._periodStat.mutex)
      self._periodStat.stat = self._periodTime.getStatistics()
      self_periodCount = 0

    self._periodCount += 1
    return


  # alive flag
  class alive_t:
    def __init__(self, val):
      self.value = val
      self.mutex = threading.RLock()
      return

  # suspend flag
  class suspend_t:
    def __init__(self, sus):
      self.suspend = sus
      self.mutex = threading.RLock()
      self.cond = threading.Condition(self.mutex)
      return

      
  # time measurement statistics struct
  class statistics_t:
    def __init__(self):
      self.stat = OpenRTM_aist.TimeMeasure.Statistics()
      self.mutex = threading.RLock()


