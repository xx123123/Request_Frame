#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import MyDB.mysql_db as mysql
import MyRequest.myrequest as myrequest 
import json
import unittest
from io import StringIO
import HTMLTestRunner,sys



class FramedTestCase(unittest.TestCase):
	def __init__(self, methodName='runTest', param=None, actualCode=None, expectCode=None, info=None):
		super(FramedTestCase, self).__init__(methodName)
		self.param = param
		self.actualCode = actualCode
		self.expectCode = expectCode
		self.info		= info
	@staticmethod
	def Frame(testcase_klass, param=None, actualCode=None, expectCode=None, info=None):
		testloader 	= unittest.TestLoader()
		testnames	= testloader.getTestCaseNames(testcase_klass)
		suite 		= unittest.TestSuite()
		method = param['method']
		url = param['url'] + ":" + str(param['port']) + param['inter_url']
		data = param['params']
		headers = param['headers']
		param_type = param['param_type']
		actual = myrequest.api_request(method = method, url = url, data = data, headers = headers, param_type = param_type)
		expect = json.loads(param['assert'])
		info = param['remark']
		suite.addTest(testcase_klass(testnames[0], param = param, actualCode = actual, expectCode = expect, info = info))
		return suite
	
	def setUp(self):
		print ('setUp')
		
		pass

	def tearDown(self):
		print ('tearDown')
		#excel.release(path)
		pass
	

class TestOne(FramedTestCase):
	def test_Frame(self):
		print('TestOne')
		print ('except-->' + str(self.actualCode['response']))
		if self.param['case_type'] == 1:
			self.assertEqual(self.actualCode['code'], self.expectCode['code'], str(self.info))
			self.assertEqual(self.actualCode['response']['error'], self.expectCode['error'], str(self.info))
		else:
			self.assertEqual(self.actualCode['code'], self.expectCode['code'], str(self.info))
			self.assertNotEqual(self.actualCode['response']['error'], self.expectCode['error'], str(self.info))

#添加Suite

def Suite():
	suiteTest = unittest.TestSuite()
	global db
	db = mysql.DB()
	#global table_name
	table_name = 'cap'
	real_sql = "select id from " + table_name + " where id < 10"
	print(real_sql)
	data_cases = db.query(real_sql)
	db.close()
	for data_case in data_cases:
		db.__init__()
		data_test = db.query('select * from %s where id = %s' %(table_name, data_case['id']))[0]
		db.close()
		suiteTest.addTest(FramedTestCase.Frame(TestOne, param=data_test))
	#excel.release(path)
	return suiteTest

if __name__ == '__main__':
    #确定生成报告的路径
    filePath = "pyResult.html"
    fp = open(filePath,'wb')

    #生成报告的Title,描述
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='Python Test Report',description='This  is Python  Report')
    runner.run(Suite())