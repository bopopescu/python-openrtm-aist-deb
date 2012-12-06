#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ConfigurationListener.py
# @brief Configuration related event listener classes
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2011
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import OpenRTM_aist

##
# @if jp
# @brief ConfigurationParamListener �Υ�����
#
# - ON_UPDATE_CONFIG_PARAM,
#
# @else
# @brief The types of ConnectorDataListener
# 
# - ON_UPDATE_CONFIG_PARAM,
#
# @endif
#
class ConfigurationParamListenerType:
  """
  """

  def __init__(self):
    pass

  ON_UPDATE_CONFIG_PARAM      = 0
  CONFIG_PARAM_LISTENER_NUM   = 1



##
# @if jp
# @class ConfigurationParamListener ���饹
# @brief ConfigurationParamListener ���饹
#
# Configuration �ѥ�᡼�����ѹ��˴ؤ���ꥹ�ʥ��饹��
# �ʲ��Υ��٥�Ȥ��Ф��ƥ�����Хå�����롣
#
# - ON_UPDATE_CONFIG_PARAM
#
# @else
# @class ConfigurationParamListener class
# @brief ConfigurationParamListener class
#
# This class is abstract base class for listener classes that
# provides callbacks for various events for Configuration parameter.
# The listener will be called on the following event.
#
# - ON_UPDATE_CONFIG_PARAM
#
# @endif
class ConfigurationParamListener:
  """
  """

  def __init__(self):
    pass

  ##
  # @if jp
  #
  # @brief ConfigurationParamListenerType ��ʸ������Ѵ�
  #
  # ConfigurationParamListenerType ��ʸ������Ѵ�����
  #
  # @param type �Ѵ��о� ConfigurationParamListenerType
  #
  # @return ʸ�����Ѵ����
  #
  # @else
  #
  # @brief Convert ConfigurationParamListenerType into the string.
  #
  # Convert ConfigurationParamListenerType into the string.
  #
  # @param type The target ConfigurationParamListenerType for transformation
  #
  # @return Trnasformation result of string representation
  #
  # @endif
  # static const char* toString(ConfigurationParamListenerType type)
  def toString(type):
    typeString = ["ON_UPDATE_CONFIG_PARAM",
                  "CONFIG_PARAM_LISTENER_NUM"]
                      
    if type < ConfigurationParamListenerType.CONFIG_PARAM_LISTENER_NUM:
      return typeString[type]
        
    return "";

  toString = staticmethod(toString)


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
  #
  # @brief ���ۥ�����Хå��ؿ�
  #
  # ConfigurationParamListener �Υ�����Хå��ؿ�
  #
  # @else
  #
  # @brief Virtual Callback function
  #
  # This is a the Callback function for ConfigurationParamListener.
  #
  # @endif
  # virtual void operator()(const char* config_set_name,
  #                         const char* config_param_name) = 0;
  def __call__(self, config_set_name, config_param_name):
    pass



#============================================================
##
# @if jp
# @brief ConfigurationSetListener �Υ�����
#
# - ON_SET_CONFIG_SET: ConfigurationSet ñ�̤��ͤ����åȤ��줿
# - ON_ADD_CONFIG_SET: ConfigurationSet ���ɲä��줿
#
# @else
# @brief The types of ConfigurationSetListener
# 
# - ON_SET_CONFIG_SET: Value list has been set as a configuration set 
# - ON_ADD_CONFIG_SET: A new configuration set has been added
#
# @endif
class ConfigurationSetListenerType:
  """
  """

  def __init__(self):
    pass

  ON_SET_CONFIG_SET       = 0
  ON_ADD_CONFIG_SET       = 1
  CONFIG_SET_LISTENER_NUM = 2



