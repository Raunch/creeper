'''
Created on 2018年1月5日

@author: shun
'''

class SubjectInfo:
    '''
    classdocs
    '''


    def __init__(self, subname):
        '''
        Constructor
        '''
        self.subject_name = subname
        self.urls = []
    
    #获取当前条目的标题，可用来做文件存储名称    
    def getSubject(self):
        return self.subject_name
    
    #获取当前条目中各个题型
    def getUrls(self):
        return self.urls
    
    #增加一个题型
    def addUrl(self, url):
        self.urls.append(url)