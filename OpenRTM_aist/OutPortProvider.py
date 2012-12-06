#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  OutPortProvider.py
# @brief OutPortProvider class
# @date  $Date: 2007/09/05$
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
# @class OutPortProvider
# @brief OutPortProvider
#
# - Port ���Ф��Ʋ����󶡤��Ƥ��뤫��������롣
#   PortProfile �� properties �� Provider �˴ؤ��������ɲä��롣
#
# (��) OutPort �� Provide ������
#
# OutPortCorbaProvider ���ʲ������
#  - dataport.interface_type = CORBA_Any
#  - dataport.dataflow_type = Push, Pull
#  - dataport.subscription_type = Once, New, Periodic
# 
# @since 0.4.0
#
# @else
#
#
# @endif
class OutPortProvider(OpenRTM_aist.DataPortStatus):
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

    def __call__(self, provider):
      provider.publishInterfaceProfile(self._prop)


  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self):
    self._properties = []
    self._portType         = ""
    self._dataType         = ""
    self._interfaceType    = ""
    self._dataflowType     = ""
    self._subscriptionType = ""
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("OutPortProvider")


  ##
  # @if jp
  # @brief InterfaceProfile������������
  #
  # InterfaceProfile�����������롣
  # �����ǻ��ꤹ��ץ�ѥƥ�������� NameValue ���֥������Ȥ�
  # dataport.interface_type �ͤ�Ĵ�١������ݡ��Ȥ����ꤵ��Ƥ���
  # ���󥿡��ե����������פȰ��פ�����Τ߾����������롣
  #
  # @param self
  # @param prop InterfaceProfile�����������ץ�ѥƥ�
  #
  # @else
  #
  # @endif
  # virtual void publishInterfaceProfile(SDOPackage::NVList& properties);
  def publishInterfaceProfile(self, prop):
    OpenRTM_aist.NVUtil.appendStringValue(prop, "dataport.interface_type", self._interfaceType)
    OpenRTM_aist.NVUtil.append(prop, self._properties)

  ##
  # @if jp
  # @brief Interface������������
  #
  # Interface�����������롣
  # �����ǻ��ꤹ��ץ�ѥƥ�������� NameValue ���֥������Ȥ�
  # dataport.interface_type �ͤ�Ĵ�١������ݡ��Ȥ����ꤵ��Ƥ��ʤ����
  # NameValue �˾�����ɲä��롣
  # ���Ǥ�Ʊ�쥤�󥿡��ե���������Ͽ�Ѥߤξ��ϲ���Ԥ�ʤ���
  #
  # @param self
  # @param prop InterfaceProfile�����������ץ�ѥƥ�
  #
  # @else
  #
  # @endif
  # virtual bool publishInterface(SDOPackage::NVList& properties);
  def publishInterface(self, prop):
    if not OpenRTM_aist.NVUtil.isStringValue(prop,"dataport.interface_type",self._interfaceType):
      return False

    OpenRTM_aist.NVUtil.append(prop,self._properties)
    return True


  ##
  # @if jp
  # @brief �ݡ��ȥ����פ����ꤹ��
  #
  # �����ǻ��ꤷ���ݡ��ȥ����פ����ꤹ�롣
  #
  # @param self
  # @param port_type �����оݥݡ��ȥ�����
  #
  # @else
  #
  # @endif
  def setPortType(self, port_type):
    self._portType = port_type


  ##
  # @if jp
  # @brief �ǡ��������פ����ꤹ��
  #
  # �����ǻ��ꤷ���ǡ��������פ����ꤹ�롣
  #
  # @param self
  # @param data_type �����оݥǡ���������
  #
  # @else
  #
  # @endif
  def setDataType(self, data_type):
    self._dataType = data_type


  ##
  # @if jp
  # @brief ���󥿡��ե����������פ����ꤹ��
  #
  # �����ǻ��ꤷ�����󥿡��ե����������פ����ꤹ�롣
  #
  # @param self
  # @param interface_type �����оݥ��󥿡��ե�����������
  #
  # @else
  #
  # @endif
  def setInterfaceType(self, interface_type):
    self._interfaceType = interface_type


  ##
  # @if jp
  # @brief �ǡ����ե������פ����ꤹ��
  #
  # �����ǻ��ꤷ���ǡ����ե������פ����ꤹ�롣
  #
  # @param self
  # @param dataflow_type �����оݥǡ����ե�������
  #
  # @else
  #
  # @endif
  def setDataFlowType(self, dataflow_type):
    self._dataflowType = dataflow_type


  ##
  # @if jp
  # @brief ���֥�����ץ���󥿥��פ����ꤹ��
  #
  # �����ǻ��ꤷ�����֥�����ץ���󥿥��פ����ꤹ�롣
  #
  # @param self
  # @param subs_type �����оݥ��֥�����ץ���󥿥���
  #
  # @else
  #
  # @endif
  def setSubscriptionType(self, subs_type):
    self._subscriptionType = subs_type



outportproviderfactory = None

class OutPortProviderFactory(OpenRTM_aist.Factory,OutPortProvider):
  def __init__(self):
    OpenRTM_aist.Factory.__init__(self)
    pass


  def __del__(self):
    pass


  def instance():
    global outportproviderfactory
    
    if outportproviderfactory is None:
      outportproviderfactory = OutPortProviderFactory()
      
    return outportproviderfactory

  instance = staticmethod(instance)
