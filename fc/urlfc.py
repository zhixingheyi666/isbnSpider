# -*- coding:utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re, pdb, os, random

#为自定义模块添加搜索路径
import sys
sysSf = 'D:\\python_learn\\sysFc'
sys.path.append(sysSf)


from logSf10 import crLog
logger = crLog()
logger.info('Succeed!!') 
from fRcd import fRecord

fgx = '\n======================================分割线======================================\n'

urlst = [ "https://www.yandex.com",
            "http://www.baidu.com",
            "http://www.1688.com",
            "https://www.zhihu.com/question/20271508",
            "http://www.cnblogs.com/wupeiqi/articles/4731930.html",
            "http://www.baidu.com/s?",
            'http://news.dbanotes.net',
            'http://opac.nl.cn',
            'http://www.zhcw.com',
            'http://www.zhihu.com'
            ]

def getHtml( url ):
    #pdb.set_trace()
    html = urlopen( url )
    bsObj = BeautifulSoup(html,'html.parser')
    #bsObj = BeautifulSoup(html)
    return bsObj

class Rule(object):
    def __init__(self,ruleNum = [-1,],tRe = re.compile('.*'),logic = 'and', tClass = 'href'):
        logger.debug("Using----> Rule(ruleNum = [-1,],tRe = re.compile('.*'),logic = 'and',tClass = 'href')")
        #tRe,是否采用正则判断，logic,判定条件之间是‘与’还是‘或’，tClass,需要判定标签的哪个属性
        #-1表示忽略所有num字典关联的规则
        self.ruleNum = ruleNum
        self.tRe = tRe
        self.logic = logic
        self.tClass = tClass
    def filter(self,tag):
        #判断结果存储字典
        result = {}
        #判断规则匹配字典
        num = {}
        #判断规则条目数
        RULENUMBERS = 10
        #pdb.set_trace()
        num[-1] = 0 
        for i in range(RULENUMBERS):
            num[i] = False
        for ir in self.ruleNum:
            num[ir] = 1
        try:
            if self.tClass not in tag.attrs:
                tR = False  
            else:
                if self.tRe:
                    logger.debug('\nRule正在应用规则---> %r' % self.tRe)
                    pattern = re.compile(self.tRe)
                    try:
                        if re.match(pattern,tag.attrs[self.tClass]):
                            result['tRe'] = True
                        else:
                            result['tRe'] = False 
                    except Exception as e:
                        pdb.set_trace()
                        logger.warning(e)
                        logger.warning(fgx + 'Function Rule Failure!!Meybe Tag not suitable' + fgx)
                        result['tRe'] = False 
                if num[-1]:
                    #-1表示忽略所有num字典关联的规则
                    pass
                else:
                    #if num[1]:
                    #   logger.debug('\nRule正在应用规则---->查找所有外链(re = compile(^(http|www)((?!"+excludeUrl+").)$))')
                    if num[0]:
                        logger.debug('\nRule正在应用规则---->href页面深度为2,(包含两个"\\")')
                        try:
                            tlink = tag.attrs['href']
                            tsplit = tlink.split('/')
                            #logger.info(len(tsplit))
                            #logger.info(tsplit)
                            if len(tsplit) == 3:
                                result[0] = True 
                            else:
                                result[0] = False 
                        except Exception as e:
                            pdb.set_trace()
                            logger.warning(e)
                            logger.warning(fgx + 'Function Rule Failure!!Meybe Tag not suitable' + fgx)
                    
                    else:
                        pdb.set_trace()
                        result[self.ruleNum] = False 
                        logger.warning(fgx + 'ruleNum(%r) not Exsit!!' %  + fgx)
                if self.logic == 'and':
                    #pdb.set_trace()
                    tR= True
                    for tv in result.values(): 
                        tR = tR and tv
                elif self.logic == 'or':
                    tR= False 
                    for tv in result.values(): 
                        tR = tR or tv
                else:
                    result[self.ruleNum] = False 
                    logger.warning(fgx +'Function Rule logic Error,it will return False!!'+ fgx)  
                    tR= False 
        except Exception as e:
            tR= False 
            pdb.set_trace()
            logger.warning(e)
            logger.warning(fgx +'Function Rule Failure!! it will return False!!'+ fgx)  
        return tR

def splitAddr(address):
    addrParts = address.replace('https://','').replace('http://','').split('/')
    return addrParts

def getExlinks( bsobj,excludeUrl,norepeat = True ):
    links = [] 
    #外链匹配正则表达式
    tRe = '^(http|www)((?!' + excludeUrl + ').)*$'
    rule = Rule(tRe = tRe)
    #pdb.set_trace()
    for link in bsobj.findAll( lambda tag: rule.filter(tag)):
        tlink = link.attrs['href']
        if tlink not in links:
                links.append(tlink)
    return links

def getInlinks( bsobj,includeUrl,norepeat = True ):
    links = [] 
    #内链匹配正则表达式
    tRe = '^(/[^/]|.*' + includeUrl + ').*'
    rule = Rule(tRe = tRe)
    #pdb.set_trace()
    for link in bsobj.findAll( lambda tag: rule.filter(tag)):
        tlink = link.attrs['href']
        #为统一格式，去除域名，只保留相对链接
        tlink = tlink.replace(includeUrl,'').replace('https://','').replace('http://','')
        if tlink not in links:
                links.append(tlink)
    return links
    
    

def getLinks( bsobj,rule = Rule([-1,]),norepeat = True ):
    links = [] 
    for link in bsobj.findAll( lambda tag: rule.filter(tag)):
        tlink = link.attrs['href']
        if tlink not in links:
                links.append(tlink)
                #logger.info(tlink)
                #print(links[-1])
    #pdb.set_trace()
    return links

        
            

if __name__ == '__main__':
    testUrl = ['/question/53030354',
                    '/people/xu-jia-nan-3-31',
                    '/people/xu-jia-nan-3-31/following']
    html = getHtml(urlst[-1])
    for il in getInlinks(html,'www.zhihu.com'):
        print(il+'\n')
        logger.info(il)

