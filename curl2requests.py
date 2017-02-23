#!/usr/bin/env python3
#coding: utf-8


'''curl2convert.py
this file converts a CURL command to Requests parameters
Input:	a CURL command (string)
Output:	(url,headers,cookies) extracted from the input (tuple)
'''


def curl2requests(a):
	if len(a) <= 2:
		print('\033[1;31;47mYour CURL command is empty\033[0m')
		return(null)
	_list = a.strip().replace('--compressed','').split('-H')
	url = _list[0].split("'")[1]
	headers = {}
	cookie = {}
	for item in _list[1:]:
		if 'cookie' in item or 'Cookie' in item:
			full = item.split("'")[1].split(': ')[-1].split(";")
			for item in full:
				both = item.split("=")
				name = both[0].strip()
				value = both[1].strip()
				cookie[name] = value
		else:
			both = item.split("'")[1].split(":")
			name = both[0].strip()
			value = both[1].strip()
			headers[name] = value


	return(url,headers,cookie)

if __name__=='__main__':
	a = '''curl 'https://www.v2ex.com/' -H 'if-none-match: W/"8130a7070b4a02a9a5b92a53e6da2466b48ba84a"' -H 'dnt: 1' -H 'accept-encoding: gzip, deflate, sdch, br' -H 'accept-language: zh,en-US;q=0.8,en;q=0.6' -H 'upgrade-insecure-requests: 1' -H 'user-agent: useragentispersonalinformation' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'cache-control: max-age=0' -H 'authority: www.v2ex.com' -H 'cookie: PB3_SESSION="2|1:0|10:1487828049|11:PB3_SESSION|40:djJleDoxMDYuMTg2LjEyNS4yMzg6NTQwODA0ODI=|1f3ea6c983601a0fbea39d63765f310e404143c4020b538e8eaac7070991bca0"; V2EX_LANG=zhcn; _ga=GA1.2.1266705876.1487828051; _gat=1' --compressed'''
	for x in curl2requests(a):
		print(x)


