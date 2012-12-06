#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# \file DataFlowComponentBase.py
# \brief DataFlowParticipant RT-Component base class
# \date $Date: 2007/09/04$
# \author Noriaki Ando <n-ando@aist.go.jp>
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import OpenRTM_aist


##
# @if jp
# @class DataFlowComponentBase
# @brief DataFlowComponentBase ���饹
#
# �ǡ����ե���RTComponent�δ��쥯�饹��
# �Ƽ�ǡ����ե���RTComponent�����������ϡ��ܥ��饹��Ѿ�������Ǽ���
# ���롣
#
# @since 0.4.0
#
# @else
# @class DataFlowComponentBase
# @brief DataFlowComponentBase class
# @endif
class DataFlowComponentBase(OpenRTM_aist.RTObject_impl):
  """
  """


  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param manager �ޥ͡����㥪�֥�������
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, manager):
    OpenRTM_aist.RTObject_impl.__init__(self, manager)


  ##
  # @if jp
  # @brief �����(���֥��饹������)
  #
  # �ǡ����ե��� RTComponent �ν������¹Ԥ��롣
  # �ºݤν���������ϡ��ƶ�ݥ��饹��˵��Ҥ��롣
  #
  # @param self
  #
  # @else
  # @brief Initialization
  # @endif
  def init(self):
    pass


