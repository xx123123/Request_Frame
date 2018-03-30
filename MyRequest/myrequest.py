#!/usr/bin/python#
#-*- coding: UTF-8 -*-
#基础包：接口测试的封装װ

import requests
import json
import time

module1 = 'module1'

def api_request(method, url, data, headers, param_type):
	try:
		startTime = time.time()
		if method == 'post' and param_type == 'json':
			results = requests.post(url = url, json = json.loads(data), headers = json.loads(headers), timeout = 10)
		if method == 'post' and param_type == 'form':
			results = requests.post(url = url, data = data, timeout = 10)
		if method == 'get':
			results = requests.get(url = url, params = data, headers = headers, timeout = 10)
		response = results.text.replace('false', 'False').replace('null', 'None').replace('true', 'True')
		print(results.status_code)
		#print(response)
		#print(json.dumps(eval(response)))
		#print(results.elapsed.microseconds/1000)
		#print((time.time() - startTime) * 1000)
		#print(len(response))
		if results.status_code == 200:
			status = results.status_code
			ret = {}
			ret['status'] = status
			ret['response'] = (eval(response))
			ret['time'] = int(results.elapsed.microseconds/1000)
			ret['len'] = len(response)
			if type(ret) == type({}):
				return ret
		else:
			return results.status_code
	except Exception as e:
		print(e)