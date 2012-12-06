#!/usr/bin/env python
# -*- coding: euc-jp -*-

#
# \file test_GlobalFactory.py
# \brief test for RTComponent factory class
# \date $Date: $
# \author Shinji Kurihara
#
# Copyright (C) 2003-2005
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

import sys
sys.path.insert(1,"../")

import OpenRTM_aist
import unittest

from GlobalFactory import *

class Test:
	def __init__(self):
		pass

	def test(self):
		return True

class TestGlobalFactory(unittest.TestCase):

	def setUp(self):
		self.factory = GlobalFactory.instance()
		self.factory.addFactory("test",Test,OpenRTM_aist.Delete)
		return

	def tearDown(self):
		self.factory.removeFactory("test")
		return

	def test_isinstance(self):
		self.assertEqual(self.factory,GlobalFactory.instance())

	def test_hasFactory(self):
		# addFactory�ˤ���Ͽ�����ե����ȥꥪ�֥������Ȥ��䤤��碌��
		self.assertEqual(self.factory.hasFactory("test"),True)
		# addFactory�ˤ���Ͽ���Ƥ��ʤ��ե����ȥꥪ�֥������Ȥ��䤤��碌��
		self.assertEqual(self.factory.hasFactory("testtest"),False)
		# addFactory�ˤ���Ͽ���Ƥ��ʤ��ե����ȥꥪ�֥������Ȥ��䤤��碌(��ʸ��)��
		self.assertEqual(self.factory.hasFactory(""),False)
		return

	def test_getIdentifiers(self):
		# �ե����ȥ꤬��Ͽ�Ѥߤξ����䤤��碌��
		self.assertEqual(self.factory.getIdentifiers(),["test"])
		GlobalFactory.instance().addFactory("test2",Test,OpenRTM_aist.Delete)
		self.assertEqual(self.factory.getIdentifiers(),["test","test2"])
		# �ե����ȥ꤬��Ͽ����Ƥ��ʤ������䤤��碌��
		self.factory.removeFactory("test")
		self.factory.removeFactory("test2")
		self.assertEqual(self.factory.getIdentifiers(),[])
		return
	
	def test_addFactory(self):
		# creator����ꤷ�ʤ���硢INVALID_ARG���֤���뤫?
		self.assertEqual(GlobalFactory.instance().addFactory("test",None,OpenRTM_aist.Delete),
				 GlobalFactory.INVALID_ARG)

		# ������Ͽ�Ѥߤ�ID�ˤ�addFactory()�򥳡��뤷����硢ALREADY_EXISTS���֤���뤫?
		self.assertEqual(GlobalFactory.instance().addFactory("test",Test,OpenRTM_aist.Delete),
				 GlobalFactory.ALREADY_EXISTS)

		# id��creator����ꤷ��addFactory()�򥳡��뤷����硢FACTORY_OK���֤���뤫?
		self.assertEqual(GlobalFactory.instance().addFactory("test1",Test,OpenRTM_aist.Delete),
				 GlobalFactory.FACTORY_OK)
		self.factory.removeFactory("test1")


		return

	def test_removeFactory(self):
		# ��Ͽ���Ƥ��ʤ�ID�ǥ����뤷����硢NOT_FOUND���֤���뤫?
		self.assertEqual(self.factory.removeFactory("testtest"),
				 GlobalFactory.NOT_FOUND)
				 
		# ��Ͽ�Ѥߤ�ID�ǥ����뤷����硢FACTORY_OK���֤���뤫?
		self.assertEqual(self.factory.removeFactory("test"),
				 GlobalFactory.FACTORY_OK)

		# �ե����ȥ꤬������������줿��?
		self.assertEqual(self.factory.getIdentifiers(),[])
		return

	def test_createObject(self):
		# ��Ͽ���Ƥ��ʤ�ID�ǥ����뤷����硢None���֤���뤫?
		self.assertEqual(self.factory.createObject("testtest"),
				 None)
		# ��Ͽ�Ѥߤ�ID�ǥ����뤷����硢���������֥������Ȥ��֤���뤫?
		self.assertEqual(self.factory.createObject("test").test(),True)
		return

	def test_deleteObject(self):
		# ��Ͽ���Ƥ��ʤ�ID�ǥ����뤷�����
		self.factory.deleteObject(self.factory.createObject("test"),"testtest")
		# ID����ꤷ�ʤ��ǥ����뤷�����
		self.factory.deleteObject(self.factory.createObject("test"))
		return

############### test #################
if __name__ == '__main__':
        unittest.main()
