#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file PortAdmin.py
# @brief RTC's Port administration class
# @date $Date: 2007/09/03 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import traceback
import sys
from omniORB import CORBA

import RTC
import OpenRTM_aist



##
# @if jp
# @class PortAdmin
# @brief PortAdmin ���饹
#
# �Ƽ� Port �δ�����Ԥ����饹��
# Port ����Ͽ/��Ͽ����ʤɳƼ��������¹Ԥ���ȤȤ�ˡ���Ͽ����Ƥ���
# Port �δ�����Ԥ����饹��
#
# @since 0.4.0
#
# @else
# @class PortAdmin
# @brief PortAdmin class
# @endif
class PortAdmin:
  """
  """



  ##
  # @if jp
  # @class comp_op
  # @brief Port �������������饹
  # @else
  #
  # @endif
  class comp_op:
    def __init__(self, name=None, factory=None):
      if name:
        self._name = name
      if factory:
        self._name = factory.getProfile().name

    def __call__(self, obj):
      name_ = obj.getProfile().name
      return self._name == name_


  ##
  # @if jp
  # @class find_port_name
  # @brief Port �����ѥե��󥯥�
  # @else
  # @endif
  class find_port_name:
    def __init__(self, name):
      self._name = name

    def __call__(self, p):
      prof = p.get_port_profile()
      name_ = prof.name 
      return self._name == name_


  ##
  # @if jp
  # @brief Port����ѥե��󥯥�
  # @else
  # @brief Functor to delete the Port
  # @endif
  class del_port:
    def __init__(self, pa):
      self._pa = pa
      return

    def __call__(self, p):
      self._pa.deletePort(p)


  class find_port:
    # find_port(const PortService_ptr& p) : m_port(p) {};
    def __init__(self, p):
      self._port = p

    # bool operator()(const PortService_ptr& p)
    def __call__(self, p):
      return self._port._is_equivalent(p)


  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param orb ORB
  # @param poa POA
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, orb, poa):
    # ORB ���֥�������
    self._orb = orb

    # POA ���֥�������
    self._poa = poa

    # Port�Υ��֥������ȥ�ե���󥹤Υꥹ��. PortServiceList
    self._portRefs = []

    # �����Х�Ȥ�ľ�ܳ�Ǽ���륪�֥������ȥޥ͡�����
    self._portServants = OpenRTM_aist.ObjectManager(self.comp_op)

    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("PortAdmin")

  ##
  # @if jp
  #
  # @brief Port �ꥹ�Ȥμ���
  #
  # registerPort() �ˤ����Ͽ���줿 Port �� �ꥹ�Ȥ�������롣
  #
  # @param self
  #
  # @return Port �ꥹ��
  #
  # @else
  #
  # @brief Get PortServiceList
  #
  # This operation returns the pointer to the PortServiceList of Ports regsitered
  # by registerPort().
  #
  # @return PortServiceList+ The pointer points PortServiceList
  #
  # @endif
  def getPortServiceList(self):
    return self._portRefs


  ##
  # @if jp
  #
  # @brief PorProfile �ꥹ�Ȥμ���
  #
  # addPort() �ˤ����Ͽ���줿 Port �� Profile �ꥹ�Ȥ�������롣
  #
  # @return PortProfile �ꥹ��
  #
  # @else
  #
  # @brief Get PorProfileList
  #
  # This operation gets the Profile list of Ports registered by 
  # addPort().
  #
  # @return The pointer points PortProfile list
  #
  # @endif
  #
  def getPortProfileList(self):
    ret = []
    for p in self._portRefs:
      ret.append(p.get_port_profile())

    return ret


  ##
  # @if jp
  #
  # @brief Port �Υ��֥������Ȼ��Ȥμ���
  #
  # port_name �ǻ��ꤷ�� Port �Υ��֥������Ȼ��Ȥ��֤���
  # port_name �ǻ��ꤹ�� Port �Ϥ��餫���� registerPort() ����Ͽ����Ƥ�
  # �ʤ���Фʤ�ʤ���
  #
  # @param self
  # @param port_name ���Ȥ��֤�Port��̾��
  #
  # @return Port_ptr Port�Υ��֥������Ȼ���
  #
  # @else
  #
  # @brief Get PortServiceList
  #
  # This operation returns the pointer to the PortServiceList of Ports regsitered
  # by registerPort().
  #
  # @param port_name The name of Port to be returned the reference.
  #
  # @return Port_ptr Port's object reference.
  #
  # @endif
  def getPortRef(self, port_name):
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._portRefs, self.find_port_name(port_name))
    if index >= 0:
      return self._portRefs[index]
    return None


  ##
  # @if jp
  #
  # @brief Port �Υ����Х�ȤΥݥ��󥿤μ���
  #
  # port_name �ǻ��ꤷ�� Port �Υ����Х�ȤΥݥ��󥿤��֤���
  # port_name �ǻ��ꤹ�� Port �Ϥ��餫���� registerPort() ����Ͽ����Ƥ�
  # �ʤ���Фʤ�ʤ���
  #
  # @param self
  # @param port_name ���Ȥ��֤�Port��̾��
  #
  # @return PortBase* Port�����Х�ȴ��쥯�饹�Υݥ���
  #
  # @else
  #
  # @brief Getpointer to the Port's servant
  #
  # This operation returns the pointer to the PortBase servant regsitered
  # by registerPort().
  #
  # @param port_name The name of Port to be returned the servant pointer.
  #
  # @return PortBase* Port's servant's pointer.
  #
  # @endif
  def getPort(self, port_name):
    return self._portServants.find(port_name)


  ##
  # @if jp
  #
  # @brief Port ����Ͽ����
  #
  # ���� port �ǻ��ꤵ�줿 Port �Υ����Х�Ȥ���Ͽ���롣
  # ��Ͽ���줿 Port �Υ����Х�Ȥϥ��󥹥ȥ饯����Ϳ����줿POA ���
  # activate ���졢���Υ��֥������Ȼ��Ȥ�Port��Profile�˥��åȤ���롣
  #
  # @param self
  # @param port Port �����Х��
  #
  # @else
  #
  # @brief Regsiter Port
  #
  # This operation registers the Port's servant given by argument.
  # The given Port's servant will be activated on the POA that is given
  # to the constructor, and the created object reference is set
  # to the Port's profile.
  #
  # @param port The Port's servant.
  #
  # @endif
  # void registerPort(PortBase& port);
  def registerPort(self, port):
    if not self.addPort(port):
      self._rtcout.RTC_ERROR("registerPort() failed.")
    return

  # void registerPort(PortService_ptr port);
  # def registerPortByReference(self, port_ref):
  #   self.addPortByReference(port_ref)
  #   return

  # new interface. since 1.0.0-RELEASE
  # void addPort(PortBase& port);
  def addPort(self, port):
    if isinstance(port, RTC._objref_PortService):
      index = OpenRTM_aist.CORBA_SeqUtil.find(self._portRefs,
                                              self.find_port_name(port.get_port_profile().name))
      if index >= 0:
        return False
      self._portRefs.append(port)
      return True
    else:
      index = OpenRTM_aist.CORBA_SeqUtil.find(self._portRefs,
                                              self.find_port_name(port.getName()))
      if index >= 0:
        return False
      self._portRefs.append(port.getPortRef())
      return self._portServants.registerObject(port)
    return False

  # new interface. since 1.0.0-RELEASE
  # void addPort(PortService_ptr port);
  # def addPortByReference(self, port_ref):
  #   self._portRefs.append(port_ref)
  #   return

  ##
  # @if jp
  #
  # @brief Port ����Ͽ��������
  #
  # ���� port �ǻ��ꤵ�줿 Port ����Ͽ�������롣
  # ������� Port �� deactivate ���졢Port��Profile�Υ�ե���󥹤ˤϡ�
  # nil�ͤ���������롣
  #
  # @param self
  # @param port Port �����Х��
  #
  # @else
  #
  # @brief Delete the Port's registration
  #
  # This operation unregisters the Port's registration.
  # When the Port is unregistered, Port is deactivated, and the object
  # reference in the Port's profile is set to nil.
  #
  # @param port The Port's servant.
  #
  # @endif
  def deletePort(self, port):
    if not self.removePort(port):
      self._rtcout.RTC_ERROR("deletePort(PortBase&) failed.")
    return

  # new interface. since 1.0.0-RELEASE
  def removePort(self, port):
    try:
      if isinstance(port,RTC._objref_PortService):
        OpenRTM_aist.CORBA_SeqUtil.erase_if(self._portRefs, self.find_port(port))
        return True

      port.disconnect_all()
      tmp = port.getProfile().name
      OpenRTM_aist.CORBA_SeqUtil.erase_if(self._portRefs, self.find_port_name(tmp))

      self._poa.deactivate_object(self._poa.servant_to_id(port))
      port.setPortRef(RTC.PortService._nil)

      if not self._portServants.unregisterObject(tmp):
        return False
      return True
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      return False


  ##
  # @if jp
  #
  # @brief ̾�λ���ˤ��Port ����Ͽ��������
  #
  # �����ǻ��ꤵ�줿̾������� Port ����Ͽ�������롣
  # ������� Port �� deactivate ���졢Port��Profile�Υ�ե���󥹤ˤϡ�
  # nil�ͤ���������롣
  #
  # @param self
  # @param port_name Port ��̾��
  #
  # @else
  #
  # @brief Delete the Port' registration
  #
  # This operation delete the Port's registration specified by port_ name.
  # When the Port is unregistered, Port is deactivated, and the object
  # reference in the Port's profile is set to nil.
  #
  # @param port_name The Port's name.
  #
  # @endif
  def deletePortByName(self, port_name):
    if not port_name:
      return

    p = self._portServants.find(port_name)
    self.removePort(p)
    return


  ##
  # @if jp
  # @brief ���Ƥ� Port �Υ��󥿡��ե������� activates ����
  # @else
  # @brief Activate all Port interfaces
  # @endif
  # void PortAdmin::activatePorts()
  def activatePorts(self):
    ports = self._portServants.getObjects()
    for port in ports:
      port.activateInterfaces()
      
    return


  ##
  # @if jp
  # @brief ���Ƥ� Port �Υ��󥿡��ե������� deactivates ����
  # @else
  # @brief Deactivate all Port interfaces
  # @endif
  # void PortAdmin::deactivatePorts()
  def deactivatePorts(self):
    ports = self._portServants.getObjects()
    for port in ports:
      port.deactivateInterfaces()

    return


  ##
  # @if jp
  #
  # @brief ���Ƥ� Port ��deactivate����Ͽ��������
  #
  # ��Ͽ����Ƥ������Ƥ�Port���Ф��ơ������Х�Ȥ�deactivate��Ԥ���
  # ��Ͽ�ꥹ�Ȥ��������롣
  #
  # @param self
  #
  # @else
  #
  # @brief Unregister the Port
  #
  # This operation deactivates the all Port and deletes the all Port's
  # registrations from the list.
  #
  # @endif
  def finalizePorts(self):
    self.deactivatePorts()
    ports = []
    ports = self._portServants.getObjects()
    len_ = len(ports)
    for i in range(len_):
      idx = (len_ - 1) - i
      self.removePort(ports[idx])
