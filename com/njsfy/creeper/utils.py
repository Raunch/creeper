'''
Created on 2018年1月5日

@author: shun
'''
import os
from com.njsfy.creeper.savefile import SaveFile

def getQuestiontype(url):
    index = url.index("questionTypeId")
    return url[index + len("questionTypeId") + 1]

def generateFilePath(rootpath, path):
    parts = path.split('>')
    temp_path = rootpath    
    for i in range(len(parts)-1):
        part = parts[i].replace("/","_")        
        temp_path = os.path.join(temp_path, part)
    if not os.path.exists(temp_path):
        os.makedirs(temp_path) 
    last_name = parts[len(parts)-1].replace("/", "_")
    real_path = os.path.join(temp_path, last_name + ".docx")    
    #print (real_path)
    return real_path

def getCurrentFolder():
    return os.getcwd();

def hasFile(files, key):
    return key in files

def getExistFile(files, key):
    return files[key]

def generateNewFile(key):
    path = generateFilePath(getCurrentFolder(), key)
    doc = SaveFile(path)
    doc.addTitle(key)
    return doc

def getDocFile(files, title):
    if hasFile(files, title):
        doc = getExistFile(files, title)
    else:
        doc = generateNewFile(title)
        files[title] = doc
    return doc
        
        
        