##
# @if jp
# @class ConfigurationSetListener ���饹
# @brief ConfigurationSetListener ���饹
#
# Configuration���åȤ��ѹ����줿���ɲä��줿���˸ƤӽФ����ꥹ�ʥ��饹��
# �ʲ���Configuration���åȤ˴�Ϣ���륤�٥�Ȥ��Ф���ꥹ�ʡ�
#
# - ON_SET_CONFIG_SET: ConfigurationSet ñ�̤��ͤ����åȤ��줿
# - ON_ADD_CONFIG_SET: ConfigurationSet ���ɲä��줿
#
# @else
# @class ConfigurationSetListener class
# @brief ConfigurationSetListener class
#
# This class is abstract base class for listener classes that
# provides callbacks for configuration set's related events.
#
# - ON_SET_CONFIG_SET: Value list has been set as a configuration set 
# - ON_ADD_CONFIG_SET: A new configuration set has been added
#
# @endif
class ConfigurationSetListener:
  """
  """

  def __init__(self):
    pass


  ##
  # @if jp
  #
  # @brief ConfigurationSetListenerType ��ʸ������Ѵ�
  #
  # ConfigurationSetListenerType ��ʸ������Ѵ�����
  #
  # @param type �Ѵ��о� ConfigurationSetListenerType
  #
  # @return ʸ�����Ѵ����
  #
  # @else
  #
  # @brief Convert ConfigurationSetListenerType into the string.
  #
  # Convert ConfigurationSetListenerType into the string.
  #
  # @param type The target ConfigurationSetListenerType for
  #             transformation
  #
  # @return Trnasformation result of string representation
  #
  # @endif
  # static const char* toString(ConfigurationSetListenerType type)
  def toString(type):
    typeString = ["ON_SET_CONFIG_SET",
                  "ON_ADD_CONFIG_SET",
                  "CONFIG_SET_LISTENER_NUM"]
    if type < ConfigurationSetListenerType.CONFIG_SET_LISTENER_NUM:
      return typeString[type]

    return "";

  toString = staticmethod(toString)


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
  #
  # @brief ���ۥ�����Хå��ؿ�
  #
  # ConfigurationSetListener �Υ�����Хå��ؿ�
  #
  # @else
  #
  # @brief Virtual Callback function
  #
  # This is a the Callback function for ConfigurationSetListener
  #
  # @endif
  # virtual void operator()(const coil::Properties& config_set) = 0;
  def __call__(self, config_set):
    pass



#============================================================
##
# @if jp
# @brief ConfigurationSetNameListenerType
#
# @else
# @brief The types of ConfigurationSetNameListener
# 
# @endif
class ConfigurationSetNameListenerType:
  """
  """

  def __init__(self):
    pass

  ON_UPDATE_CONFIG_SET          = 0
  ON_REMOVE_CONFIG_SET          = 1
  ON_ACTIVATE_CONFIG_SET        = 2
  CONFIG_SET_NAME_LISTENER_NUM  = 3



##
# @if jp
# @class ConfigurationSetNameListener ���饹
# @brief ConfigurationSetNameListener ���饹
#
# ConfigurationSet�˴ؤ��륤�٥�Ȥ˴ؤ���ꥹ�ʡ����饹��
#
# - ON_UPDATE_CONFIG_SET:
# - ON_REMOVE_CONFIG_SET:
# - ON_ACTIVATE_CONFIG_SET:
#
# @else
# @class ConfigurationSetNameListener class
# @brief ConfigurationSetNameListener class
#
# This class is abstract base class for listener classes that
# provides callbacks for various events for ConfigurationSet.
#
# - ON_UPDATE_CONFIG_SET:
# - ON_REMOVE_CONFIG_SET:
# - ON_ACTIVATE_CONFIG_SET:
#
# @endif
class ConfigurationSetNameListener:
  """
  """

  def __init__(self):
    pass
  

  ##
  # @if jp
  #
  # @brief ConfigurationSetNameListenerType ��ʸ������Ѵ�
  #
  # ConfigurationSetNameListenerType ��ʸ������Ѵ�����
  #
  # @param type �Ѵ��о� ConfigurationSetNameListenerType
  #
  # @return ʸ�����Ѵ����
  #
  # @else
  #
  # @brief Convert ConfigurationSetNameListenerType into the string.
  #
  # Convert ConfigurationSetNameListenerType into the string.
  #
  # @param type The target ConfigurationSetNameListenerType for
  #             transformation
  #
  # @return Trnasformation result of string representation
  #
  # @endif
  # static const char* toString(ConfigurationSetNameListenerType type)
  def toString(type):
    typeString = ["ON_UPDATE_CONFIG_SET",
                  "ON_REMOVE_CONFIG_SET",
                  "ON_ACTIVATE_CONFIG_SET",
                  "CONFIG_SET_NAME_LISTENER_NUM"]
    if type < ConfigurationSetNameListenerType.CONFIG_SET_NAME_LISTENER_NUM:
      return typeString[type]

    return "";

  toString = staticmethod(toString)


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
  #
  # @brief ���ۥ�����Хå��ؿ�
  #
  # ConfigurationSetNameListener �Υ�����Хå��ؿ�
  #
  # @else
  #
  # @brief Virtual Callback function
  #
  # This is a the Callback function for ConfigurationSetNameListener.
  #
  # @endif
  # virtual void operator()(const char* config_set_name) = 0;
  def __call__(self, config_set_name):
    pass



