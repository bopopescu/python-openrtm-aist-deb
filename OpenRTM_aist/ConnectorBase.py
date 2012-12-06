#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ConnectorBase.py
# @brief Connector base class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2009
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import OpenRTM_aist


##
# @if jp
# @class ConnectorInfo ���饹
# @brief ConnectorInfo ���饹
#
# @class ConnectorInfo class
# @brief ConnectorInfo class
#
# @endif
#
class ConnectorInfo:
  """
  """
  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  # 
  # ���󥹥ȥ饯��
  #
  # @param name_ ��³̾��
  # @param id_ ��³ID
  # @param ports_ ��³�ݡ���IOR
  # @param properties_ �ץ�ѥƥ�
  # 
  # @else
  #
  # @brief Constructor
  # 
  # Constructor
  #
  # @param name_ connection name
  # @param id_ connection ID
  # @param ports_ connection Ports
  # @param properties_ connection properties
  #
  # @endif
  # ConnectorInfo(const char* name_, const char* id_,
  #               coil::vstring ports_, coil::Properties properties_)
  def __init__(self, name_, id_, ports_, properties_):
    self.name       = name_        # str
    self.id         = id_          # str
    self.ports      = ports_       # [str,...]
    self.properties = properties_  # OpenRTM_aist.Properties

#!
# @if jp
# @class ConnectorBase
# @brief Connector ���쥯�饹
#
# InPort/OutPort, Push/Pull �Ƽ� Connector �����������뤿���
# ���쥯�饹��
#
# @since 1.0.0
#
# @else
# @class ConnectorBase
# @brief Connector Base class
#
# The base class to derive subclasses for InPort/OutPort,
# Push/Pull Connectors
#
# @since 1.0.0
#
# @endif
class ConnectorBase(OpenRTM_aist.DataPortStatus):
  """
  """

  ##
  # @if jp
  # @class Profile
  # @brief Connector profile �����빽¤��
  #
  # ConnectorBase ����Ӥ����������饹�ǰ��� ConnectorProfile ��¤�Ρ�
  #
  # @since 1.0.0
  #
  # @else
  # @class Profile
  # @brief local representation of Connector profile
  #
  # ConnectorProfile struct for ConnectorBase and its subclasses.
  #
  # @since 1.0.0
  #
  # @endif

  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  def __del__(self):
    pass


  ##
  # @if jp
  # @brief Profile ����
  #
  # Connector Profile ���������
  #
  # @else
  # @brief Getting Profile
  #
  # This operation returns Connector Profile
  #
  # @endif
  # virtual const ConnectorInfo& profile() = 0;
  def profile(self):
    pass

  ##
  # @if jp
  # @brief Connector ID ����
  #
  # Connector ID ���������
  #
  # @else
  # @brief Getting Connector ID
  #
  # This operation returns Connector ID
  #
  # @endif
  # virtual const char* id() = 0;
  def id(self):
    pass


  ##
  # @if jp
  # @brief Connector ̾����
  #
  # Connector ̾���������
  #
  # @else
  # @brief Getting Connector name
  #
  # This operation returns Connector name
  #
  # @endif
  # virtual const char* name() = 0;
  def name(self):
    pass


  ##
  # @if jp
  # @brief ��³����ؿ�
  #
  # Connector ���ݻ����Ƥ�����³��������
  #
  # @else
  # @brief Disconnect connection
  #
  # This operation disconnect this connection
  #
  # @endif
  # virtual ReturnCode disconnect() = 0;
  def disconnect(self):
    pass


  ##
  # @if jp
  # @brief Buffer ���������
  #
  # Connector ���ݻ����Ƥ��� Buffer ���֤�
  #
  # @else
  # @brief Getting Buffer
  #
  # This operation returns this connector's buffer
  #
  # @endif
  # virtual CdrBufferBase* getBuffer() = 0;
  def getBuffer(self):
    pass


  ##
  # @if jp
  # @brief �����ƥ��ֲ�
  #
  # ���Υ��ͥ����򥢥��ƥ��ֲ�����
  #
  # @else
  #
  # @brief Connector activation
  #
  # This operation activates this connector
  #
  # @endif
  # virtual void activate() = 0;
  def activate(self):
    pass

  
  ##
  # @if jp
  # @brief �󥢥��ƥ��ֲ�
  #
  # ���Υ��ͥ������󥢥��ƥ��ֲ�����
  #
  # @else
  #
  # @brief Connector deactivation
  #
  # This operation deactivates this connector
  #
  # @endif
  # virtual void deactivate() = 0;
  def deactivate(self):
    pass
