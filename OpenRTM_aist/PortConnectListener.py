#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file PortConnectListener.py
# @brief port's internal action listener classes
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2011
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import threading

class Lock:
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param mutex ��å��ѥߥ塼�ƥå���
  #
  # @else
  #
  # @endif
  def __init__(self, mutex):
    self.mutex = mutex
    self.mutex.acquire()


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
  #
  # @param self
  #
  # @else
  #
  # @endif
  def __del__(self):
    self.mutex.release()

#============================================================

##
# @if jp
# @brief PortConnectListener �Υ�����
#
# - ON_NOTIFY_CONNECT:         notify_connect() �ؿ���ƤӽФ�ľ��
# - ON_NOTIFY_DISCONNECT:      notify_disconnect() �ƤӽФ�ľ��
# - ON_UNSUBSCRIBE_INTERFACES: notify_disconnect() ���IF���ɲ����
#
# @else
# @brief The types of ConnectorDataListener
# 
# - ON_NOTIFY_CONNECT:         right after entering into notify_connect()
# - ON_NOTIFY_DISCONNECT:      right after entering into notify_disconnect()
# - ON_UNSUBSCRIBE_INTERFACES: unsubscribing IF in notify_disconnect()
#
# @endif
class PortConnectListenerType:
  """
  """

  ON_NOTIFY_CONNECT         = 0
  ON_NOTIFY_DISCONNECT      = 1
  ON_UNSUBSCRIBE_INTERFACES = 2
  PORT_CONNECT_LISTENER_NUM = 3

  def __init__(self):
    pass



##
# @if jp
# @class PortConnectListener ���饹
# @brief PortConnectListener ���饹
#
# �ƥ����������б�����桼���������ɤ��ƤФ��ľ���Υ����ߥ�
# �ǥ����뤵���ꥹ�ʥ��饹�δ��쥯�饹��
#
# - ON_NOTIFY_CONNECT:         notify_connect() �ؿ���ƤӽФ�ľ��
# - ON_NOTIFY_DISCONNECT:      notify_disconnect() �ƤӽФ�ľ��
# - ON_UNSUBSCRIBE_INTERFACES: notify_disconnect() ���IF���ɲ����
#
# @else
# @class PortConnectListener class
# @brief PortConnectListener class
#
# This class is abstract base class for listener classes that
# provides callbacks for various events in rtobject.
#
# - ON_NOTIFY_CONNECT:         right after entering into notify_connect()
# - ON_NOTIFY_DISCONNECT:      right after entering into notify_disconnect()
# - ON_UNSUBSCRIBE_INTERFACES: unsubscribing IF in notify_disconnect()
#
# @endif
class PortConnectListener:
  """
  """

  def __init__(self):
    pass

  ##
  # @if jp
  #
  # @brief PortConnectListenerType ��ʸ������Ѵ�
  #
  # PortConnectListenerType ��ʸ������Ѵ�����
  #
  # @param type �Ѵ��о� PortConnectListenerType
  #
  # @return ʸ�����Ѵ����
  #
  # @else
  #
  # @brief Convert PortConnectListenerType into the string.
  #
  # Convert PortConnectListenerType into the string.
  #
  # @param type The target PortConnectListenerType for transformation
  #
  # @return Trnasformation result of string representation
  #
  # @endif
  #static const char* toString(PortConnectListenerType type);
  def toString(type):
    typeString = ["ON_NOTIFY_CONNECT",
                  "ON_NOTIFY_DISCONNECT",
                  "ON_UNSUBSCRIBE_INTERFACES",
                  "ON_UPDATE_CONFIG_PARAM",
                  ""]
                      
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
  # PortConnectListener �Υ�����Хå��ؿ�
  #
  # @else
  #
  # @brief Virtual Callback function
  #
  # This is a the Callback function for PortConnectListener.
  #
  # @endif
  #virtual void operator()(const char* portname,
  #                        RTC::ConnectorProfile& profile) = 0;
  def __call__(self, portname, profile):
    return



