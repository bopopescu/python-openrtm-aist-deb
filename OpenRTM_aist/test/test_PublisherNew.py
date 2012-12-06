#!/usr/bin/env python
# -*- coding: euc-jp -*-

#
#  \file  test_PublisherNew.py
#  \brief test for PublisherNew class
#  \date  $Date: 2007/09/27 $
#  \author Shinji Kurihara
# 
#  Copyright (C) 2006
#      Noriaki Ando
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.
 
import sys,time
sys.path.insert(1,"../")

import unittest

import OpenRTM_aist
from PublisherNew import *

class ConsumerMock(OpenRTM_aist.InPortCorbaCdrConsumer):
  def __init__(self):
    buff = OpenRTM_aist.CdrRingBuffer()
    prop = OpenRTM_aist.Properties()
    prop.setProperty("write.full_policy","do_nothing")
    buff.init(prop)
    self._buffer = buff

  def __del__(self):
    pass

  def convertReturnCode(self, ret):
    if ret == OpenRTM_aist.BufferStatus.BUFFER_OK:
      return self.PORT_OK

    elif ret == OpenRTM_aist.BufferStatus.BUFFER_ERROR:
      return self.PORT_ERROR

    elif ret == OpenRTM_aist.BufferStatus.BUFFER_FULL:
      return self.SEND_FULL

    elif ret == OpenRTM_aist.BufferStatus.TIMEOUT:
      return self.SEND_TIMEOUT

    elif ret == OpenRTM_aist.BufferStatus.NOT_SUPPORTED:
      return self.UNKNOWN_ERROR

    else:
      return self.UNKNOWN_ERROR

  def put(self,data):
    ret = self.convertReturnCode(self._buffer.write(data))
    return ret
    """
    if self._buffer.full():
      return OpenRTM_aist.DataPortStatus.BUFFER_FULL

    ret = self._buffer.write(data)
    if ret == OpenRTM_aist.BufferStatus.BUFFER_OK:
      return OpenRTM_aist.DataPortStatus.PORT_OK
    elif ret == OpenRTM_aist.BufferStatus.BUFFER_ERROR:
      return OpenRTM_aist.DataPortStatus.PORT_ERROR
    elif ret == OpenRTM_aist.BufferStatus.BUFFER_FULL:
      return OpenRTM_aist.DataPortStatus.BUFFER_FULL
    elif ret == OpenRTM_aist.BufferStatus.BUFFER_EMPTY:
      return OpenRTM_aist.DataPortStatus.BUFFER_EMPTY
    elif ret == OpenRTM_aist.BufferStatus.TIMEOUT:
      return OpenRTM_aist.DataPortStatus.BUFFER_TIMEOUT
    else:
      return OpenRTM_aist.DataPortStatus.UNKNOWN_ERROR
    """

  def get_m_put_data(self):
    cdr = [0]
    self._buffer.read(cdr)
    return cdr[0]

  def get_m_put_data_len(self):
    ic = self._buffer.readable()
    return ic



