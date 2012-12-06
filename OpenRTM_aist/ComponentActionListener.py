#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ComponentActionListener.py
# @brief component action listener class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2011
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


#============================================================

##
# @if jp
# @brief PreComponentActionListener �Υ�����
#
# - PRE_ON_INITIALIZE:    onInitialize ľ��
# - PRE_ON_FINALIZE:      onFinalize ľ��
# - PRE_ON_STARTUP:       onStartup ľ��
# - PRE_ON_SHUTDOWN:      onShutdown ľ��
# - PRE_ON_ACTIVATED:     onActivated ľ��
# - PRE_ON_DEACTIVATED:   onDeactivated ľ��
# - PRE_ON_ABORTING:      onAborted ľ��
# - PRE_ON_ERROR:         onError ľ��
# - PRE_ON_RESET:         onReset ľ��
# - PRE_ON_EXECUTE:       onExecute ľ��
# - PRE_ON_STATE_UPDATE:  onStateUpdate ľ��
# - PRE_ON_RATE_CHANGED:  onRateChanged ľ��
#
# @else
# @brief The types of ConnectorDataListener
# 
# @endif
class PreComponentActionListenerType:
  """
  """

  def __init__(self):
    pass

  PRE_ON_INITIALIZE                 = 0
  PRE_ON_FINALIZE                   = 1
  PRE_ON_STARTUP                    = 2
  PRE_ON_SHUTDOWN                   = 3
  PRE_ON_ACTIVATED                  = 4
  PRE_ON_DEACTIVATED                = 5
  PRE_ON_ABORTING                   = 6
  PRE_ON_ERROR                      = 7
  PRE_ON_RESET                      = 8
  PRE_ON_EXECUTE                    = 9
  PRE_ON_STATE_UPDATE               = 10
  PRE_ON_RATE_CHANGED               = 11
  PRE_COMPONENT_ACTION_LISTENER_NUM = 12


##
# @if jp
# @class PreComponentActionListener ���饹
# @brief PreComponentActionListener ���饹
#
# OMG RTC���ͤ��������Ƥ���ʲ��Υ���ݡ��ͥ�ȥ��������ȤˤĤ�
# �ơ�
#
# - on_initialize()
# - on_finalize()
# - on_startup()
# - on_shutdown()
# - on_activated
# - on_deactivated()
# - on_aborted()
# - on_error()
# - on_reset()
# - on_execute()
# - on_state_update()
# - on_rate_changed()
#
# �ƥ����������б�����桼���������ɤ��ƤФ��ľ���Υ����ߥ�
# �ǥ����뤵���ꥹ�ʥ��饹�δ��쥯�饹��
#
# - PRE_ON_INITIALIZE:
# - PRE_ON_FINALIZE:
# - PRE_ON_STARTUP:
# - PRE_ON_SHUTDOWN:
# - PRE_ON_ACTIVATED:
# - PRE_ON_DEACTIVATED:
# - PRE_ON_ABORTING:
# - PRE_ON_ERROR:
# - PRE_ON_RESET:
# - PRE_IN_EXECUTE:
# - PRE_ON_STATE_UPDATE:
# - PRE_ON_RATE_CHANGED:
#
# @else
# @class PreComponentActionListener class
# @brief PreComponentActionListener class
#
# This class is abstract base class for listener classes that
# provides callbacks for various events in rtobject.
#
# @endif
class PreComponentActionListener:
  """
  """

  def __init__(self):
    pass

  ##
  # @if jp
  #
  # @brief PreComponentActionListenerType ��ʸ������Ѵ�
  #
  # PreComponentActionListenerType ��ʸ������Ѵ�����
  #
  # @param type �Ѵ��о� PreComponentActionListenerType
  #
  # @return ʸ�����Ѵ����
  #
  # @else
  #
  # @brief Convert PreComponentActionListenerType into the string.
  #
  # Convert PreComponentActionListenerType into the string.
  #
  # @param type The target PreComponentActionListenerType for transformation
  #
  # @return Trnasformation result of string representation
  #
  # @endif
  # static const char* toString(PreComponentActionListenerType type) 
  def toString(type):
    typeString = ["PRE_ON_INITIALIZE",
                  "PRE_ON_FINALIZE",
                  "PRE_ON_STARTUP",
                  "PRE_ON_SHUTDOWN",
                  "PRE_ON_ACTIVATED",
                  "PRE_ON_DEACTIVATED",
                  "PRE_ON_ABORTING",
                  "PRE_ON_ERROR",
                  "PRE_ON_RESET",
                  "PRE_ON_EXECUTE",
                  "PRE_ON_STATE_UPDATE",
                  "PRE_ON_RATE_CHANGED",
                  "PRE_COMPONENT_ACTION_LISTENER_NUM"]
    if type < PreComponentActionListenerType.PRE_COMPONENT_ACTION_LISTENER_NUM:
      return typeString[type]

    return ""
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
  # PreComponentActionListener �Υ�����Хå��ؿ�
  #
  # @else
  #
  # @brief Virtual Callback function
  #
  # This is a the Callback function for PreComponentActionListener.
  #
  # @endif
  # virtual void operator()(UniqueId ec_id) = 0;
  def __call__(self, ec_id):
    pass


