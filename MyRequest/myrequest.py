#!/usr/bin/python#
#-*- coding: UTF-8 -*-
#基础包：接口测试的封装װ

import requests
import json


def api_request(method, url, data, headers, param_type):
	try:
		if method == 'post' and param_type == 'json':
			results = requests.post(url = url, json = json.loads(data), headers = json.loads(headers))
		if method == 'post' and param_type == 'key-val':
			results = requests.post(url = url, data = data)
		if method == 'get':
			results = requests.get(url = url, params = data, headers = headers)
		response = results.text
		code = results.status_code
		ret = {}
		ret['code'] = code
		ret['response'] = json.loads(response.replace("'", '"'))
		if type(ret) == type({"1":"1"}):
			return ret
		else:
			return {}
	except Exception as e:
		print(e)