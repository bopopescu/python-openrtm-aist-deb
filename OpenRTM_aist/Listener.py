#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file Listener.py
# @brief Listener class
# @date $Date: 2007/08/23$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2007-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.



##
# @if jp
# @class ListenerBase
# @brief ListenerBase ���饹
#
# �����ޡ�����Ͽ����ꥹ�ʡ�����ݥ��󥿡��ե��������饹��
#
# @since 0.4.0
#
# @else
# @class ListenerBase
# @brief ListenerBase class
# @endif
class ListenerBase:
  """
  """

  ##
  # @if jp
  # @brief ������Хå�����(���֥��饹������)
  #
  # ������Хå������Ѵؿ�<BR>
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  #
  # @else
  #
  # @endif
  def invoke(self):
    pass



##
# @if jp
# @class ListenerObject
# @brief ListenerObject ���饹
#
# �����ޡ�����Ͽ����ꥹ�ʡ��Ѵ��쥯�饹��
#
# @since 0.4.0
#
# @else
# @class ListenerObject
# @brief ListenerObject class
# @endif
class ListenerObject(ListenerBase):
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param obj �ꥹ�ʡ����֥�������
  # @param cbf ������Хå��Ѵؿ�
  #
  # @else
  #
  # @endif
  def __init__(self,obj,cbf):
    self.obj = obj
    self.cbf = cbf


  ##
  # @if jp
  # @brief ������Хå��ѽ���
  #
  # ������Хå������Ѵؿ�
  #
  # @param self
  #
  # @else
  #
  # @endif
  def invoke(self):
    self.cbf(self.obj)



##
# @if jp
# @class ListenerFunc
# @brief ListenerFunc ���饹
#
# ������Хå��ѥ��֥������ȡ�
#
# @since 0.4.0
#
# @else
# @class ListenerFunc
# @brief ListenerFunc class
# @endif
class ListenerFunc(ListenerBase):
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param cbf ������Хå��Ѵؿ�
  #
  # @else
  #
  # @endif
  def __init__(self,cbf):
    self.cbf = cbf


  ##
  # @if jp
  # @brief ������Хå�����
  #
  # ������Хå������Ѵؿ�
  #
  # @param self
  #
  # @else
  #
  # @endif
  def invoke(self):
    self.cbf()
