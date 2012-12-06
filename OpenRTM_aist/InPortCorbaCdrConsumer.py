#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  InPortCorbaCdrConsumer.py
# @brief InPortCorbaCdrConsumer class
# @date  $Date: 2007-12-31 03:08:03 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

import sys
from omniORB import any
from omniORB import CORBA
import OpenRTM_aist
import OpenRTM

##
# @if jp
#
# @class InPortCorbaCdrConsumer
#
# @brief InPortCorbaCdrConsumer ���饹
#
# �̿����ʤ� CORBA �����Ѥ������ϥݡ��ȥ��󥷥塼�ޤμ������饹��
#
# @param DataType �ܥݡ��Ȥˤư����ǡ�����
#
# @since 1.0
#
# @else
# @class InPortCorbaCdrConsumer
#
# @brief InPortCorbaCdrConsumer class
#
# This is an implementation class of the input port Consumer 
# that uses CORBA for means of communication.
#
# @param DataType Data type for this port
#
# @since 0.4.0
#
# @endif
#
class InPortCorbaCdrConsumer(OpenRTM_aist.InPortConsumer,OpenRTM_aist.CorbaConsumer):
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param buffer �������󥷥塼�ޤ˳�����Ƥ�Хåե����֥�������
  #
  # @else
  # @brief Constructor
  #
  # Constructor
  #
  # @param buffer The buffer object that is attached to this Consumer
  #
  # @endif
  #
  def __init__(self):
    OpenRTM_aist.CorbaConsumer.__init__(self)
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("InPortCorbaCdrConsumer")
    self._properties = None
    return

  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
  #
  # @else
  # @brief Destructor
  #
  # Destructor
  #
  # @endif
  #
  def __del__(self, CorbaConsumer=OpenRTM_aist.CorbaConsumer):
    self._rtcout.RTC_PARANOID("~InPortCorbaCdrConsumer()")
    CorbaConsumer.__del__(self)
    return

  ##
  # @if jp
  # @brief ��������
  #
  # InPortConsumer�γƼ������Ԥ�
  #
  # @else
  # @brief Initializing configuration
  #
  # This operation would be called to configure this consumer
  # in initialization.
  #
  # @endif
  #
  # virtual void init(coil::Properties& prop);
  def init(self, prop):
    self._rtcout.RTC_TRACE("init()")
    self._properties = prop
    return

  ##
  # @if jp
  # @brief ��³��ؤΥǡ�������
  #
  # ��³��Υݡ��Ȥإǡ������������뤿��ν�貾�۴ؿ���
  # 
  # ���δؿ��ϡ��ʲ��Υ꥿���󥳡��ɤ��֤���
  #
  # - PORT_OK:       ���ｪλ��
  # - PORT_ERROR:    �ǡ��������β����ǲ��餫�Υ��顼��ȯ��������
  # - SEND_FULL:     �ǡ��������������������¦�Хåե����ե���ä���
  # - SEND_TIMEOUT:  �ǡ��������������������¦�Хåե��������ॢ���Ȥ�����
  # - UNKNOWN_ERROR: ���������Υ��顼
  #
  # @param data ��������ǡ���
  # @return �꥿���󥳡���
  #
  # @else
  # @brief Send data to the destination port
  #
  # Pure virtual function to send data to the destination port.
  #
  # This function might the following return codes
  #
  # - PORT_OK:       Normal return
  # - PORT_ERROR:    Error occurred in data transfer process
  # - SEND_FULL:     Buffer full although OutPort tried to send data
  # - SEND_TIMEOUT:  Timeout although OutPort tried to send data
  # - UNKNOWN_ERROR: Unknown error
  #
  # @endif
  #
  # virtual ReturnCode put(const cdrMemoryStream& data);
  def put(self, data):
    self._rtcout.RTC_PARANOID("put()")

    try:
      ref_ = self.getObject()
      if ref_:
        inportcdr = ref_._narrow(OpenRTM.InPortCdr)
        return self.convertReturnCode(inportcdr.put(data))
      return self.CONNECTION_LOST
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
      return self.CONNECTION_LOST
        
    return self.UNKNOWN_ERROR

  ##
  # @if jp
  # @brief InterfaceProfile������������
  #
  # InterfaceProfile�����������롣
  # �����ǻ��ꤹ��ץ�ѥƥ�������� NameValue ���֥������Ȥ�
  # dataport.interface_type �ͤ�Ĵ�١������ݡ��Ȥ����ꤵ��Ƥ���
  # ���󥿡��ե����������פȰ��פ�����Τ߾����������롣
  #
  # @param properties InterfaceProfile�����������ץ�ѥƥ�
  #
  # @else
  # @brief Publish InterfaceProfile information
  #
  # Publish interfaceProfile information.
  # Check the dataport.interface_type value of the NameValue object 
  # specified by an argument in property information and get information
  # only when the interface type of the specified port is matched.
  #
  # @param properties Properties to get InterfaceProfile information
  #
  # @endif
  #
  # virtual void publishInterfaceProfile(SDOPackage::NVList& properties);
  def publishInterfaceProfile(self, properties):
    return

  ##
  # @if jp
  # @brief �ǡ����������Τؤ���Ͽ
  #
  # ���ꤵ�줿�ץ�ѥƥ��˴�Ť��ơ��ǡ����������Τμ���������Ͽ���롣
  #
  # @param properties ��Ͽ����
  #
  # @return ��Ͽ�������(��Ͽ����:true����Ͽ����:false)
  #
  # @else
  # @brief Subscribe to the data sending notification
  #
  # Subscribe to the data sending notification based on specified 
  # property information.
  #
  # @param properties Information for subscription
  #
  # @return Subscription result (Successful:true, Failed:false)
  #
  # @endif
  #
  # virtual bool subscribeInterface(const SDOPackage::NVList& properties);
  def subscribeInterface(self, properties):
    self._rtcout.RTC_TRACE("subscribeInterface()")
    # self._rtcout.RTC_DEBUG_STR(OpenRTM_aist.NVUtil.toString(properties))
    
    # getting InPort's ref from IOR string
    if self.subscribeFromIor(properties):
      return True
    
    # getting InPort's ref from Object reference
    if self.subscribeFromRef(properties):
      return True
    
    return False
    
  ##
  # @if jp
  # @brief �ǡ����������Τ������Ͽ���
  #
  # �ǡ����������Τμ�����꤫����Ͽ�������롣
  #
  # @param properties ��Ͽ�������
  #
  # @else
  # @brief Unsubscribe the data send notification
  #
  # Unsubscribe the data send notification.
  #
  # @param properties Information for unsubscription
  #
  # @endif
  #
  # virtual void unsubscribeInterface(const SDOPackage::NVList& properties);
  def unsubscribeInterface(self, properties):
    self._rtcout.RTC_TRACE("unsubscribeInterface()")
    # self._rtcout.RTC_DEBUG_STR(OpenRTM_aist.NVUtil.toString(properties))
    
    if self.unsubscribeFromIor(properties):
      return
        
    self.unsubscribeFromRef(properties)
    return

  ##
  # @if jp
  # @brief IORʸ���󤫤饪�֥������Ȼ��Ȥ��������
  #
  # @return true: �������, false: ��������
  #
  # @else
  # @brief Getting object reference fromn IOR string
  #
  # @return true: succeeded, false: failed
  #
  # @endif
  #
  # bool subscribeFromIor(const SDOPackage::NVList& properties);
  def subscribeFromIor(self, properties):
    self._rtcout.RTC_TRACE("subscribeFromIor()")
    
    index = OpenRTM_aist.NVUtil.find_index(properties,
                                           "dataport.corba_cdr.inport_ior")
    if index < 0:
      self._rtcout.RTC_ERROR("inport_ior not found")
      return False
    
    ior = ""
    try:
      ior = any.from_any(properties[index].value, keep_structs=True)
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if not ior:
      self._rtcout.RTC_ERROR("inport_ior has no string")
      return False
    
    orb = OpenRTM_aist.Manager.instance().getORB()
    obj = orb.string_to_object(ior)
    
    if CORBA.is_nil(obj):
      self._rtcout.RTC_ERROR("invalid IOR string has been passed")
      return False
    
    if not self.setObject(obj):
      self._rtcout.RTC_WARN("Setting object to consumer failed.")
      return False

    return True

  ##
  # @if jp
  # @brief Any����ľ�ܥ��֥������Ȼ��Ȥ��������
  #
  # @return true: �������, false: ��������
  #
  # @else
  # @brief Getting object reference fromn Any directry
  #
  # @return true: succeeded, false: failed
  #
  # @endif
  #
  # bool subscribeFromRef(const SDOPackage::NVList& properties);
  def subscribeFromRef(self, properties):
    self._rtcout.RTC_TRACE("subscribeFromRef()")
    index = OpenRTM_aist.NVUtil.find_index(properties,
                                           "dataport.corba_cdr.inport_ref")
    if index < 0:
      self._rtcout.RTC_ERROR("inport_ref not found")
      return False
    
    obj = None
    try:
      obj = any.from_any(properties[index].value, keep_structs=True)
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
    
    if not obj:
      self._rtcout.RTC_ERROR("prop[inport_ref] is not objref")
      return False
    
    if CORBA.is_nil(obj):
      self._rtcout.RTC_ERROR("prop[inport_ref] is not objref")
      return False
    
    if not self.setObject(obj):
      self._rtcout.RTC_ERROR("Setting object to consumer failed.")
      return False

    return True

  ##
  # @if jp
  # @brief ��³���(IOR��)
  #
  # @return true: �������, false: ��������
  #
  # @else
  # @brief ubsubscribing (IOR version)
  #
  # @return true: succeeded, false: failed
  #
  # @endif
  #
  # bool unsubscribeFromIor(const SDOPackage::NVList& properties);
  def unsubscribeFromIor(self, properties):
    self._rtcout.RTC_TRACE("unsubscribeFromIor()")
    index = OpenRTM_aist.NVUtil.find_index(properties,
                                           "dataport.corba_cdr.inport_ior")
    if index < 0:
      self._rtcout.RTC_ERROR("inport_ior not found")
      return False
    
    ior = ""
    try:
      ior = any.from_any(properties[index].value, keep_structs=True)
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())

    if not ior:
      self._rtcout.RTC_ERROR("prop[inport_ior] is not string")
      return False
    
    orb = OpenRTM_aist.Manager.instance().getORB()
    var = orb.string_to_object(ior)
    if not self._ptr()._is_equivalent(var):
      self._rtcout.RTC_ERROR("connector property inconsistency")
      return False
    
    self.releaseObject()
    return True

  ##
  # @if jp
  # @brief ��³���(Object reference��)
  #
  # @return true: �������, false: ��������
  #
  # @else
  # @brief ubsubscribing (Object reference version)
  #
  # @return true: succeeded, false: failed
  #
  # @endif
  #
  # bool unsubscribeFromRef(const SDOPackage::NVList& properties);
  def unsubscribeFromRef(self, properties):
    self._rtcout.RTC_TRACE("unsubscribeFromRef()")
    index = OpenRTM_aist.NVUtil.find_index(properties,
                                           "dataport.corba_cdr.inport_ref")

    if index < 0:
      return False
    
    obj = None
    try:
      obj = any.from_any(properties[index].value, keep_structs=True)
    except:
      self._rtcout.RTC_ERROR(OpenRTM_aist.Logger.print_exception())
    
    if not obj:
      return False

    if not self._ptr()._is_equivalent(obj):
      return False
    
    self.releaseObject()
    return True

  ##
  # @if jp
  # @brief �꥿���󥳡����Ѵ�
  # @else
  # @brief Return codes conversion
  # @endif
  #
    # ReturnCode convertReturnCode(OpenRTM::PortStatus ret)
  def convertReturnCode(self, ret):
    if ret == OpenRTM.PORT_OK:
      return self.PORT_OK

    elif ret == OpenRTM.PORT_ERROR:
      return self.PORT_ERROR

    elif ret == OpenRTM.BUFFER_FULL:
      return self.SEND_FULL

    elif ret == OpenRTM.BUFFER_TIMEOUT:
      return self.SEND_TIMEOUT

    elif ret == OpenRTM.UNKNOWN_ERROR:
      return self.UNKNOWN_ERROR

    else:
      return self.UNKNOWN_ERROR


def InPortCorbaCdrConsumerInit():
  factory = OpenRTM_aist.InPortConsumerFactory.instance()
  factory.addFactory("corba_cdr",
                     OpenRTM_aist.InPortCorbaCdrConsumer,
                     OpenRTM_aist.Delete)
