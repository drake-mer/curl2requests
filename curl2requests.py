#!/usr/bin/env python3
#coding: utf-8
import sys
import json
import requests
'''curl2convert.py
this file converts a CURL command to Requests parameters
Input:    a CURL command (string)
Output:    (url,headers,cookies) extracted from the input (tuple)
'''

def build_cookies(item):
    cookies = item.replace('Cookie:','').strip('\'').strip().strip().split(';')
    cookys = {}
    for cookie in cookies:
        name, value = cookie.split('=', 1)
        cookys[name.strip()] = value.strip()
    return cookys


def curl2requests(cmd):
    if len(cmd) <= 2:
         print('\033[1;31;47mYour CURL command is empty\033[0m')
         return None
    cmd = cmd.replace('--compressed','').strip()
    cmd, post_data = cmd.split('--data-binary')

    list_headers = cmd.split(' -H ')
    _, url = list_headers[0].split()
    url = url.strip('\'')
    headers = {}
    for item in list_headers[1:]:
        if 'cookie' in item or 'Cookie' in item:
            cookies = build_cookies(item)
        else:
            header = item.strip().strip('\'')
            name, value = header.split(':', 1)
            headers[name.strip()] = value.strip()

    return (url,headers,cookies, eval(post_data))

if __name__=='__main__':
    a=open(sys.argv[1]).read()
    url, headers, cookies, post_data = curl2requests(a)
    # r = requests.post(url, headers=headers, cookies=cookies, data=post_data, verify=False)
    #print(headers)
    print(cookies)