##
# @if jp
#
# @class Entry
# @brief �ꥹ�ʡ��ȼ�ư����ե饰��Ǽ�Ѥ����ѥ��饹
#
# �ꥹ�ʡ����֥������Ȥȼ�ư����Τ���Υե饰���Ǽ���뤿������ѥ��饹
#  
# @else
#
# @class Entry
# @brief Listner and autoclean-flag holder class
#
# A general-purpose class to store away a listener object and
# a flag for automatic deletion
#
# @endif
class Entry:
  def __init__(self,listener,autoclean):
    self.listener  = listener
    self.autoclean = autoclean
    return



##
# @if jp
# @class ConfigurationParamListenerHolder
# @brief ConfigurationParamListener �ۥ�����饹
#
# ʣ���� ConfigurationParamListener ���ݻ����������륯�饹��
#
# @else
# @class ConfigurationParamListenerHolder
# @brief ConfigurationParamListener holder class
#
# This class manages one ore more instances of
# ConfigurationParamListener class.
#
# @endif
class ConfigurationParamListenerHolder:
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # @else
  # @brief Constructor
  # @endif
  # ConfigurationParamListenerHolder();
  def __init__(self):
    self._listeners = []
    pass
  

  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  def __del__(self):
    for (idx, listener) in enumerate(self._listeners):
      if listener.autoclean:
        self._listeners[idx] = None
    return
  

  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ����ɲ�
  #
  # �ꥹ�ʡ����ɲä��롣
  #
  # @param listener �ɲä���ꥹ��
  # @param autoclean true:�ǥ��ȥ饯���Ǻ������,
  #                  false:�ǥ��ȥ饯���Ǻ�����ʤ�
  # @else
  #
  # @brief Add the listener.
  #
  # This method adds the listener. 
  #
  # @param listener Added listener
  # @param autoclean true:The listener is deleted at the destructor.,
  #                  false:The listener is not deleted at the destructor. 
  # @endif
  # void addListener(ConfigurationParamListener* listener, bool autoclean);
  def addListener(self, listener, autoclean):
    self._listeners.append(Entry(listener, autoclean))
    return


  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ��κ��
  #
  # �ꥹ�ʤ������롣
  #
  # @param listener �������ꥹ��
  # @else
  #
  # @brief Remove the listener. 
  #
  # This method removes the listener. 
  #
  # @param listener Removed listener
  # @endif
  # void removeListener(ConfigurationParamListener* listener);
  def removeListener(self, listener):
    len_ = len(self._listeners)
    for i in range(len_):
      idx = (len_ - 1) - i
      if self._listeners[idx].listener == listener:
        if self._listeners[idx].autoclean:
          self._listeners[idx].listener = None
          del self._listeners[idx]
          return
    return
    

  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ������Τ���
  #
  # ��Ͽ����Ƥ���ꥹ�ʤΥ�����Хå��᥽�åɤ�ƤӽФ���
  #
  # @param info ConnectorInfo
  # @param cdrdata �ǡ���
  # @else
  #
  # @brief Notify listeners. 
  #
  # This calls the Callback method of the registered listener. 
  #
  # @param info ConnectorInfo
  # @param cdrdata Data
  # @endif
  # void notify(const char* config_set_name, const char* config_param_name);
  def notify(self, config_set_name, config_param_name):
    for listener in self._listeners:
      listener.listener(config_set_name, config_param_name)
    return
    