class TestPublisherNew(unittest.TestCase):

  def setUp(self):
    time.sleep(0.1)
    return

  def tearDown(self):
    OpenRTM_aist.Manager.instance().shutdownManager()
    return

  def test_init(self):
    _pn = PublisherNew()
    prop = OpenRTM_aist.Properties()
    # Properties�����ξ��֤Ǥ������ư��뤳�Ȥ��ǧ����
    ret = _pn.init(prop)
    self.assertEqual(OpenRTM_aist.DataPortStatus.PORT_OK, ret)
    _pn.__del__()
    
    _pn = PublisherNew()
    prop.setProperty("publisher.push_policy","new")
    prop.setProperty("thread_type","bar")
    prop.setProperty("measurement.exec_time","default")
    prop.setProperty("measurement.period_count","1")
    
    #thread_type �������ξ�� INVALID_ARGS ���֤����Ȥ��ǧ���롣
    ret = _pn.init(prop)
    self.assertEqual(OpenRTM_aist.DataPortStatus.INVALID_ARGS, ret)
    _pn.__del__()
    
    _pn = PublisherNew()
    #�ʲ���properties�������ư��뤳�Ȥ��ǧ���롣
    prop.setProperty("publisher.push_policy","all")
    prop.setProperty("publisher.skip_count","0")
    prop.setProperty("thread_type","default")
    prop.setProperty("measurement.exec_time","enable")
    prop.setProperty("measurement.exec_count","0")
    prop.setProperty("measurement.period_time","enable")
    prop.setProperty("measurement.period_count","0")
    retcode = _pn.init(prop)
    self.assertEqual(OpenRTM_aist.DataPortStatus.PORT_OK, retcode)
    _pn.__del__()
    
    _pn = PublisherNew()
    prop.setProperty("publisher.push_policy","fifo")
    prop.setProperty("publisher.skip_count","1")
    prop.setProperty("thread_type","default")
    prop.setProperty("measurement.exec_time","disable")
    prop.setProperty("measurement.exec_count","1")
    prop.setProperty("measurement.period_time","disable")
    prop.setProperty("measurement.period_count","0")
    retcode = _pn.init(prop)
    self.assertEqual(OpenRTM_aist.DataPortStatus.PORT_OK, retcode)
    _pn.__del__()
    
    _pn = PublisherNew()
    prop.setProperty("publisher.push_policy","fifo")
    prop.setProperty("publisher.skip_count","1")
    prop.setProperty("thread_type","default")
    prop.setProperty("measurement.exec_time","disable")
    prop.setProperty("measurement.exec_count","1")
    prop.setProperty("measurement.period_time","disable")
    prop.setProperty("measurement.period_count","1")
    retcode = _pn.init(prop)
    self.assertEqual(OpenRTM_aist.DataPortStatus.PORT_OK, retcode)
    _pn.__del__()
    
    _pn = PublisherNew()
    prop.setProperty("publisher.push_policy","skip")
    prop.setProperty("publisher.skip_count","-1")
    prop.setProperty("thread_type","default")
    prop.setProperty("measurement.exec_time","bar")
    prop.setProperty("measurement.exec_count","-1")
    prop.setProperty("measurement.period_time","bar")
    prop.setProperty("measurement.period_count","-1")
    retcode = _pn.init(prop)
    self.assertEqual(OpenRTM_aist.DataPortStatus.PORT_OK, retcode)
    _pn.__del__()
    
    _pn = PublisherNew()
    prop.setProperty("publisher.push_policy","new")
    prop.setProperty("publisher.skip_count","1")
    prop.setProperty("thread_type","default")
    prop.setProperty("measurement.exec_time","enable")
    prop.setProperty("measurement.exec_count","1")
    prop.setProperty("measurement.period_time","enable")
    prop.setProperty("measurement.period_count","1")
    retcode = _pn.init(prop)
    self.assertEqual(OpenRTM_aist.DataPortStatus.PORT_OK, retcode)
    _pn.__del__()
    
    _pn = PublisherNew()
    prop.setProperty("publisher.push_policy","bar")
    prop.setProperty("publisher.skip_count","0")
    prop.setProperty("thread_type","default")
    prop.setProperty("measurement.exec_time","enable")
    prop.setProperty("measurement.exec_count","0")
    prop.setProperty("measurement.period_time","enable")
    prop.setProperty("measurement.period_count","0")
    retcode = _pn.init(prop)
    self.assertEqual(OpenRTM_aist.DataPortStatus.PORT_OK, retcode)
    _pn.__del__()
    return

  def test_setConsumer(self):
    _pn = PublisherNew()
    self.assertEqual(_pn.setConsumer(None),OpenRTM_aist.DataPortStatus.INVALID_ARGS)
    self.assertEqual(_pn.setConsumer(ConsumerMock()),OpenRTM_aist.DataPortStatus.PORT_OK)
    _pn.__del__()
    return

  def test_setBuffer(self):
    _pn = PublisherNew()
    self.assertEqual(_pn.setBuffer(None),OpenRTM_aist.DataPortStatus.INVALID_ARGS)
    self.assertEqual(_pn.setBuffer(OpenRTM_aist.RingBuffer()),OpenRTM_aist.DataPortStatus.PORT_OK)
    _pn.__del__()
    return

  def test_write(self):
    _pn = PublisherNew()
    prop = OpenRTM_aist.Properties()
    retcode = _pn.init(prop)
    _pn.setBuffer(OpenRTM_aist.RingBuffer())
    #self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    _pn.__del__()
    return

  def test_activate_deactivate_isActive(self):
    _pn = PublisherNew()
    self.assertEqual(_pn.isActive(),False)
    self.assertEqual(_pn.activate(),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.isActive(),True)
    self.assertEqual(_pn.deactivate(),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.isActive(),False)
    _pn.__del__()
    return

  def test_pushAll(self):
    _pn = PublisherNew()
    prop = OpenRTM_aist.Properties()
    cinfo = OpenRTM_aist.ConnectorInfo("",
                                       "",
                                       [],
                                       prop)
    self.assertEqual(_pn.setListener(cinfo,OpenRTM_aist.ConnectorListeners()),
                     OpenRTM_aist.DataPortStatus.PORT_OK)
    prop = OpenRTM_aist.Properties()
    prop.setProperty("publisher.push_policy","all")
    prop.setProperty("publisher.skip_count","0")
    prop.setProperty("thread_type","default")
    prop.setProperty("measurement.exec_time","enable")
    prop.setProperty("measurement.exec_count","0")
    prop.setProperty("measurement.period_time","enable")
    prop.setProperty("measurement.period_count","0")
    retcode = _pn.init(prop)
    cons = ConsumerMock()
    self.assertEqual(_pn.setConsumer(cons),OpenRTM_aist.DataPortStatus.PORT_OK)
    _pn.setBuffer(OpenRTM_aist.CdrRingBuffer())
    _pn.activate()

    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    _pn.deactivate()
    _pn.__del__()
    return

  def test_pushFifo(self):
    _pn = PublisherNew()
    prop = OpenRTM_aist.Properties()
    cinfo = OpenRTM_aist.ConnectorInfo("",
                                       "",
                                       [],
                                       prop)
    self.assertEqual(_pn.setListener(cinfo,OpenRTM_aist.ConnectorListeners()),
                     OpenRTM_aist.DataPortStatus.PORT_OK)
    prop = OpenRTM_aist.Properties()
    prop.setProperty("publisher.push_policy","fifo")
    prop.setProperty("publisher.skip_count","0")
    prop.setProperty("thread_type","default")
    prop.setProperty("measurement.exec_time","enable")
    prop.setProperty("measurement.exec_count","0")
    prop.setProperty("measurement.period_time","enable")
    prop.setProperty("measurement.period_count","0")
    retcode = _pn.init(prop)
    cons = ConsumerMock()
    self.assertEqual(_pn.setConsumer(cons),OpenRTM_aist.DataPortStatus.PORT_OK)
    _pn.setBuffer(OpenRTM_aist.CdrRingBuffer())
    _pn.activate()

    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    _pn.deactivate()
    _pn.__del__()
    return


  def test_pushSkip(self):
    _pn = PublisherNew()
    prop = OpenRTM_aist.Properties()
    cinfo = OpenRTM_aist.ConnectorInfo("",
                                       "",
                                       [],
                                       prop)
    self.assertEqual(_pn.setListener(cinfo,OpenRTM_aist.ConnectorListeners()),
                     OpenRTM_aist.DataPortStatus.PORT_OK)
    prop = OpenRTM_aist.Properties()
    prop.setProperty("publisher.push_policy","skip")
    prop.setProperty("publisher.skip_count","0")
    prop.setProperty("thread_type","default")
    prop.setProperty("measurement.exec_time","enable")
    prop.setProperty("measurement.exec_count","0")
    prop.setProperty("measurement.period_time","enable")
    prop.setProperty("measurement.period_count","0")
    retcode = _pn.init(prop)
    cons = ConsumerMock()
    self.assertEqual(_pn.setConsumer(cons),OpenRTM_aist.DataPortStatus.PORT_OK)
    _pn.setBuffer(OpenRTM_aist.CdrRingBuffer())
    _pn.activate()

    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    _pn.deactivate()
    _pn.__del__()
    return

  def test_pushNew(self):
    _pn = PublisherNew()
    prop = OpenRTM_aist.Properties()
    cinfo = OpenRTM_aist.ConnectorInfo("",
                                       "",
                                       [],
                                       prop)
    self.assertEqual(_pn.setListener(cinfo,OpenRTM_aist.ConnectorListeners()),
                     OpenRTM_aist.DataPortStatus.PORT_OK)
    prop = OpenRTM_aist.Properties()
    prop.setProperty("publisher.push_policy","new")
    prop.setProperty("publisher.skip_count","0")
    prop.setProperty("thread_type","default")
    prop.setProperty("measurement.exec_time","enable")
    prop.setProperty("measurement.exec_count","0")
    prop.setProperty("measurement.period_time","enable")
    prop.setProperty("measurement.period_count","0")
    retcode = _pn.init(prop)
    cons = ConsumerMock()
    self.assertEqual(_pn.setConsumer(cons),OpenRTM_aist.DataPortStatus.PORT_OK)
    _pn.setBuffer(OpenRTM_aist.CdrRingBuffer())
    _pn.activate()

    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.write(123,0,0),OpenRTM_aist.DataPortStatus.PORT_OK)
    _pn.deactivate()
    _pn.__del__()
    return

  def test_convertReturn(self):
    _pn = PublisherNew()
    self.assertEqual(_pn.convertReturn(OpenRTM_aist.BufferStatus.BUFFER_OK,0),
         OpenRTM_aist.DataPortStatus.PORT_OK)
    self.assertEqual(_pn.convertReturn(OpenRTM_aist.BufferStatus.BUFFER_FULL,0),
         OpenRTM_aist.DataPortStatus.BUFFER_FULL)
    self.assertEqual(_pn.convertReturn(OpenRTM_aist.BufferStatus.TIMEOUT,0),
         OpenRTM_aist.DataPortStatus.BUFFER_TIMEOUT)
    self.assertEqual(_pn.convertReturn(OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET,0),
         OpenRTM_aist.DataPortStatus.PRECONDITION_NOT_MET)
    self.assertEqual(_pn.convertReturn(100,0),
         OpenRTM_aist.DataPortStatus.PORT_ERROR)
    _pn.__del__()
    return

############ test #################
if __name__ == '__main__':
  unittest.main()