#============================================================
##
# @if jp
# @brief PortConnectRetListenerType �Υ�����
#
# - ON_CONNECT_NEXTPORT:     notify_connect() ��Υ��������ɸƤӽФ�ľ��
# - ON_SUBSCRIBE_INTERFACES: notify_connect() ��Υ��󥿡��ե���������ľ��
# - ON_CONNECTED:            nofity_connect() ��³������λ���˸ƤӽФ����
# - ON_DISCONNECT_NEXT:      notify_disconnect() ��˥��������ɸƤӽФ�ľ��
# - ON_DISCONNECTED:         notify_disconnect() �꥿�����
#
# @else
# @brief The types of PortConnectRetListenerType
# 
# - ON_CONNECT_NEXTPORT:     after cascade-call in notify_connect()
# - ON_SUBSCRIBE_INTERFACES: after IF subscribing in notify_connect()
# - ON_CONNECTED:            completed nofity_connect() connection process
# - ON_DISCONNECT_NEXT:      after cascade-call in notify_disconnect()
# - ON_DISCONNECTED:         completed notify_disconnect() disconnection
#
# @endif
class PortConnectRetListenerType:
  """
  """

  ON_PUBLISH_INTERFACES         = 0
  ON_CONNECT_NEXTPORT           = 1
  ON_SUBSCRIBE_INTERFACES       = 2
  ON_CONNECTED                  = 3
  ON_DISCONNECT_NEXT            = 4
  ON_DISCONNECTED               = 5
  PORT_CONNECT_RET_LISTENER_NUM = 6

  def __init__(self):
    pass



##
# @if jp
# @class PortConnectRetListener ���饹
# @brief PortConnectRetListener ���饹
#
# �ƥ����������б�����桼���������ɤ��ƤФ��ľ���Υ����ߥ�
# �ǥ����뤵���ꥹ�ʥ��饹�δ��쥯�饹��
#
# - ON_PUBLISH_INTERFACES:   notify_connect() ��Υ��󥿡��ե���������ľ��
# - ON_CONNECT_NEXTPORT:     notify_connect() ��Υ��������ɸƤӽФ�ľ��
# - ON_SUBSCRIBE_INTERFACES: notify_connect() ��Υ��󥿡��ե���������ľ��
# - ON_CONNECTED:            nofity_connect() ��³������λ���˸ƤӽФ����
# - ON_DISCONNECT_NEXT:      notify_disconnect() ��˥��������ɸƤӽФ�ľ��
# - ON_DISCONNECTED:         notify_disconnect() �꥿�����
#
# @else
# @class PortConnectRetListener class
# @brief PortConnectRetListener class
#
# This class is abstract base class for listener classes that
# provides callbacks for various events in rtobject.
#
# - ON_CONNECT_NEXTPORT:     after cascade-call in notify_connect()
# - ON_SUBSCRIBE_INTERFACES: after IF subscribing in notify_connect()
# - ON_CONNECTED:            completed nofity_connect() connection process
# - ON_DISCONNECT_NEXT:      after cascade-call in notify_disconnect()
# - ON_DISCONNECTED:         completed notify_disconnect() disconnection
#
# @endif
class PortConnectRetListener:
  """
  """

  def __init__(self):
    pass


  ##
  # @if jp
  #
  # @brief PortConnectRetListenerType ��ʸ������Ѵ�
  #
  # PortConnectRetListenerType ��ʸ������Ѵ�����
  #
  # @param type �Ѵ��о� PortConnectRetListenerType
  #
  # @return ʸ�����Ѵ����
  #
  # @else
  #
  # @brief Convert PortConnectRetListenerType into string.
  #
  # Convert PortConnectRetListenerType into string.
  #
  # @param type The target PortConnectRetListenerType for transformation
  #
  # @return Trnasformation result of string representation
  #
  # @endif
  #static const char* toString(PortConnectRetListenerType type);
  def toString(type):
    return
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
  # PortConnectRetListener �Υ�����Хå��ؿ�
  #
  # @else
  #
  # @brief Virtual Callback function
  #
  # This is a the Callback function for PortConnectRetListener.
  #
  # @endif
  #virtual void operator()(const char* portname,
  #                        RTC::ConnectorProfile& profile,
  #                        ReturnCode_t ret) = 0;
  def __call__(self, portname, profile, ret):
    pass



