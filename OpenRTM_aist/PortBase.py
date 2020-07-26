#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file PortBase.py
# @brief RTC's Port base class
# @date $Date: 2007/09/18 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import threading
import copy

import OpenRTM_aist
import RTC, RTC__POA



##
# @if jp
# @class PortBase
# @brief Port �δ��쥯�饹
#
# RTC::Port �δ���Ȥʤ륯�饹��
# RTC::Port �Ϥۤ� UML Port �γ�ǰ��Ѿ����Ƥ��ꡢ�ۤ�Ʊ���Τ�ΤȤߤʤ�
# ���Ȥ��Ǥ��롣RT ����ݡ��ͥ�ȤΥ��󥻥ץȤˤ����Ƥϡ�
# Port �ϥ���ݡ��ͥ�Ȥ���°��������ݡ��ͥ�Ȥ�¾�Υ���ݡ��ͥ�Ȥ���ߺ���
# ��Ԥ������Ǥ��ꡢ�̾���Ĥ��Υ��󥿡��ե������ȴ�Ϣ�դ����롣
# ����ݡ��ͥ�Ȥ� Port ���̤��Ƴ������Ф����󥿡��ե��������󶡤ޤ����׵�
# ���뤳�Ȥ��Ǥ���Port�Ϥ�����³�������������ô����
# <p>
# Port �ζ�ݥ��饹�ϡ��̾� RT ����ݡ��ͥ�ȥ��󥹥�����������Ʊ����
# �������졢�󶡡��׵ᥤ�󥿡��ե���������Ͽ�����塢RT ����ݡ��ͥ�Ȥ�
# ��Ͽ���졢�������饢��������ǽ�� Port �Ȥ��Ƶ�ǽ���뤳�Ȥ����ꤷ�Ƥ��롣
# <p>
# RTC::Port �� CORBA ���󥿡��ե������Ȥ��ưʲ��Υ��ڥ졼�������󶡤��롣
#
# - get_port_profile()
# - get_connector_profiles()
# - get_connector_profile()
# - connect()
# - notify_connect()
# - disconnect()
# - notify_disconnect()
# - disconnect_all()
#
# ���Υ��饹�Ǥϡ������Υ��ڥ졼�����μ������󶡤��롣
# <p>
# �����Υ��ڥ졼�����Τ�����get_port_profile(), get_connector_profiles(),
# get_connector_profile(), connect(), disconnect(), disconnect_all() �ϡ�
# ���֥��饹�ˤ������ä˿����񤤤��ѹ�����ɬ�פ��ʤ����ᡢ�����С��饤��
# ���뤳�ȤϿ侩����ʤ���
# <p>
# notify_connect(), notify_disconnect() �ˤĤ��Ƥϡ����֥��饹���󶡡��׵�
# ���륤�󥿡��ե������μ���˱����ơ������񤤤��ѹ�����ɬ�פ�������
# ���⤷��ʤ�����������ľ�ܥ����С��饤�ɤ��뤳�ȤϿ侩���줺��
# ��Ҥ� notify_connect(), notify_disconnect() �ι�ˤ����Ƥ�Ҥ٤����̤�
# �����δؿ��˴�Ϣ���� �ؿ��򥪡��С��饤�ɤ��뤳�Ȥˤ�꿶���񤤤��ѹ�����
# ���Ȥ��侩����롣
#
# @since 0.4.0
#
# @else
# @class PortBase
# @brief Port base class
#
# This class is a base class of RTC::Port.
# RTC::Port inherits a concept of RT-Component, and can be regarded as almost
# the same as it. In the concept of RT-Component, Port is attached to the
# component, can mediate interaction between other components and usually is
# associated with some interfaces.
# Component can provide or require interface for outside via Port, and the
# Port plays a role to manage the connection.
# <p>
# Concrete class of Port assumes to be usually created at the same time that
# RT-Component's instance is created, be registerd to RT-Component after
# provided and required interfaces are registerd, and function as accessible
# Port from outside.
# <p>
# RTC::Port provides the following operations as CORBA interface:
#
# - get_port_profile()
# - get_connector_profiles()
# - get_connector_profile()
# - connect()
# - notify_connect()
# - disconnect()
# - notify_disconnect()
# - disconnect_all()
#
# This class provides implementations of these operations.
# <p>
# In these operations, as for get_port_profile(), get_connector_profiles(),
# get_connector_profile(), connect(), disconnect() and disconnect_all(),
# since their behaviors especially need not to be change in subclass, 
# overriding is not recommended.
# <p>
# As for notify_connect() and notify_disconnect(), you may have to modify
# behavior according to the kind of interfaces that subclass provides and
# requires, however it is not recommended these are overriden directly.
# In the section of notify_connect() and notify_disconnect() as described
# below, it is recommended that you modify behavior by overriding the
# protected function related to these functions.
#
# @since 0.4.0
#
# @endif
class PortBase(RTC__POA.PortService):
  """
  """



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # PortBase �Υ��󥹥ȥ饯���� Port ̾ name ������˼��������Ԥ�
  # ��Ʊ���ˡ���ʬ���Ȥ� CORBA Object �Ȥ��Ƴ������������Ȥ� PortProfile
  # �� port_ref �˼��ȤΥ��֥������ȥ�ե���󥹤��Ǽ���롣
  # ̾���ˤϡ�"." �ʳ���ʸ�������Ѥ��뤳�Ȥ��Ǥ��롣
  #
  # @param self
  # @param name Port ��̾��(�ǥե������:None)
  #
  # @else
  #
  # @brief Constructor
  #
  # The constructor of the ProtBase class is given the name of this Port
  # and initialized. At the same time, the PortBase activates itself
  # as CORBA object and stores its object reference to the PortProfile's 
  # port_ref member.
  # Characters except "." can be used for the name of the port.
  #
  # @param name The name of Port 
  #
  # @endif
  def __init__(self, name=None):
    self._ownerInstanceName = "unknown"
    self._objref = self._this()

    self._profile = RTC.PortProfile("", [], RTC.PortService._nil, [], RTC.RTObject._nil,[])
    # Now Port name is <instance_name>.<port_name>. r1648
    if name is None:
      self._profile.name = "unknown.unknown"
    else:
      self._profile.name = self._ownerInstanceName+"."+name
      
    self._profile.port_ref = self._objref
    self._profile.owner = RTC.RTObject._nil
    self._profile_mutex = threading.RLock()
    self._connection_mutex = threading.RLock()
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf(name)
    self._onPublishInterfaces = None
    self._onSubscribeInterfaces = None
    self._onConnected = None
    self._onUnsubscribeInterfaces = None
    self._onDisconnected = None
    self._onConnectionLost = None
    self._connectionLimit   = -1
    self._portconnListeners = None
    return

  
  ##
  # @if jp
  #
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯���Ǥϡ�PortService CORBA ���֥������Ȥ� deactivate ��
  # �Ԥ���deactivate�˺ݤ����㳰���ꤲ�뤳�ȤϤʤ���
  #
  # @else
  #
  # @brief Destructor
  #
  # In the destructor, PortService CORBA object is deactivated.
  # This function never throws exception.
  #
  # @endif
  #
  def __del__(self):
    self._rtcout.RTC_TRACE("PortBase.__del__()")
    try:
      mgr = OpenRTM_aist.Manager.instance().getPOA()
      oid = mgr.servant_to_id(self)
      mgr.deactivate_object(oid)
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
    

  ##
  # @if jp
  #
  # @brief [CORBA interface] PortProfile���������
  #
  # Port���ݻ�����PortProfile���֤���
  # PortProfile ��¤�Τϰʲ��Υ��С�����ġ�
  #
  # - name              [string ��] Port ��̾����
  # - interfaces        [PortInterfaceProfileList ��] Port ���ݻ�����
  #                     PortInterfaceProfile �Υ�������
  # - port_ref          [Port Object ��] Port ���ȤΥ��֥������ȥ�ե����
  # - connector_profile [ConnectorProfileList ��] Port �������ݻ�����
  #                     ConnectorProfile �Υ�������
  # - owner             [RTObject Object ��] ���� Port ���ͭ����
  #                     RTObject�Υ�ե����
  # - properties        [NVList ��] ����¾�Υץ�ѥƥ���
  #
  # @param self
  #
  # @return PortProfile
  #
  # @else
  #
  # @brief [CORBA interface] Get the PortProfile of the Port
  #
  # This operation returns the PortProfile of the Port.
  # PortProfile struct has the following members,
  #
  # - name              [string ] The name of the Port.
  # - interfaces        [PortInterfaceProfileList] The sequence of 
  #                     PortInterfaceProfile owned by the Port
  # - port_ref          [Port Object] The object reference of the Port.
  # - connector_profile [ConnectorProfileList] The sequence of 
  #                     ConnectorProfile owned by the Port.
  # - owner             [RTObject Object] The object reference of 
  #                     RTObject that is owner of the Port.
  # - properties        [NVList] The other properties.
  #
  # @return the PortProfile of the Port
  #
  # @endif
  # PortProfile* get_port_profile()
  def get_port_profile(self):
    self._rtcout.RTC_TRACE("get_port_profile()")

    self.updateConnectors()

    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)

    prof = RTC.PortProfile(self._profile.name,
                           self._profile.interfaces,
                           self._profile.port_ref,
                           self._profile.connector_profiles,
                           self._profile.owner,
                           self._profile.properties)

    return prof


  ##
  # @if jp
  #
  # @brief PortProfile ��������롣
  #
  # ���δؿ��ϡ����֥��������������ݻ�����Ƥ��� PortProfile ��
  # const ���Ȥ��֤� const �ؿ��Ǥ��롣
  # 
  # @post ���δؿ���ƤӽФ����Ȥˤ���������֤��ѹ�����뤳�ȤϤʤ���
  #
  # @return PortProfile
  #
  # @else
  #
  # @brief Get the PortProfile of the Port
  #
  # This function is a const function that returns a const
  # reference of the PortProfile stored in this Port.
  #
  # @post This function never changes the state of the object.
  #
  # @return PortProfile
  #
  # @endif
  # PortProfile& getPortProfile() const;
  def getPortProfile(self):
    self._rtcout.RTC_TRACE("getPortProfile()")
    return self._profile


  ##
  # @if jp
  #
  # @brief [CORBA interface] ConnectorProfileList���������
  #
  # Port���ݻ����� ConnectorProfile �� sequence ���֤���
  # ConnectorProfile �� Port �֤���³�ץ�ե����������ݻ����빽¤�ΤǤ��ꡢ
  # ��³����Port�֤Ǿ���򴹤�Ԥ�����Ϣ���뤹�٤Ƥ� Port ��Ʊ����ͤ�
  # �ݻ�����롣
  # ConnectorProfile �ϰʲ��Υ��С����ݻ����Ƥ��롣
  #
  # - name         [string ��] ���Υ��ͥ�����̾����
  # - connector_id [string ��] ��ˡ�����ID
  # - ports        [Port sequnce] ���Υ��ͥ����˴�Ϣ���� Port �Υ��֥�������
  #                ��ե���󥹤Υ������󥹡�
  # - properties   [NVList ��] ����¾�Υץ�ѥƥ���
  #
  # @param self
  #
  # @return ���� Port ���ݻ����� ConnectorProfile
  #
  # @else
  #
  # @brief [CORBA interface] Get the ConnectorProfileList of the Port
  #
  # This operation returns a list of the ConnectorProfiles of the Port.
  # ConnectorProfile includes the connection information that describes 
  # relation between (among) Ports, and Ports exchange the ConnectionProfile
  # on connection process and hold the same information in each Port.
  # ConnectionProfile has the following members,
  #
  # - name         [string] The name of the connection.
  # - connector_id [string] Unique identifier.
  # - ports        [Port sequnce] The sequence of Port's object reference
  #                that are related the connection.
  # - properties   [NVList] The other properties.
  #
  # @return the ConnectorProfileList of the Port
  #
  # @endif
  # virtual ConnectorProfileList* get_connector_profiles()
  def get_connector_profiles(self):
    self._rtcout.RTC_TRACE("get_connector_profiles()")

    self.updateConnectors()

    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    return self._profile.connector_profiles


  ##
  # @if jp
  #
  # @brief [CORBA interface] ConnectorProfile ���������
  #
  # connector_id �ǻ��ꤵ�줿 ConnectorProfile ���֤���
  # ���ꤷ�� connector_id ����� ConnectorProfile ���ݻ����Ƥ��ʤ����ϡ�
  # ���� ConnectorProfile ���֤���
  #
  # @param self
  # @param connector_id ConnectorProfile �� ID
  #
  # @return connector_id �ǻ��ꤵ�줿 ConnectorProfile
  #
  # @else
  #
  # @brief [CORBA interface] Get the ConnectorProfile
  #
  # This operation returns the ConnectorProfiles specified connector_id.
  #
  # @param connector_id ID of the ConnectorProfile
  #
  # @return the ConnectorProfile identified by the connector_id
  #
  # @endif
  # ConnectorProfile* get_connector_profile(const char* connector_id)
  def get_connector_profile(self, connector_id):
    self._rtcout.RTC_TRACE("get_connector_profile(%s)", connector_id)

    self.updateConnectors()

    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                            self.find_conn_id(connector_id))
    if index < 0:
      conn_prof = RTC.ConnectorProfile("","",[],[])
      return conn_prof

    conn_prof = RTC.ConnectorProfile(self._profile.connector_profiles[index].name,
                                     self._profile.connector_profiles[index].connector_id,
                                     self._profile.connector_profiles[index].ports,
                                     self._profile.connector_profiles[index].properties)
    return conn_prof


  ##
  # @if jp
  #
  # @brief [CORBA interface] Port ����³��Ԥ�
  #
  # Ϳ����줿 ConnectoionProfile �ξ���˴�Ť���Port�֤���³���Ω
  # ���롣���δؿ��ϼ�˥��ץꥱ�������ץ�����ġ��뤫��Ƥӽ�
  # �����Ȥ�����Ȥ��Ƥ��롣
  # 
  # @pre ���ץꥱ�������ץ����ϡ�����ݡ��ͥ�ȴ֤�ʣ����
  # Port ����³���뤿��ˡ�Ŭ�ڤ��ͤ򥻥åȤ��� ConnectorProfile ��
  # connect() �ΰ����Ȥ���Ϳ���ƸƤӽФ��ʤ���Фʤ�ʤ���
  #
  # @pre connect() ��Ϳ���� ConnectorProfile �Υ��С��Τ�����
  # name, ports, properties ���С����Ф��ƥǡ����򥻥åȤ��ʤ����
  # �ʤ�ʤ���connector_id �ˤ��̾��ʸ�������ꤹ�뤫��Ŭ����UUID��
  # ʸ��������ꤹ��ɬ�פ����롣
  #
  # @pre ConnectorProfile::name ����³�ˤĤ���̾���� CORBA::string
  # ���˳�Ǽ�Ǥ���Ǥ�դ�ʸ����Ǥ���ɬ�פ����롣
  # 
  # @pre ConnectorProfile::connector_id �Ϥ��٤Ƥ���³���Ф��ư�դ�
  # ID (�̾��UUID) ����Ǽ����롣UUID������� connect() �ؿ���ǹ�
  # ����Τǡ��ƤӽФ�¦�϶�ʸ�������ꤹ�롣��¸����³��Ʊ��UUID��
  # ���ꤷ connect() ��ƤӽФ������ˤ� PRECONDITION_NOT_MET ���顼
  # ���֤���������������γ�ĥ�Ǵ�¸����³�ץ�ե�����򹹿����뤿��
  # �˴�¸�� UUID �����ꤷ�ƸƤӽФ�����ˡ���Ѥ������ǽ�������롣
  #
  # @pre ConnectorProfile::ports �� RTC::PortService �Υ������󥹤ǡ�
  # ��³���������̾�2�İʾ�Υݡ��ȤΥ��֥������Ȼ��Ȥ���������ɬ
  # �פ����롣�㳰�Ȥ��ơ��ݡ��ȤΥ��֥������Ȼ��Ȥ�1�Ĥ�����Ǽ����
  # connect()��ƤӽФ����Ȥǡ��ݡ��ȤΥ��󥿡��ե���������������
  # ���ꡢ�ü�ʥݡ���(CORBA��RTC::PortService�ʳ������)���Ф�����
  # ³��Ԥ����⤢�롣
  #
  # @pre ConnectorProfile::properties �ϥݡ��Ȥ˴�Ϣ�դ���줿���󥿡�
  # �ե��������Ф���ץ�ѥƥ���Ϳ���뤿��˻��Ѥ��롣�ץ�ѥƥ��ϡ�
  # string ���򥭡���Any �����ͤȤ��Ƥ�ĥڥ��Υ������󥹤Ǥ��ꡢ��
  # �ˤ�Ǥ�դ�CORBA�ǡ��������Ǽ�Ǥ��뤬����ǽ�ʸ¤� string ���Ȥ�
  # �Ƴ�Ǽ����뤳�Ȥ��侩����롣
  #
  # @pre �ʾ� connect() �ƤӽФ��������ꤹ�� ConnectorProfile �Υ��
  # �Ф�ޤȤ��Ȱʲ��Τ褦�ˤʤ롣
  #
  # - ConnectorProfile::name: Ǥ�դ���³̾
  # - ConnectorProfile::connector_id: ��ʸ��
  # - ConnectorProfile::ports: 1�İʾ�Υݡ���
  # - ConnectorProfile::properties: ���󥿡��ե��������Ф���ץ�ѥƥ�
  #
  # @post connect() �ؿ��ϡ�ConnectorProfile::ports�˳�Ǽ���줿�ݡ�
  # �ȥ������󥹤���Ƭ�Υݡ��Ȥ��Ф��� notify_connect() ��Ƥ֡�
  #
  # @post notify_connect() �� ConnectorProfile::ports �˳�Ǽ���줿�ݡ�
  # �Ƚ�� notify_connect() �򥫥������ɸƤӽФ����롣���Υ���������
  # �ƤӽФ��ϡ������notify_connect() �ǥ��顼���ФƤ�ݡ��ȤΥ���
  # �������Ȼ��Ȥ�ͭ���Ǥ���¤ꡢɬ�����٤ƤΥݡ��Ȥ��Ф��ƹԤ���
  # ���Ȥ��ݾڤ���롣ͭ���Ǥʤ����֥������Ȼ��Ȥ������������¸��
  # �����硢���Υݡ��Ȥ򥹥��åפ��ơ����Υݡ��Ȥ��Ф���
  # notify_connect() ��ƤӽФ���
  #
  # @post connect() �ؿ��ϡ�notify_connect()������ͤ�RTC_OK�Ǥ���С�
  # RTC_OK ���֤������λ�������³�ϴ�λ���롣RTC_OK�ʳ�
  # �ξ��ϡ�������³ID���Ф���disconnect()��ƤӽФ���³��������
  # notify_connect() ���֤������顼�꥿���󥳡��ɤ򤽤Τޤ��֤���
  # 
  # @post connect() �ΰ����Ȥ����Ϥ��� ConnectorProfile �ˤϡ�
  # ConnectorProfile::connector_id ����ӡ�����Υݡ��Ȥ�
  # publishInterfaces() �Ǹ��������ݡ��ȥ��󥿡��ե������γƼ����
  # ��Ǽ����Ƥ��롣connect() ���������� notify_connect() ��
  # ConnectorProfile::{name, ports} ���ѹ����뤳�ȤϤʤ���
  #  
  # @param connector_profile ConnectorProfile
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [CORBA interface] Connect the Port
  #
  # This operation establishes connection according to the given
  # ConnectionProfile inforamtion. This function is premised on
  # calling from mainly application program or tools.
  #
  # @pre To establish the connection among Ports of RT-Components,
  # application programs must call this operation giving
  # ConnectorProfile with valid values as an argument.
  #
  # @pre Out of ConnectorProfile member variables, "name", "ports"
  # and "properties" members shall be set valid
  # data. "connector_id" shall be set as empty string value or
  # valid string UUID value.
  #
  # @pre ConnectorProfile::name that is connection identifier shall
  # be any valid CORBA::string.
  # 
  #
  # @pre ConnectorProfile::connector_id shall be set unique
  # identifier (usually UUID is used) for all connections. Since
  # UUID string value is usually set in the connect() function,
  # caller should just set empty string. If the connect() is called
  # with the same UUID as existing connection, this function
  # returns PRECONDITION_NOT_MET error. However, in order to update
  # the existing connection profile, the "connect()" operation with
  # existing connector ID might be used as valid method by future
  # extension
  #
  # @pre ConnectorProfile::ports, which is sequence of
  # RTC::PortService references, shall store usually two or more
  # ports' references. As exceptions, the "connect()" operation
  # might be called with only one reference in ConnectorProfile, in
  # case of just getting interfaces information from the port, or
  # connecting a special port (i.e. the peer port except
  # RTC::PortService on CORBA).
  #
  # @pre ConnectorProfile::properties might be used to give certain
  # properties to the service interfaces associated with the port.
  # The properties is a sequence variable with a pair of key string
  # and Any type value. Although the A variable can store any type
  # of values, it is not recommended except string.
  #
  # @pre The following is the summary of the ConnectorProfile
  # member to be set when this operation is called.
  #
  # - ConnectorProfile::name: The any name of connection
  # - ConnectorProfile::connector_id: Empty string
  # - ConnectorProfile::ports: One or more port references
  # - ConnectorProfile::properties: Properties for the interfaces
  #
  # @post connect() operation will call the first port in the
  # sequence of the ConnectorProfile.
  #
  # @post "noify_connect()"s perform cascaded call to the ports
  # stored in the ConnectorProfile::ports by order. Even if errors
  # are raised by intermediate notify_connect() operation, as long
  # as ports' object references are valid, it is guaranteed that
  # this cascaded call is completed in all the ports.  If invalid
  # or dead ports exist in the port's sequence, the ports are
  # skipped and notify_connect() is called for the next valid port.
  #
  # @post connect() function returns RTC_OK if all the
  # notify_connect() return RTC_OK. At this time the connection is
  # completed.  If notify_connect()s return except RTC_OK,
  # connect() calls disconnect() operation with the connector_id to
  # destruct the connection, and then it returns error code from
  # notify_connect().
  #
  # @post The ConnectorProfile argument of the connect() operation
  # returns ConnectorProfile::connector_id and various information
  # about service interfaces that is published by
  # publishInterfaces() in the halfway ports. The connect() and
  # halfway notify_connect() functions never change
  # ConnectorProfile::{name, ports}.
  #
  # @param connector_profile The ConnectorProfile.
  # @return ReturnCode_t The return code of ReturnCode_t type.
  #
  # @endif
  #
  # virtual ReturnCode_t connect(ConnectorProfile& connector_profile)
  def connect(self, connector_profile):
    self._rtcout.RTC_TRACE("connect()")
    if self.isEmptyId(connector_profile):
      guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
      self.setUUID(connector_profile)
      assert(not self.isExistingConnId(connector_profile.connector_id))
      del guard
    else:
      guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
      if self.isExistingConnId(connector_profile.connector_id):
        self._rtcout.RTC_ERROR("Connection already exists.")
        return (RTC.PRECONDITION_NOT_MET,connector_profile)
      del guard

    try:
      retval,connector_profile = connector_profile.ports[0].notify_connect(connector_profile)
      if retval != RTC.RTC_OK:
        self._rtcout.RTC_ERROR("Connection failed. cleanup.")
        self.disconnect(connector_profile.connector_id)
    
      return (retval, connector_profile)
      #return connector_profile.ports[0].notify_connect(connector_profile)
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      return (RTC.BAD_PARAMETER, connector_profile)

    return (RTC.RTC_ERROR, connector_profile)


  ##
  # @if jp
  #
  # @brief [CORBA interface] Port ����³���Τ�Ԥ�
  #
  # ���Υ��ڥ졼�����ϡ�Port�֤���³���Ԥ���ݤˡ�Port�֤�����Ū
  # �˸ƤФ�륪�ڥ졼�����Ǥ��äơ��̾異�ץꥱ�������ץ����
  # �䡢Port�ʳ���RTC��Ϣ���֥�������������ƤӽФ���뤳�Ȥ����ꤵ
  # ��Ƥ��ʤ���
  #
  # notify_connect() ���Τϥƥ�ץ졼�ȥ᥽�åɥѥ�����Ȥ��ơ�����
  # ���饹�Ǽ�������뤳�Ȥ������ publishInterfaces(),
  # subscribeInterfaces() ��2�Ĥδؿ��������ǸƤӽФ��������μ���
  # �ʲ����̤�Ǥ��롣
  #
  # - publishInterfaces(): ���󥿡��ե���������θ���
  # - connectNext(): ���� Port �� notify_connect() �θƤӽФ�
  # - subscribeInterfaces(): ���󥿡��ե���������μ���
  # - ��³�������¸
  #
  # notify_connect() �� ConnectorProfile::ports �˳�Ǽ����Ƥ���
  # Port �ν���˽��äơ����������ɾ��˸ƤӽФ���Ԥ����Ȥˤ�ꡢ��
  # �󥿡��ե���������θ����ȼ������Ϣ�����٤ƤΥݡ��Ȥ��Ф��ƹԤ���
  # ���Υ��������ɸƤӽФ�����������Ǥ���뤳�ȤϤʤ���ɬ��
  # ConnectorProfile::ports �˳�Ǽ����Ƥ������ݡ��Ȥ��Ф��ƹԤ��롣
  #
  # @pre notify_connect() �� ConnectorProfile::ports ��˳�Ǽ�����
  # ���� Port ���ȥꥹ�ȤΤ��������� Port ���Ȥλ��Ȥμ��˳�Ǽ�����
  # ���� Port ���Ф��� notify_connect() ��ƤӽФ����������ä�
  # ConnectorProfile::ports �ˤ����� Port �λ��Ȥ���Ǽ����Ƥ���ɬ��
  # �����롣�⤷�����Ȥλ��Ȥ���Ǽ����Ƥ��ʤ���硢����¾�ν����ˤ�
  # �ꥨ�顼����񤭤���ʤ���С�BAD_PARAMETER ���顼���֤���롣
  #
  # @pre �ƤӽФ����� ConnectorProfile::connector_id �ˤϰ�դ�ID��
  # ���� UUID ���ݻ�����Ƥ���ɬ�פ����롣�̾� connector_id ��
  # connect() �ؿ��ˤ��Ϳ����졢��ʸ���ξ���ư���̤����Ǥ��롣
  #
  # @post ConnectorProfile::name, ConnectorProfile::connector_id,
  # ConnectorProfile::ports �� notify_connect() �θƤӽФ��ˤ��
  # �񤭴������뤳�ȤϤʤ����ѤǤ��롣
  #
  # @post ConnectorProfile::properties �� notify_connect() �������ǡ�
  # ���� Port �����ĥ����ӥ����󥿡��ե������˴ؤ�������¾�� Port
  # �������뤿��ˡ��ץ�ѥƥ����󤬽񤭹��ޤ�롣
  #
  # @post �ʤ���ConnectorProfile::ports �Υꥹ�Ȥκǽ� Port ��
  # notify_connet() ����λ���������Ǥϡ����٤Ƥδ�Ϣ���� Port ��
  # notify_connect() �θƤӽФ�����λ���롣publishInterfaces(),
  # connectNext(), subscribeInterfaces() �������³�������¸�Τ���
  # �줫���ʳ��ǥ��顼��ȯ���������Ǥ⡢���顼�����ɤ�����Ū���ݻ�
  # ����Ƥ��ꡢ�ǽ�����������顼�Υ��顼�����ɤ��֤���롣
  #
  # @param connector_profile ConnectorProfile
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [CORBA interface] Notify the Ports connection
  #
  # This operation is usually called from other ports' connect() or
  # notify_connect() operations when connection between ports is
  # established.  This function is not premised on calling from
  # other functions or application programs.
  #
  # According to the template method pattern, the notify_connect()
  # calls "publishInterfaces()" and "subsctiveInterfaces()"
  # functions, which are premised on implementing in the
  # subclasses. The processing sequence is as follows.
  #
  # - publishInterfaces(): Publishing interface information
  # - connectNext(): Calling notify_connect() of the next port
  # - subscribeInterfaces(): Subscribing interface information
  # - Storing connection profile
  #
  # According to the order of port's references stored in the
  # ConnectorProfile::ports, publishing interface information to
  # all the ports and subscription interface information from all
  # the ports is performed by "notify_connect()"s.  This cascaded
  # call never aborts in the halfway operations, and calling
  # sequence shall be completed for all the ports.
  #
  # @pre notify_connect() calls notify_connect() for the port's
  # reference that is stored in next of this port's reference in
  # the sequence of the ConnectorProfile::ports. Therefore the
  # reference of this port shall be stored in the
  # ConnectorProfile::ports. If this port's reference is not stored
  # in the sequence, BAD_PARAMETER error will be returned, except
  # the return code is overwritten by other operations.
  #
  # @pre UUID shall be set to ConnectorProfile::connector_id as a
  # unique identifier when this operation is called.  Usually,
  # connector_id is given by a connect() function and, the behavior
  # is undefined in the case of a null character.
  #
  # @post ConnectorProfile::name, ConnectorProfile::connector_id,
  # ConnectorProfile::ports are invariant, and they are never
  # rewritten by notify_connect() operations.
  #
  # @post In order to transfer interface information to other
  # ports, interface property information is stored into the
  # ConnectorProfile::properties.
  #
  # @post At the end of notify_connect() operation for the first
  # port stored in the ConnectorProfile::ports sequence, the
  # related ports' notify_connect() invocations complete. Even if
  # errors are raised at the halfway of publishInterfaces(),
  # connectNext(), subscribeInterfaces() and storing process of
  # ConnectorProfile, error codes are saved and the first error is
  # returned.
  #
  # @param connector_profile The ConnectorProfile.
  # @return ReturnCode_t The return code of ReturnCode_t type.
  #
  # @endif
  #
  # virtual ReturnCode_t notify_connect(ConnectorProfile& connector_profile)
  def notify_connect(self, connector_profile):
    self._rtcout.RTC_TRACE("notify_connect()")

    guard_connection = OpenRTM_aist.ScopedLock(self._connection_mutex)

    # publish owned interface information to the ConnectorProfile
    retval = [RTC.RTC_OK for i in range(3)]

    self.onNotifyConnect(self.getName(),connector_profile)
    retval[0] = self.publishInterfaces(connector_profile)
    if retval[0] != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("publishInterfaces() in notify_connect() failed.")

    self.onPublishInterfaces(self.getName(), connector_profile, retval[0])
    if self._onPublishInterfaces:
      self._onPublishInterfaces(connector_profile)

    # call notify_connect() of the next Port
    retval[1], connector_profile = self.connectNext(connector_profile)
    if retval[1] != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("connectNext() in notify_connect() failed.")

    self.onConnectNextport(self.getName(), connector_profile, retval[1])
    # subscribe interface from the ConnectorProfile's information
    if self._onSubscribeInterfaces:
      self._onSubscribeInterfaces(connector_profile)

    retval[2] = self.subscribeInterfaces(connector_profile)
    if retval[2] != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("subscribeInterfaces() in notify_connect() failed.")
      #self.notify_disconnect(connector_profile.connector_id)

    self.onSubscribeInterfaces(self.getName(), connector_profile, retval[2])

    self._rtcout.RTC_PARANOID("%d connectors are existing",
                              len(self._profile.connector_profiles))

    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    # update ConnectorProfile
    index = self.findConnProfileIndex(connector_profile.connector_id)
    if index < 0:
      OpenRTM_aist.CORBA_SeqUtil.push_back(self._profile.connector_profiles,
                                           connector_profile)
      self._rtcout.RTC_PARANOID("New connector_id. Push backed.")

    else:
      self._profile.connector_profiles[index] = connector_profile
      self._rtcout.RTC_PARANOID("Existing connector_id. Updated.")

    for ret in retval:
      if ret != RTC.RTC_OK:
        self.onConnected(self.getName(), connector_profile, ret)
        return (ret, connector_profile)

    # connection established without errors
    if self._onConnected:
      self._onConnected(connector_profile)
    self.onConnected(self.getName(), connector_profile, RTC.RTC_OK)
    return (RTC.RTC_OK, connector_profile)


  ##
  # @if jp
  #
  # @brief [CORBA interface] Port ����³��������
  #
  # ���Υ��ڥ졼������Ϳ����줿 connector_id ���б�������³����
  # ���롣connector_id ���̾�����ƥ����Τˤ����ư�դ� UUID ��ʸ
  # ����Ǥ��ꡢ������ connect()/notify_connect() �θƤӽФ��ˤ���
  # Ω���줿��³�ץ�ե����� ConnectorProfile::connector_id ���б���
  # �롣
  #
  # @pre connector_id �� Port ���ݻ����� ConnectorProfile �ξ��ʤ���
  # ���Ĥ� ID �˰��פ���ʸ����Ǥʤ���Фʤ�ʤ������� Port ������
  # ConnectorProfile �Υꥹ����� connector_id ��Ʊ��� ID �����
  # ConnectorProfile ��¸�ߤ��ʤ���Ф��δؿ��� BAD_PARAMETER ���顼
  # ���֤���
  #
  # @pre connector_id ��Ʊ�� ID ����� ConnectorProfile::ports �ˤ�
  # ͭ���� Port �λ��Ȥ��ޤޤ�Ƥ��ʤ���Фʤ�ʤ���
  #
  # @post disconnect() �ؿ��ϡ�ConnectorProfile::ports �� Port �λ�
  # �ȥꥹ�Ȥ���Ƭ���Ф��ơ�notify_disconnect() ��ƤӽФ������Ȥ�̵
  # ���Ǥ���ʤɡ�notify_disconnect() �θƤӽФ��˼��Ԥ������ˤϡ�
  # ���ȥꥹ�Ȥ���Ƭ������֤���������ޤ� notify_disconnect() �θ�
  # �ӽФ�����notify_disconnect() �θƤӽФ��˰�ĤǤ���������С�
  # notify_disconnect() ���ֵ��ͤ򤽤Τޤ��֤�����Ĥ��������ʤ��ä�
  # ���ˤ� RTC_ERROR ���顼���֤���
  # 
  # @param connector_id ConnectorProfile �� ID
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [CORBA interface] Disconnect the Port
  #
  # This operation destroys connection between this port and the
  # peer port according to given connector_id. Usually connector_id
  # should be a UUID string that is unique in the system.  And the
  # connection, which is established by connect()/notify_connect()
  # functions, is identified by the ConnectorProfile::connector_id.
  #
  # @pre connector_id shall be a character string which is same
  # with ID of at least one of the ConnectorProfiles stored in this
  # port. If ConnectorProfile that has same ID with the given
  # connector_id does not exist in the list of ConnectorProfile,
  # this operation returns BAD_PARAMTER error.
  #
  # @pre ConnectorProfile::ports that is same ID with given
  # connector_id shall store the valid ports' references.
  #
  # @post disconnect() function invokes the notify_disconnect() for
  # the port that is stored in the first of the
  # ConnectorProfile::ports. If notify_disconnect() call fails for
  # the first port, It tries on calling "notify_disconnect()" in
  # order for ports stored in ConnectorProfile::ports until the
  # operation call is succeeded. If notify_disconnect() succeeded
  # for at least one port, it returns return code from
  # notify_disconnect(). If none of notify_connect() call
  # succeeded, it returns RTC_ERROR error.
  #
  # @param connector_id The ID of the ConnectorProfile.
  # @return ReturnCode_t The return code of ReturnCode_t type.
  #
  # @endif
  #
  # virtual ReturnCode_t disconnect(const char* connector_id)
  def disconnect(self, connector_id):
    self._rtcout.RTC_TRACE("disconnect(%s)", connector_id)

    index = self.findConnProfileIndex(connector_id)

    if index < 0:
      self._rtcout.RTC_ERROR("Invalid connector id: %s", connector_id)
      return RTC.BAD_PARAMETER

    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    if index < len(self._profile.connector_profiles):
      prof = self._profile.connector_profiles[index]
    del guard
    
    if len(prof.ports) < 1:
      self._rtcout.RTC_FATAL("ConnectorProfile has empty port list.")
      return RTC.PRECONDITION_NOT_MET

    for i in range(len(prof.ports)):
      p = prof.ports[i]
      try:
        return p.notify_disconnect(connector_id)
      except:
        self._rtcout.RTC_WARN(OpenRTM_aist.Logger.print_exception())
        continue

    self._rtcout.RTC_ERROR("notify_disconnect() for all ports failed.")
    return RTC.RTC_ERROR


  ##
  # @if jp
  #
  # @brief [CORBA interface] Port ����³������Τ�Ԥ�
  #
  # ���Υ��ڥ졼�����ϡ�Port�֤���³������Ԥ���ݤˡ�Port�֤���
  # ��Ū�˸ƤФ�륪�ڥ졼�����Ǥ��ꡢ�̾異�ץꥱ�������ץ���
  # ��䡢 Port �ʳ��� RTC ��Ϣ���֥�������������ƤӽФ���뤳�Ȥ�
  # ���ꤵ��Ƥ��ʤ���
  #
  # notify_disconnect() ���Τϥƥ�ץ졼�ȥ᥽�åɥѥ�����Ȥ��ơ���
  # �֥��饹�Ǽ�������뤳�Ȥ������ unsubscribeInterfaces() �ؿ���
  # �����ǸƤӽФ��������μ��ϰʲ����̤�Ǥ��롣
  #
  # - ConnectorProfile �θ���
  # - ���� Port �� notify_disconnect() �ƤӽФ�
  # - unsubscribeInterfaces()
  # - ConnectorProfile �κ��
  #
  # notify_disconnect() �� ConnectorProfile::ports �˳�Ǽ����Ƥ���
  # Port �ν���˽��äơ����������ɾ��˸ƤӽФ���Ԥ����Ȥˤ�ꡢ��
  # ³�β���򤹤٤Ƥ� Port �����Τ��롣
  #
  # @pre Port ��Ϳ����줿 connector_id ���б����� ConnectorProfile
  # ���ݻ����Ƥ��ʤ���Фʤ�ʤ���
  #
  # @post connector_id ���б����� ConnectorProfile �����Ĥ���ʤ���
  # ���BAD_PARAMETER ���顼���֤���
  #
  # @post ���������ɸƤӽФ���Ԥ��ݤˤ� ConnectorProfile::ports ��
  # �ݻ�����Ƥ��� Port �λ��ȥꥹ�ȤΤ��������Ȥλ��Ȥμ��λ��Ȥ���
  # ���� notify_disconnect() ��ƤӽФ��������θƤӽФ����㳰��ȯ��
  # �������ˤϡ��ƤӽФ��򥹥��åפ��ꥹ�Ȥμ��λ��Ȥ��Ф���
  # notify_disconnect() ��ƤӽФ�����Ĥ�ƤӽФ����������ʤ���硢
  # RTC_ERROR ���顼�����ɤ��֤���
  #
  # @post �ʤ���ConnectorProfile::ports �Υꥹ�Ȥκǽ� Port ��
  # notify_disconnet() ����λ���������Ǥϡ����٤Ƥδ�Ϣ���� Port ��
  # notify_disconnect() �θƤӽФ�����λ���롣
  # 
  # @param connector_id ConnectorProfile �� ID
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [CORBA interface] Notify the Ports disconnection
  #
  # This operation is invoked between Ports internally when the
  # connection is destroied. Generally it is not premised on
  # calling from application programs or RTC objects except Port
  # object.
  #
  # According to the template method pattern, the
  # notify_disconnect() calls unsubsctiveInterfaces() function,
  # which are premised on implementing in the subclasses. The
  # processing sequence is as follows.
  #
  # - Searching ConnectorProfile
  # - Calling notify_disconnect() for the next port
  # - Unsubscribing interfaces
  # - Deleting ConnectorProfile
  #
  # notify_disconnect() notifies disconnection to all the ports by
  # cascaded call to the stored ports in the
  # ConnectorProfile::ports in order.
  #
  # @pre The port shall store the ConnectorProfile having same id
  # with connector_id.
  #
  # @post If ConnectorProfile of same ID with connector_id does not
  # exist, it returns BAD_PARAMETER error.
  #
  # @post For the cascaded call, this operation calls
  # noify_disconnect() for the port that is stored in the next of
  # this port in the ConnectorProfile::ports.  If the operation
  # call raises exception for some failure, it tries to call
  # notify_disconnect() and skips until the operation succeeded.
  # If none of operation call succeeded, it returns RTC_ERROR.
  #
  # @post At the end of notify_disconnect() operation for the first
  # port stored in the ConnectorProfile::ports sequence, the
  # related ports' notify_disconnect() invocations complete.
  #
  # @param connector_id The ID of the ConnectorProfile.
  # @return ReturnCode_t The return code of ReturnCode_t type.
  #
  # @endif
  #
  # virtual ReturnCode_t notify_disconnect(const char* connector_id)
  def notify_disconnect(self, connector_id):
    self._rtcout.RTC_TRACE("notify_disconnect(%s)", connector_id)

    guard_connection = OpenRTM_aist.ScopedLock(self._connection_mutex)
    # The Port of which the reference is stored in the beginning of
    # connectorProfile's PortServiceList is main Port.
    # The main Port has the responsibility of disconnecting all Ports.
    # The subordinate Ports have only responsibility of deleting its own
    # ConnectorProfile.

    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)

    index = self.findConnProfileIndex(connector_id)

    if index < 0:
      self._rtcout.RTC_ERROR("Invalid connector id: %s", connector_id)
      return RTC.BAD_PARAMETER

    prof = RTC.ConnectorProfile(self._profile.connector_profiles[index].name,
                                self._profile.connector_profiles[index].connector_id,
                                self._profile.connector_profiles[index].ports,
                                self._profile.connector_profiles[index].properties)
    self.onNotifyDisconnect(self.getName(), prof)

    retval = self.disconnectNext(prof)
    self.onDisconnectNextport(self.getName(), prof, retval)

    if self._onUnsubscribeInterfaces:
      self._onUnsubscribeInterfaces(prof)
    self.onUnsubscribeInterfaces(self.getName(), prof)
    self.unsubscribeInterfaces(prof)

    if self._onDisconnected:
      self._onDisconnected(prof)

    OpenRTM_aist.CORBA_SeqUtil.erase(self._profile.connector_profiles, index)
    
    self.onDisconnected(self.getName(), prof, retval)
    return retval


  ##
  # @if jp
  #
  # @brief [CORBA interface] Port ������³��������
  #
  # ���Υ��ڥ졼�����Ϥ��� Port �˴�Ϣ�������Ƥ���³�������롣
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief [CORBA interface] Connect the Port
  #
  # This operation destroys all connection channels owned by the Port.
  #
  # @return ReturnCode_t The return code of this operation.
  #
  # @endif
  # virtual ReturnCode_t disconnect_all()
  def disconnect_all(self):
    self._rtcout.RTC_TRACE("disconnect_all()")
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    plist = copy.deepcopy(self._profile.connector_profiles)
    del guard
    
    retcode = RTC.RTC_OK
    len_ = len(plist)
    self._rtcout.RTC_DEBUG("disconnecting %d connections.", len_)

    # disconnect all connections
    # Call disconnect() for each ConnectorProfile.
    for i in range(len_):
      tmpret = self.disconnect(plist[i].connector_id)
      if tmpret != RTC.RTC_OK:
        retcode = tmpret

    return retcode


  #============================================================
  # Local operations
  #============================================================

  ##
  # @if jp
  # @brief Port ��̾�������ꤹ��
  #
  # Port ��̾�������ꤹ�롣����̾���� Port ���ݻ����� PortProfile.name
  # ��ȿ�Ǥ���롣
  #
  # @param self
  # @param name Port ��̾��
  #
  # @else
  # @brief Set the name of this Port
  #
  # This operation sets the name of this Port. The given Port's name is
  # applied to Port's PortProfile.name.
  #
  # @param name The name of this Port.
  #
  # @endif
  # void setName(const char* name);
  def setName(self, name):
    self._rtcout.RTC_TRACE("setName(%s)", name)
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    self._profile.name = name
    return

  ##
  # @if jp
  # @brief Port ��̾�����������
  # @else
  # @brief Get the name of this Port
  # @return The name of this Port.
  # @endif
  #
  # const char* PortBase::getName() const
  def getName(self):
    self._rtcout.RTC_TRACE("getName() = %s", self._profile.name)
    return self._profile.name


  ##
  # @if jp
  # @brief PortProfile���������
  #
  # Port���ݻ����� PortProfile �� const ���Ȥ��֤���
  #
  # @param self
  #
  # @return ���� Port �� PortProfile
  #
  # @else
  # @brief Get the PortProfile of the Port
  #
  # This operation returns const reference of the PortProfile.
  #
  # @return the PortProfile of the Port
  #
  # @endif
  # const PortProfile& getProfile() const;
  def getProfile(self):
    self._rtcout.RTC_TRACE("getProfile()")
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    return self._profile


  ##
  # @if jp
  #
  # @brief Port �Υ��֥������Ȼ��Ȥ����ꤹ��
  #
  # ���Υ��ڥ졼������ Port �� PortProfile �ˤ��� Port ���Ȥ�
  # ���֥������Ȼ��Ȥ����ꤹ�롣
  #
  # @param self
  # @param port_ref ���� Port �Υ��֥������Ȼ���
  #
  # @else
  #
  # @brief Set the object reference of this Port
  #
  # This operation sets the object reference itself
  # to the Port's PortProfile.
  #
  # @param The object reference of this Port.
  #
  # @endif
  # void setPortRef(PortService_ptr port_ref);
  def setPortRef(self, port_ref):
    self._rtcout.RTC_TRACE("setPortRef()")
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    self._profile.port_ref = port_ref


  ##
  # @if jp
  #
  # @brief Port �Υ��֥������Ȼ��Ȥ��������
  #
  # ���Υ��ڥ졼������ Port �� PortProfile ���ݻ����Ƥ���
  # ���� Port ���ȤΥ��֥������Ȼ��Ȥ�������롣
  #
  # @param self
  #
  # @return ���� Port �Υ��֥������Ȼ���
  #
  # @else
  #
  # @brief Get the object reference of this Port
  #
  # This operation returns the object reference
  # that is stored in the Port's PortProfile.
  #
  # @return The object reference of this Port.
  #
  # @endif
  # PortService_ptr getPortRef();
  def getPortRef(self):
    self._rtcout.RTC_TRACE("getPortRef()")
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    return self._profile.port_ref


  ##
  # @if jp
  #
  # @brief Port �� owner �� RTObject ����ꤹ��
  #
  # ���Υ��ڥ졼������ Port �� PortProfile.owner �����ꤹ�롣
  #
  # @param self
  # @param owner ���� Port ���ͭ���� RTObject �λ���
  #
  # @else
  #
  # @brief Set the owner RTObject of the Port
  #
  # This operation sets the owner RTObject of this Port.
  #
  # @param owner The owner RTObject's reference of this Port
  #
  # @endif
  # void setOwner(RTObject_ptr owner);
  def setOwner(self, owner):
    prof = owner.get_component_profile()
    self._ownerInstanceName = prof.instance_name
    self._rtcout.RTC_TRACE("setOwner(%s)", self._ownerInstanceName)

    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    plist = self._profile.name.split(".")
    if not self._ownerInstanceName:
      self._rtcout.RTC_ERROR("Owner is not set.")
      self._rtcout.RTC_ERROR("addXXXPort() should be called in onInitialize().")
    portname = self._ownerInstanceName+"."+plist[-1]

    self._profile.owner = owner
    self._profile.name = portname


  #============================================================
  # callbacks
  #============================================================

  ##
  # @if jp
  #
  # @brief ���󥿡��ե��������������ݤ˸ƤФ�륳����Хå��򥻥åȤ���
  #
  # ���Υ��ڥ졼�����ϡ����Υݡ��Ȥ���³���ˡ��ݡ��ȼ��Ȥ����ĥ���
  # �ӥ����󥿡��ե����������������륿���ߥ󥰤ǸƤФ�륳����Х�
  # ���ե��󥯥��򥻥åȤ��롣
  #
  # ������Хå��ե��󥯥��ν�ͭ���ϡ��ƤӽФ�¦�ˤ��ꡢ���֥�������
  # ��ɬ�פʤ��ʤä����˲��Τ���ΤϸƤӽФ�¦����Ǥ�Ǥ��롣
  #
  # ���Υ�����Хå��ե��󥯥��ϡ�PortBase���饹�β��۴ؿ��Ǥ���
  # publishInterfaces() ���ƤФ줿���Ȥˡ�Ʊ������ ConnectorProfile ��
  # �Ȥ�˸ƤӽФ���롣���Υ�����Хå������Ѥ��ơ�
  # publishInterfaces() ���������� ConnectorProfile ���ѹ����뤳�Ȥ���
  # ǽ�Ǥ��뤬����³�ط���������򾷤��ʤ��褦��ConnectorProfile ��
  # �ѹ��ˤ���դ��פ��롣
  #
  # @param on_publish ConnectionCallback �Υ��֥��饹���֥������ȤΥݥ���
  #
  # @else
  #
  # @brief Setting callback called on publish interfaces
  #
  # This operation sets a functor that is called after publishing
  # interfaces process when connecting between ports.
  #
  # Since the ownership of the callback functor object is owned by
  # the caller, it has the responsibility of object destruction.
  # 
  # The callback functor is called after calling
  # publishInterfaces() that is virtual member function of the
  # PortBase class with an argument of ConnectorProfile type that
  # is same as the argument of publishInterfaces() function.
  # Although by using this functor, you can modify the ConnectorProfile
  # published by publishInterfaces() function, the modification
  # should be done carefully for fear of causing connection
  # inconsistency.
  #
  # @param on_publish a pointer to ConnectionCallback's subclasses
  #
  # @endif
  #
  # void setOnPublishInterfaces(ConnectionCallback* on_publish);
  def setOnPublishInterfaces(self, on_publish):
    self._onPublishInterfaces = on_publish
    return


  ##
  # @if jp
  #
  # @brief ���󥿡��ե��������������ݤ˸ƤФ�륳����Хå��򥻥åȤ���
  #
  # ���Υ��ڥ졼�����ϡ����Υݡ��Ȥ���³���ˡ����Υݡ��Ȥ����ĥ���
  # �ӥ����󥿡��ե����������������륿���ߥ󥰤ǸƤФ�륳����Х�
  # ���ե��󥯥��򥻥åȤ��롣
  #
  # ������Хå��ե��󥯥��ν�ͭ���ϡ��ƤӽФ�¦�ˤ��ꡢ���֥�������
  # ��ɬ�פʤ��ʤä����˲��Τ���ΤϸƤӽФ�¦����Ǥ�Ǥ��롣
  #
  # ���Υ�����Хå��ե��󥯥��ϡ�PortBase���饹�β��۴ؿ��Ǥ���
  # subscribeInterfaces() ���ƤФ�����ˡ�Ʊ������ ConnectorProfile ��
  # �Ȥ�˸ƤӽФ���롣���Υ�����Хå������Ѥ��ơ�
  # subscribeInterfaces() ��Ϳ���� ConnectorProfile ���ѹ����뤳�Ȥ���
  # ǽ�Ǥ��뤬����³�ط���������򾷤��ʤ��褦��ConnectorProfile ��
  # �ѹ��ˤ���դ��פ��롣
  #
  # @param on_subscribe ConnectionCallback �Υ��֥��饹���֥������ȤΥݥ���
  #
  # @else
  #
  # @brief Setting callback called on publish interfaces
  #
  # This operation sets a functor that is called before subscribing
  # interfaces process when connecting between ports.
  #
  # Since the ownership of the callback functor object is owned by
  # the caller, it has the responsibility of object destruction.
  # 
  # The callback functor is called before calling
  # subscribeInterfaces() that is virtual member function of the
  # PortBase class with an argument of ConnectorProfile type that
  # is same as the argument of subscribeInterfaces() function.
  # Although by using this functor, you can modify ConnectorProfile
  # argument for subscribeInterfaces() function, the modification
  # should be done carefully for fear of causing connection
  # inconsistency.
  #
  # @param on_subscribe a pointer to ConnectionCallback's subclasses
  #
  # @endif
  #
  #void setOnSubscribeInterfaces(ConnectionCallback* on_subscribe);
  def setOnSubscribeInterfaces(self, on_subscribe):
    self._onSubscribeInterfaces = on_subscribe
    return


  ##
  # @if jp
  #
  # @brief ��³��λ���˸ƤФ�륳����Хå��򥻥åȤ���
  #
  # ���Υ��ڥ졼�����ϡ����Υݡ��Ȥ���³��λ���˸ƤФ�롢������Х�
  # ���ե��󥯥��򥻥åȤ��롣
  #
  # ������Хå��ե��󥯥��ν�ͭ���ϡ��ƤӽФ�¦�ˤ��ꡢ���֥�������
  # ��ɬ�פʤ��ʤä����˲��Τ���ΤϸƤӽФ�¦����Ǥ�Ǥ��롣
  #
  # ���Υ�����Хå��ե��󥯥��ϡ��ݡ��Ȥ���³�¹Դؿ��Ǥ���
  # notify_connect() �ν�λľ���ˡ���³���������ｪλ����ݤ˸¤ä�
  # �ƤӽФ���륳����Хå��Ǥ��롣��³�����β����ǥ��顼��ȯ������
  # ���ˤϸƤӽФ���ʤ���
  # 
  # ���Υ�����Хå��ե��󥯥��� notify_connect() �� out �ѥ�᡼��
  # �Ȥ����֤��Τ�Ʊ������ ConnectorProfile �ȤȤ�˸ƤӽФ����Τǡ�
  # ������³�ˤ����Ƹ������줿���٤ƤΥ��󥿡��ե�������������뤳��
  # ���Ǥ��롣���Υ�����Хå������Ѥ��ơ�notify_connect() ���֤�
  # ConnectorProfile ���ѹ����뤳�Ȥ���ǽ�Ǥ��뤬����³�ط���������
  # �򾷤��ʤ��褦��ConnectorProfile ���ѹ��ˤ���դ��פ��롣
  #
  # @param on_subscribe ConnectionCallback �Υ��֥��饹���֥������ȤΥݥ���
  #
  # @else
  #
  # @brief Setting callback called on connection established
  #
  # This operation sets a functor that is called when connection
  # between ports established.
  #
  # Since the ownership of the callback functor object is owned by
  # the caller, it has the responsibility of object destruction.
  # 
  # The callback functor is called only when notify_connect()
  # function successfully returns. In case of error, the functor
  # will not be called.
  #
  # Since this functor is called with ConnectorProfile argument
  # that is same as out-parameter of notify_connect() function, you
  # can get all the information of published interfaces of related
  # ports in the connection.  Although by using this functor, you
  # can modify ConnectorProfile argument for out-paramter of
  # notify_connect(), the modification should be done carefully for
  # fear of causing connection inconsistency.
  #
  # @param on_subscribe a pointer to ConnectionCallback's subclasses
  #
  # @endif
  #
  # void setOnConnected(ConnectionCallback* on_connected);
  def setOnConnected(self, on_connected):
    self._onConnected = on_connected
    return


  ##
  # @if jp
  #
  # @brief ���󥿡��ե��������������ݤ˸ƤФ�륳����Хå��򥻥åȤ���
  #
  # ���Υ��ڥ졼�����ϡ����Υݡ��Ȥ���³���ˡ����Υݡ��Ȥ����ĥ���
  # �ӥ����󥿡��ե����������������륿���ߥ󥰤ǸƤФ�륳����Х�
  # ���ե��󥯥��򥻥åȤ��롣
  #
  # ������Хå��ե��󥯥��ν�ͭ���ϡ��ƤӽФ�¦�ˤ��ꡢ���֥�������
  # ��ɬ�פʤ��ʤä����˲��Τ���ΤϸƤӽФ�¦����Ǥ�Ǥ��롣
  #
  # ���Υ�����Хå��ե��󥯥��ϡ�PortBase���饹�β��۴ؿ��Ǥ���
  # unsubscribeInterfaces() ���ƤФ�����ˡ�Ʊ������ ConnectorProfile ��
  # �Ȥ�˸ƤӽФ���롣���Υ�����Хå������Ѥ��ơ�
  # unsubscribeInterfaces() ��Ϳ���� ConnectorProfile ���ѹ����뤳�Ȥ���
  # ǽ�Ǥ��뤬����³�ط���������򾷤��ʤ��褦��ConnectorProfile ��
  # �ѹ��ˤ���դ��פ��롣
  #
  # @param on_unsubscribe ConnectionCallback �Υ��֥��饹���֥�����
  # �ȤΥݥ���
  #
  # @else
  #
  # @brief Setting callback called on unsubscribe interfaces
  #
  # This operation sets a functor that is called before unsubscribing
  # interfaces process when disconnecting between ports.
  #
  # Since the ownership of the callback functor object is owned by
  # the caller, it has the responsibility of object destruction.
  # 
  # The callback functor is called before calling
  # unsubscribeInterfaces() that is virtual member function of the
  # PortBase class with an argument of ConnectorProfile type that
  # is same as the argument of unsubscribeInterfaces() function.
  # Although by using this functor, you can modify ConnectorProfile
  # argument for unsubscribeInterfaces() function, the modification
  # should be done carefully for fear of causing connection
  # inconsistency.
  #
  # @param on_unsubscribe a pointer to ConnectionCallback's subclasses
  #
  # @endif
  #
  # void setOnUnsubscribeInterfaces(ConnectionCallback* on_subscribe);
  def setOnUnsubscribeInterfaces(self, on_subscribe):
    self._onUnsubscribeInterfaces = on_subscribe
    return


  ##
  # @if jp
  #
  # @brief ��³����˸ƤФ�륳����Хå��򥻥åȤ���
  #
  # ���Υ��ڥ졼�����ϡ����Υݡ��Ȥ���³������˸ƤФ�롢������Х�
  # ���ե��󥯥��򥻥åȤ��롣
  #
  # ������Хå��ե��󥯥��ν�ͭ���ϡ��ƤӽФ�¦�ˤ��ꡢ���֥�������
  # ��ɬ�פʤ��ʤä����˲��Τ���ΤϸƤӽФ�¦����Ǥ�Ǥ��롣
  #
  # ���Υ�����Хå��ե��󥯥��ϡ��ݡ��Ȥ���³����¹Դؿ��Ǥ���
  # notify_disconnect() �ν�λľ���ˡ��ƤӽФ���륳����Хå��Ǥ��롣
  # 
  # ���Υ�����Хå��ե��󥯥�����³���б����� ConnectorProfile �Ȥ�
  # ��˸ƤӽФ���롣���� ConnectorProfile �Ϥ��Υե��󥯥��ƽФ���
  # ���˴������Τǡ��ѹ����ۤ��˱ƶ���Ϳ���뤳�ȤϤʤ���
  #
  # @param on_disconnected ConnectionCallback �Υ��֥��饹���֥�����
  # �ȤΥݥ���
  #
  # @else
  #
  # @brief Setting callback called on disconnected
  #
  # This operation sets a functor that is called when connection
  # between ports is destructed.
  #
  # Since the ownership of the callback functor object is owned by
  # the caller, it has the responsibility of object destruction.
  # 
  # The callback functor is called just before notify_disconnect()
  # that is disconnection execution function returns.
  #
  # This functor is called with argument of corresponding
  # ConnectorProfile.  Since this ConnectorProfile will be
  # destructed after calling this functor, modifications never
  # affect others.
  #
  # @param on_disconnected a pointer to ConnectionCallback's subclasses
  #
  # @endif
  #
  # void setOnDisconnected(ConnectionCallback* on_disconnected);
  def setOnDisconnected(self, on_disconnected):
    self._onDisconnected = on_disconnected
    return

  # void setOnConnectionLost(ConnectionCallback* on_connection_lost);
  def setOnConnectionLost(self, on_connection_lost):
    self._onConnectionLost = on_connection_lost
    return


  ##
  # @if jp
  # @brief PortConnectListeners �Υۥ���򥻥åȤ���
  #
  # �ݡ��Ȥ���³�˴ؤ���ꥹ�ʷ����ݻ�����ۥ�����饹�ؤΥݥ��󥿤�
  # ���åȤ��롣���δؿ����̾�Ƥ�RTObject����ƤФ졢RTObject������
  # �ۥ�����饹�ؤΥݥ��󥿤����åȤ���롣
  #
  # @param portconnListeners PortConnectListeners ���֥������ȤΥݥ���
  #
  # @else
  # @brief Setting PortConnectListener holder
  #
  # This operation sets a functor that is called when connection
  # of this port does lost. 
  #
  # @param on_connection_lost a pointer to ConnectionCallback's subclasses
  #
  # @endif
  #
  # void setPortConnectListenerHolder(PortConnectListeners* portconnListeners);
  def setPortConnectListenerHolder(self, portconnListeners):
    self._portconnListeners = portconnListeners
    return


  ##
  # @if jp
  #
  # @brief Interface ������������(���֥��饹������)
  #
  # ���Υ��ڥ졼�����ϡ�notify_connect() �����������󥹤λϤ�˥�����
  # �����ؿ��Ǥ��롣
  # notify_connect() �Ǥϡ�
  #
  # - publishInterfaces()
  # - connectNext()
  # - subscribeInterfaces()
  # - updateConnectorProfile()
  #
  # �ν�� protected �ؿ��������뤵����³�������Ԥ��롣
  # <br>
  # ��� Port �ǤϤ��Υ��ڥ졼�����򥪡��С��饤�ɤ��������Ȥ���
  # Ϳ����줿 ConnectorProfile �˽���������Ԥ����ѥ�᡼������Ŭ��
  # �Ǥ���С�RteurnCode_t ���Υ��顼�����ɤ��֤���
  # �̾� publishInterafaces() ��ˤ����Ƥϡ����� Port ��°����
  # ���󥿡��ե������˴ؤ������� ConnectorProfile ���Ф���Ŭ�ڤ����ꤷ
  # ¾�� Port �����Τ��ʤ���Фʤ�ʤ���
  # <br>
  # �ޤ������δؿ��������뤵����ʳ��Ǥϡ�¾�� Port �� Interface �˴ؤ���
  # ����Ϥ��٤ƴޤޤ�Ƥ��ʤ��Τǡ�¾�� Port �� Interface ������������
  # �� subscribeInterfaces() ��ǹԤ���٤��Ǥ��롣
  # <br>
  # ���Υ��ڥ졼�����ϡ������� connector_id ���Ф��Ƥ���³��������
  # ��¸�� connector_id ���Ф��ƤϹ�����Ŭ�ڤ˹Ԥ���ɬ�פ����롣<BR>
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  # @param connector_profile ��³�˴ؤ���ץ�ե��������
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Publish interface information
  #
  # This operation is pure virutal method that would be called at the
  # beginning of the notify_connect() process sequence.
  # In the notify_connect(), the following methods would be called in order.
  #
  # - publishInterfaces()
  # - connectNext()
  # - subscribeInterfaces()
  # - updateConnectorProfile() 
  #
  # In the concrete Port, this method should be overridden. This method
  # processes the given ConnectorProfile argument and if the given parameter
  # is invalid, it would return error code of ReturnCode_t.
  # Usually, publishInterfaces() method should set interfaces information
  # owned by this Port, and publish it to the other Ports.
  # <br>
  # When this method is called, other Ports' interfaces information may not
  # be completed. Therefore, the process to obtain other Port's interfaces
  # information should be done in the subscribeInterfaces() method.
  # <br>
  # This operation should create the new connection for the new
  # connector_id, and should update the connection for the existing
  # connection_id.
  #
  # @param connector_profile The connection profile information
  # @return The return code of ReturnCode_t type.
  #
  #@endif
  def publishInterfaces(self, connector_profile):
    pass


  ##
  # @if jp
  #
  # @brief ���� Port ���Ф��� notify_connect() �򥳡��뤹��
  #
  # ConnectorProfile �� port_ref ��˳�Ǽ����Ƥ��� Port �Υ��֥�������
  # ��ե���󥹤Υ������󥹤��椫�顢���Ȥ� Port �μ��� Port ���Ф���
  # notify_connect() �򥳡��뤹�롣
  #
  # @param self
  # @param connector_profile ��³�˴ؤ���ץ�ե��������
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Call notify_connect() of the next Port
  #
  # This operation calls the notify_connect() of the next Port's 
  # that stored in ConnectorProfile's port_ref sequence.
  #
  # @param connector_profile The connection profile information
  #
  # @return The return code of ReturnCode_t type.
  #
  # @endif
  # virtual ReturnCode_t connectNext(ConnectorProfile& connector_profile);
  def connectNext(self, connector_profile):
    index = OpenRTM_aist.CORBA_SeqUtil.find(connector_profile.ports,
                                            self.find_port_ref(self._profile.port_ref))
    if index < 0:
      return (RTC.BAD_PARAMETER, connector_profile)

    index += 1
    if index < len(connector_profile.ports):
      p = connector_profile.ports[index]
      return p.notify_connect(connector_profile)

    return (RTC.RTC_OK, connector_profile)


  ##
  # @if jp
  #
  # @brief ���� Port ���Ф��� notify_disconnect() �򥳡��뤹��
  #
  # ConnectorProfile �� port_ref ��˳�Ǽ����Ƥ��� Port �Υ��֥�������
  # ��ե���󥹤Υ������󥹤��椫�顢���Ȥ� Port �μ��� Port ���Ф���
  # notify_disconnect() �򥳡��뤹�롣
  #
  # @param self
  # @param connector_profile ��³�˴ؤ���ץ�ե��������
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Call notify_disconnect() of the next Port
  #
  # This operation calls the notify_disconnect() of the next Port's 
  # that stored in ConnectorProfile's port_ref sequence.
  #
  # @param connector_profile The connection profile information
  #
  # @return The return code of ReturnCode_t type.
  #
  # @endif
  # virtual ReturnCode_t disconnectNext(ConnectorProfile& connector_profile);
  def disconnectNext(self, connector_profile):
    index = OpenRTM_aist.CORBA_SeqUtil.find(connector_profile.ports,
                                            self.find_port_ref(self._profile.port_ref))
    if index < 0:
      return RTC.BAD_PARAMETER

    if index == (len(connector_profile.ports) - 1):
      return RTC.RTC_OK

    index += 1

    while index < len(connector_profile.ports):
      p = connector_profile.ports[index]
      index += 1
      try:
        return p.notify_disconnect(connector_profile.connector_id)
      except:
        self._rtcout.RTC_WARN(OpenRTM_aist.Logger.print_exception())
        continue

    return RTC.RTC_ERROR


  ##
  # @if jp
  #
  # @brief Interface ������������(���֥��饹������)
  #
  # ���Υ��ڥ졼�����ϡ�notify_connect() �����������󥹤���֤˥�����
  # �����ؿ��Ǥ��롣
  # notify_connect() �Ǥϡ�
  #
  #  - publishInterfaces()
  #  - connectNext()
  #  - subscribeInterfaces()
  #  - updateConnectorProfile()
  #
  # �ν�� protected �ؿ��������뤵����³�������Ԥ��롣
  # <br>
  # ��� Port �ǤϤ��Υ��ڥ졼�����򥪡��С��饤�ɤ��������Ȥ���
  # Ϳ����줿 ConnectorProfile �˽���������Ԥ����ѥ�᡼������Ŭ��
  # �Ǥ���С�RteurnCode_t ���Υ��顼�����ɤ��֤���
  # ���� ConnectorProfile �ˤ�¾�� Port �� Interface �˴ؤ������
  # ���ƴޤޤ�Ƥ��롣
  # �̾� subscribeInterafaces() ��ˤ����Ƥϡ����� Port �����Ѥ���
  # Interface �˴ؤ���������������׵�¦�Υ��󥿡��ե��������Ф���
  # ��������ꤷ�ʤ���Фʤ�ʤ���
  # <br>
  # ���Υ��ڥ졼�����ϡ������� connector_id ���Ф��Ƥ���³��������
  # ��¸�� connector_id ���Ф��ƤϹ�����Ŭ�ڤ˹Ԥ���ɬ�פ����롣<BR>
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  # @param connector_profile ��³�˴ؤ���ץ�ե��������
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Publish interface information
  #
  # This operation is pure virutal method that would be called at the
  # mid-flow of the notify_connect() process sequence.
  # In the notify_connect(), the following methods would be called in order.
  #
  #  - publishInterfaces()
  #  - connectNext()
  #  - subscribeInterfaces()
  #  - updateConnectorProfile()
  #
  # In the concrete Port, this method should be overridden. This method
  # processes the given ConnectorProfile argument and if the given parameter
  # is invalid, it would return error code of ReturnCode_t.
  # The given argument ConnectorProfile includes all the interfaces
  # information in it.
  # Usually, subscribeInterafaces() method obtains information of interfaces
  # from ConnectorProfile, and should set it to the interfaces that require
  # them.
  # <br>
  # This operation should create the new connection for the new
  # connector_id, and should update the connection for the existing
  # connection_id.
  #
  # @param connector_profile The connection profile information
  #
  # @return The return code of ReturnCode_t type.
  #
  #@endif
  def subscribeInterfaces(self, connector_profile):
    pass


  ##
  # @if jp
  #
  # @brief Interface ����³��������(���֥��饹������)
  #
  # ���Υ��ڥ졼�����ϡ�notify_disconnect() �����������󥹤ν����˥�����
  # �����ؿ��Ǥ��롣
  # notify_disconnect() �Ǥϡ�
  #  - disconnectNext()
  #  - unsubscribeInterfaces()
  #  - eraseConnectorProfile()
  # �ν�� protected �ؿ��������뤵����³����������Ԥ��롣
  # <br>
  # ��� Port �ǤϤ��Υ��ڥ졼�����򥪡��С��饤�ɤ��������Ȥ���
  # Ϳ����줿 ConnectorProfile �˽�����³���������Ԥ���<BR>
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  # @param connector_profile ��³�˴ؤ���ץ�ե��������
  #
  # @else
  #
  # @brief Disconnect interface connection
  #
  # This operation is pure virutal method that would be called at the
  # end of the notify_disconnect() process sequence.
  # In the notify_disconnect(), the following methods would be called.
  #  - disconnectNext()
  #  - unsubscribeInterfaces()
  #  - eraseConnectorProfile() 
  # <br>
  # In the concrete Port, this method should be overridden. This method
  # processes the given ConnectorProfile argument and disconnect interface
  # connection.
  #
  # @param connector_profile The connection profile information
  #
  # @endif
  def unsubscribeInterfaces(self, connector_profile):
    pass


  ##
  # @if jp
  #
  # @brief ��³�κ���������ꤹ�롣
  #
  # @param limit_value �����
  #
  # @else
  #
  # @brief Set the maximum number of connections
  #
  #
  # @param limit_value The maximum number of connections
  #
  # @endif
  #
  # virtual void setConnectionLimit(int limit_value);
  def setConnectionLimit(self, limit_value):
    self._connectionLimit = limit_value
    return
    

  ##
  # @if jp
  # @brief Interface������������
  #
  # Interface�����������롣
  #
  #  dataport.dataflow_type
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  # @brief Publish interface information
  #
  # Publish interface information.
  #
  #
  # @return The return code of ReturnCode_t type
  #
  # @endif
  #
  # virtual ReturnCode_t _publishInterfaces(void);
  def _publishInterfaces(self):
    if not (self._connectionLimit < 0) :
      if self._connectionLimit <= len(self._profile.connector_profiles):
        self._rtcout.RTC_PARANOID("Connected number has reached the limitation.")
        self._rtcout.RTC_PARANOID("Can connect the port up to %d ports.",
                                  self._connectionLimit)
        self._rtcout.RTC_PARANOID("%d connectors are existing",
                                  len(self._profile.connector_profiles))
        return RTC.RTC_ERROR

    return RTC.RTC_OK


  ##
  # @if jp
  #
  # @brief ConnectorProfile �� connector_id �ե�����ɤ������ɤ���Ƚ��
  #
  # ���ꤵ�줿 ConnectorProfile �� connector_id �����Ǥ��뤫�ɤ�����Ƚ���
  # �Ԥ���
  #
  # @param self
  # @param connector_profile Ƚ���оݥ��ͥ����ץ�ե�����
  #
  # @return ������Ϳ����줿 ConnectorProfile �� connector_id �����Ǥ���С�
  #         true�������Ǥʤ���� false ���֤���
  #
  # @else
  #
  # @brief Whether connector_id of ConnectorProfile is empty
  #
  # @return If the given ConnectorProfile's connector_id is empty string,
  #         it returns true.
  #
  # @endif
  # bool isEmptyId(const ConnectorProfile& connector_profile) const;
  def isEmptyId(self, connector_profile):
    return connector_profile.connector_id == ""


  ##
  # @if jp
  #
  # @brief UUID����������
  #
  # ���Υ��ڥ졼������ UUID ���������롣
  #
  # @param self
  #
  # @return uuid
  #
  # @else
  #
  # @brief Get the UUID
  #
  # This operation generates UUID.
  #
  # @return uuid
  #
  # @endif
  # const std::string getUUID() const;
  def getUUID(self):
    return str(OpenRTM_aist.uuid1())


  ##
  # @if jp
  #
  # @brief UUID�������� ConnectorProfile �˥��åȤ���
  #
  # ���Υ��ڥ졼������ UUID ����������ConnectorProfile �˥��åȤ��롣
  #
  # @param self
  # @param connector_profile connector_id �򥻥åȤ��� ConnectorProfile
  #
  # @else
  #
  # @brief Create and set the UUID to the ConnectorProfile
  #
  # This operation generates and set UUID to the ConnectorProfile.
  #
  # @param connector_profile ConnectorProfile to be set connector_id
  #
  # @endif
  # void setUUID(ConnectorProfile& connector_profile) const;
  def setUUID(self, connector_profile):
    connector_profile.connector_id = self.getUUID()
    assert(connector_profile.connector_id != "")


  ##
  # @if jp
  #
  # @brief id ����¸�� ConnectorProfile �Τ�Τ��ɤ���Ƚ�ꤹ��
  #
  # ���Υ��ڥ졼������Ϳ����줿 ID ����¸�� ConnectorProfile �Υꥹ�����
  # ¸�ߤ��뤫�ɤ���Ƚ�ꤹ�롣
  #
  # @param self
  # @param id_ Ƚ�ꤹ�� connector_id
  #
  # @return id ��¸��Ƚ����
  #
  # @else
  #
  # @brief Whether the given id exists in stored ConnectorProfiles
  #
  # This operation returns boolean whether the given id exists in 
  # the Port's ConnectorProfiles.
  #
  # @param id connector_id to be find in Port's ConnectorProfiles
  #
  # @endif
  # bool isExistingConnId(const char* id);
  def isExistingConnId(self, id_):
    return OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                           self.find_conn_id(id_)) >= 0


  ##
  # @if jp
  #
  # @brief id ����� ConnectorProfile ��õ��
  #
  # ���Υ��ڥ졼������Ϳ����줿 ID ����� ConnectorProfile �� Port ��
  # ��� ConnectorProfile �Υꥹ���椫��õ����
  # �⤷��Ʊ��� id ����� ConnectorProfile ���ʤ���С����� ConnectorProfile
  # ���֤���롣
  #
  # @param self
  # @param id_ �������� connector_id
  #
  # @return connector_id ����� ConnectorProfile
  #
  # @else
  #
  # @brief Find ConnectorProfile with id
  #
  # This operation returns ConnectorProfile with the given id from Port's
  # ConnectorProfiles' list.
  # If the ConnectorProfile with connector id that is identical with the
  # given id does not exist, empty ConnectorProfile is returned.
  #
  # @param id the connector_id to be searched in Port's ConnectorProfiles
  #
  # @return CoonectorProfile with connector_id
  #
  # @endif
  # ConnectorProfile findConnProfile(const char* id);
  def findConnProfile(self, id_):
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                            self.find_conn_id(id_))
    if index < 0 or index >= len(self._profile.connector_profiles):
      return RTC.ConnectorProfile("","",[],[])

    return self._profile.connector_profiles[index]


  ##
  # @if jp
  #
  # @brief id ����� ConnectorProfile ��õ��
  #
  # ���Υ��ڥ졼������Ϳ����줿 ID ����� ConnectorProfile �� Port ��
  # ��� ConnectorProfile �Υꥹ���椫��õ������ǥå������֤���
  # �⤷��Ʊ��� id ����� ConnectorProfile ���ʤ���С�-1 ���֤���
  #
  # @param self
  # @param id_ �������� connector_id
  #
  # @return Port �� ConnectorProfile �ꥹ�ȤΥ���ǥå���
  #
  # @else
  #
  # @brief Find ConnectorProfile with id
  #
  # This operation returns ConnectorProfile with the given id from Port's
  # ConnectorProfiles' list.
  # If the ConnectorProfile with connector id that is identical with the
  # given id does not exist, empty ConnectorProfile is returned.
  #
  # @param id the connector_id to be searched in Port's ConnectorProfiles
  #
  # @return The index of ConnectorProfile of the Port
  #
  # @endif
  # CORBA::Long findConnProfileIndex(const char* id);
  def findConnProfileIndex(self, id_):
    return OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                           self.find_conn_id(id_))


  ##
  # @if jp
  #
  # @brief ConnectorProfile ���ɲä⤷���Ϲ���
  #
  # ���Υ��ڥ졼������Ϳ����줿Ϳ����줿 ConnectorProfile ��
  # Port ���ɲä⤷���Ϲ�����¸���롣
  # Ϳ����줿 ConnectorProfile �� connector_id ��Ʊ�� ID �����
  # ConnectorProfile ���ꥹ�Ȥˤʤ���С��ꥹ�Ȥ��ɲä���
  # Ʊ�� ID ��¸�ߤ���� ConnectorProfile ������¸���롣
  #
  # @param self
  # @param connector_profile �ɲä⤷���Ϲ������� ConnectorProfile
  #
  # @else
  #
  # @brief Append or update the ConnectorProfile list
  #
  # This operation appends or updates ConnectorProfile of the Port
  # by the given ConnectorProfile.
  # If the connector_id of the given ConnectorProfile does not exist
  # in the Port's ConnectorProfile list, the given ConnectorProfile would be
  # append to the list. If the same id exists, the list would be updated.
  #
  # @param connector_profile the ConnectorProfile to be appended or updated
  #
  # @endif
  # void updateConnectorProfile(const ConnectorProfile& connector_profile);
  def updateConnectorProfile(self, connector_profile):
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                            self.find_conn_id(connector_profile.connector_id))

    if index < 0:
      OpenRTM_aist.CORBA_SeqUtil.push_back(self._profile.connector_profiles,
                                           connector_profile)
    else:
      self._profile.connector_profiles[index] = connector_profile


  ##
  # @if jp
  #
  # @brief ConnectorProfile ��������
  #
  # ���Υ��ڥ졼������ Port �� PortProfile ���ݻ����Ƥ���
  # ConnectorProfileList �Τ���Ϳ����줿 id ����� ConnectorProfile
  # �������롣
  #
  # @param self
  # @param id_ ������� ConnectorProfile �� id
  #
  # @return ����˺���Ǥ������� true��
  #         ���ꤷ�� ConnectorProfile �����Ĥ���ʤ����� false ���֤�
  #
  # @else
  #
  # @brief Delete the ConnectorProfile
  #
  # This operation deletes a ConnectorProfile specified by id from
  # ConnectorProfileList owned by PortProfile of this Port.
  #
  # @param id The id of the ConnectorProfile to be deleted.
  #
  # @endif
  # bool eraseConnectorProfile(const char* id);
  def eraseConnectorProfile(self, id_):
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)

    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.connector_profiles,
                                            self.find_conn_id(id_))

    if index < 0:
      return False

    OpenRTM_aist.CORBA_SeqUtil.erase(self._profile.connector_profiles, index)

    return True


  ##
  # @if jp
  #
  # @brief PortInterfaceProfile �� ���󥿡��ե���������Ͽ����
  #
  # ���Υ��ڥ졼������ Port ������ PortProfile �Ρ�PortInterfaceProfile
  # �˥��󥿡��ե������ξ�����ɲä��롣
  # ���ξ���ϡ�get_port_profile() ����ä������� PortProfile �Τ���
  # PortInterfaceProfile ���ͤ��ѹ�����ΤߤǤ��ꡢ�ºݤ˥��󥿡��ե�������
  # �󶡤������׵ᤷ���ꤹ����ˤϡ����֥��饹�ǡ� publishInterface() ,
  #  subscribeInterface() ���δؿ���Ŭ�ڤ˥����С��饤�ɤ����󥿡��ե�������
  # �󶡡��׵������Ԥ�ʤ���Фʤ�ʤ���
  #
  # ���󥿡��ե�����(�Υ��󥹥���)̾�� Port ��ǰ�դǤʤ���Фʤ�ʤ���
  # Ʊ̾�Υ��󥿡��ե����������Ǥ���Ͽ����Ƥ����硢���δؿ��� false ��
  # �֤���
  #
  # @param self
  # @param instance_name ���󥿡��ե������Υ��󥹥��󥹤�̾��
  # @param type_name ���󥿡��ե������η���̾��
  # @param pol ���󥿡��ե�������°�� (RTC::PROVIDED �⤷���� RTC:REQUIRED)
  #
  # @return ���󥿡��ե�������Ͽ������̡�
  #         Ʊ̾�Υ��󥿡��ե�������������Ͽ����Ƥ���� false ���֤���
  #
  # @else
  #
  # @brief Append an interface to the PortInterfaceProfile
  #
  # This operation appends interface information to the PortInterfaceProfile
  # that is owned by the Port.
  # The given interfaces information only updates PortInterfaceProfile of
  # PortProfile that is obtained through get_port_profile().
  # In order to provide and require interfaces, proper functions (for
  # example publishInterface(), subscribeInterface() and so on) should be
  # overridden in subclasses, and these functions provide concrete interface
  # connection and disconnection functionality.
  #
  # The interface (instance) name have to be unique in the Port.
  # If the given interface name is identical with stored interface name,
  # this function returns false.
  #
  # @param name The instance name of the interface.
  # @param type_name The type name of the interface.
  # @param pol The interface's polarity (RTC::PROVIDED or RTC:REQUIRED)
  #
  # @return false would be returned if the same name is already registered.
  #
  # @endif
  # bool appendInterface(const char* name, const char* type_name,
  #                      PortInterfacePolarity pol);
  def appendInterface(self, instance_name, type_name, pol):
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.interfaces,
                                            self.find_interface(instance_name, pol))

    if index >= 0:
      return False

    # setup PortInterfaceProfile
    prof = RTC.PortInterfaceProfile(instance_name, type_name, pol)
    OpenRTM_aist.CORBA_SeqUtil.push_back(self._profile.interfaces, prof)

    return True


  ##
  # @if jp
  #
  # @brief PortInterfaceProfile ���饤�󥿡��ե�������Ͽ��������
  #
  # ���Υ��ڥ졼������ Port ������ PortProfile �Ρ�PortInterfaceProfile
  # ���饤�󥿡��ե������ξ���������롣
  #
  # @param self
  # @param name ���󥿡��ե������Υ��󥹥��󥹤�̾��
  # @param pol ���󥿡��ե�������°�� (RTC::PROVIDED �⤷���� RTC:REQUIRED)
  #
  # @return ���󥿡��ե��������������̡�
  #         ���󥿡��ե���������Ͽ����Ƥ��ʤ���� false ���֤���
  #
  # @else
  #
  # @brief Delete an interface from the PortInterfaceProfile
  #
  # This operation deletes interface information from the
  # PortInterfaceProfile that is owned by the Port.
  #
  # @param name The instance name of the interface.
  # @param pol The interface's polarity (RTC::PROVIDED or RTC:REQUIRED)
  #
  # @return false would be returned if the given name is not registered.
  #
  # @endif
  # bool deleteInterface(const char* name, PortInterfacePolarity pol);
  def deleteInterface(self, name, pol):
    index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.interfaces,
                                            self.find_interface(name, pol))

    if index < 0:
      return False

    OpenRTM_aist.CORBA_SeqUtil.erase(self._profile.interfaces, index)
    return True


  ##
  # @if jp
  #
  # @brief PortProfile �� properties �� NameValue �ͤ��ɲä���
  #
  # PortProfile �� properties �� NameValue �ͤ��ɲä��롣
  # �ɲä���ǡ����η���ValueType�ǻ��ꤹ�롣
  #
  # @param self
  # @param key properties �� name
  # @param value properties �� value
  #
  # @else
  #
  # @brief Add NameValue data to PortProfile's properties
  #
  # @param key The name of properties
  # @param value The value of properties
  #
  # @endif
  #  template <class ValueType>
  #  void addProperty(const char* key, ValueType value)
  def addProperty(self, key, value):
    OpenRTM_aist.CORBA_SeqUtil.push_back(self._profile.properties,
                                         OpenRTM_aist.NVUtil.newNV(key, value))

  ##
  # @if jp
  #
  # @brief PortProfile �� properties �� NameValue �ͤ����Ǥ��ɲä���
  #
  # PortProfile �� properties �� NameValue �ͤ����Ǥ��ɲä��롣
  #
  # @param key properties �� name
  # @param value properties �� value
  #
  # @else
  #
  # @brief Append NameValue data to PortProfile's properties
  #
  # Append NameValue data to PortProfile's properties.
  #
  # @param key The name of properties
  # @param value The value of properties
  #
  # @endif
  # void appendProperty(const char* key, const char* value)
  def appendProperty(self, key, value):
    OpenRTM_aist.NVUtil.appendStringValue(self._profile.properties, key, value)



  ##
  # @if jp
  #
  # @brief ¸�ߤ��ʤ��ݡ��Ȥ�disconnect���롣
  #
  # @else
  #
  # @brief Disconnect ports that doesn't exist. 
  #
  # @endif
  # void updateConnectors()
  def updateConnectors(self):
    guard = OpenRTM_aist.ScopedLock(self._profile_mutex)
    
    connector_ids = []
    clist = self._profile.connector_profiles

    for cprof in clist:
      if not self.checkPorts(cprof.ports):
        connector_ids.append(cprof.connector_id)
        self._rtcout.RTC_WARN("Dead connection: %s", cprof.connector_id)

    for cid in connector_ids:
      self.disconnect(cid)

    return


  ##
  # @if jp
  #
  # @brief �ݡ��Ȥ�¸�ߤ��ǧ���롣
  #
  # @param ports ��ǧ����ݡ���
  # @return true:¸�ߤ���,false:¸�ߤ��ʤ�
  #
  # @else
  #
  # @brief Existence of ports
  #
  # @param ports Checked ports
  # @return true:existent,false:non existent
  #
  # @endif
  # bool checkPorts(::RTC::PortServiceList& ports)
  def checkPorts(self, ports):
    for port in ports:
      try:
        if port._non_existent():
          self._rtcout.RTC_WARN("Dead Port reference detected.")
          return False
      except:
        self._rtcout.RTC_WARN(OpenRTM_aist.Logger.print_exception())
        return False

    return True


  #inline void onNotifyConnect(const char* portname,
  #                            RTC::ConnectorProfile& profile)
  def onNotifyConnect(self, portname, profile):
    if self._portconnListeners != None:
      type = OpenRTM_aist.PortConnectListenerType.ON_NOTIFY_CONNECT
      self._portconnListeners.portconnect_[type].notify(portname, profile)
    return


  #inline void onNotifyDisconnect(const char* portname,
  #                               RTC::ConnectorProfile& profile)
  def onNotifyDisconnect(self, portname, profile):
    if self._portconnListeners != None:
      type = OpenRTM_aist.PortConnectListenerType.ON_NOTIFY_DISCONNECT
      self._portconnListeners.portconnect_[type].notify(portname, profile)
    return


  #inline void onUnsubscribeInterfaces(const char* portname,
  #                                    RTC::ConnectorProfile& profile)
  def onUnsubscribeInterfaces(self, portname, profile):
    if self._portconnListeners != None:
      type = OpenRTM_aist.PortConnectListenerType.ON_UNSUBSCRIBE_INTERFACES
      self._portconnListeners.portconnect_[type].notify(portname, profile)
    return


  #inline void onPublishInterfaces(const char* portname,
  #                                RTC::ConnectorProfile& profile,
  #                                ReturnCode_t ret)
  def onPublishInterfaces(self, portname, profile, ret):
    if self._portconnListeners != None:
      type = OpenRTM_aist.PortConnectRetListenerType.ON_PUBLISH_INTERFACES
      self._portconnListeners.portconnret_[type].notify(portname, profile, ret)
    return


  #inline void onConnectNextport(const char* portname,
  #                              RTC::ConnectorProfile& profile,
  #                              ReturnCode_t ret)
  def onConnectNextport(self, portname, profile, ret):
    if self._portconnListeners != None:
      type = OpenRTM_aist.PortConnectRetListenerType.ON_CONNECT_NEXTPORT
      self._portconnListeners.portconnret_[type].notify(portname, profile, ret)
    return


  #inline void onSubscribeInterfaces(const char* portname,
  #                                  RTC::ConnectorProfile& profile,
  #                                  ReturnCode_t ret)
  def onSubscribeInterfaces(self, portname, profile, ret):
    if self._portconnListeners != None:
      type = OpenRTM_aist.PortConnectRetListenerType.ON_SUBSCRIBE_INTERFACES
      self._portconnListeners.portconnret_[type].notify(portname, profile, ret)
    return


  #inline void onConnected(const char* portname,
  #                        RTC::ConnectorProfile& profile,
  #                        ReturnCode_t ret)
  def onConnected(self, portname, profile, ret):
    if self._portconnListeners != None:
      type = OpenRTM_aist.PortConnectRetListenerType.ON_CONNECTED
      self._portconnListeners.portconnret_[type].notify(portname, profile, ret)
    return


  #inline void onDisconnectNextport(const char* portname,
  #                                 RTC::ConnectorProfile& profile,
  #                                 ReturnCode_t ret)
  def onDisconnectNextport(self, portname, profile, ret):
    if self._portconnListeners != None:
      type = OpenRTM_aist.PortConnectRetListenerType.ON_DISCONNECT_NEXT
      self._portconnListeners.portconnret_[type].notify(portname, profile, ret)
    return


  #inline void onDisconnected(const char* portname,
  #                           RTC::ConnectorProfile& profile,
  #                           ReturnCode_t ret)
  def onDisconnected(self, portname, profile, ret):
    if self._portconnListeners != None:
      type = OpenRTM_aist.PortConnectRetListenerType.ON_DISCONNECTED
      self._portconnListeners.portconnret_[type].notify(portname, profile, ret)
    return



  #============================================================
  # Functor
  #============================================================

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

    def __call__(self, prof):
      return str(self._name) == str(prof.instance_name)
    

  ##
  # @if jp
  # @class find_conn_id
  # @brief id ����� ConnectorProfile ��õ�� Functor
  # @else
  # @brief A functor to find a ConnectorProfile named id
  # @endif
  class find_conn_id:
    def __init__(self, id_):
      """
       \param id_(string)
      """
      self._id = id_

    def __call__(self, cprof):
      """
       \param cprof(RTC.ConnectorProfile)
      """
      return str(self._id) == str(cprof.connector_id)

  ##
  # @if jp
  # @class find_port_ref
  # @brief ���󥹥ȥ饯������ port_ref ��Ʊ�����֥������Ȼ��Ȥ�õ�� Functor
  # @else
  # @brief A functor to find the object reference that is identical port_ref
  # @endif
  class find_port_ref:
    def __init__(self, port_ref):
      """
       \param port_ref(RTC.PortService)
      """
      self._port_ref = port_ref

    def __call__(self, port_ref):
      """
       \param port_ref(RTC.PortService)
      """
      return self._port_ref._is_equivalent(port_ref)

  ##
  # @if jp
  # @class connect_func
  # @brief Port ����³��Ԥ� Functor
  # @else
  # @brief A functor to connect Ports
  # @endif
  class connect_func:
    def __init__(self, p, prof):
      """
       \param p(RTC.PortService)
       \param prof(RTC.ConnectorProfile)
      """
      self._port_ref = p
      self._connector_profile = prof
      self.return_code = RTC.RTC_OK

    def __call__(self, p):
      """
       \param p(RTC.PortService)
      """
      if not self._port_ref._is_equivalent(p):
        retval = p.notify_connect(self._connector_profile)
        if retval != RTC.RTC_OK:
          self.return_code = retval

  ##
  # @if jp
  # @class disconnect_func
  # @brief Port ����³�����Ԥ� Functor
  # @else
  # @brief A functor to disconnect Ports
  # @endif
  class disconnect_func:
    def __init__(self, p, prof):
      """
       \param p(RTC.PortService)
       \param prof(RTC.ConnectorProfile)
      """
      self._port_ref = p
      self._connector_profile = prof
      self.return_code = RTC.RTC_OK
      
    def __call__(self, p):
      """
       \param p(RTC.PortService)
      """
      if not self._port_ref._is_equivalent(p):
        retval = p.disconnect(self._connector_profile.connector_id)
        if retval != RTC.RTC_OK:
          self.return_code = retval

  ##
  # @if jp
  # @class disconnect_all_func
  # @brief Port ������³�����Ԥ� Functor
  # @else
  # @brief A functor to disconnect all Ports
  # @endif
  class disconnect_all_func:
    def __init__(self, p):
      """
       \param p(OpenRTM_aist.PortBase)
      """
      self.return_code = RTC.RTC_OK
      self._port = p

    def __call__(self, p):
      """
       \param p(RTC.ConnectorProfile)
      """
      retval = self._port.disconnect(p.connector_id)
      if retval != RTC.RTC_OK:
        self.return_code = retval

  ##
  # @if jp
  # @class find_interface
  # @brief name �� polarity ���� interface ��õ�� Functor
  # @else
  # @brief A functor to find interface from name and polarity
  # @endif
  class find_interface:
    def __init__(self, name, pol):
      """
       \param name(string)
       \param pol(RTC.PortInterfacePolarity)
      """
      self._name = name
      self._pol = pol

    def __call__(self, prof):
      """
       \param prof(RTC.PortInterfaceProfile)
      """
      name = prof.instance_name
      return (str(self._name) == str(name)) and (self._pol == prof.polarity)