#============================================================
##
# @if jp
# @class ConfigurationSetListenerHolder
# @brief ConfigurationSetListener �ۥ�����饹
#
# ʣ���� ConfigurationSetListener ���ݻ����������륯�饹��
#
# @else
# @class ConfigurationSetListenerHolder
# @brief ConfigurationSetListener holder class
#
# This class manages one ore more instances of
# ConfigurationSetListener class.
#
# @endif
class ConfigurationSetListenerHolder:
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # @else
  # @brief Constructor
  # @endif
  # ConfigurationSetListenerHolder();
  def __init__(self):
    self._listeners = []
    pass


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  def __del__(self):
    for (idx, listener) in enumerate(self._listeners):
      if listener.autoclean:
        self._listeners[idx] = None
    return
    

  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ����ɲ�
  #
  # �ꥹ�ʡ����ɲä��롣
  #
  # @param listener �ɲä���ꥹ��
  # @param autoclean true:�ǥ��ȥ饯���Ǻ������,
  #                  false:�ǥ��ȥ饯���Ǻ�����ʤ�
  # @else
  #
  # @brief Add the listener.
  #
  # This method adds the listener. 
  #
  # @param listener Added listener
  # @param autoclean true:The listener is deleted at the destructor.,
  #                  false:The listener is not deleted at the destructor. 
  # @endif
  # void addListener(ConfigurationSetListener* listener, bool autoclean);
  def addListener(self, listener, autoclean):
    self._listeners.append(Entry(listener, autoclean))
    return
  
    
  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ��κ��
  #
  # �ꥹ�ʤ������롣
  #
  # @param listener �������ꥹ��
  # @else
  #
  # @brief Remove the listener. 
  #
  # This method removes the listener. 
  #
  # @param listener Removed listener
  # @endif
  # void removeListener(ConfigurationSetListener* listener);
  def removeListener(self, listener):
    len_ = len(self._listeners)
    for i in range(len_):
      idx = (len_ - 1) - i
      if self._listeners[idx].listener == listener:
        if self._listeners[idx].autoclean:
          self._listeners[idx].listener = None
          del self._listeners[idx]
          return
    return
    

  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ������Τ���
  #
  # ��Ͽ����Ƥ���ꥹ�ʤΥ�����Хå��᥽�åɤ�ƤӽФ���
  #
  # @param info ConnectorInfo
  # @param cdrdata �ǡ���
  # @else
  #
  # @brief Notify listeners. 
  #
  # This calls the Callback method of the registered listener. 
  #
  # @param info ConnectorInfo
  # @param cdrdata Data
  # @endif
  # void notify(const coil::Properties& config_set);
  def notify(self, config_set):
    for listener in self._listeners:
      listener.listener(config_set)
    return
    