#============================================================

##
# @if jp
# @brief PostCompoenntActionListener �Υ�����
#
# - POST_ON_INITIALIZE:
# - POST_ON_FINALIZE:
# - POST_ON_STARTUP:
# - POST_ON_SHUTDOWN:
# - POST_ON_ACTIVATED:
# - POST_ON_DEACTIVATED:
# - POST_ON_ABORTING:
# - POST_ON_ERROR:
# - POST_ON_RESET:
# - POST_ON_EXECUTE:
# - POST_ON_STATE_UPDATE:
# - POST_ON_RATE_CHANGED:
#
# @else
# @brief The types of ConnectorDataListener
# 
# @endif
class PostComponentActionListenerType:
  """
  """
  def __init__(self):
    pass

  POST_ON_INITIALIZE                 = 0
  POST_ON_FINALIZE                   = 1
  POST_ON_STARTUP                    = 2
  POST_ON_SHUTDOWN                   = 3
  POST_ON_ACTIVATED                  = 4
  POST_ON_DEACTIVATED                = 5
  POST_ON_ABORTING                   = 6
  POST_ON_ERROR                      = 7
  POST_ON_RESET                      = 8
  POST_ON_EXECUTE                    = 9
  POST_ON_STATE_UPDATE               = 10
  POST_ON_RATE_CHANGED               = 11
  POST_COMPONENT_ACTION_LISTENER_NUM = 12



##
# @if jp
# @class PostComponentActionListener ���饹
# @brief PostComponentActionListener ���饹
#
# OMG RTC���ͤ��������Ƥ���ʲ��Υ���ݡ��ͥ�ȥ��������ȤˤĤ�
# �ơ�
#
# - on_initialize()
# - on_finalize()
# - on_startup()
# - on_shutdown()
# - on_activated
# - on_deactivated()
# - on_aborted()
# - on_error()
# - on_reset()
# - on_execute()
# - on_state_update()
# - on_rate_changed()
#
# �ƥ����������б�����桼���������ɤ��ƤФ��ľ���Υ����ߥ�
# �ǥ����뤵���ꥹ�ʥ��饹�δ��쥯�饹��
#
# - POST_ON_INITIALIZE:
# - POST_ON_FINALIZE:
# - POST_ON_STARTUP:
# - POST_ON_SHUTDOWN:
# - POST_ON_ACTIVATED:
# - POST_ON_DEACTIVATED:
# - POST_ON_ABORTING:
# - POST_ON_ERROR:
# - POST_ON_RESET:
# - POST_ON_EXECUTE:
# - POST_ON_STATE_UPDATE:
# - POST_ON_RATE_CHANGED:
#
# @else
# @class PostComponentActionListener class
# @brief PostComponentActionListener class
#
# This class is abstract base class for listener classes that
# provides callbacks for various events in rtobject.
#
# @endif
class PostComponentActionListener:
  """
  """

  def __init__(self):
    pass

  ##
  # @if jp
  #
  # @brief PostComponentActionListenerType ��ʸ������Ѵ�
  #
  # PostComponentActionListenerType ��ʸ������Ѵ�����
  #
  # @param type �Ѵ��о� PostComponentActionListenerType
  #
  # @return ʸ�����Ѵ����
  #
  # @else
  #
  # @brief Convert PostComponentActionListenerType into the string.
  #
  # Convert PostComponentActionListenerType into the string.
  #
  # @param type The target PostComponentActionListenerType for transformation
  #
  # @return Trnasformation result of string representation
  #
  # @endif
  # static const char* toString(PostComponentActionListenerType type)
  def toString(type):
    typeString = ["POST_ON_INITIALIZE",
                  "POST_ON_FINALIZE",
                  "POST_ON_STARTUP",
                  "POST_ON_SHUTDOWN",
                  "POST_ON_ACTIVATED",
                  "POST_ON_DEACTIVATED",
                  "POST_ON_ABORTING",
                  "POST_ON_ERROR",
                  "POST_ON_RESET",
                  "POST_ON_EXECUTE",
                  "POST_ON_STATE_UPDATE",
                  "POST_ON_RATE_CHANGED",
                  "POST_COMPONENT_ACTION_LISTENER_NUM"]
    if type < PostComponentActionListenerType.POST_COMPONENT_ACTION_LISTENER_NUM:
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
  # PostComponentActionListener �Υ�����Хå��ؿ�
  #
  # @else
  #
  # @brief Virtual Callback function
  #
  # This is a the Callback function for PostComponentActionListener.
  #
  # @endif
  #virtual void operator()(UniqueId ec_id,
  #                        ReturnCode_t ret) = 0;
  def __call__(self, ec_id, ret):
    pass



