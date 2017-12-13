#!/usr/bin/python#
#-*- coding: UTF-8 -*-
import sys
import MyDB.mysql_db as mysql
import MyRequest.myrequest as myrequest 
import json
import unittest
from io import StringIO
#import HTMLTestRunner,sys

if __name__ == '__main__':
	db = mysql.DB()
	table_name = 'cap'
	real_sql = "select id from " + table_name 
	print(real_sql)
	data_cases = db.query(real_sql)
	db.close()
	for data_case in data_cases:
		real_sql = "select * from " + table_name + " where id = " + str(data_case['id'])
		db.__init__()
		data_test = db.query(real_sql)[0]
		db.close()
		method = data_test['method']
		url = data_test['url'] + ":" + str(data_test['port']) + data_test['inter_url']
		data = data_test['params']
		headers = data_test['headers']
		param_type = data_test['param_type']
		actual = myrequest.api_request(method = method, url = url, data = data, headers = headers, param_type = param_type)
		expect = json.loads(data_test['assert'])
		print(data_case['id'])
		if actual:
			print('url: %s' %(url))
			print('param: %s' %(data.replace("\r\n","")))
			print('response: %s' %(actual['response']))
			if actual['code'] == expect['code']:
				if data_test['case_type']:
					if actual['response']['error'] == expect['error']:
						print('success')
					else:
						print('failed')
				else:
					if actual['response']['error'] != expect['error']:
						print('success')
					else:
						print('failed')
			else:
				print('failed')
		print("")
	#db.close()