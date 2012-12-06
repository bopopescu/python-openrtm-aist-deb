#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file Async.py
# @brief Asynchronous function invocation helper class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2009
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#
# $Id$
#
#

import threading
import OpenRTM_aist


class Async_t(OpenRTM_aist.Task):

  def __init__(self, obj, func, *args):
    OpenRTM_aist.Task.__init__(self)
    self._obj        = obj
    self._func       = func
    self._finished   = False
    self._args       = args
    self._mutex      = threading.RLock()

  def invoke(self):
    self.activate()


  def finished(self):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    return self._finished


  def svc(self):
    if len(self._args) > 0:
      self._func(self._obj, self._args)
    else:
      self._func(self._obj)

    guard = OpenRTM_aist.ScopedLock(self._mutex)
    self._finished = True
    return 0


class Async_ref_t(OpenRTM_aist.Task):

  def __init__(self, obj, func, *args):
    OpenRTM_aist.Task.__init__(self)
    self._obj        = obj
    self._func       = func
    self._args       = args
    self._finished   = False
    

  def invoke(self):
    self.activate()


  def finished(self):
    return self._finished
  

  def svc(self):
    if len(self._args) > 0:
      self._func(self._obj, self._args)
    else:
      self._func(self._obj)

    self._finished = True
    return 0
  
  
##
# @if jp
# @brief ��Ʊ�����С��ؿ��ƤӽФ��إ�ѡ��ؿ�
#
# ���С��ؿ�����Ʊ���˸Ƥ֤���Υإ�ѡ��ؿ�
# ��
#
#  class A
#  {
#  public:
#    // ���֤Τ�����ؿ�
#    void hoge() {
#      for (int i(0); i < 5; ++i) {
#        std::cout << "hoge" << std::endl;
#        sleep(1);
#      }
#    }
#    // ���֤Τ�����ؿ�
#    void munya(const char* msg) {
#      for (int i(0); i < 10; ++i) {
#        std::cout << "message is: " << msg << std::endl;
#        sleep(1);
#      }
#    }
#    int add_one(int val) {
#      return val + 1;
#    }
#  };
# �����ͤʥ��饹�Υ��֥������Ȥ��Ф��ơ�
#
#  A a;
#  Async* invoker0(AsyncInvoker(&a,
#                               std::mem_fun(&A::hoge)));
#  Async* invoker1(AsyncInvoker(&a,
#                               std::bind2nd(std::mem_fun(&A::munya),
#                                            "�ۤ�")));
#  invoker0->invoke(); // ���������
#  invoker1->invoke(); // ���������
#
#  delete invoker0; // ɬ��������뤳��
#  delete invoker1; // ɬ��������뤳��
#
# �Τ褦����Ʊ���θƤӽФ����Ǥ��롣
# �ƤӽФ�������ͤ�������������ϡ������δؿ����֥������Ȥ��Ѱդ��롣
#
#  class add_one_functor
#  {
#    int m_val, m_ret;
#  public:
#    add_one_functor(int val) : m_val(val), m_ret(0) {}
#    void operaotr(A* obj) {
#      m_ret = obj->add_one(m_val);
#    }
#    int get_ret() {
#      return m_ret;
#    }
#  };
#
# �嵭�δؿ����֥������ȤΥ��󥹥��󥹤�����������Υݥ��󥿤��Ϥ���
#
#  add_one_functor aof(100);
#  Async* invoker2(AsyncInvoker(&a, &aof));
#  invoker2->invoke();
#  invoker2->wait();
#  std::cout << "result: " << aof.get_ret() << std::endl;
#  delete invoker2;
#
# �̾AsyncInvoker ���֤����֥������Ȥ�����Ū�˺�����ʤ����
# �ʤ�ʤ������軰������ true ���Ϥ����Ȥǡ���Ʊ���¹Ԥ���λ�����Ʊ����
# ��ưŪ�˥��󥹥��󥹤��������롣
#
# // invoker3 �Ϻ�� (delete invoker3) ���ƤϤ����ʤ�
# Async* invoker3(AsyncInvoker(&a, std::mem_fun(&A::hoge), true));
#
# // ���󥹥���������Ʊ���˼¹Ԥ��뤳�Ȥ�Ǥ��롣
# AsyncInvoker(&a, std::mem_fun(&A::hoge))->invoke();
#
# @else
#
# @endif
#
#def Async_tInvoker(func, auto_delete = False):
def Async_tInvoker(obj, func, *args):
  return Async_t(obj, func, *args)


def Async_ref_tInvoker(obj, func, *args):
  return Async_ref_t(obj, func, *args)
