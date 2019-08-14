#!/usr/bin/python
# coding: UTF-8
'''
Created on 2018年1月4日

@author: shun
'''

from com.njsfy.creeper import fetchurl, parsehtml, subjectinfo
import os
import Common
import utils
from com.njsfy.creeper.savefile import SaveFile

def getSubjectTitle(parser):
    try:
        title_doc = parser.getNodeHtml(".answer-desc-content")[1]
        return parser.getSingleInfo(title_doc, "p").text()
    except:
        return ""
        
        

def generateSubjectType(index, subject):
    if index == 1:
        return "[" + subject + "]" + "\n"
    else:
        return ""
    

if __name__ == '__main__':
    print ("go")
    enter_url = fetchurl.FecthUrl("http://121.40.106.163:8081/onts/system/check_user_login.do")
    params = {'j_username':'571' , 'j_password':'123456'}
    headers = {'Content-Type':'application/x-www-form-urlencoded'}
    content = enter_url.post(params = params, headers = headers)
    print (content)
    
    exam_url = fetchurl.FecthUrl("http://121.40.106.163:8081/onts/learn/user_exam_exercise_100.do")
    headers = {'Content-Type':'application/x-www-form-urlencoded', 'Cookie':'JSESSIONID=E4764AA61A3D9C0114E09DE86050AD7D'}
    content = exam_url.get(headers = headers)
    #print (content)
    #开始解析网页    
    parser = parsehtml.ParseHTML(content)
    
    #获取章节名称
    titles = []
    for title in parser.getNodeHtml('.knowledge-title-name'):
        subject = parser.getSingleInfo(title, "span").text()
        titles.append(subject)
    print (len(titles))
    
    question_list = parser.getNodeHtml('.question-list-knowledge')    
    print (len(question_list))
    
    subjects = []
    #获取某一科目下所有题型的网址
    for i in range(len(question_list)):
        subject = subjectinfo.SubjectInfo(titles[i])
        list = question_list[i]
        for question in parser.getSingleInfo(list, "li"):            
            url = parser.getAttrValue(question, "a", "href")
            subject.addUrl(url)                       
        subjects.append(subject)    
    
    print (len(subjects))    
    
    path = os.getcwd();
    
    for subject_info in subjects: 
        '''       
        save_path = os.path.join(path, subject_info.getSubject().replace("/", "_") + ".docx")
        if os.path.exists(save_path):
            continue
        doc = SaveFile(save_path)  
        '''   
        #文件存储结构,其中key为当前题目所属类型，如这种结构a>b>c, value为savefile的实体
        #单选，多选判断等可能属于同一key，要保存在同一文件，只能用同一savefile     
        files = {}
        #获取单一网址进行解析
        for sub_url in subject_info.getUrls(): 
            #用来获取单一题型          
            print (sub_url)
            type = utils.getQuestiontype(sub_url)
            #获取某题型的真实网址
            url = Common.root_url + sub_url
            #获取网页内容
            question = fetchurl.FecthUrl(url)
            headers = {'Content-Type':'application/x-www-form-urlencoded', 'Cookie':'JSESSIONID=E4764AA61A3D9C0114E09DE86050AD7D'}
            content = question.get(headers = headers)
            content_parser = parsehtml.ParseHTML(content)
                      
            if type == Common.single_question_type : 
                print ("1")
                title = getSubjectTitle(content_parser)                
                #print(title)
                #doc = utils.getDocFile(files, title)
                if utils.hasFile(files, title):
                    doc = utils.getExistFile(files, title)
                else:
                    doc = utils.generateNewFile(title)
                    files[title] = doc
                index = 0               
                for singele_choice in content_parser.getNodeHtml(".question.qt-singlechoice"):
                    index = index + 1 
                    info = generateSubjectType(index, "单选题")                  
                    info = info + str(index) + ". " + content_parser.getSingleInfo(singele_choice, ".question-body-text").text()
                    #print (single_title)
                    for list_item in content_parser.getSingleInfo(singele_choice, ".question-list-item"):
                        info = info + "\n" + content_parser.getSingleInfo(list_item, "span").text()
                        pass
                    info = info + "\n" + "正确答案： " + content_parser.getSingleInfo(singele_choice, ".answer_value").text() 
                    info = info + "\n" + "难度： " +  content_parser.getNode(singele_choice, ".answer-desc-difficult", subject = "p").text()                  
                    paragraph = doc.addContent(info)
                    analyzs ="\n" + "解析： " + content_parser.getNode(singele_choice, ".answer-desc-content", subject = "p").text()
                    doc.appendContent(paragraph, analyzs)
                    #print (info) 
                                      
                    pass
                pass
            elif type == Common.multi_question_type: 
                print ("2")
                title = getSubjectTitle(content_parser) 
                if (title == ""):
                    continue
                print(title)
                if utils.hasFile(files, title):
                    doc = utils.getExistFile(files, title)
                else:
                    doc = utils.generateNewFile(title)
                    files[title] = doc
                index = 0               
                for singele_choice in content_parser.getNodeHtml(".question.qt-multiplechoice"):
                    index = index + 1 
                    info = generateSubjectType(index, "多选题")                    
                    info = info + str(index) + ". " + content_parser.getSingleInfo(singele_choice, ".question-body-text").text()
                    #print (single_title)
                    for list_item in content_parser.getSingleInfo(singele_choice, ".question-list-item"):
                        info = info + "\n" + content_parser.getSingleInfo(list_item, "span").text()
                        pass
                    info = info + "\n" + "正确答案： " + content_parser.getSingleInfo(singele_choice, ".answer_value").text()  
                    info = info + "\n" + "难度： " +  content_parser.getNode(singele_choice, ".answer-desc-difficult", subject = "p").text()                  
                    paragraph = doc.addContent(info)
                    analyzs = "\n" + "解析： " + content_parser.getNode(singele_choice, ".answer-desc-content", subject = "p").text()
                    doc.appendContent(paragraph, analyzs)
                    #doc.addContent(info)                    
                pass 
            elif type == Common.deside_question_type:
                continue
                title = getSubjectTitle(content_parser) 
                print ("3")
                print(title)
                if utils.hasFile(files, title):
                    doc = utils.getExistFile(files, title)
                else:
                    doc = utils.generateNewFile(title)
                    files[title] = doc
                index = 0
                for singele_choice in content_parser.getNodeHtml(".question.qt-trueorfalse"):
                    index = index + 1   
                    info = generateSubjectType(index, "判断题")                 
                    info = info + str(index) + ". " + content_parser.getSingleInfo(singele_choice, ".question-body-text").text()                    
                    info = info + "\n" + "正确答案： " + content_parser.getSingleInfo(singele_choice, ".answer_value").text() 
                    info = info + "\n" + "难度： " +  content_parser.getNode(singele_choice, ".answer-desc-difficult", subject = "p").text()                   
                    paragraph = doc.addContent(info)
                    analyzs = "\n" + "解析： " + content_parser.getNode(singele_choice, ".answer-desc-content", subject = "p").text()
                    doc.appendContent(paragraph, analyzs)
                    #doc.addContent(info)                    
                pass       
            elif type == Common.subject_question_type:  
                title = getSubjectTitle(content_parser) 
                print ("4")
                print(title) 
                if utils.hasFile(files, title):
                    doc = utils.getExistFile(files, title)
                else:
                    doc = utils.generateNewFile(title)
                    files[title] = doc
                index = 0             
                for singele_choice in content_parser.getNodeHtml(".question.qt-example"):
                    index = index + 1   
                    info = generateSubjectType(index, "案例题")                 
                    info = info + str(index) + ". " + content_parser.getSingleInfo(singele_choice, ".question-body-text").text()
                    #print (single_title)
                    for list_item in content_parser.getSingleInfo(singele_choice, ".question-list-item"):
                        info = info + "\n" + content_parser.getSingleInfo(list_item, "span").text()
                        pass
                    info = info + "\n" + "正确答案： " + content_parser.getSingleInfo(singele_choice, ".answer_value").text()  
                    info = info + "\n" + "难度： " +  content_parser.getNode(singele_choice, ".answer-desc-difficult", subject = "p").text()                  
                    paragraph = doc.addContent(info)
                    analyzs = "\n" + "解析： " + content_parser.getNode(singele_choice, ".answer-desc-content", subject = "p").text()
                    doc.appendContent(paragraph, analyzs)
                    #doc.addContent(info)                    
                pass
            elif type == Common.analyze_question_type:
                continue
                title = getSubjectTitle(content_parser) 
                print ("5")
                print(title)
                if utils.hasFile(files, title):
                    doc = utils.getExistFile(files, title)
                else:
                    doc = utils.generateNewFile(title)
                    files[title] = doc
                index = 0
                for singele_choice in content_parser.getNodeHtml(".question.qt-analytical"):
                    index = index + 1   
                    info = generateSubjectType(index, "分析题")                 
                    info = info + str(index) + ". " + content_parser.getNode(singele_choice, ".question-body", subject = "p").text()
                    #print (single_title)
                    
                    info = info + "\n" + "正确答案： " + content_parser.getSingleInfo(singele_choice, ".answer_value").text() 
                    info = info + "\n" + "难度： " +  content_parser.getNode(singele_choice, ".answer-desc-difficult", subject = "p").text()                   
                    paragraph = doc.addContent(info)
                    analyzs = "\n" + "解析： " + content_parser.getNode(singele_choice, ".answer-desc-content", subject = "p").text()
                    doc.appendContent(paragraph, analyzs)
                    #doc.addContent(info)
                pass
            else:
                print ("fucking")
            pass
        
        for key in files.keys():
            doc = files[key]
            doc.saveDoc()          
              
        
    '''
    path = os.getcwd();
    doc = SaveFile(os.path.join(path, "test.docx"))
    
    for question in parser.getNodeHtml('.question.single-question-warp'):
        number = parser.getNode(question, ".number.fl").text()
        type = parser.getNode(question, ".problem.fr", subject="span").text()
        title = parser.getNode(question, ".problem.fr", subject="p").text()
        #print (number + "." + type + title)
        paragraph = number + "." + type + title
        
        
        options = parser.getNode(question, ".options")
        for option in parser.getNode(options, ".option"):
            index = parser.getNode(option, ".option", subject ="span").text()
            answer = parser.getNode(option, ".option", subject ="p").text()
            paragraph = paragraph + "\n" + index + answer
            #doc.addContent(index + answer)           
        
        doc.addContent(paragraph)  
        pass
    
    doc.saveDoc()
    '''
    pass