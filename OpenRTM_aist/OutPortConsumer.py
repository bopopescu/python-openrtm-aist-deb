#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  OutPortConsumer.py
# @brief OutPortConsumer class
# @date  $Date: 2007/09/04$
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
#
# @class OutPortConsumer
#
# @brief OutPortConsumer ���饹
#
# ���ϥݡ��ȥ��󥷥塼�ޤΤ���Υ��饹
# �ƶ�ݥ��饹�ϡ��ʲ��δؿ��μ������󶡤��ʤ���Фʤ�ʤ���
# - pull(): �ǡ�������
# - subscribeInterface(): �ǡ����������Τؤ���Ͽ
# - unsubscribeInterface(): �ǡ����������Τ���Ͽ���
#
# @since 0.4.0
#
# @else
# @class OutPortConsumer
# @brief OutPortConsumer class
# @endif
class OutPortConsumer(OpenRTM_aist.DataPortStatus):
  """
  """

  ##
  # @if jp
  # @brief Interface��³��Functor
  # @else
  # @brief Functor to subscribe the interface
  # @endif
  #
  class subscribe:
    # subscribe(const SDOPackage::NVList& prop)
    def __init__(self, prop):
      self._prop = prop
      return

    # void operator()(OutPortConsumer* consumer)
    def __call__(self, consumer):
      consumer.subscribeInterface(self._prop)
      return
    
  ##
  # @if jp
  # @brief Interface��³�����Functor
  # @else
  # @brief Functor to unsubscribe the interface
  # @endif
  #
  class unsubscribe:
    # unsubscribe(const SDOPackage::NVList& prop)
    def __init__(self, prop):
      self._prop = prop
      return

    # void operator()(OutPortConsumer* consumer)
    def __call__(self, consumer):
      consumer.unsubscribeInterface(self._prop)
      return


outportconsumerfactory = None

class OutPortConsumerFactory(OpenRTM_aist.Factory,OutPortConsumer):
  def __init__(self):
    OpenRTM_aist.Factory.__init__(self)
    pass


  def __del__(self):
    pass


  def instance():
    global outportconsumerfactory

    if outportconsumerfactory is None:
      outportconsumerfactory = OutPortConsumerFactory()

    return outportconsumerfactory

  instance = staticmethod(instance)
