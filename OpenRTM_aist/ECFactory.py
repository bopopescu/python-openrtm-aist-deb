#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ECFactory.py
# @brief ExecutionContext Factory class
# @date $Date: 2007/04/13 16:06:22 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2007-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import string

import OpenRTM_aist


##
# @if jp
#
# @brief ExecutionContext�˴��Ѵؿ�
# 
# ExecutionContext�Υ��󥹥��󥹤��˴����뤿��δؿ���
#
# \param ec �˴��о�ExecutionContext�Υ��󥹥���
#
# @else
#
# @endif
def ECDelete(ec):
  del ec


##
# @if jp
# @class ECFactoryBase
# @brief ECFactoryBase ��ݥ��饹
# 
# ExecutionContext������Factory����ݥ��饹��
# ��ExecutionContext���������뤿��ζ��Factory���饹�ϡ�
# �ʲ��δؿ��μ������󶡤��ʤ���Фʤ�ʤ���
#
# public���󥿡��ե������Ȥ��ưʲ��Τ�Τ��󶡤��롣
# - name()   : �����о�ExecutionContext̾�Τμ���
# - create() : ExecutionContext���󥹥��󥹤�����
# - destroy(): ExecutionContext���󥹥��󥹤��˴�
#
# @since 0.4.0
#
# @else
#
# @endif
class ECFactoryBase :
  """
  """

  ##
  # @if jp
  #
  # @brief �����о�ExecutionContext̾�μ����Ѵؿ�(���֥��饹������)
  # 
  # �����о�ExecutionContext��̾�Τ�������뤿��δؿ���<BR>
  # ���δؿ��϶�ݥ��֥��饹�Ǽ�������ɬ�פ����롣
  #
  # @param self
  #
  # @return �����о�ExecutionContext̾��
  # 
  # @else
  # 
  # This method should be implemented in subclasses
  #
  # @endif
  def name(self):
    pass


  ##
  # @if jp
  #
  # @brief ExecutionContext�����Ѵؿ�(���֥��饹������)
  # 
  # ExecutionContext�Υ��󥹥��󥹤��������뤿��δؿ���<BR>
  # ���δؿ��϶�ݥ��֥��饹�Ǽ�������ɬ�פ����롣
  #
  # @param self
  #
  # @return ��������ExecutionContext���󥹥���
  # 
  # @else
  #
  # @endif
  def create(self):
    pass

  ##
  # @if jp
  #
  # @brief ExecutionContext�˴��Ѵؿ�(���֥��饹������)
  # 
  # ExecutionContext�Υ��󥹥��󥹤��˴����뤿��δؿ���<BR>
  # ���δؿ��϶�ݥ��֥��饹�Ǽ�������ɬ�פ����롣
  #
  # @param self
  # @param comp �˴��оݤ�ExecutionContext���󥹥���
  # 
  # @else
  #
  # @endif
  def destroy(self, comp):
    pass



##
# @if jp
# @class ECFactoryPython
# @brief ECFactoryPython ���饹
# 
# Python������ExecutionContext���󥹥��󥹤���������Factory���饹��
#
# @since 0.4.1
#
# @else
#
# @endif
class ECFactoryPython(ECFactoryBase):
  """
  """

  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  # 
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param name �����о�ExecutionContext̾��
  # @param new_func ExecutionContext�����Ѵؿ�
  # @param delete_func ExecutionContext�˴��Ѵؿ�
  # 
  # @else
  #
  # @endif
  def __init__(self, name, new_func, delete_func):
    self._name   = name
    self._New    = new_func
    self._Delete = delete_func
    
    return


  ##
  # @if jp
  #
  # @brief �����о�ExecutionContext̾�Τ����
  # 
  # �����оݤ�ExecutionContext̾�Τ�������롣
  #
  # @param self
  #
  # @return �����о�ExecutionContext̾��
  # 
  # @else
  #
  # @endif
  def name(self):
    return self._name

  ##
  # @if jp
  #
  # @brief �����о�ExecutionContext���󥹥��󥹤�����
  # 
  # �����оݤ�ExecutionContext���饹�Υ��󥹥��󥹤��������롣
  #
  # @param self
  #
  # @return ��������ExecutionContext���󥹥���
  # 
  # @else
  #
  # @endif
  def create(self):
    return self._New()

  ##
  # @if jp
  #
  # @brief �о�ExecutionContext���󥹥��󥹤��˴�
  # 
  # �о�ExecutionContext���饹�Υ��󥹥��󥹤��˴����롣
  #
  # @param self
  # @param ec �˴��о�ExecutionContext���󥹥���
  # 
  # @else
  #
  # @endif
  def destroy(self, ec):
    self._Delete(ec)
    
