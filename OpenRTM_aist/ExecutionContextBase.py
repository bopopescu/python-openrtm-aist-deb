#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ExecutionContextBase.py
# @brief ExecutionContext base class
# @date $Date: 2007/08/31$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2007-2008
#    Task-intelligence Research Group,
#    Intelligent Systems Research Institute,
#    National Institute of
#       Advanced Industrial Science and Technology (AIST), Japan
#    All rights reserved.


import OpenRTM__POA
import OpenRTM_aist

##
# @if jp
# @class ExecutionContextBase
# @brief ExecutionContext�Ѵ��쥯�饹
#
# ExecutionContext�δ��쥯�饹��
#
# @since 0.4.0
#
# @else
# @endif
class ExecutionContextBase(OpenRTM__POA.ExtTrigExecutionContextService):
  """
  """

  def __del__(self):
    return

  ##
  # @if jp
  # @brief ExecutionContext�ν�����ʤ��(���֥��饹������)
  #
  # ExecutionContext�ν����򣱼���ʬ�ʤ�롣<BR>
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  #
  # @else
  # @brief Destructor
  # @endif
  def tick(self):
    pass


  def bindComponent(self, rtc):
    pass


  def getObjeRef(self):
    pass
