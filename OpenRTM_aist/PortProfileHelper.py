#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file PortProfileHelper.py
# @brief RTCs PortProfile helper class
# @date $Date: 2007-04-26 15:32:25 $
# @author Noriaki Ando <n-ando@aist.go.jp>
#
# Copyright (C) 2006
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#
# $Id: PortProfileHelper.py 1135 2009-01-19 16:11:02Z n-ando $
#
#

import threading
import OpenRTM_aist
import RTC


##
# @if jp
#
# @class PortProfileHelper
# @brief PortProfile �إ�ѡ����饹
#
# RTC::Port �μ�Υץ�ե�������ݻ����� PortProfile ��������륯�饹��
# ��Ȥ��� PortBase �������ǻ��Ѥ���롣
#
# @else
#
# @class PortProfileHelper
# @brief PortProfile helper class
#
# This class manages the PortProfile that is profiles of the RTC:Port.
# This is mainly used in PortBase class.
#
# @endif
#
class PortProfileHelper:
  """
  """

  def __init__(self):
    self._mutex        = threading.RLock()
    self._name         = ""
    self._ifProfiles   = []
    self._portRef      = None
    self._connProfiles = []
    self._owner        = None
    self._properties   = []
    return

  ##
  # @if jp
  #
  # @brief PortProfile �����ꤹ��
  #
  # ���Υ��֥������Ȥ��ݻ����� PortProfile �������Ϳ����줿 PortProfile
  # �򥳥ԡ�����񤭤�����¸���롣
  #
  # @param PortProfile ��񤭤��� PortProfile
  #
  # @else
  #
  # @brief Set PortProfile
  #
  # This operation copies the given PortProfile and overwrites the existent
  # PortProfile by the given ProtProfile.
  #
  # @param PortProfile The PortProfile to be stored.
  #
  # @endif
  #
  # void setPortProfile(const PortProfile& profile);
  def setPortProfile(self, profile):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    self._name         = profile.name
    self._ifProfiles   = profile.interfaces
    self._portRef      = profile.port_ref
    self._connProfiles = profile.connector_profiles
    self._owner        = profile.owner
    self._properties   = profile.properties
    return

  ##
  # @if jp
  #
  # @brief PortProfile ���������
  #
  # ���Υ��֥������Ȥ��ݻ����� PortProfile ���֤���
  #
  # @return ���Υ��֥������Ȥ��ݻ����� PortProfile
  #
  # @else
  #
  # @brief Get PortProfile
  #
  # This operation returns the PortProfile.
  #
  # @return The PortProfile stored by the object.
  #
  # @endif
  #
  # PortProfile* getPortProfile();
  def getPortProfile(self):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    prof = RTC.PortProfile(self._name,
                           self._ifProfiles,
                           self._portRef,
                           self._connProfiles,
                           self._owner,
                           self._properties)
    return prof


  ##
  # @if jp
  #
  # @brief PortProfile.name �����ꤹ��
  #
  # ���Υ��ڥ졼�����ϰ�����Ϳ����줿ʸ����򥳥ݡ�����
  # PortProfile.name �Ȥ����ݻ����롣
  #
  # @param name PortProfile.name �˳�Ǽ���� Port ��̾��
  #
  # @else
  #
  # @brief Set PortProfile.name
  #
  # This operation stores a copy of given name to the PortProfile.name.
  #
  # @param name The name of Port to be stored to the PortProfile.name.
  #
  # @endif
  #
  # void setName(const char* name);
  def setName(self, name):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    self._name = name
    return

  ##
  # @if jp
  #
  # @brief PortProfile.name ���������
  #
  # ���Υ��ڥ졼������ PortProfile.name ��������롣
  #
  # @return PortProfile.name �ؤΥݥ���
  #
  # @else
  #
  # @brief Get PortProfile.name
  #
  # This operation returns a pointer to the PortProfile.name.
  #
  # @return The pointer to PortProfile.name.
  #
  # @endif
  #
  # const char* getName() const;
  def getName(self):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    return self._name


  ##
  # @if jp
  #
  # @brief PortInterfaceProfile ���ɲä���
  #
  # ���Υ��ڥ졼������ PortProfile �� PortInterfaceProfile ���ɲä��롣
  #
  # @param if_profile PortProfile ���ɲä��� PortInterfaceProfile
  #
  # @else
  #
  # @brief Append PortInterfaceProfile to the PortProfile
  #
  # This operation appends the PortInterfaceProfile to the PortProfile
  #
  # @param if_profile PortInterfaceProfile to be appended the PortProfile
  #
  # @endif
  #
  # void appendPortInterfaceProfile(PortInterfaceProfile if_prof);
  def appendPortInterfaceProfile(self, if_prof):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    self._ifProfiles.append(if_prof)
    return

  ##
  # @if jp
  #
  # @brief PortInterfaceProfileList ���������
  #
  # ���Υ��ڥ졼������ PortInterfaceProfileList ���֤���
  #
  # @return PortInterfaceProfileList
  #
  # @else
  #
  # @brief Get PortInterfaceProfileList
  #
  # This operation returns the PortInterfaceProfileList.
  #
  # @return PortInterfaceProfileList
  #
  # @endif
  #
  # const PortInterfaceProfileList& getPortInterfaceProfiles() const;
  def getPortInterfaceProfiles(self):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    return self._ifProfiles


  ##
  # @if jp
  #
  # @brief PortInterfaceProfile ���������
  #
  # ���Υ��ڥ졼������ instance_name �ǻ��ꤵ�줿 PortInterfaceProfile
  # ���֤���
  #
  # @param instance_name PortInterfaceProfile �� instance_name
  # @return PortInterfaceProfile
  #
  # @else
  #
  # @brief Get PortInterfaceProfile
  #
  # This operation returns the PortInterfaceProfile specified
  # by instance_name.
  #
  # @param instance_name instance_name of the PortInterfaceProfile
  # @return PortInterfaceProfile
  #
  # @endif
  #
  # const PortInterfaceProfile getPortInterfaceProfile(const char* instance_name) const;
  def getPortInterfaceProfile(self, instance_name):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._ifProfiles,
                                            self.if_name(instance_name))
    if index < 0:
      return None
    else:
      return self._ifProfiles[index]


  ##
  # @if jp
  #
  # @brief PortInterfaceProfile ��������
  #
  # ���Υ��ڥ졼������ instance_name �ǻ��ꤵ�줿��PortInterfaceProfile
  # �������롣���ꤷ��̾���� PortInterfaceProfile ��¸�ߤ��ʤ����ˤϡ�
  # NotFound exception ���֤���
  #
  # @param instance_name ������� PortInterfaceProfile ��̾��
  #
  # @else
  #
  # @brief Erase PortInterfaceProfile from the PortProfile
  #
  # This operation erases the PortInterfaceProfile from the PortProfile
  #
  # @param instance_name PortInterfaceProfile to be erased from the
  #        PortProfile
  #
  # @endif
  #
  # void erasePortInterfaceProfile(const char* instance_name);
  def erasePortInterfaceProfile(self, instance_name):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._ifProfiles,
                                            self.if_name(instance_name))
    if index < 0:
      return
    else:
      del self._ifProfiles[index]


  ##
  # @if jp
  #
  # @brief Port �Υ��֥������Ȼ��Ȥ򥻥åȤ���
  #
  # ���Υ��ڥ졼������ PortProfile �ˡ���Ϣ���� Port �Υ��֥������Ȼ���
  # �����ꤹ�롣
  #
  # @param port ���ꤹ�� Port �Υ��֥������ȥ�ե����
  #
  # @else
  #
  # @brief Set Port's object reference
  #
  # This operation set the object reference of the Port.
  #
  # @param port Port's object reference to be set.
  #
  # @endif
  #
  # void setPortRef(PortService_ptr port);
  def setPortRef(self, port):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    self._portRef = port
    return


  ##
  # @if jp
  #
  # @brief Port �Υ��֥������Ȼ��Ȥ��������
  #
  # ���Υ��ڥ졼������ PortProfile �˴�Ϣ�դ���줿 Port ��
  # ���֥������Ȼ��Ȥ��֤���
  #
  # @return ��Ϣ�դ���줿 Port �Υ��֥������Ȼ���
  #
  # @else
  #
  # @brief Get Port's object reference
  #
  # This operation returns the object reference of the PortProfile.
  #
  # @return Port's object reference associated with the PortProfile.
  #
  # @endif
  #
  # PortService_ptr getPortRef() const;
  def getPortRef(self):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    return self._portRef


  ##
  # @if jp
  #
  # @brief ConnectorProfile ���ɲä���
  #
  # ���Υ��ڥ졼������ PortProfile �� ConnectorProfile ���ɲä��롣
  #
  # @param conn_profile ConnectorProfile 
  #
  # @else
  #
  # @brief Append ConnectorProfile
  #
  # This operation appends the ConnectorProfile to the PortProfile.
  #
  # @param conn_profile ConnectorProfile to be added.
  #
  # @endif
  #
  # void appendConnectorProfile(ConnectorProfile conn_profile);
  def appendConnectorProfile(self, conn_profile):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    self._connProfiles.append(conn_profile)
    return

  ##
  # @if jp
  #
  # @brief ConnectorProfileList ���������
  #
  # ���Υ��ڥ졼������ PortProfile �˴�Ϣ�դ���줿 ConnectorProfile ��
  # �ꥹ�� ConnectorProfileList ���֤���
  #
  # @return ��Ϣ�դ���줿 ConnectorProfileList
  #
  # @else
  #
  # @brief Get ConnectorProfileList
  #
  # This operation returns the list of ConnectorProfile of the PortProfile.
  #
  # @return Port's ConnectorProfileList.
  #
  # @endif
  #
  # const ConnectorProfileList getConnectorProfiles() const;
  def getConnectorProfiles(self):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    return self._connProfiles


  ##
  # @if jp
  #
  # @brief ConnectorProfile ���������
  #
  # ���Υ��ڥ졼�����ϰ����ǻ��ꤵ�줿̾������� ConnectorProfile ���֤���
  #
  # @param name ConnectorProfile ��̾��
  # @return ConnectorProfile
  #
  # @else
  #
  # @brief Get ConnectorProfile
  #
  # This operation returns the ConnectorProfile specified by name.
  #
  # @param name The name of ConnectorProfile
  # @return ConnectorProfile.
  #
  # @endif
  #
  # const ConnectorProfile getConnectorProfile(const char* name) const;
  def getConnectorProfile(self, name):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._connProfiles,
                                            self.conn_name(name))
    if index < 0:
      return None
    else:
      return self._connProfiles[index]

    return None


  ##
  # @if jp
  #
  # @brief ConnectorProfile ���������
  #
  # ���Υ��ڥ졼�����ϰ����ǻ��ꤵ�줿ID����� ConnectorProfile ���֤���
  #
  # @param id ConnectorProfile ��ID
  # @return ConnectorProfile
  #
  # @else
  #
  # @brief Get ConnectorProfile
  #
  # This operation returns the ConnectorProfile specified by ID.
  #
  # @param id The ID of ConnectorProfile
  # @return ConnectorProfile.
  #
  # @endif
  #
  # const ConnectorProfile getConnectorProfileById(const char* id) const;
  def getConnectorProfileById(self, id):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._connProfiles,
                                            self.conn_id(id))
    if index < 0:
      return None
    else:
      return self._connProfiles[index]

    return None

  ##
  # @if jp
  #
  # @brief ConnectorProfile ��������
  #
  # ���Υ��ڥ졼������ PortProfile �� ConnectorProfile ��
  # ̾���ǻ��ꤷ�ƺ�����롣
  #
  # @param naem ConnectorProfile ��̾��
  #
  # @else
  #
  # @brief Erase ConnectorProfile
  #
  # This operation erases the ConnectorProfile from the PortProfile.
  #
  # @param name The name of the ConnectorProfile to be erased.
  #
  # @endif
  #
  # void eraseConnectorProfile(const char* name);
  def eraseConnectorProfile(self, name):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._connProfiles,
                                            self.conn_name(name))
    if index < 0:
      return
    else:
      del self._connProfiles[index]

    return


  ##
  # @if jp
  #
  # @brief ConnectorProfile ��������
  #
  # ���Υ��ڥ졼������ PortProfile �� ConnectorProfile ��
  # ID �ǻ��ꤷ�ƺ�����롣
  #
  # @param id ConnectorProfile ��ID
  #
  # @else
  #
  # @brief Erase ConnectorProfile
  #
  # This operation erases the ConnectorProfile from the PortProfile.
  #
  # @param id The ID of the ConnectorProfile to be erased.
  #
  # @endif
  #
  # void eraseConnectorProfileById(const char* id);
  def eraseConnectorProfileById(self, id):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._connProfiles,
                                            self.conn_id(id))
    if index < 0:
      return
    else:
      del self._connProfiles[index]

    return

  ##
  # @if jp
  #
  # @brief PortProfile �� owner �����ꤹ��
  #
  # ���Υ��ڥ졼������ PortProfile �� owner �����ꤹ�롣
  #
  # @param owner PortProfile �� owner �Υ��֥������Ȼ���
  #
  # @else
  #
  # @brief Set owner's object reference to the PortProfile
  #
  # This operation sets the owner's object reference to the PortProfile.
  #
  # @param owner The owner's object reference of PortProfile.
  #
  # @endif
  #
  # void setOwner(RTObject_ptr owner);
  def setOwner(self, owner):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    self._owner = owner
    return

  ##
  # @if jp
  #
  # @brief PortProfile �� owner ���������
  #
  # ���Υ��ڥ졼������ PortProfile �� owner �Υ��֥������Ȼ��Ȥ��֤���
  #
  # @return PortProfile �� owner �Υ��֥������Ȼ���
  #
  # @else
  #
  # @brief Get owner's object reference from the PortProfile
  #
  # This operation returns the owner's object reference of the PortProfile.
  #
  # @return The owner's object reference of PortProfile.
  #
  # @endif
  #
  # RTObject_ptr getOwner() const;
  def getOwner(self):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    return self._owner


  ##
  # @if jp
  #
  # @brief PortProfile �� properties �����ꤹ��
  #
  # ���Υ��ڥ졼������ PortProfile �� properties �����ꤹ�롣
  #
  # @param prop PortProfile �� properties �� NVList
  #
  # @else
  #
  # @brief Set properties to the PortProfile
  #
  # This operation set the properties to the PortProfile.
  #
  # @param prop The NVList of PortProfile's properties.
  #
  # @endif
  #
  # void setProperties(NVList& prop);
  def setProperties(self, prop):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    self._properties = prop
    return

  ##
  # @if jp
  #
  # @brief PortProfile �� properties ���������
  #
  # ���Υ��ڥ졼������ PortProfile �� properties���֤���
  #
  # @return PortProfile �� properties �� NVList
  #
  # @else
  #
  # @brief Get properties of the PortProfile
  #
  # This operation returns the properties of the PortProfile.
  #
  # @return The NVList of PortProfile's properties.
  #
  # @endif
  #
  # const NVList& getProperties() const;
  def getProperties(self):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    return self._properties


  ##
  # @if jp
  # @class if_name
  # @brief instance_name ����� PortInterfaceProfile ��õ�� Functor
  # @else
  # @brief A functor to find a PortInterfaceProfile named instance_name
  # @endif
  class if_name:
    def __init__(self, name):
      self._name = name
      return

    def __call__(self, prof):
      return str(self._name) == str(prof.instance_name)


  # Functor to find ConnectorProfile by name
  class conn_name:
    def __init__(self, name):
      self._name = name
      return

    def __call__(self, cprof):
      return str(self._name) == str(cprof.name)

    
  # Functor to find ConnectorProfile by id
  class conn_id:
    def __init__(self, id_):
      self._id = id_
      return

    def __call__(self, cprof):
      return str(self._id) == str(cprof.connector_id)
