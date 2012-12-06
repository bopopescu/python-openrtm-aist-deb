#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file SdoService.py
# @brief SDO Service administration class
# @date $Date: 2007/09/12 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
# 

import SDOPackage, SDOPackage__POA

##
# @if jp
#
# @class SDOServiceProfile
# @brief SDO Service Profile���饹
#
# SDO Service Profile �� SDO Service �ξ�����ݻ����뤿��Υ��饹�Ǥ��롣
#
# @since 0.4.0
#
# @else
#
# @class SDOServiceProfile
# @brief SDO Service Profile class
#
# @since 0.4.0
#
# @endif
class SDOServiceProfile:
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
  # @param id_ Service ��ID(�ǥե������:None)
  # @param type_ Service �η�(�ǥե������:None)
  #
  # @else
  #
  # @endif
  def __init__(self, id_=None, type_=None):
    if id_ is None:
      self.id = ""
    else:
      self.id = id_

    if type_ is None:
      self.type = ""
    else:
      self.type = type_
      
    self.interfaceType = ""
    self.idlDefinition = ""
    self.properties = []
    self.serviceRef = None


  ##
  # @if jp
  #
  # @brief Service Profile���������
  # 
  # Service Profile���������
  #
  # @param self
  # 
  # @return Service Profile
  # 
  # @else
  #
  # @endif
  def getProfile(self):
    return self


  ##
  # @if jp
  # @brief ServiceProfile.id �򥻥åȤ���
  # 
  # SDO Service ��ID�򥻥åȤ���
  # 
  # @param self
  # @param id_ Service ��ID
  # 
  # @else
  # @brief Setting ServiceProfile.id
  # @endif
  def setName(self, id_):
    self.id = id_


  ##
  # @if jp
  # @brief ServiceProfile.id �����
  # 
  # SDO Service ��ID���������
  # 
  # @param self
  # 
  # @return Service ��ID
  # 
  # @else
  # @brief Getting ServiceProfile.id
  # @endif
  def getName(self):
    return self.id


  ##
  # @if jp
  # @brief SDO ServiceProfile.interfaceType �򥻥åȤ���
  # 
  # SDO Service ��interfaceType�򥻥åȤ���
  # 
  # @param self
  # @param interfaceType Service ��interfaceType
  # 
  # @else
  # @brief Setting SDOServiceProfile.interfaceType
  # @endif
  def setInterfaceType(self, interfaceType):
    self.interfaceType = interfaceType
    


  # @if jp
  # @brief SDO ServiceProfile.interfaceType ���������
  # 
  # SDO Service ��interfaceType���������
  # 
  # @param self
  # 
  # @return Service ��interfaceType
  # 
  # @else
  # @brief Getting SDOServiceProfile.interfaceType
  # @endif
  def getInterfaceType(self):
    return self.interfaceType


  ##
  # @if jp
  # @brief SDO ServiceProfile.idlDefinition �򥻥åȤ���
  # 
  # SDO Service ��idlDefinition�򥻥åȤ���
  # 
  # @param self
  # @param idlDefinition Service ��idlDefinition
  # 
  # @else
  # @brief Setting SDOServiceProfile.idlDefnition
  # @endif
  def setIdlDefinition(self, idlDefinition):
    self.idlDefinition = idlDefinition


  ##
  # @if jp
  # @brief SDO ServiceProfile.idlDefinition ���������
  # 
  # SDO Service ��idlDefinition���������
  # 
  # @param self
  # 
  # @return Service ��idlDefinition
  # 
  # @else
  # @brief Getting SDO ServiceProfile.idlDefnition
  # @endif
  def getIdlDefinition(self):
    return self.idlDefinition


  ##
  # @if jp
  # @brief SDO ServiceProfile.properties �򥻥åȤ���
  # 
  # SDO Service ��properties�򥻥åȤ���
  # 
  # @param self
  # @param properties Service ��properties
  # 
  # @else
  # @brief Setting SDO ServiceProfile.properties
  # @endif
  def setProperties(self, properties):
    self.properties = properties


  ##
  # @if jp
  # @brief SDO ServiceProfile.properties ���������
  # 
  # SDO Service ��properties���������
  # 
  # @param self
  # 
  # @return Service ��properties
  # 
  # @else
  # @brief Getting SDO ServiceProfile.properties
  # @endif
  def getProperties(self):
    return self.properties


  # bool addProperty(char name, CORBA::Any data);


  ##
  # @if jp
  # @brief SDO ServiceProfile.serviceRef �򥻥åȤ���
  # 
  # SDO Service ��serviceRef�򥻥åȤ���
  # 
  # @param self
  # @param serviceRef Service�ؤλ���
  # 
  # @else
  # @brief Setting SDO ServiceProfile.serviceRef
  # @endif
  def setServiceRef(self, serviceRef):
    self.serviceRef = serviceRef


  ##
  # @if jp
  # @brief SDO ServiceProfile.serviceRef ���������
  # 
  # SDO Service �ؤλ��Ȥ��������
  # 
  # @param self
  # 
  # @return Service�ؤλ���
  # 
  # @else
  # @brief Getting SDO ServiceProfile.serviceRef
  # @endif
  def getServiceRef(self):
    return self.serviceRef
  
