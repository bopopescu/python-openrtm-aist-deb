#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file RTCUtil.py
# @brief RTComponent utils
# @date $Date: 2007/09/11 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2007-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

from omniORB import CORBA

import RTC
import OpenRTM

##
# @if jp
#
# @brief DataFlowComponent �Ǥ��뤫Ƚ�ꤹ��
#
# ���ꤵ�줿RT����ݡ��ͥ�Ȥ� DataFlowComponent �Ǥ��뤫Ƚ�ꤹ�롣
# DataFlowComponent�� ExecutionContext �� Semantics ��
# Periodic Sampled Data Processing �ξ������Ѥ����RT����ݡ��ͥ�Ȥη�
# �Ǥ��롣
#
# @param obj Ƚ���оݤ� CORBA ���֥�������
#
# @return DataFlowComponent Ƚ����
#
# @since 0.4.0
#
# @else
#
# @endif
def isDataFlowComponent(obj):
  dfp = obj._narrow(OpenRTM.DataFlowComponent)
  return not CORBA.is_nil(dfp)


##
# @if jp
#
# @brief FsmParticipant �Ǥ��뤫Ƚ�ꤹ��
#
# ���ꤵ�줿RT����ݡ��ͥ�Ȥ� FsmParticipant �Ǥ��뤫Ƚ�ꤹ�롣
# FsmParticipant �ϡ� ExecutionContext �� Semantics ��
# Stimulus Response Processing �ξ��ˡ�������Υ���������������뤿���
# ���Ѥ����RT����ݡ��ͥ�Ȥη��Ǥ��롣
#
# @param obj Ƚ���оݤ� CORBA ���֥�������
#
# @return FsmParticipant Ƚ����
#
# @since 0.4.0
#
# @else
#
# @endif
def isFsmParticipant(obj):
  fsmp = obj._narrow(RTC.FsmParticipant)
  return not CORBA.is_nil(fsmp)


##
# @if jp
#
# @brief Fsm �Ǥ��뤫Ƚ�ꤹ��
#
# ���ꤵ�줿RT����ݡ��ͥ�Ȥ� Fsm �Ǥ��뤫Ƚ�ꤹ�롣
# Fsm �ϡ� ExecutionContext �� Semantics �� Stimulus Response Processing ��
# ���ˡ��������ܤ�������뤿������Ѥ����RT����ݡ��ͥ�Ȥη��Ǥ��롣
#
# @param obj Ƚ���оݤ� CORBA ���֥�������
#
# @return Fsm Ƚ����
#
# @since 0.4.0
#
# @else
#
# @endif
def isFsmObject(obj):
  fsm = obj._narrow(RTC.FsmObject)
  return not CORBA.is_nil(fsm)


##
# @if jp
#
# @brief multiModeComponent �Ǥ��뤫Ƚ�ꤹ��
#
# ���ꤵ�줿RT����ݡ��ͥ�Ȥ� multiModeComponent �Ǥ��뤫Ƚ�ꤹ�롣
# multiModeComponent �ϡ� ExecutionContext �� Semantics �� Modes of Operatin 
# �ξ��ˡ� Mode ��������뤿������Ѥ����RT����ݡ��ͥ�Ȥη��Ǥ��롣
#
# @param obj Ƚ���оݤ� CORBA ���֥�������
#
# @return multiModeComponent Ƚ����
#
# @since 0.4.0
#
# @else
#
# @endif
def isMultiModeObject(obj):
  mmc = obj._narrow(RTC.MultiModeObject)
  return not CORBA.is_nil(mmc)