class Entry:
  def __init__(self,listener, autoclean):
    self.listener  = listener
    self.autoclean = autoclean
    return

#============================================================
##
# @if jp
# @class PortConnectListenerHolder 
# @brief PortConnectListener �ۥ�����饹
#
# ʣ���� PortConnectListener ���ݻ����������륯�饹��
#
# @else
# @class PortConnectListenerHolder
# @brief PortConnectListener holder class
#
# This class manages one ore more instances of
# PortConnectListener class.
#
# @endif
class PortConnectListenerHolder:
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
    self._mutex = threading.RLock()
    return

    
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
  #void addListener(PortConnectListener* listener, bool autoclean);
  def addListener(self, listener, autoclean):
    guard = Lock(self._mutex)
    self._listeners.append(Entry(listener, autoclean))
    del guard
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
  #void removeListener(PortConnectListener* listener);
  def removeListener(self, listener):
    guard = Lock(self._mutex)
    len_ = len(self._listeners)
    for i in range(len_):
      if (self._listeners[i].listener == listener) and self._listeners[i].autoclean:
        self._listeners[i].listener = None
      del self._listeners[i]
      del guard
      return
    del guard
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
  #void notify(const char* portname, RTC::ConnectorProfile& profile);
  def notify(self, portname, profile):
    guard = Lock(self._mutex)
    for listener in self._listeners:
      listener.listener(portname, profile)
    del guard
    return


##
# @if jp
# @class PortConnectRetListenerHolder
# @brief PortConnectRetListener �ۥ�����饹
#
# ʣ���� PortConnectRetListener ���ݻ����������륯�饹��
#
# @else
# @class PortConnectRetListenerHolder
# @brief PortConnectRetListener holder class
#
# This class manages one ore more instances of
# PortConnectRetListener class.
#
# @endif
class PortConnectRetListenerHolder:
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  # @else
  # @brief Constructor
  # @endif
  #PortConnectRetListenerHolder();
  def __init__(self):
    self._listeners = []
    self._mutex = threading.RLock()
    return


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
  #void addListener(PortConnectRetListener* listener, bool autoclean);
  def addListener(self, listener, autoclean):
    guard = Lock(self._mutex)
    self._listeners.append(Entry(listener, autoclean))
    del guard
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
  #void removeListener(PortConnectRetListener* listener);
  def removeListener(self, listener):
    guard = Lock(self._mutex)
    len_ = len(self._listeners)
    for i in range(len_):
      if (self._listeners[i].listener == listener) and self._listeners[i].autoclean:
        self._listeners[i].listener = None
      del self._listeners[i]
      del guard
      return
    del guard
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
  #void notify(const char* portname, RTC::ConnectorProfile& profile,
  #            ReturnCode_t ret);
  def notify(self, portname, profile, ret):
    guard = Lock(self._mutex)
    for listener in self._listeners:
      listener.listener(portname, profile, ret)
    del guard
    return



##
# @if jp
# @class PortConnectListeners
# @brief PortConnectListeners ���饹
#
#
# @else
# @class PortConnectListeners
# @brief PortConnectListeners class
#
#
# @endif
class PortConnectListeners:
  """
  """

  def __init__(self):
    pass


  ##
  # @if jp
  # @brief PortConnectListenerType �ꥹ������
  # PortConnectListenerType �ꥹ�ʤ��Ǽ
  # @else
  # @brief PortConnectListenerType listener array
  # The PortConnectListenerType listener is stored. 
  # @endif
  portconnect_num = PortConnectListenerType.PORT_CONNECT_LISTENER_NUM
  portconnect_ = [PortConnectListenerHolder() for i in range(portconnect_num)]
    
  ##
  # @if jp
  # @brief PortConnectRetType�ꥹ������
  # PortConnectRetType�ꥹ�ʤ��Ǽ
  # @else
  # @brief PortConnectRetType listener array
  # The PortConnectRetType listener is stored.
  # @endif
  portconnret_num = PortConnectRetListenerType.PORT_CONNECT_RET_LISTENER_NUM
  portconnret_ = [PortConnectRetListenerHolder() for i in range(portconnret_num)]
