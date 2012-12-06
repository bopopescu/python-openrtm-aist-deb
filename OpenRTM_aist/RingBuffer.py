#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file RingBuffer.py
# @brief Defautl Buffer class
# @date $Date: 2007/09/12 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import threading
import OpenRTM_aist


##
# @if jp
# @class RingBuffer
# @brief ��󥰥Хåե��������饹
# 
# ���ꤷ��Ĺ���Υ�󥰾��Хåե�����ĥХåե��������饹��
# �Хåե����Τ˥ǡ�������Ǽ���줿��硢�ʹߤΥǡ����ϸŤ��ǡ�������
# �缡��񤭤���롣
# ���äơ��Хåե���ˤ�ľ��ΥХåե�Ĺʬ�Υǡ����Τ��ݻ�����롣
#
# ��)���ߤμ����Ǥϡ����ֺǸ�˳�Ǽ�����ǡ����ΤߥХåե������ɤ߽Ф���ǽ
#
# @param DataType �Хåե��˳�Ǽ����ǡ�����
#
# @since 0.4.0
#
# @else
#
# @endif
class RingBuffer(OpenRTM_aist.BufferBase):
  """
  """

  RINGBUFFER_DEFAULT_LENGTH = 8

  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  # 
  # ���󥹥ȥ饯��
  # ���ꤵ�줿�Хåե�Ĺ�ǥХåե����������롣
  #
  # @param length �Хåե�Ĺ
  # 
  # @else
  #
  # @brief Constructor
  # 
  # Constructor.
  # Initialize the buffer by specified buffer length.
  # However, if the specified length is less than two, the buffer should
  # be initialized by two in length.
  #
  # @param length Buffer length
  # 
  # @endif
  #
  # @endif
  def __init__(self, length=RINGBUFFER_DEFAULT_LENGTH):
    self._overwrite = True
    self._readback = True
    self._timedwrite = False
    self._timedread  = False
    self._wtimeout = OpenRTM_aist.TimeValue(1,0)
    self._rtimeout = OpenRTM_aist.TimeValue(1,0)
    self._length   = length
    self._wpos = 0
    self._rpos = 0
    self._fillcount = 0
    self._wcount = 0
    self._buffer = [None for i in range(self._length)]
    self._pos_mutex = threading.RLock()
    self._full_mutex = threading.RLock()
    self._empty_mutex = threading.RLock()
    self._full_cond = threading.Condition(self._full_mutex)
    self._empty_cond = threading.Condition(self._empty_mutex)


    self.reset()


  ##
  # @if jp
  # @brief �Хåե�������
  #
  # Properties ��Ϳ������ץ�ѥƥ��ˤ�ꡢ
  # �Хåե���������������롣
  # ���ѤǤ��륪�ץ����Ȱ�̣�ϰʲ����̤�
  #
  # - buffer.length:
  #     �Хåե���Ĺ�����������ʳ��ο��ͤ����ꤵ��Ƥ�̵�뤵��롣��
  #     �Ǥ˥Хåե������Ѿ��֤Ǥ⡢Ĺ���������ꤵ�줿�Τ������٤Ƥ�
  #     �ݥ��󥿤����������롣
  #
  # - buffer.write.full_policy:
  #     ��񤭤��뤫�ɤ����Υݥꥷ����
  #     overwrite (���), do_nothing (���⤷�ʤ�), block (�֥�å�����)
  #     block ����ꤷ����硢���� timeout �ͤ���ꤹ��С�������ָ�
  #     �񤭹����Բ�ǽ�Ǥ���Х����ॢ���Ȥ��롣
  #     �ǥե���Ȥ�  overwrite (���)��
  #
  # - buffer.write.timeout:
  #     �����ॢ���Ȼ��֤� [sec] �ǻ��ꤹ�롣�ǥե���Ȥ� 1.0 [sec]��
  #     1 sec -> 1.0, 1 ms -> 0.001, �����ॢ���Ȥ��ʤ� -> 0.0
  #
  # - buffer.read.empty_policy:
  #     �Хåե������ΤȤ����ɤ߽Ф��ݥꥷ����
  #     readback (�Ǹ������), do_nothing (���⤷�ʤ�), block (�֥�å�����)
  #     block ����ꤷ����硢���� timeout �ͤ���ꤹ��С�������ָ�
  #     �ɤ߽Ф��Բ�ǽ�Ǥ���Х����ॢ���Ȥ��롣
  #     �ǥե���Ȥ� readback (�Ǹ������)��
  #
  # - buffer.read.timeout:
  #     �����ॢ���Ȼ��� [sec] �ǻ��ꤹ�롣�ǥե���Ȥ� 1.0 [sec]��
  #     1sec -> 1.0, 1ms -> 0.001, �����ॢ���Ȥ��ʤ� -> 0.0
  #
  # @else
  #
  # @endif
  #
  # void init(const coil::Properties& prop)
  def init(self, prop):
    self.__initLength(prop)
    self.__initWritePolicy(prop)
    self.__initReadPolicy(prop)


  ##
  # @if jp
  #
  # @brief �Хåե�Ĺ���������
  # 
  # �Хåե�Ĺ��������롣
  #
  # @param self
  # 
  # @return �Хåե�Ĺ
  # 
  # @else
  #
  # @brief Get the buffer length
  #
  # @endif
  #
  # size_t length(void) const
  def length(self, n = None):
    if n is None:
      guard = OpenRTM_aist.ScopedLock(self._pos_mutex)
      return self._length

    if n < 1:
      return OpenRTM_aist.BufferStatus.NOT_SUPPORTED

    self._buffer = [None for i in range(n)]
    self._length = n
    self.reset()
    return OpenRTM_aist.BufferStatus.BUFFER_OK

  
  ##
  # @if jp
  #
  # @brief �Хåե��ξ��֤�ꥻ�åȤ���
  # 
  # �Хåե����ɤ߽Ф��ݥ��󥿤Ƚ񤭹��ߥݥ��󥿤ΰ��֤�ꥻ�åȤ��롣
  # ���μ����Ǥ� BUFFER_OK �����֤��ʤ���
  # 
  # @return BUFFER_OK: ���ｪλ
  #         NOT_SUPPORTED: �ꥻ�å��Բ�ǽ
  #         BUFFER_ERROR: �۾ｪλ
  # 
  # @else
  #
  # @brief Get the buffer length
  #
  # Pure virtual function to get the buffer length.
  #
  # @return buffer length
  # 
  # @endif
  # 
  # ReturnCode reset()
  def reset(self):
    guard = OpenRTM_aist.ScopedLock(self._pos_mutex)
    self._fillcount = 0
    self._wcount = 0
    self._wpos = 0
    self._rpos = 0
    return OpenRTM_aist.BufferStatus.BUFFER_OK


  ##
  # @if jp
  #
  # @brief �Хåե��θ��ߤν�������ǤΥݥ���
  # 
  # �Хåե��θ��ߤν�������ǤΥݥ��󥿤ޤ��ϡ�n����Υݥ��󥿤��֤�
  # 
  # @param  n ����ߥݥ��� + n �ΰ��֤Υݥ��� 
  # @return ����߰��֤Υݥ���
  # 
  # @else
  #
  # @brief Get the buffer length
  #
  # Pure virtual function to get the buffer length.
  #
  # @return buffer length
  # 
  # @endif
  # 
  # DataType* wptr(long int n = 0) 
  def wptr(self, n = 0):
    guard = OpenRTM_aist.ScopedLock(self._pos_mutex)
    return self._buffer[(self._wpos + n + self._length) % self._length]

    
  ##
  # @if jp
  #
  # @brief ����ߥݥ��󥿤�ʤ��
  # 
  # ���ߤν񤭹��߰��֤Υݥ��󥿤� n �Ŀʤ�롣
  # �񤭹��߲�ǽ�����ǿ��ʾ�ο��ͤ���ꤷ����硢PRECONDITION_NOT_MET
  # ���֤���
  # 
  # @param  n ����ߥݥ��� + n �ΰ��֤Υݥ��� 
  # @return BUFFER_OK:            ���ｪλ
  #         PRECONDITION_NOT_MET: n > writable()
  # 
  # @else
  #
  # @brief Get the buffer length
  #
  # Pure virtual function to get the buffer length.
  #
  # @return buffer length
  # 
  # @endif
  # 
  # ReturnCode advanceWptr(long int n = 1)
  def advanceWptr(self, n = 1):
    # n > 0 :
    #     n satisfies n <= writable elements
    #                 n <= m_length - m_fillcout
    # n < 0 : -n = n'
    #     n satisfies n'<= readable elements
    #                 n'<= m_fillcount
    #                 n >= - m_fillcount
    guard = OpenRTM_aist.ScopedLock(self._pos_mutex)
    if (n > 0 and n > (self._length - self._fillcount)) or \
          (n < 0 and n < (-self._fillcount)):
      return OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET

    self._wpos = (self._wpos + n + self._length) % self._length
    self._fillcount += n
    return OpenRTM_aist.BufferStatus.BUFFER_OK


  ##
  # @if jp
  #
  # @brief �Хåե��˥ǡ�����񤭹���
  # 
  # �Хåե��˥ǡ�����񤭹��ࡣ�񤭹��ߥݥ��󥿤ΰ��֤��ѹ�����ʤ���
  # ���μ����ǤϾ�� BUFFER_OK ���֤���
  # 
  # @param value �񤭹����оݥǡ���
  #
  # @return BUFFER_OK: ���ｪλ
  #         BUFFER_ERROR: �۾ｪλ
  # 
  # @else
  #
  # @brief Write data into the buffer
  #
  # Pure virtual function to write data into the buffer.

  #
  # @param value Target data to write.
  #
  # @return BUFFER_OK:    Successful
  #         BUFFER_ERROR: Failed
  #
  # @endif
  #
  # ReturnCode put(const DataType& value)
  def put(self, value):
    guard = OpenRTM_aist.ScopedLock(self._pos_mutex)
    self._buffer[self._wpos] = value
    return OpenRTM_aist.BufferStatus.BUFFER_OK
    
  ##
  # @if jp
  #
  # @brief �Хåե��˽񤭹���
  # 
  # ������Ϳ����줿�ǡ�����Хåե��˽񤭹��ࡣ
  #
  # ��2����(sec)����3����(nsec)�����ꤵ��Ƥ��ʤ���硢�Хåե��ե�
  # ���ν���ߥ⡼�� (overwrite, do_nothing, block) �� init() ������
  # ���줿�⡼�ɤ˽�����
  #
  # ��2����(sec) �˰��������ꤵ�줿���ϡ�init() �����ꤵ�줿�⡼��
  # �˴ؤ�餺��block �⡼�ɤȤʤꡢ�Хåե����ե���֤Ǥ���л����
  # �֤ޤ��������ॢ���Ȥ��롣��3����(nsec)�ϻ��ꤵ��ʤ����0�Ȥ���
  # �����롣�����ॢ�����Ԥ���ˡ��ɤ߽Ф�����å�¦�ǥХåե�����
  # �ɤ߽Ф��С��֥�å��󥰤ϲ������ǡ������񤭹��ޤ�롣
  #
  # �񤭹��߻��˥Хåե�����(empty)���֤ǡ��̤Υ���åɤ�block�⡼��
  # ���ɤ߽Ф��Ԥ��򤷤Ƥ����硢signal��ȯ�Ԥ����ɤ߽Ф�¦�Υ֥��
  # ���󥰤��������롣
  # 
  # @param value �񤭹����оݥǡ���
  # @param sec   �����ॢ���Ȼ��� sec  (default -1: ̵��)
  # @param nsec  �����ॢ���Ȼ��� nsec (default 0)
  # @return BUFFER_OK            ���ｪλ
  #         BUFFER_FULL          �Хåե����ե����
  #         TIMEOUT              ����ߤ������ॢ���Ȥ���
  #         PRECONDITION_NOT_MET ����۾�
  # 
  # @else
  #
  # @brief Write data into the buffer
  # 
  # Write data which is given argument into the buffer.
  #
  # @param value Target data for writing
  #
  # @return Writing result (Always true: writing success is returned)
  # 
  # @endif
  # 
  # ReturnCode write(const DataType& value,
  #                  long int sec = -1, long int nsec = 0)
  def write(self, value, sec = -1, nsec = 0):
    try:
      self._full_cond.acquire()
      if self.full():
        timedwrite = self._timedwrite # default is False
        overwrite  = self._overwrite  # default is True

        if not (sec < 0): # if second arg is set -> block mode
          timedwrite = True
          overwrite  = False

        if overwrite and not timedwrite:       # "overwrite" mode
          self.advanceRptr()

        elif not overwrite and not timedwrite: # "do_nothiong" mode
          self._full_cond.release()
          return OpenRTM_aist.BufferStatus.BUFFER_FULL

        elif not overwrite and timedwrite:     # "block" mode

          if sec < 0:
            sec = self._wtimeout.sec()
            nsec = self._wtimeout.usec() * 1000

          # true: signaled, false: timeout
          if not self._full_cond.wait(sec + (nsec/1000000000.0)):
            self._full_cond.release()
            return OpenRTM_aist.BufferStatus.TIMEOUT

        else: # unknown condition
          self._full_cond.release()
          return OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET
      
      self._full_cond.release()

      self.put(value)
      
      self._empty_cond.acquire()
      empty = self.empty()
      if empty:
        self.advanceWptr(1)
        self._empty_cond.notify()
      else:
        self.advanceWptr(1)
      self._empty_cond.release()

      return OpenRTM_aist.BufferStatus.BUFFER_OK
    except:
      return OpenRTM_aist.BufferStatus.BUFFER_OK

    
  ##
  # @if jp
  #
  # @brief �Хåե��˽���߲�ǽ�����ǿ�
  # 
  # �Хåե��˽���߲�ǽ�����ǿ����֤���
  # 
  # @return �񤭹��߲�ǽ�����ǿ�
  # 
  # @else
  #
  # @brief Write data into the buffer
  #
  # Pure virtual function to write data into the buffer.
  #
  # @param value Target data to write.
  #
  # @return Result of having written in data (true:Successful, false:Failed)
  #
  # @endif
  #
  # size_t writable() const
  def writable(self):
    guard = OpenRTM_aist.ScopedLock(self._pos_mutex)
    return self._length - self._fillcount
    

  ##
  # @if jp
  #
  # @brief �Хåե�full�����å�
  # 
  # �Хåե�full�����å��ѽ�貾�۴ؿ�
  #
  # @return full�����å����(true:�Хåե�full��false:�Хåե���������)
  # 
  # @else
  #
  # @brief Check on whether the buffer is full.
  #
  # Pure virtual function to check on whether the buffer is full.
  #
  # @return True if the buffer is full, else false.
  #
  # @endif
  #
  # bool full(void) const
  def full(self):
    guard = OpenRTM_aist.ScopedLock(self._pos_mutex)
    return self._length == self._fillcount
    

  ##
  # @if jp
  #
  # @brief �Хåե��θ��ߤ��ɤ߽Ф����ǤΥݥ���
  # 
  # �Хåե��θ��ߤ��ɤ߽Ф����ǤΥݥ��󥿤ޤ��ϡ�n����Υݥ��󥿤��֤�
  # 
  # @param  n �ɤ߽Ф��ݥ��� + n �ΰ��֤Υݥ��� 
  # @return �ɤ߽Ф����֤Υݥ���
  # 
  # @else
  #
  # @brief Get the buffer length
  #
  # Pure virtual function to get the buffer length.
  #
  # @return buffer length
  # 
  # @endif
  def rptr(self, n = 0):
    guard = OpenRTM_aist.ScopedLock(self._pos_mutex)
    return self._buffer[(self._rpos + n + self._length) % self._length]

    
  ##
  # @if jp
  #
  # @brief �ɤ߽Ф��ݥ��󥿤�ʤ��
  # 
  # ���ߤ��ɤ߽Ф����֤Υݥ��󥿤� n �Ŀʤ�롣
  # 
  # @param  n �ɤ߽Ф��ݥ��� + n �ΰ��֤Υݥ��� 
  # @return BUFFER_OK: ���ｪλ
  #         BUFFER_ERROR: �۾ｪλ
  # 
  # @else
  #
  # @brief Get the buffer length
  #
  # Pure virtual function to get the buffer length.
  #
  # @return buffer length
  # 
  # @endif
  # 
  # DataType* rptr(long int n = 0)
  def advanceRptr(self, n = 1):
    # n > 0 :
    #     n satisfies n <= readable elements
    #                 n <= m_fillcout 
    # n < 0 : -n = n'
    #     n satisfies n'<= m_length - m_fillcount
    #                 n >= m_fillcount - m_length
    guard = OpenRTM_aist.ScopedLock(self._pos_mutex)
    if (n > 0 and n > self._fillcount) or \
          (n < 0 and n < (self._fillcount - self._length)):
      return OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET

    self._rpos = (self._rpos + n + self._length) % self._length
    self._fillcount -= n
    return OpenRTM_aist.BufferStatus.BUFFER_OK


    
  ##
  # @if jp
  #
  # @brief �Хåե�����ǡ������ɤ߽Ф�
  # 
  # �Хåե�����ǡ������ɤߤ������ɤ߽Ф��ݥ��󥿤ΰ��֤��ѹ�����ʤ���
  # 
  # @param value �ɤ߽Ф��ǡ���
  #
  # @return BUFFER_OK: ���ｪλ
  #         BUFFER_ERROR: �۾ｪλ
  # 
  # @else
  #
  # @brief Write data into the buffer
  #
  # Pure virtual function to write data into the buffer.
  #
  # @param value Target data to write.
  #
  # @return Result of having written in data (true:Successful, false:Failed)
  #
  # @endif
  #
  # ReturnCode get(DataType& value)
  def get(self, value=None):
    guard = OpenRTM_aist.ScopedLock(self._pos_mutex)
    if value is None:
      return self._buffer[self._rpos]

    value[0] = self._buffer[self._rpos]
    return OpenRTM_aist.BufferStatus.BUFFER_OK
    
    
  ##
  # @if jp
  #
  # @brief �Хåե������ɤ߽Ф�
  # 
  # �Хåե��˳�Ǽ���줿�ǡ������ɤ߽Ф���
  #
  # ��2����(sec)����3����(nsec)�����ꤵ��Ƥ��ʤ���硢�Хåե�����
  # �֤Ǥ��ɤ߽Ф��⡼�� (readback, do_nothing, block) �� init() ����
  # �ꤵ�줿�⡼�ɤ˽�����
  #
  # ��2����(sec) �˰��������ꤵ�줿���ϡ�init() �����ꤵ�줿�⡼��
  # �˴ؤ�餺��block �⡼�ɤȤʤꡢ�Хåե��������֤Ǥ���л������
  # �Ԥ��������ॢ���Ȥ��롣��3����(nsec)�ϻ��ꤵ��ʤ����0�Ȥ��ư�
  # ���롣�����ॢ�����Ԥ���ˡ�����ߥ���å�¦�ǥХåե��ؽ����
  # ������С��֥�å��󥰤ϲ������ǡ������ɤߤ�����롣
  #
  # �ɤ߽Ф����˥Хåե�����(empty)���֤ǡ��̤Υ���åɤ�block�⡼��
  # �ǽ�����Ԥ��򤷤Ƥ����硢signal��ȯ�Ԥ��ƽ����¦�Υ֥�å���
  # �����������롣
  # 
  # @param value(list) �ɤ߽Ф��оݥǡ���
  # @param sec   �����ॢ���Ȼ��� sec  (default -1: ̵��)
  # @param nsec  �����ॢ���Ȼ��� nsec (default 0)
  # @return BUFFER_OK            ���ｪλ
  #         BUFFER_EMPTY         �Хåե����ե����
  #         TIMEOUT              ����ߤ������ॢ���Ȥ���
  #         PRECONDITION_NOT_MET ����۾�
  # 
  # @else
  #
  # @brief Readout data from the buffer
  # 
  # Readout data stored into the buffer.
  # 
  # @param value(list) Readout data
  #
  # @return Readout result (Always true: readout success is returned)
  # 
  # @endif
  #
  # ReturnCode read(DataType& value,
  #                 long int sec = -1, long int nsec = 0)
  def read(self, value, sec = -1, nsec = 0):
    self._empty_cond.acquire()
      
    if self.empty():
      timedread = self._timedread
      readback  = self._readback

      if not (sec < 0):  # if second arg is set -> block mode
        timedread = True
        readback  = False
        sec = self._rtimeout.sec()
        nsec = self._rtimeout.usec() * 1000

      if readback and  not timedread:      # "readback" mode
        if not self._wcount > 0:
          self._empty_cond.release()
          return OpenRTM_aist.BufferStatus.BUFFER_EMPTY
        self.advanceRptr(-1)

      elif not readback and not timedread: # "do_nothiong" mode
        self._empty_cond.release()
        return OpenRTM_aist.BufferStatus.BUFFER_EMPTY

      elif not readback and timedread:     # "block" mode
        if sec < 0:
          sec = self._rtimeout.sec()
          nsec = self._rtimeout.usec() * 1000
        #  true: signaled, false: timeout
        if not self._empty_cond.wait(sec + (nsec/1000000000.0)):
          self._empty_cond.release()
          return OpenRTM_aist.BufferStatus.TIMEOUT

      else:                              # unknown condition
        self._empty_cond.release()
        return OpenRTM_aist.BufferStatus.PRECONDITION_NOT_MET
      
    self._empty_cond.release()

    val = self.get()

    if len(value) > 0:
      value[0] = val
    else:
      value.append(val)

    self._full_cond.acquire()
    full_ = self.full()

    if full_:
      self.advanceRptr()
      self._full_cond.notify()
    else:
      self.advanceRptr()

    self._full_cond.release()


    return OpenRTM_aist.BufferStatus.BUFFER_OK

    
  ##
  # @if jp
  #
  # @brief �Хåե������ɤ߽Ф���ǽ�����ǿ�
  # 
  # �Хåե������ɤ߽Ф���ǽ�����ǿ����֤���
  # 
  # @return �ɤ߽Ф���ǽ�����ǿ�
  #
  # @return BUFFER_OK: ���ｪλ
  #         BUFFER_ERROR: �۾ｪλ
  # 
  # @else
  #
  # @brief Write data into the buffer
  #
  # Pure virtual function to write data into the buffer.
  #
  # @param value Target data to write.
  #
  # @return Result of having written in data (true:Successful, false:Failed)
  #
  # @endif
  #
  # size_t readable() const
  def readable(self):
    guard = OpenRTM_aist.ScopedLock(self._pos_mutex)
    return self._fillcount
    

  ##
  # @if jp
  #
  # @brief �Хåե�empty�����å�
  # 
  # �Хåե�empty�����å��ѽ�貾�۴ؿ�
  #
  # @return empty�����å����(true:�Хåե�empty��false:�Хåե��ǡ�������)
  # 
  # @else
  #
  # @brief Check on whether the buffer is empty.
  #
  # Pure virtual function to check on whether the buffer is empty.
  #
  # @return True if the buffer is empty, else false.
  #
  # @endif
  #
  # bool empty(void) const
  def empty(self):
    guard = OpenRTM_aist.ScopedLock(self._pos_mutex)
    return self._fillcount == 0

    
  ## void initLength(const coil::Properties& prop)
  def __initLength(self, prop):
    if prop.getProperty("length"):
      n = [0]
      if OpenRTM_aist.stringTo(n, prop.getProperty("length")):
        n = n[0]
        if n > 0:
          self.length(n)

    
  ## void initWritePolicy(const coil::Properties& prop)
  def __initWritePolicy(self, prop):
    policy = OpenRTM_aist.normalize([prop.getProperty("write.full_policy")])

    if policy == "overwrite":
      self._overwrite  = True
      self._timedwrite = False
    
    elif policy == "do_nothing":
      self._overwrite  = False
      self._timedwrite = False

    elif policy == "block":
      self._overwrite  = False
      self._timedwrite = True

      tm = [0.0]
      if OpenRTM_aist.stringTo(tm, prop.getProperty("write.timeout")):
        tm = tm[0]
        if not (tm < 0):
          self._wtimeout.set_time(tm)

    
  ## void initReadPolicy(const coil::Properties& prop)
  def __initReadPolicy(self, prop):
    policy = prop.getProperty("read.empty_policy")

    if policy == "readback":
      self._readback  = True
      self._timedread = False

    elif policy == "do_nothing":
      self._readback  = False
      self._timedread = False

    elif policy == "block":
      self._readback  = False
      self._timedread = True
      tm = [0.0]
      if OpenRTM_aist.stringTo(tm, prop.getProperty("read.timeout")):
        self._rtimeout.set_time(tm[0])