#============================================================
##
# @if jp
# @class ConfigurationSetNameListenerHolder 
# @brief ConfigurationSetNameListener �ۥ�����饹
#
# ʣ���� ConfigurationSetNameListener ���ݻ����������륯�饹��
#
# @else
# @class ConfigurationSetNameListenerHolder
# @brief ConfigurationSetNameListener holder class
#
# This class manages one ore more instances of
# ConfigurationSetNameListener class.
#
# @endif
class ConfigurationSetNameListenerHolder:
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # @else
  # @brief Constructor
  # @endif
  # ConfigurationSetNameListenerHolder();
  def __init__(self):
    self._listeners = []
    pass
    

  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  def __del__(self):
    for (idx, listener) in enumerate(self._listeners):
      if listener.autoclean:
        self._listeners[idx] = None
    return


  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ����ɲ�
  #
  # �ꥹ�ʡ����ɲä��롣
  #
  # @param listener �ɲä���ꥹ��
  # @param autoclean true:�ǥ��ȥ饯���Ǻ������,
  #                  false:�ǥ��ȥ饯���Ǻ�����ʤ�
  # @else
  #
  # @brief Add the listener.
  #
  # This method adds the listener. 
  #
  # @param listener Added listener
  # @param autoclean true:The listener is deleted at the destructor.,
  #                  false:The listener is not deleted at the destructor. 
  # @endif
  # void addListener(ConfigurationSetNameListener* listener, bool autoclean);
  def addListener(self, listener, autoclean):
    self._listeners.append(Entry(listener, autoclean))
    return
    

  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ��κ��
  #
  # �ꥹ�ʤ������롣
  #
  # @param listener �������ꥹ��
  # @else
  #
  # @brief Remove the listener. 
  #
  # This method removes the listener. 
  #
  # @param listener Removed listener
  # @endif
  # void removeListener(ConfigurationSetNameListener* listener);
  def removeListener(self, listener):
    len_ = len(self._listeners)
    for i in range(len_):
      idx = (len_ - 1) - i
      if self._listeners[idx].listener == listener:
        if self._listeners[idx].autoclean:
          self._listeners[idx].listener = None
          del self._listeners[idx]
          return
    return


  ##
  # @if jp
  #
  # @brief �ꥹ�ʡ������Τ���
  #
  # ��Ͽ����Ƥ���ꥹ�ʤΥ�����Хå��᥽�åɤ�ƤӽФ���
  #
  # @param info ConnectorInfo
  # @else
  #
  # @brief Notify listeners. 
  #
  # This calls the Callback method of the registered listener. 
  #
  # @param info ConnectorInfo
  # @endif
  # void notify(const char* config_set_name);
  def notify(self, config_set_name):
    for listener in self._listeners:
      listener.listener(config_set_name)
    return
     


#------------------------------------------------------------
##
# @if jp
# @class ConfigurationActionListeners
# @brief ConfigurationActionListeners ���饹
#
#
# @else
# @class ConfigurationActionListeners
# @brief ConfigurationActionListeners class
#
#
# @endif
class ConfigurationListeners:
  """
  """

  def __init__(self):
    pass


  ##
  # @if jp
  # @brief ConfigurationParamListenerType�ꥹ������
  # ConfigurationParamType�ꥹ�ʤ��Ǽ
  # @else
  # @brief ConfigurationParamListenerType listener array
  # The ConfigurationParamListenerType listener is stored.
  # @endif
  configparam_num = ConfigurationParamListenerType.CONFIG_PARAM_LISTENER_NUM
  configparam_ = [ConfigurationParamListenerHolder()
                  for i in range(configparam_num)]

  ##
  # @if jp
  # @brief ConfigurationSetListenerType�ꥹ������
  # ConfigurationSetListenerType�ꥹ�ʤ��Ǽ
  # @else
  # @brief ConfigurationSetListenerType listener array
  # The ConfigurationSetListenerType listener is stored.
  # @endif
  configset_num = ConfigurationSetListenerType.CONFIG_SET_LISTENER_NUM
  configset_ = [ConfigurationSetListenerHolder()
                for i in range(configset_num)]

  ##
  # @if jp
  # @brief ConfigurationSetNameListenerType�ꥹ������
  # ConfigurationSetNameListenerType�ꥹ�ʤ��Ǽ
  # @else
  # @brief ConfigurationSetNameListenerType listener array
  # The ConfigurationSetNameListenerType listener is stored. 
  # @endif
  configsetname_num = ConfigurationSetNameListenerType.CONFIG_SET_NAME_LISTENER_NUM
  configsetname_ = [ConfigurationSetNameListenerHolder()
                    for i in range(configsetname_num)]
