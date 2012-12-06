#!/usr/bin/env/python
# -*- coding: euc-jp -*-

##
# @file Timer.py
# @brief Timer class
# @date $Date: $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2007-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import time
import threading

import OpenRTM_aist


##
# @if jp
# @class Timer
# @brief Timer���饹
# 
# ��Ͽ���줿�ꥹ�ʡ��Υ�����Хå��ؿ������ꤵ�줿���������Ū�˸ƤӽФ���
#
# @since 0.4.0
#
# @else
#
# @class Timer
# @brief Timer class
# 
# Invoke the callback function of registered listener periodically
# at the set cycle.
#
# @since 0.4.0
#
# @endif
class Timer:
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # 
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param interval �����޵�ư����
  #
  # @else
  #
  # @brief Constructor
  # 
  # Constructor
  #
  # @param interval The interval of timer
  #
  # @endif
  def __init__(self, interval):
    self._interval = interval
    self._running  = False
    self._runningMutex = threading.RLock()
    self._tasks = []
    self._taskMutex = threading.RLock()
    self._thread = threading.Thread(target=self.run)
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
    self._running = False
    try:
      self.join()
    except:
      pass
    self._thread = None

  def join(self):
    try:
      self._thread.join()
      self._thread = threading.Thread(target=self.run)
    except:
      pass

    return

  ##
  # @if jp
  # @brief Timer �ѤΥ���åɼ¹Դؿ�
  #
  # Timer �ѤΥ���åɼ¹Դؿ���
  # ��Ͽ���줿�ꥹ�ʡ��Υ�����Хå��ؿ���ƤӽФ���
  #
  # @return �¹Է��
  #
  # @else
  # @brief Thread execution function for Timer
  #
  # Thread execution function for Timer.
  # Invoke the callback function of registered listener.
  #
  # @return Execution result
  #
  # @endif
  def run(self):
    while self._running:
      self.invoke()
      if self._interval.tv_sec != 0:
        time.sleep(self._interval.tv_sec)
      elif self._interval.tv_usec:
        time.sleep(self._interval.tv_usec/1000000.0)
    return 0


  ##
  # @if jp
  # @brief Timer ����������
  #
  # Timer �ѿ�������åɤ��������������򳫻Ϥ��롣
  #
  # @param self
  #
  # @brief Start Timer task
  #
  # Create a new theread for Timer and start processing.
  #
  # @else
  #
  # @endif
  def start(self):
    guard = OpenRTM_aist.ScopedLock(self._runningMutex)
    if not self._running:
      self._running = True
      self._thread.start()
    return


  ##
  # @if jp
  # @brief Timer ���������
  #
  # @param self
  #
  # Timer ����������ߤ��롣
  #
  # @else
  #
  # @brief Stop Timer task
  #
  # Stop Timer task.
  #
  # @endif
  def stop(self):
    guard = OpenRTM_aist.ScopedLock(self._runningMutex)
    if self._running:
      self._running = False
      self.join()
    return


  ##
  # @if jp
  # @brief Timer �������¹�
  #
  # @param self
  #
  # ��Ͽ���줿�ƥꥹ�ʤε�ư�Ԥ����֤��饿���޵�ư�����򸺻����롣
  # ��ư�Ԥ����֤�����Ȥʤä��ꥹ�ʤ�¸�ߤ�����ϡ�
  # ������Хå��ؿ���ƤӽФ���
  #
  # @else
  #
  # @brief Invoke Timer task
  #
  # Subtract the interval of timer from the waiting time for invocation
  # of each registered listener.
  # If the listener whose waiting time reached 0 exists, invoke the
  # callback function.
  #
  # @endif
  def invoke(self):
    guard = OpenRTM_aist.ScopedLock(self._taskMutex)
    for i in range(len(self._tasks)):
      self._tasks[i].remains = self._tasks[i].remains - self._interval
      if self._tasks[i].remains.sign() <= 0.0:
        self._tasks[i].remains = self._tasks[i].period
        self._tasks[i].listener.invoke()
    del guard
    return

  ##
  # @if jp
  # @brief �ꥹ�ʡ���Ͽ
  #
  # �� Timer ���鵯ư���륳����Хå��ؿ��ѤΥꥹ�ʡ���ư��������ꤷ��
  # ��Ͽ���롣
  # Ʊ��ꥹ�ʡ���������Ͽ�Ѥߤξ��ϡ��ꥹ�ʡ��ε�ư��������ꤷ���ͤ�
  # �������롣
  #
  # @param self
  # @param listener ��Ͽ�оݥꥹ�ʡ�
  # @param tm �ꥹ�ʡ���ư����
  #
  # @return ��Ͽ�ꥹ�ʡ�
  #
  # @else
  #
  # @brief Register listener
  #
  # Register the listener of callback function invoked from this Timer by
  # specifying the interval.
  # If the same listener has already been regiseterd, the value specified
  # the invocation interval of listener will be updated.
  # 
  #
  # @param listener Listener for the registration
  # @param tm The invocation interval of listener
  #
  # @return ID of the registerd listener
  #
  # @endif
  # ListenerId registerListener(ListenerBase* listener, TimeValue tm);
  def registerListener(self, listener, tm):
    guard = OpenRTM_aist.ScopedLock(self._taskMutex)
    for i in range(len(self._tasks)):
      if self._tasks[i].listener == listener:
        self._tasks[i].period = tm
        self._tasks[i].remains = tm
        return listener
    self._tasks.append(self.Task(listener, tm))
    return listener


  ##
  # @if jp
  # @brief �ꥹ�ʡ���Ͽ
  #
  # ������Хå��оݥ��֥������ȡ�������Хå��оݥ᥽�åɤ���ӵ�ư������
  # ���ꤷ�ƥꥹ�ʡ�����Ͽ���롣
  #
  # @param self
  # @param obj ������Хå��оݥ��֥�������
  # @param cbf ������Хå��оݥ᥽�å�
  # @param tm �ꥹ�ʡ���ư����
  #
  # @return ��Ͽ�ꥹ�ʡ�
  #
  # @else
  #
  # @brief Register listener
  #
  # Register listener by specifying the object for callback, the method
  # for callback and the invocation interval.
  #
  # @param obj Target object for callback
  # @param cbf Target method for callback
  # @param tm The invocation interval of listener
  #
  # @return ID of the registerd listener
  #
  #
  # @endif
  #  template <class ListenerClass>
  #  ListenerId registerListenerObj(ListenerClass* obj,
  #                                 void (ListenerClass::*cbf)(),
  #                                 TimeValue tm)
  def registerListenerObj(self, obj, cbf, tm):
    return self.registerListener(OpenRTM_aist.ListenerObject(obj, cbf), tm)


  ##
  # @if jp
  # @brief �ꥹ�ʡ���Ͽ
  #
  # ������Хå��оݥ᥽�åɤȵ�ư��������ꤷ�ƥꥹ�ʡ�����Ͽ���롣
  #
  # @param self
  # @param cbf ������Хå��оݥ᥽�å�
  # @param tm �ꥹ�ʡ���ư����
  #
  # @return ��Ͽ�ꥹ�ʡ�
  #
  # @else
  #
  # @brief Register listener
  #
  # Register listener by specifying the method for callback and the
  # invocation interval.
  #
  # @param cbf Target method for callback
  # @param tm The invocation interval of listener
  #
  # @return ID of the registerd listener
  #
  # @endif
  # ListenerId registerListenerFunc(void (*cbf)(), TimeValue tm)
  def registerListenerFunc(self, cbf, tm):
    return self.registerListener(OpenRTM_aist.ListenerFunc(cbf), tm)


  ##
  # @if jp
  # @brief �ꥹ�ʡ���Ͽ���
  #
  # ���ꤷ��ID�Υꥹ�ʡ�����Ͽ�������롣
  # ���ꤷ��ID�Υꥹ�ʡ���̤��Ͽ�ξ�硢false ���֤���
  #
  # @param self
  # @param id ��Ͽ����оݥꥹ�ʡ�ID
  #
  # @return ��Ͽ������
  #
  # @else
  #
  # @brief Unregister listener
  #
  # Unregister the listener specified by ID.
  # If the listener specified by ID is not registerd, false will be returned.
  #
  # @param id ID of the unregisterd listener
  #
  # @return Unregistration result
  #
  # @endif
  # bool unregisterListener(ListenerId id);
  def unregisterListener(self, id):
    guard = OpenRTM_aist.ScopedLock(self._taskMutex)
    len_ = len(self._tasks)
    for i in range(len_):
      idx = (len_ - 1) - i
      if self._tasks[idx].listener == id:
        del self._tasks[idx]
        return True
    return False


  ##
  # @if jp
  # @class Task
  # @brief �����������ѥ��饹
  # @else
  #
  # @endif
  class Task:
    def __init__(self, lb, tm):
      self.listener = lb
      self.period = tm
      self.remains = tm
      return
