#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file  InPortConsumer.py
# @brief InPortConsumer class
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
# @class InPortConsumer
#
# @brief InPortConsumer ���쥯�饹
#
# ���ϥݡ��ȥ��󥷥塼�ޤΤ������ݥ��󥿡��ե��������饹
# �ƶ�ݥ��饹�ϡ��ʲ��δؿ��μ������󶡤��ʤ���Фʤ�ʤ���
# - push(): �ǡ�������
# - clone(): �ݡ��ȤΥ��ԡ�
# - subscribeInterface(): �ǡ����������Τؤ���Ͽ
# - unsubscribeInterface(): �ǡ����������Τ���Ͽ���
#
# @since 0.4.0
#
# @else
# @class InPortConsumer
# @brief InPortConsumer class
# @endif
class InPortConsumer(OpenRTM_aist.DataPortStatus):
  """
  """



  ##
  # @if jp
  # @brief ���󥿡��ե������ץ�ե������������뤿�Υե��󥯥�
  # @else
  # @brief Functor to publish interface profile
  # @endif
  #
  class publishInterfaceProfileFunc:
    def __init__(self, prop):
      self._prop = prop

    def __call__(self, consumer):
      consumer.publishInterfaceProfile(self._prop)


  ##
  # @if jp
  # @brief ���󥿡��ե������ץ�ե������������뤿�Υե��󥯥�
  # @else
  # @brief Functor to publish interface profile
  # @endif
  #
  class subscribeInterfaceFunc:
    def __init__(self, prop):
      self._prop = prop

    def __call__(self, consumer):
      return consumer.subscribeInterface(self._prop)


inportconsumerfactory = None

class InPortConsumerFactory(OpenRTM_aist.Factory,InPortConsumer):

  def __init__(self):
    OpenRTM_aist.Factory.__init__(self)
    pass


  def __del__(self):
    pass


  def instance():
    global inportconsumerfactory

    if inportconsumerfactory is None:
      inportconsumerfactory = InPortConsumerFactory()

    return inportconsumerfactory

  instance = staticmethod(instance)