#============================================================
##
# @if jp
# @brief PortActionListener �Υ�����
#
# - ADD_PORT:             Port �ɲû�
# - REMOVE_PORT:          Port �����
#
# @else
# @brief The types of PortActionListener
# 
# @endif
class PortActionListenerType:
  """
  """
  
  def __init__(self):
    pass

  ADD_PORT                 = 0
  REMOVE_PORT              = 1
  PORT_ACTION_LISTENER_NUM = 2



##
# @if jp
# @class PortActionListener ���饹
# @brief PortActionListener ���饹
#
# �ƥ����������б�����桼���������ɤ��ƤФ��ľ���Υ����ߥ�
# �ǥ����뤵���ꥹ�ʥ��饹�δ��쥯�饹��
#
# - ADD_PORT:
# - REMOVE_PORT:
#
# @else
# @class PortActionListener class
# @brief PortActionListener class
#
# This class is abstract base class for listener classes that
# provides callbacks for various events in rtobject.
#
# @endif
class PortActionListener:
  """
  """

  def __init__(self):
    pass

  ##
  # @if jp
  #
  # @brief PortActionListenerType ��ʸ������Ѵ�
  #
  # PortActionListenerType ��ʸ������Ѵ�����
  #
  # @param type �Ѵ��о� PortActionListenerType
  #
  # @return ʸ�����Ѵ����
  #
  # @else
  #
  # @brief Convert PortActionListenerType into the string.
  #
  # Convert PortActionListenerType into the string.
  #
  # @param type The target PortActionListenerType for transformation
  #
  # @return Trnasformation result of string representation
  #
  # @endif
  #static const char* toString(PortActionListenerType type)
  def toString(type):
    typeString = ["ADD_PORT",
                  "REMOVE_PORT",
                  "PORT_ACTION_LISTENER_NUM"]
    if type < PortActionListenerType.PORT_ACTION_LISTENER_NUM:
      return typeString[type]
    return ""

  toString = staticmethod(toString)

  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  #virtual ~PortActionListener();
  def __del__(self):
    pass

  ##
  # @if jp
  #
  # @brief ���ۥ�����Хå��ؿ�
  #
  # PortActionListener �Υ�����Хå��ؿ�
  #
  # @else
  #
  # @brief Virtual Callback function
  #
  # This is a the Callback function for PortActionListener
  #
  # @endif
  #virtual void operator()(const ::RTC::PortProfile& pprof) = 0;
  def __call__(self, pprof):
    pass


