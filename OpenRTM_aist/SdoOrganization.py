#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file SdoOrganization.py
# @brief SDO Organization implementation class
# @date $Date: 2007/09/12 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2006
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import sys
import omniORB.any
from omniORB import CORBA
import threading

import OpenRTM_aist
import SDOPackage, SDOPackage__POA


##
# @if jp
# 
# @class Organization_impl
# @brief SDO Organization �������饹
# 
# Organization interface �� Resource Data Model ��������줿�ǡ�����
# �ɲá������������Ԥ�����Υ��󥿡��ե������Ǥ��롣
# 
# @since 0.4.0
# 
# @else
# 
# @class Organization_impl
# @brief Organization implementation class
# 
# The Organization interface is used to manage the Organization attribute.
# 
# @since 0.4.0
# 
# @endif
class Organization_impl(SDOPackage__POA.Organization):
  """
  """

  ##
  # @if jp
  # 
  # @brief ���󥹥ȥ饯��
  # 
  # ���󥹥ȥ饯��
  # 
  # @else
  # 
  # @endif
  def __init__(self, sdo):
    self._pId         = str(OpenRTM_aist.uuid1())
    self._org_mutex   = threading.RLock()

    self._orgProperty = SDOPackage.OrganizationProperty([])
    self._varOwner    = sdo
    self._memberList  = []
    self._dependency  = SDOPackage.OWN
    self._objref      = self._this()
    self.__rtcout = OpenRTM_aist.Manager.instance().getLogbuf("rtobject.sdo_organization")


  #============================================================
  #
  # <<< CORBA interfaces >>>
  #
  #============================================================
  ##
  # @if jp
  # 
  # @brief [CORBA interface] Organization ID ���������
  # 
  # Organization �� ID ���֤����ڥ졼�����
  #
  # @param self
  # 
  # @return Resource Data Model ��������줿 Organization ID��
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  # 
  # @brief [CORBA interface] Get Organization Id
  # 
  # This operation returns the 'id' of the Organization.
  #
  # @param self
  # 
  # @return The id of the Organization defined in the resource data model.
  # 
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def get_organization_id(self):
    self.__rtcout.RTC_TRACE("get_organization_id() = %s", self._pId)
    return self._pId


  ##
  # @if jp
  # 
  # @brief [CORBA interface] OrganizationProperty �μ���
  # 
  # Organization ����ͭ���� OrganizationProperty ���֤����ڥ졼�����
  # Organization ���ץ�ѥƥ�������ʤ���ж��Υꥹ�Ȥ��֤���
  # 
  # @param self
  # 
  # @return Organization �Υץ�ѥƥ��Υꥹ�ȡ�
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  # 
  # @brief [CORBA interface] Get OrganizationProperty
  # 
  # This operation returns the OrganizationProperty that an Organization
  # has. An empty OrganizationProperty is returned if the Organization does
  # not have any properties.
  # 
  # @param self
  # 
  # @return The list with properties of the organization.
  # 
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def get_organization_property(self):
    self.__rtcout.RTC_TRACE("get_organization_property()")
    guard = OpenRTM_aist.ScopedLock(self._org_mutex)
    prop = SDOPackage.OrganizationProperty(self._orgProperty.properties)
    return prop


  ##
  # @if jp
  # 
  # @brief [CORBA interface] OrganizationProperty ��������ͤμ���
  # 
  # OrganizationProperty �λ��ꤵ�줿�ͤ��֤����ڥ졼�����
  # ���� "name" �ǻ��ꤵ�줿�ץ�ѥƥ����ͤ��֤���
  # 
  # @param self
  # @param name �ͤ��֤��ץ�ѥƥ���̾����
  # 
  # @return ���� "name" �ǻ��ꤵ�줿�ץ�ѥƥ����͡�
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter ���� "namne" �ǻ��ꤵ�줿�ץ�ѥƥ���
  #            ¸�ߤ��ʤ���
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  # 
  # @brief [CORBA interface] Get specified value of OrganizationProperty
  # 
  # This operation returns a value in the OrganizationProperty.
  # The value to be returned is specified by argument "name."
  # 
  # @param self
  # @param name The name of the value to be returned.
  # 
  # @return The value of property which is specified by argument "name".
  # 
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception InvalidParameter If there are no Property stored with argument
  #                             "name".
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def get_organization_property_value(self, name):
    self.__rtcout.RTC_TRACE("get_organization_property_value(%s)", name)
    if not name:
      raise SDOPackage.InvalidParameter("Empty name.")

    index = OpenRTM_aist.CORBA_SeqUtil.find(self._orgProperty.properties, self.nv_name(name))

    if index < 0:
      raise SDOPackage.InvalidParameter("Not found.")

    try:
      value = omniORB.any.to_any(self._orgProperty.properties[index].value)
      return value
    except:
      self.__rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("get_organization_property_value()")

    # never reach here
    return None


  ##
  # @if jp
  # 
  # @brief [CORBA interface] OrganizationProperty �Υ��å�
  # 
  # �� SDO Specification �� PIM ���Ҥȥ��ڥ졼�����̾���ۤʤ롣
  # �� addOrganizationProperty ���б�����<BR>
  # OrganizationProperty �� Organization ���ɲä��륪�ڥ졼�����
  # OrganizationProperty �� Organization �Υץ�ѥƥ����ҤǤ��롣
  # 
  # @param self
  # @param org_property ���åȤ��� OrganizationProperty
  # 
  # @return ���ڥ졼����������������ɤ������֤���
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter "org_property" �� null��
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  # 
  # @brief [CORBA interface] Set OrganizationProperty
  # 
  # This operation adds the OrganizationProperty to an Organization. The
  # OrganizationProperty is the property description of an Organization.
  # 
  # @param self
  # @param org_property The type of organization to be added.
  # 
  # @return If the operation was successfully completed.
  # 
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception InvalidParameter The argument "organizationProperty" is null.
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def add_organization_property(self, org_property):
    self.__rtcout.RTC_TRACE("add_organization_property()")
    if org_property is None:
      raise SDOPackage.InvalidParameter("org_property is Empty.")

    try:
      guard = OpenRTM_aist.ScopedLock(self._org_mutex)
      self._orgProperty = org_property
      return True
    except:
      self.__rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("add_organization_property()")

    return False


  ##
  # @if jp
  # 
  # @brief [CORBA interface] OrganizationProperty ���ͤΥ��å�
  # 
  # OrganizationProperty �� NVList �� name �� value �Υ��åȤ��ɲä⤷����
  # �������륪�ڥ졼�����name �� value �ϰ��� "name" �� "value" �ˤ��
  # ���ꤹ�롣
  # 
  # @param self
  # @param name �ɲá����������ץ�ѥƥ���̾����
  # @param value �ɲá����������ץ�ѥƥ����͡�
  # 
  # @return ���ڥ졼����������������ɤ������֤���
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter ���� "name" �ǻ��ꤵ�줿�ץ�ѥƥ���
  #            ¸�ߤ��ʤ���
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  # 
  # @brief [CORBA interface] Set specified value of OrganizationProperty
  # 
  # This operation adds or updates a pair of name and value as a property
  # of Organization to/in NVList of the OrganizationProperty. The name and
  # the value to be added/updated are specified by argument "name" and
  # "value."
  # 
  # @param self
  # @param name The name of the property to be added/updated.
  # @param value The value of the property to be added/updated.
  # 
  # @return If the operation was successfully completed.
  # 
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InvalidParameter The property that is specified by argument
  #            "name" does not exist.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def set_organization_property_value(self, name, value):
    self.__rtcout.RTC_TRACE("set_organization_property_value(name=%s)", name)
    if not name:
      raise SDOPackage.InvalidParameter("set_organization_property_value(): Enpty name.")

    index = OpenRTM_aist.CORBA_SeqUtil.find(self._orgProperty.properties, self.nv_name(name))

    if index < 0:
      nv = SDOPackage.NameValue(name, value)
      OpenRTM_aist.CORBA_SeqUtil.push_back(self._orgProperty.properties, nv)
    else:
      self._orgProperty.properties[index].value = value

    return True


  ##
  # @if jp
  # 
  # @brief [CORBA interface] OrganizationProperty �κ��
  # 
  # OrganizationProperty �� NVList ��������Υץ�ѥƥ��������롣
  # ��������ץ�ѥƥ���̾���ϰ��� "name" �ˤ����ꤵ��롣
  # 
  # @param self
  # @param name �������ץ�ѥƥ���̾����
  # 
  # @return ���ڥ졼����������������ɤ������֤���
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter ���� "name" �ǻ��ꤵ�줿�ץ�ѥƥ���
  #            ¸�ߤ��ʤ���
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  # 
  # @brief [CORBA interface] Remove specified OrganizationProperty
  # 
  # This operation removes a property of Organization from NVList of the
  # OrganizationProperty. The property to be removed is specified by
  # argument "name."
  # 
  # @param self
  # @param name The name of the property to be removed.
  # 
  # @return If the operation was successfully completed.
  # 
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InvalidParameter The property that is specified by argument
  #            "name" does not exist.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def remove_organization_property(self, name):
    self.__rtcout.RTC_TRACE("remove_organization_property(%s)", name)
    if not name:
      raise SDOPackage.InvalidParameter("remove_organization_property_value(): Enpty name.")

    index = OpenRTM_aist.CORBA_SeqUtil.find(self._orgProperty.properties, self.nv_name(name))

    if index < 0:
      raise SDOPackage.InvalidParameter("remove_organization_property_value(): Not found.")

    try:
      OpenRTM_aist.CORBA_SeqUtil.erase(self._orgProperty.properties, index)
      return True
    except:
      self.__rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("remove_organization_property_value()")

    return False


  ##
  # @if jp
  # 
  # @brief [CORBA interface] Organization �Υ����ʡ����������
  # 
  # ���� Organization �Υ����ʡ��ؤλ��Ȥ��֤���
  # 
  # @param self
  # 
  # @return �����ʡ����֥������Ȥؤλ��ȡ�
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  # 
  # @brief [CORBA interface] Get the owner of the SDO
  # 
  # This operation returns the SDOSystemElement that is owner of
  # the Organization.
  # 
  # @param self
  # 
  # @return Reference of owner object.
  # 
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def get_owner(self):
    self.__rtcout.RTC_TRACE("get_owner()")
    return self._varOwner


  ##
  # @if jp
  # 
  # @brief [CORBA interface] Organization �˥����ʡ��򥻥åȤ���
  # 
  # Organization ���Ф��� SDOSystemElement �򥪡��ʡ��Ȥ��ƥ��åȤ��롣
  # ���� "sdo" �˥��åȤ��� SDOSystemElement ����ꤹ�롣
  # 
  # @param self
  # @param sdo �����ʡ����֥������Ȥλ��ȡ�
  # 
  # @return ���ڥ졼����������������ɤ������֤���
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter ���� "sdo" �� null�Ǥ��롢�⤷���ϡ�
  #                             "sdo" ��¸�ߤ��ʤ���
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  # 
  # @brief [CORBA interface] Set the orner of the Organization
  # 
  # This operation sets an SDOSystemElement to the owner of the
  # Organization. The SDOSystemElement to be set is specified by argument
  # "sdo."
  # 
  # @param self
  # @param sdo Reference of owner object.
  # 
  # @return If the operation was successfully completed.
  # 
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InvalidParameter The argument "sdo" is null, or the object
  #            that is specified by "sdo" in argument "sdo" does not exist.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def set_owner(self, sdo):
    self.__rtcout.RTC_TRACE("set_owner()")
    if CORBA.is_nil(sdo):
      raise SDOPackage.InvalidParameter("set_owner()")

    try:
      self._varOwner = sdo
      return True
    except:
      self.__rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("set_owner()")

    return True


  ##
  # @if jp
  # 
  # @brief [CORBA interface] Organization �Υ��С����������
  # 
  # Organization �Υ��С��� SDO �Υꥹ�Ȥ��֤���
  # ���С���¸�ߤ��ʤ���ж��Υꥹ�Ȥ��֤���
  # 
  # @param self
  # 
  # @return Organization �˴ޤޤ����С� SDO �Υꥹ�ȡ�
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  # 
  # @brief [CORBA interface] Get a menber list of the Organization
  # 
  # This operation returns a list of SDOs that are members of an
  # Organization. An empty list is returned if the Organization does not
  # have any members.
  # 
  # @param self
  # 
  # @return Member SDOs that are contained in the Organization object.
  # 
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def get_members(self):
    self.__rtcout.RTC_TRACE("get_members()")
    try:
      return self._memberList
    except:
      self.__rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("get_members()")


  ##
  # @if jp
  # 
  # @brief [CORBA interface] SDO �� ���å�
  # 
  # SDO �Υꥹ�Ȥ� Organization �Υ��С��Ȥ��ƥ��åȤ��롣
  # Organization �����Ǥ˥��С��� SDO ��������Ƥ�����ϡ�
  # Ϳ����줿 SDO �Υꥹ�Ȥ��֤������롣
  # 
  # @param self
  # @param sdos ���С��� SDO��
  # 
  # @return ���ڥ졼����������������ɤ������֤���
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter ���� "SDOList" �� null�Ǥ��롢�⤷����
  #            �����˻��ꤵ�줿 "SDOList" ��¸�ߤ��ʤ���
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  # 
  # @brief [CORBA interface] Set SDO's ServiceProfile
  # 
  # This operation assigns a list of SDOs to an Organization as its members.
  # If the Organization has already maintained a member SDO(s) when it is
  # called, the operation replaces the member(s) with specified list of
  # SDOs.
  # 
  # @param self
  # @param sdos Member SDOs to be assigned.
  # 
  # @return If the operation was successfully completed.
  # 
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InvalidParameter The argument "SDOList" is null, or if the
  #            object that is specified by the argument "sdos" does not
  #            exist.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def set_members(self, sdos):
    self.__rtcout.RTC_TRACE("set_members()")
    if sdos is None:
      raise SDOPackage.InvalidParameter("set_members(): SDOList is empty.")

    try:
      self._memberList = sdos
      return True
    except:
      self.__rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("set_members()")

    return True


  ##
  # @if jp
  # 
  # @brief [CORBA interface] SDO ���С����ɲ�
  # 
  # Organization �˥��С��Ȥ��� SDO ���ɲä��롣
  # ���� "sdo" ���ɲä�����С� SDO ����ꤹ�롣
  # 
  # @param self
  # @param sdo_list Organization ���ɲä���� SDO �Υꥹ�ȡ�
  # 
  # @return ���ڥ졼����������������ɤ������֤���
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter ���� "sdo" �� null�Ǥ��롣
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  # 
  # @brief [CORBA interface] Add the menebr SDOs
  # 
  # This operation adds a member that is an SDO to the organization.
  # The member to be added is specified by argument "sdo."
  # 
  # @param self
  # @param sdo The member to be added to the organization.
  # 
  # @return If the operation was successfully completed.
  # 
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InvalidParameter The argument "sdo" is null.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def add_members(self, sdo_list):
    self.__rtcout.RTC_TRACE("add_members()")
    if not sdo_list:
      raise SDOPackage.InvalidParameter("add_members(): SDOList is empty.")

    try:
      OpenRTM_aist.CORBA_SeqUtil.push_back_list(self._memberList, sdo_list)
      return True
    except:
      self.__rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("add_members()")

    return False


  ##
  # @if jp
  # 
  # @brief [CORBA interface] SDO ���С��κ��
  # 
  # Organization ��������ǻ��ꤵ�줿 "id" �� SDO �������롣
  # 
  # @param self
  # @param id ������� SDO �� id��
  # 
  # @return ���ڥ졼����������������ɤ������֤���
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter ���� "id" �� null �⤷����¸�ߤ��ʤ���
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  # 
  # @brief [CORBA interface] Remove menber SDO from Organization
  # 
  # This operation removes a member from the organization. The member to be
  # removed is specified by argument "id."
  # 
  # @param self
  # @param id Id of the SDO to be removed from the organization.
  # 
  # @return If the operation was successfully completed.
  # 
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InvalidParameter The argument "id" is null or does not exist.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def remove_member(self, id):
    self.__rtcout.RTC_TRACE("remove_member(%s)", id)
    if not id:
      self.__rtcout.RTC_ERROR("remove_member(): Enpty name.")
      raise SDOPackage.InvalidParameter("remove_member(): Empty name.")

    index = OpenRTM_aist.CORBA_SeqUtil.find(self._memberList, self.sdo_id(id))

    if index < 0:
      self.__rtcout.RTC_ERROR("remove_member(): Not found.")
      raise SDOPackage.InvalidParameter("remove_member(): Not found.")

    try:
      OpenRTM_aist.CORBA_SeqUtil.erase(self._memberList, index)
      return True
    except:
      self.__rtcout.RTC_ERROR("unknown exception")
      raise SDOPackage.InternalError("remove_member(): Not found.")

    return False


  ##
  # @if jp
  # 
  # @brief [CORBA interface] Organization �� DependencyType �����
  # 
  # Organization �δط���ɽ�� "DependencyType" ���֤���
  # 
  # @param self
  # 
  # @return Organizaton �ΰ�¸�ط� DependencyType ���֤���
  #         DependencyType �� OMG SDO ���ͤ� Section 2.2.2 2-3 �ڡ�����
  #         "Data Structures Used by Resource Data Model" �򻲾ȡ�
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  # 
  # @brief [CORBA interface] Get the DependencyType of the Organization
  # 
  # This operation gets the relationship "DependencyType" of the
  # Organization.
  # 
  # @param self
  # 
  # @return The relationship of the Organization as DependencyType.
  #         DependencyType is defined in Section 2.2.2, "Data Structures
  #         Used by Resource Data Model," on page 2-3
  #         of OMG SDO Specification.
  # 
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def get_dependency(self):
    self.__rtcout.RTC_TRACE("get_dependency()")
    return self._dependency


  ##
  # @if jp
  # 
  # @brief [CORBA interface] Organization �� DependencyType �򥻥åȤ���
  # 
  # Organization �ΰ�¸�ط� "DependencyType" �򥻥åȤ��롣
  # ���� "dependencty" �ˤ���¸�ط���Ϳ���롣
  # 
  # @param self
  # @param dependency Organization �ΰ�¸�ط���ɽ�� DependencyType��
  #        DependencyType �� OMG SDO ���ͤ� Section 2.2.2��2-3 �ڡ�����
  #        "Data Structures Used by Resource Data Model" �򻲾ȡ�
  # 
  # @return ���ڥ졼����������������ɤ������֤���
  # 
  # @exception SDONotExists �������åȤ�SDO��¸�ߤ��ʤ���(���㳰�ϡ�CORBAɸ��
  #                         �����ƥ��㳰��OBJECT_NOT_EXIST�˥ޥåԥ󥰤����)
  # @exception InvalidParameter ���� "sProfile" �� null�Ǥ��롣
  # @exception NotAvailable SDO��¸�ߤ��뤬�������ʤ���
  # @exception InternalError ����Ū���顼��ȯ��������
  # @else
  # 
  # @brief [CORBA interface] Set the DependencyType of the Organization
  # 
  # This operation sets the relationship "DependencyType" of the
  # Organization. The value to be set is specified by argument "dependency."
  # 
  # @param self
  # @param dependency The relationship of the Organization as
  #                   DependencyType. DependencyType is defined in Section
  #                   2.2.2, "Data Structures Used by Resource Data Model,"
  #                   on page 2-3.
  # 
  # @return If the operation was successfully completed.
  # 
  # @exception SDONotExists if the target SDO does not exist.(This exception 
  #                         is mapped to CORBA standard system exception
  #                         OBJECT_NOT_EXIST.)
  # @exception NotAvailable The target SDO is reachable but cannot respond.
  # @exception InvalidParameter The argument "dependency" is null.
  # @exception InternalError The target SDO cannot execute the operation
  #                          completely due to some internal error.
  # @endif
  def set_dependency(self, dependency):
    self.__rtcout.RTC_TRACE("set_dependency()")
    if dependency is None:
      raise SDOPackage.InvalidParameter("set_dependency(): Empty dependency.")

    try:
      self._dependency = dependency
      return True
    except:
      self.__rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      raise SDOPackage.InternalError("set_dependency(): Unknown.")

    return False


  def getObjRef(self):
    return self._objref



  # end of CORBA interface definition
  #============================================================


  ##
  # @if jp
  # @class nv_name
  # @brief NVList������functor
  # @else
  #
  # @endif
  class nv_name:
    def __init__(self, name):
      self._name = name

    def __call__(self, nv):
      return str(self._name) == str(nv.name)

  ##
  # @if jp
  # @class sdo_id
  # @brief SDO������functor
  # @else
  #
  # @endif
  class sdo_id:
    def __init__(self, id_):
      self._id = id_

    def __call__(self, sdo):
      id_ = sdo.get_sdo_id()
      return str(self._id) == str(id_)
    
