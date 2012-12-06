#!/usr/bin/env python 
# -*- coding: euc-jp -*-

##
# @file PublisherBase.py
# @brief Publisher base class
# @date $Date: 2007/09/05$
# @author Noriaki Ando <n-ando@aist.go.jp>
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
# @class PublisherBase
#
# @brief Publisher ���쥯�饹
# 
# �ǡ������Х����ߥ󥰤�����������Ф��ư����Publisher* �δ��쥯�饹��
# �Ƽ� Publisher �Ϥ��Υ��饹��Ѿ����ƾܺ٤�������롣
#
# @since 0.4.0
#
# @else
#
# @class PublisherBase
#
# @brief Base class of Publisher.
#
# A base class of Publisher*.
# Variation of Publisher* which implements details of Publisher
# inherits this PublisherBase class.
#
# @endif
class PublisherBase(OpenRTM_aist.DataPortStatus):
  """
  """


  ##
  # @if jp
  # @brief ��������
  #
  # InPortConsumer�γƼ������Ԥ����������饹�Ǥϡ�Ϳ����줿
  # Properties����ɬ�פʾ����������ƳƼ������Ԥ������� init() ��
  # ���ϡ�OutPortProvider����ľ�太��ӡ���³���ˤ��줾��ƤФ���
  # ǽ�������롣�������äơ����δؿ���ʣ����ƤФ�뤳�Ȥ����ꤷ�Ƶ�
  # �Ҥ����٤��Ǥ��롣
  # 
  # @param prop �������
  #
  # @else
  #
  # @brief Initializing configuration
  #
  # This operation would be called to configure in initialization.
  # In the concrete class, configuration should be performed
  # getting appropriate information from the given Properties data.
  # This function might be called right after instantiation and
  # connection sequence respectivly.  Therefore, this function
  # should be implemented assuming multiple call.
  #
  # @param prop Configuration information
  #
  # @endif
  ## virtual ReturnCode init(coil::Properties& prop) = 0;
  def init(self, prop):
    pass

  ## virtual ReturnCode setConsumer(InPortConsumer* consumer) = 0;
  def setConsumer(self, consumer):
    pass

  ## virtual ReturnCode setBuffer(BufferBase<cdrMemoryStream>* buffer) = 0;
  def setBuffer(self, buffer):
    pass

  # virtual ReturnCode setListener(ConnectorInfo& info,
  #                                ConnectorListeners* listeners) = 0;
  def setListener(self, info, listeners):
    pass

  # virtual ReturnCode write(const cdrMemoryStream& data,
  #                          unsigned long sec,
  #                          unsigned long usec) = 0;
  def write(self, data, sec, usec):
    pass

  ## virtual bool isActive() = 0;
  def isActive(self):
    pass

  ## virtual ReturnCode activate() = 0;
  def activate(self):
    pass

  ## virtual ReturnCode deactivate() = 0;
  def deactivate(self):
    pass


    
  ##
  # @if jp
  #
  # @brief Publisher ���˴����롣
  #
  # ���� Publisher ���˴����롣
  # ���� Publisher �����פˤʤä����� PublisherFactory ����ƤӽФ���롣
  #
  # @else
  #
  # @brief Release the Publisher
  #
  # Release this Publisher.
  # When Publisher becomes unnecessary, this is invoked from
  # PublisherFactory. 
  #
  # @endif
  # virtual void release(){}
  def release(self):
    pass


publisherfactory = None

class PublisherFactory(OpenRTM_aist.Factory,PublisherBase):
  def __init__(self):
    OpenRTM_aist.Factory.__init__(self)
    pass


  def __del__(self):
    pass


  def instance():
    global publisherfactory

    if publisherfactory is None:
      publisherfactory = PublisherFactory()

    return publisherfactory

  instance = staticmethod(instance)
