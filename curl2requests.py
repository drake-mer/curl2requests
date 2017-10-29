#!/usr/bin/env python3
#coding: utf-8
import sys
import json
import requests
from requests import Request

'''curl2convert.py
this file converts a CURL command to Requests parameters
Input:    a CURL command (string)
Output:    (url,headers,cookies) extracted from the input (tuple)
'''

import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

def build_cookies(item):
    cookies = item.replace('Cookie:','').strip().strip('\'').strip().split(';')
    cookys = {}
    for cookie in filter(None, cookies):
        try:
            name, value = cookie.split('=', 1)
        except:
            import ipdb; ipdb.set_trace()
        cookys[name.strip()] = value.strip()
    return cookys


def curl2requests(cmd):
    if len(cmd) <= 2:
         print('\033[1;31;47mYour CURL command is empty\033[0m')
         return None
    cmd = cmd.replace('--compressed','').strip()
    cmd, post_data = cmd.split('--data-binary')
    post_data = post_data.strip().strip('\'')
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
    null_val = {'null': None}
    return (url,headers,cookies, json.decoder.JSONDecoder().decode(post_data))

if __name__=='__main__':
    a=open(sys.argv[1]).read()
    url, headers, cookies, post_data = curl2requests(a)
    headers.update({'Accept': '*/*'})
    print(url)
    print(headers)
    print(cookies)
    print(post_data)

    r = requests.post(
        url, 
        headers=headers, 
        cookies=cookies, 
        json=post_data
    )
    if not r.ok:
        import ipdb; ipdb.set_trace()
        print('something went wrong')
    else:
        print(r.content)
