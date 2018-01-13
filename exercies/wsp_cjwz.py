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
os.chdir('d:\\python_learn\\spider')
from fc.urlfc import getHtml,getLinks,Rule,getInlinks


#================全局变量====================
fgx = '\n======================================分割线======================================\n'
#遍历整个网站时，记录已经爬过的页面
pages = set()

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

def getSite(urlHead,urlTail='',recursionD = 0):
    global pages
    try:
        #这里必须区分内链，外链，页面内定位链接
        #内链:以字符'/',开头的链接,可以考虑用正则实现
        #本网址内链:以http开头，域名是本网址域名的,搜索一下 域名 的相关知识,这一条可以写一个Rule项
        #外链仅记录地址
        #内链正则表达式
        url = urlHead + urlTail
#        tRe = '^/[^/].*' 
#        rule = Rule(tRe = tRe)
        html = getHtml(url)
#        for li in getLinks(html,rule):
        for li in getInlinks(html,urlHead):
            if li not in pages:
                logger.info(li)
                pages.add(li)
                if recursionD < 10:
                    #这里必须区分内链，外链，页面内定位链接
                    getSite(urlHead,li,recursionD + 1)
                else:
                    logger.warning(fgx + 'Reached recursionD --->  %r!!' % li + fgx)
    except Exception as e:
        pdb.set_trace()
        logger.warning(e)
        logger.warning(fgx + 'Failed Open Website %r!!' % li + fgx)



            

if __name__ == '__main__':
    #html = getHtml(urlst[-1])
    #getSite(urlst[-2])
    getSite(urlst[-1])
    
    

    
"""

    html = getHtml(urlst[-2])
    links = getLinks(html)
    for il in links:
        logger.info(il)
    fRecord(fgx,iIter = False,cls = False)
    fRecord(links,cls = False)
=======================================================
    
    questionUrl = ['/question/53030354',
                    '/people/xu-jia-nan-3-31',
                    '/people/xu-jia-nan-3-31/following']
    #bsObj = getHtml(urlst[-1] + questionUrl[-1])
    papa(urlst[-1], questionUrl[-1])
=======================================================
    rule = re.compile('^(\/people\/).*')
    links = getLinks(bsObj,rule)
    fRcord = 'D:\\桌面\\tempStdout.out'
    frSize = os.path.getsize(fRcord) 
    with open(fRcord,'a') as tff:
        if frSize > 1024 * 10:
            tff.truncate()
        for il in links:
            tff.write(il+'\n')
        tff.write(fgx)
============================================================
string = re.compile('\.\.\/img\/gifts/img.*\.jpg')
^\/people\/.*
^\/people\/((?!:).)*$
"""



