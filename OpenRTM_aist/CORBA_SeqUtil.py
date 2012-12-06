#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
#  @file CORBA_SeqUtil.py
#  @brief CORBA sequence utility template functions
#  @date $Date: 2007/09/03 $
#  @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
#  Copyright (C) 2006-2008
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.

import OpenRTM_aist

##
# @if jp
# 
# @brief CORBA sequence ���Ф��� functor ��Ŭ�Ѥ���
# 
# CORBA sequence ���Ƥ����Ǥ��Ф��ơ�Ϳ����줿 functor ��Ŭ�Ѥ��롣
# functor �� void functor(CORBA sequence ������) �η�����Ȥ�ɬ�פ����롣
# 
# @param seq Functor ��Ŭ�Ѥ��� CORBA sequence
# @param f CORBA sequence �����Ǥ�������� Functor
# 
# @return ���Ƥ����Ǥ�������� Functor
# 
# @since 0.4.0
# 
# @else
# 
# @brief Apply the functor to all CORBA sequence elements
# 
# Apply the given functor to the given CORBA sequence.
# functor should be void functor(CORBA sequence element).
# 
# @param seq CORBA sequence to be applied the functor
# @param functor A functor to process CORBA sequence elements
# 
# @return Functor that processed all CORBA sequence elements
# 
# @endif
def for_each(seq, f):
  len_ = len(seq)
  for i in range(len_):
    f(seq[i])
  return f


##
# @if jp
# @brief CORBA sequence ���椫�� functor ��Ŭ�礹�����ǤΥ���ǥå������֤�
# 
# CORBA sequence ���Ƥ����Ǥ��Ф��ơ�Ϳ����줿 functor ��Ŭ�Ѥ���
# functor �� true ���֤��褦���Υ���ǥå������֤���
# functor �� bool functor(const CORBA sequence ������) �η�����Ȥꡢ
# Ŭ�礹�����Ǥ��Ф��� true ���֤�ɬ�פ����롣
# 
# @param seq Functor ��Ŭ�Ѥ��� CORBA sequence
# @param f CORBA sequence �������Ǥ򸫤Ĥ��� Functor
# 
# @return Functor ��Ŭ�礹�����ǤΥ���ǥå��������Ĥ���ʤ��Ȥ��� -1 ���֤���
# 
# @else
# 
# @brief Return the index of CORBA sequence element that functor matches 
# 
# This operation applies the given functor to the given CORBA sequence,
# and returns the index of the sequence element that the functor matches.
# The functor should be bool functor(const CORBA sequence element) type,
# and it would return true, if the element matched the functor.
# 
# @param seq CORBA sequence to be applied the functor
# @param functor A functor to process CORBA sequence elements
# 
# @return The index of the element that functor matches.
#          If no element found, it would return -1.
# 
# @endif
def find(seq, f):
  len_ = len(seq)
  for i in range(len_):
    if f(seq[i]):
      return i
  return -1


##
# @if jp
# @brief CORBA sequence �κǸ�����Ǥ��ɲä���
# 
# CORBA sequence �κǸ��Ϳ����줿���Ǥ��ɲä��롣
# CORBA sequence ��Ĺ���ϼ�ưŪ�˳�ĥ����롣
# 
# @param seq ���Ǥ��ɲä��� CORBA sequence
# @param elem �ɲä�������
# 
# @else
# 
# @brief Push the new element back to the CORBA sequence
# 
# Add the given element to the last of CORBA sequence.
# The length of the CORBA sequence will be expanded automatically.
# 
# @param seq CORBA sequence to be added a new element
# @param elem The new element to be added to the CORBA sequence
# 
# @endif
def push_back(seq, elem):
  seq.append(elem)


##
# @if jp
# @brief CORBA sequence ��ޡ�������
# 
# Ϳ����줿 CORBA sequence ��ޡ������롣
# 
# @param seq1 �ޡ�������� CORBA sequence
# @param seq2 �ޡ�������� CORBA sequence
# 
# @else
# 
# @endif
def push_back_list(seq1, seq2):
  for elem in seq2:
    seq1.append(elem)


