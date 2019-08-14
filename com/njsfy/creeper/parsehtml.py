#!/usr/bin/python
# coding: UTF-8
'''
Created on 2018年1月4日
解析当前网页
@author: shun
'''
from pyquery import PyQuery as pq

class ParseHTML:
    '''
             初始化时传入解析网页内容              
    '''


    def __init__(self, content):
        '''
        Constructor
        '''
        self.d = pq(content)
    
    '''
    html: 网页内容
    class_name: 节点中对应类名称
    subject: 节点名称
    '''     
    def getNode(self, html, class_name, subject = None):
        node = pq(html) 
        if subject is None:
            return node(class_name)
        else:
            return node(class_name).find(subject).eq(0)
            
        
    '''
    name: 网页中的类名称或者节点类型
    '''
    def getNodeHtml(self, name):
        return self.d(name)    

    
    def getSingleInfo(self, html, name):
        node = pq(html)
        return node(name)
    
    def getAttrValue(self, content, name, attr):
        node = pq(content)
        return node(name).attr(attr)        
        
    
    