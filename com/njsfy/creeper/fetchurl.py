#!/usr/bin/python
# coding: UTF-8
'''
Created on 2018年1月4日
获取给定网页内容

@author: shun
'''

import requests


class FecthUrl:    

    def __init__(self, url):
        '''
        Constructor url为给定网址
        '''
        self.url = url
        
    '''
    get方法获取网页内容
    '''    
    def get(self, params=None, headers = None):
        if params is None:
            if headers is None:
                content = requests.get(self.url)
            else:
                content = requests.get(self.url, headers = headers)
            
        else:
            if headers is None:
                content = requests.get(self.url, params = params) 
            else:
                content = requests.get(self.url, params = params, headers = headers)
                   
        
        return content.text
        
    '''
    post方法获取网页内容
    '''
    def post(self, params = None, headers = None):
        if params is None:
            if headers is None:
                return requests.post(self.url)
            else:
                return requests.post(self.url, headers = headers)
        else:
            if headers is None:
                return requests.post(self.url, params = params)
            else:
                return requests.post(self.url, params = params, headers = headers)
        
        