##
# @if jp
# @brief CORBA sequence �����Ǥ���������
# 
# CORBA sequence �� index �ΰ��֤����Ǥ�ä��롣
# index �� Ϳ����줿��CORBA sequence �κ���� index ����礭�����
# �Ǹ�����ǤȤ��Ʋä����롣
# CORBA sequence ��Ĺ���ϼ�ưŪ�˳�ĥ����롣
# 
# @param seq ���Ǥ��ɲä��� CORBA sequence
# @param elem �ɲä�������
# @param index ���Ǥ��ɲä������
# 
# @else
# 
# @brief Insert the element to the CORBA sequence
# 
# Insert a new element in the given position to the CORBA sequence.
# If the given index is greater than the length of the sequence,
# the given element is pushed back to the last of the sequence.
# The length of the CORBA sequence will be expanded automatically.
# 
# @param seq The CORBA sequence to be inserted a new element
# @param elem The new element to be inserted the sequence
# @param index The inserting position
# 
# @endif
def insert(seq, elem, index):
  len_ = len(seq)
  if index > len:
    seq.append(elem)
    return
  seq.insert(index, elem)


##
# @if jp
# @brief CORBA sequence ����Ƭ���Ǥ��������
# 
# CORBA sequence ����Ƭ���Ǥ�������롣
# seq[0] ��Ʊ����
# 
# @param seq ���Ǥ�������� CORBA sequence
# 
# @return ������������
# 
# @else
# 
# @brief Get the front element of the CORBA sequence
# 
# This operation returns seq[0].
# 
# @param seq The CORBA sequence to be get the element
# 
# @endif
def front(seq):
  return seq[0]


##
# @if jp
# @brief CORBA sequence ���������Ǥ��������
# 
# CORBA sequence ���������Ǥ�������롣
# seq[seq.length() - 1] ��Ʊ����
# 
# @param seq ���Ǥ�������� CORBA sequence
# 
# @return ������������
# 
# @else
# 
# @brief Get the last element of the CORBA sequence
# 
# This operation returns seq[seq.length() - 1].
# 
# @param seq The CORBA sequence to be get the element
# 
# @endif
def back(seq):
  if len(seq) > 0:
    return seq[-1]


##
# @if jp
# @brief CORBA sequence �λ��ꤵ�줿���֤����Ǥ�������
# 
# ���ꤵ�줿����ǥå��������Ǥ������롣
# ������줿���Ǥϵͤ��졢sequence ��Ĺ����1���롣
# 
# @param seq ���Ǥ������� CORBA sequence
# @param index ����������ǤΥ���ǥå���
# 
# @else
# 
# @brief Erase the element of the specified index
# 
# This operation removes the element of the given index.
# The other elements are closed up around the hole.
# 
# @param seq The CORBA sequence to be get the element
# @param index The index of the element to be removed
# 
# @endif
def erase(seq, index):
  if index > len(seq):
    return

  del seq[index]

##
# @if jp
# 
# @brief �������󥹤����Ǥ�Ҹ�ˤ������äƺ������
# 
# ���Υ��ڥ졼�����ϽҸ�Ȥ���Ϳ����줿�ؿ����֥������Ȥ�
# ��郎���ΤȤ������Υ������󥹤����Ǥ������롣
# 
# @param seq ���Ǹ����оݤ� CORBA sequence
# @param f ������륷�����󥹤���ꤹ��Ѹ�
# 
# @else
# 
# @endif
def erase_if(seq, f):
  index = find(seq, f)
  if index < 0:
    return
  del seq[index]


##
# @if jp
# @brief CORBA sequence �������Ǥ���
# 
# CORBA sequence �������Ǥ������롣
# seq.length(0) ��Ʊ����
# 
# @else
# 
# @brief Erase all the elements of the CORBA sequence
# 
# same as seq.length(0).
# 
# @endif
def clear(seq):
  del seq[0:]


## coil::vstring refToVstring(const CorbaRefSequence& objlist)
def refToVstring(objlist):
  iorlist = []
  orb = OpenRTM_aist.Manager.instance().getORB()
  
  for obj in objlist:
    iorlist.append(orb.object_to_string(obj))

  return iorlist