#============================================================
##
# @if jp
# @brief ExecutionContextActionListener �Υ�����
#
# - EC_ATTACHED:          ExecutionContext �ɲû�
# - EC_DETACHED:          ExecutionContext �����
#
# @else
# @brief The types of ExecutionContextActionListener
# 
# @endif
class ExecutionContextActionListenerType:
  """
  """
  def __init__(self):
    pass

  EC_ATTACHED            = 0
  EC_DETACHED            = 1
  EC_ACTION_LISTENER_NUM = 2

##
# @if jp
# @class ExecutionContextActionListener ���饹
# @brief ExecutionContextActionListener ���饹
#
# �ƥ����������б�����桼���������ɤ��ƤФ��ľ���Υ����ߥ�
# �ǥ����뤵���ꥹ�ʥ��饹�δ��쥯�饹��
#
# - ADD_PORT:
# - REMOVE_PORT:
#
# @else
# @class ExecutionContextActionListener class
# @brief ExecutionContextActionListener class
#
# This class is abstract base class for listener classes that
# provides callbacks for various events in rtobject.
#
# @endif
class ExecutionContextActionListener:
  """
  """

  def __init__(self):
    pass


  ##
  # @if jp
  #
  # @brief ExecutionContextActionListenerType ��ʸ������Ѵ�
  #
  # ExecutionContextActionListenerType ��ʸ������Ѵ�����
  #
  # @param type �Ѵ��о� ExecutionContextActionListenerType
  #
  # @return ʸ�����Ѵ����
  #
  # @else
  #
  # @brief Convert ExecutionContextActionListenerType into the string.
  #
  # Convert ExecutionContextActionListenerType into the string.
  #
  # @param type The target ExecutionContextActionListenerType for transformation
  #
  # @return Trnasformation result of string representation
  #
  # @endif
  #static const char* toString(ExecutionContextActionListenerType type)
  def toString(type):
    typeString = ["ATTACH_EC",
                  "DETACH_EC",
                  "EC_ACTION_LISTENER_NUM"]
    if type < ExecutionContextActionListenerType.EC_ACTION_LISTENER_NUM:
      return typeString[type]
    return ""

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
  # ExecutionContextActionListener �Υ�����Хå��ؿ�
  #
  # @else
  #
  # @brief Virtual Callback function
  #
  # This is a the Callback function for ExecutionContextActionListener
  #
  # @endif
  #virtual void operator()(UniqueId ec_id) = 0;
  def __call__(self, ec_id):
    pass


class Entry:
  def __init__(self,listener, autoclean):
    self.listener  = listener
    self.autoclean = autoclean
    return


#============================================================
##
# @if jp
# @class PreComponentActionListenerHolder 
# @brief PreComponentActionListener �ۥ�����饹
#
# ʣ���� PreComponentActionListener ���ݻ����������륯�饹��
#
# @else
# @class PreComponentActionListenerHolder
# @brief PreComponentActionListener holder class
#
# This class manages one ore more instances of
# PreComponentActionListener class.
#
# @endif
class PreComponentActionListenerHolder:
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # @else
  # @brief Constructor
  # @endif
  def __init__(self):
    self._listeners = []
    return
  
    
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
  #void addListener(PreComponentActionListener* listener, bool autoclean);
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
  #void removeListener(PreComponentActionListener* listener);
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
  #void notify(UniqueId ec_id);
  def notify(self, ec_id):
    for listener in self._listeners:
      listener.listener(ec_id)
    return

      

##
# @if jp
# @class PostComponentActionListenerHolder
# @brief PostComponentActionListener �ۥ�����饹
#
# ʣ���� PostComponentActionListener ���ݻ����������륯�饹��
#
# @else
# @class PostComponentActionListenerHolder
# @brief PostComponentActionListener holder class
#
# This class manages one ore more instances of
# PostComponentActionListener class.
#
# @endif
class PostComponentActionListenerHolder:
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # @else
  # @brief Constructor
  # @endif
  def __init__(self):
    self._listeners = []
    return


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
  #void addListener(PostComponentActionListener* listener, bool autoclean);
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
  #void removeListener(PostComponentActionListener* listener);
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
  #void notify(UniqueId ec_id, ReturnCode_t ret);
  def notify(self, ec_id, ret):
    for listener in self._listeners:
      listener.listener(ec_id, ret)
    return
    


#============================================================
##
# @if jp
# @class PortActionListenerHolder
# @brief PortActionListener �ۥ�����饹
#
# ʣ���� PortActionListener ���ݻ����������륯�饹��
#
# @else
# @class PortActionListenerHolder
# @brief PortActionListener holder class
#
# This class manages one ore more instances of
# PortActionListener class.
#
# @endif
class PortActionListenerHolder:
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # @else
  # @brief Constructor
  # @endif
  def __init__(self):
    self._listeners = []
    return


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
    pass
    
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
  #void addListener(PortActionListener* listener, bool autoclean);
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
  #void removeListener(PortActionListener* listener);
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
  #void notify(const RTC::PortProfile& pprofile);
  def notify(self, pprofile):
    for listener in self._listeners:
      listener.listener(pprofile)
    return

    

##
# @if jp
# @class ExecutionContextActionListenerHolder
# @brief ExecutionContextActionListener �ۥ�����饹
#
# ʣ���� ExecutionContextActionListener ���ݻ����������륯�饹��
#
# @else
# @class ExecutionContextActionListenerHolder
# @brief ExecutionContextActionListener holder class
#
# This class manages one ore more instances of
# ExecutionContextActionListener class.
#
# @endif
class ExecutionContextActionListenerHolder:
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # @else
  # @brief Constructor
  # @endif
  def __init__(self):
    self._listeners = []
    return


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
    pass
    

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
  #void addListener(ExecutionContextActionListener* listener, bool autoclean);
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
  #void removeListener(ExecutionContextActionListener* listener);
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
  #void notify(UniqueId ec_id);
  def notify(self, ec_id):
    for listener in self._listeners:
      listener.listener(ec_id)
    return



##
# @if jp
# @class ComponentActionListeners
# @brief ComponentActionListeners ���饹
#
#
# @else
# @class ComponentActionListeners
# @brief ComponentActionListeners class
#
#
# @endif
class ComponentActionListeners:
  """
  """

  def __init__(self):
    pass

  ##
  # @if jp
  # @brief PreComponentActionListenerType�ꥹ������
  # PreComponentActionListenerType�ꥹ�ʤ��Ǽ
  # @else
  # @brief PreComponentActionListenerType listener array
  # The PreComponentActionListenerType listener is stored. 
  # @endif
  preaction_num = PreComponentActionListenerType.PRE_COMPONENT_ACTION_LISTENER_NUM
  preaction_ = [PreComponentActionListenerHolder() 
                for i in range(preaction_num)]

  ##
  # @if jp
  # @brief PostComponentActionListenerType�ꥹ������
  # PostComponentActionListenerType�ꥹ�ʤ��Ǽ
  # @else
  # @brief PostComponentActionListenerType listener array
  # The PostComponentActionListenerType listener is stored.
  # @endif
  postaction_num = PostComponentActionListenerType.POST_COMPONENT_ACTION_LISTENER_NUM
  postaction_ = [PostComponentActionListenerHolder()
                 for i in range(postaction_num)]

  ##
  # @if jp
  # @brief PortActionListenerType�ꥹ������
  # PortActionListenerType�ꥹ�ʤ��Ǽ
  # @else
  # @brief PortActionListenerType listener array
  # The PortActionListenerType listener is stored.
  # @endif
  portaction_num = PortActionListenerType.PORT_ACTION_LISTENER_NUM
  portaction_ = [PortActionListenerHolder()
                 for i in range(portaction_num)]
  
  ##
  # @if jp
  # @brief ExecutionContextActionListenerType�ꥹ������
  # ExecutionContextActionListenerType�ꥹ�ʤ��Ǽ
  # @else
  # @brief ExecutionContextActionListenerType listener array
  # The ExecutionContextActionListenerType listener is stored.
  # @endif
  ecaction_num = ExecutionContextActionListenerType.EC_ACTION_LISTENER_NUM
  ecaction_ = [ExecutionContextActionListenerHolder()
               for i in range(ecaction_num)]
