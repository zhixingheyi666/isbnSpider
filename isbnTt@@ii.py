# _*_coding:utf-8_*_

__author__ = 'Master Wang'

from urllib.request import urlopen
from bs4 import BeautifulSoup
import collections
import re
import time
import random

# 为自定义的模块添加搜索路径
import sys

sysFc = 'D:\\python_learn\\sysFc'
sys.path.append(sysFc)

from logSf10 import crLog

logger = crLog(fname='D:\桌面\isbn.log')
# logger = crLog(fname = 'D:\桌面\handlers.log')
logger.info('Succeed')

# 引入数据库连接
from connSql import mkcon

cursor, mkconn = mkcon('mic', database='catalog')
cursorE, mkconnE = mkcon('mic', database='easybook')

isbnIn = open('D:\\桌面\\isbnIn.log', 'w')
insertRecord = set()
# failRecord = set()
insertCount = 0


# def isbnData(path='D:\\Pycharm\\isbnSpider\\data\\testData.txt'):
def isbnData(cursor=cursor, mkconn=mkconn):
    isbnS = set()
    sql = 'SELECT ISBN FROM preISBN'
    cursor.execute(sql)
    for ir in cursor.fetchall():
        isbnS.add(ir[0])
    return list(isbnS)


def delISBN(isbnS, cursor=cursor, mkconn=mkconn):
    # global cursor, mkconn
    sql = 'DELETE FROM preISBN WHERE ISBN = ?'
    logger.info('func <delISBN> : 去除已经录入的ISBN条目')
    for isbn in isbnS:
        cursor.execute(sql, isbn)
    cursor.commit()


def marc(isbnS, baseUrl='http://opac.nlc.cn/F', **kw):
    # source = open(data,'r')
    # okw = dict(func='full-set-set_body',find_code='ISB',request='',set_entry='000001',format='001',local_base='NLC01')
    okw = collections.OrderedDict()
    okw['find_code'] = 'ISB'
    okw['request'] = ''
    okw['local_base'] = 'NLC01'
    okw['func'] = 'find_b'
    arg = ''
    for k in kw:
        try:
            tti = okw[k]
        except KeyError:
            logger.warn('File:isbnTt\nLine 29: tti = okw[k]\nFunc: isbn(isbnS,**kw)\n\
            KeyError:{} is not a property request arguments'.format(k))
            choice = input('Please input "Y" to Accept or any other key to Jump :')
            if choice == 'Y':
                okw[k] = kw[k]
    index = urlopen(baseUrl)
    indexObj = BeautifulSoup(index, 'html.parser')
    iterObj = indexObj.find('form')
    iterUrlTt = iterObj.get('action')
    iterUrl = iterUrlTt[:-5] + '{:0>5}'.format(int(iterUrlTt[-5:]) + 1)
    isbnFailure = []
    # global cursorE, mkconnE
    for isbn in isbnS:
        try:
            okw['request'] = isbn
            arg = '?'
            for k, v in okw.items():
                arg = arg + k + '=' + v + '&'
            arg = arg[:-1]
            logger.info(iterUrl + arg)
            iterHtml = urlopen(iterUrl + arg)
            iterObjI = BeautifulSoup(iterHtml, 'html.parser')
            # 获取下一次链接以及xhr参数URL
            iterObjII = iterObjI.find('form')
            iterUrl = iterObjII.get('action')
            # $('#hitnum')多结果分支
            objHit = iterObjI.find('div', id='hitnum')
            if objHit:
                xhrUrls = []
                objS = iterObjI.findAll('div', {'class': 'itemtitle'})
                numStr = objHit.get_text()
                num = int(numStr.split('"')[1].split(' ')[-1])
                preUrl = objS[0].a.get('href')[:-3] + '001'
                logger.info(preUrl)
                u0 = preUrl[:75]
                u1 = int(preUrl[75:80])
                u2 = preUrl[80:98] + '_body'
                u3 = preUrl[98:127]
                u4 = '&format=001'
                for i in range(num):
                    pUrl = (u0 + '{:0>5}' + u2 + u3 + '{:0>6}' + u4).format(u1 + i * 9, i + 1)
                    logger.info(pUrl)
                    xhrUrls.append(pUrl)
                logger.info('==| Len of xhrUrls: {} |== '.format(len(xhrUrls)))
                for ix in xhrUrls:
                    try:
                        iterXhr = urlopen(ix)
                        marcObj = BeautifulSoup(iterXhr, 'html.parser')
                        marcEngine(marcObj)
                    except:
                        logger.exception('Failed: {} \n'.format(ix))
            else:
                # 查询结果唯一 的分支
                # 根据分析网页得到的action和xhr请求url的推算关系
                # 构造XHR参数
                iterUrlII = iterUrl[:-5] + '{:0>5}'.format(int(iterUrl[-5:]) + 12)
                numberObj = iterObjI.find('input', id='set_number')
                if not numberObj:
                    continue
                set_number = numberObj.get('value')
                argFont = "?func=full-set-set_body&set_number="
                argEdn = "&set_entry=000001&format=001"
                iterUrlIII = iterUrlII + argFont + set_number + argEdn
                iterXhr = urlopen(iterUrlIII)
                marcObj = BeautifulSoup(iterXhr, 'html.parser')
                marcEngine(marcObj)
        except:
            logger.exception("Failed ISBN: {} ".format(isbn))
            isbnFailure.append(isbn)
            continue
        finally:
            rest = random.randint(0, 10)
            logger.info('-------------Have A Rest: {}s----------------\n'.format(rest))
            time.sleep(rest)


def marcEngine(marcObj, cursor=cursor, mkconn=mkconn):
    # global cursorE, mkconnE, insertCount
    global insertCount, insertRecord
    try:
        tds = marcObj.findAll('td')
        tdEven = tds[::2]
        tdOrd = tds[1::2]
        marcPre = dict()
        for (ei, oi) in zip(tdEven, tdOrd):
            marcPre[ei.get_text()] = oi.get_text() + ' '
        marc = {'ISBN': '', 'BCid': '', 'Title': '', 'Writer': '', 'Epitome': '', 'Pages': '', 'Price': 0.0,
                'PublishDate': '', 'PageMode': '', 'Version': '', 'extName': '', 'translator': '', 'keyword': '',
                'PubID': '', 'id': '', 'publish': '', 'adds': '', 'Caste': ''}
        for k, v in marcPre.items():
            if k == '010':
                m010 = v.split('|')
                for mi in m010[1:]:
                    if mi[0] == 'a':
                        marc['ISBN'] = mi[2:-1]
                    elif mi[0] == 'd':
                        # 提取价格，\d表示任意数字，.在[]内失去特殊含义，表示本来的意思
                        marc['Price'] = float((re.findall(r'[\d.]+', mi))[0])
            elif k == '690':
                m690 = v.split('|')
                for mi in m690[1:]:
                    if mi[0] == 'a':
                        marc['BCid'] = mi[2:-1]
            elif k == '2001':
                m2001 = v.split('|')
                for mi in m2001[1:]:
                    if mi[0] == 'a':
                        marc['Title'] += mi[2:-1]
                    elif mi[0] == 'e':
                        marc['Title'] = marc['Title'] + '[' + mi[2:-1] + ']'
                    elif mi[0] == 'h':
                        marc['Title'] = marc['Title'] + '（' + mi[2:-1] + '）'
                    elif mi[0] == 'i':
                        marc['Title'] = marc['Title'] + '，' + mi[2:-1]
                    elif mi[0] == 'f':
                        marc['Writer'] = mi[2:-1]
            elif k == '300':
                m300 = v.split('|')
                for mi in m300[1:]:
                    if mi[0] == 'a':
                        marc['Epitome'] = marc['Epitome'] + mi[2:-1] + ' '
            elif k == '330':
                m330 = v.split('|')
                for mi in m330[1:]:
                    if mi[0] == 'a':
                        marc['Epitome'] = marc['Epitome'] + mi[2:-1] + ' '
            elif k == '215':
                m215 = v.split('|')
                for mi in m215[1:]:
                    if mi[0] == 'a':
                        try:
                            marc['Pages'] = int(mi[2:-2])
                        except:
                            marc['Pages'] = int((re.findall(r'[\d]+$', mi[2:-2]))[0])
                    elif mi[0] == 'c':
                        marc['PageMode'] = marc['PageMode'] + mi[2:-1] + ' '
                    elif mi[0] == 'd':
                        marc['PageMode'] = marc['PageMode'] + mi[2:-1] + ' '
                    elif mi[0] == 'e':
                        marc['PageMode'] = marc['PageMode'] + mi[2:-1] + ' '
            elif k == '205':
                m205 = v.split('|')
                for mi in m205[1:]:
                    if mi[0] == 'a':
                        marc['Version'] = mi[2:-1]
            elif k == '410 0':
                m4100 = v.split('|')
                for mi in m4100[1:]:
                    if mi[0] == 'a':
                        marc['extName'] = marc['extName'] + mi[2:-1] + ' '
            elif k == '2252':
                m2252 = v.split('|')
                for mi in m2252[1:]:
                    if mi[0] == 'a' and marc['extName'] == '':
                        marc['extName'] = marc['extName'] + mi[2:-1] + ' '
            elif k == '6060':
                m6060 = v.split('|')
                for mi in m6060[1:]:
                    marc['keyword'] = marc['keyword'] + mi[2:-1] + ' '
            elif k == '210':
                m210 = v.split('|')
                for mi in m210[1:]:
                    if mi[0] == 'a':
                        marc['adds'] = mi[2:-1]
                    elif mi[0] == 'c':
                        marc['publish'] = mi[2:-1]
                    elif mi[0] == 'd':
                        marc['PublishDate'] = mi[2:-1]
        for k, v in marc.items():
            logger.info('|{}|--|{}|'.format(k, v))
        sql = """INSERT INTO  AttBooklist (ISBN, BCid, Title, Writer, Epitome, Pages, Price, PublishDate, PageMode,
                    Version, extName, keyword, publish, adds)\
                    VALUES(  ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )"""
        # sql = """INSERT INTO AtestBooklist (ISBN, BCid, Title, Writer, Epitome, Pages, Price, PageMode)\
        #             VALUES( ?, ?, ?, ?, ?, ?, ?, ? )"""
        # cursor.execute(sql, marc['ISBN'], marc['BCid'], marc['Title'], marc['Writer'], marc['Epitome'], marc['Pages'],
        #                 marc['Price'], marc['PageMode'])
        cursor.execute(sql, marc['ISBN'], marc['BCid'], marc['Title'], marc['Writer'], marc['Epitome'], marc['Pages'],
                       marc['Price'], marc['PublishDate'], marc['PageMode'], marc['Version'], marc['extName'],
                       marc['keyword'], marc['publish'], marc['adds'])
        insertCount += 1
        insertRecord.add(marc['ISBN'].replace('-', ''))
        try:
            isbnIn.write(marc['ISBN'] + '\n')
        except:
            logger.exception('Failed to Record:\n')
        if insertCount % 10 == 0:
            # 总数量除以10，一般是有余数的，所以最后别忘记在主程序末尾在commit一次
            logger.info(insertCount)
            cursor.commit()
    except:
        raise

def check(cursor=cursor,mkconn=mkconn):
    sqlI = "select ISBN from booklist where replace(ISBN,'-','') = ?"
    sqlII = "select ISBN from attbooklist where replace(ISBN,'-','') = ?"
    while 1:
        isbn = input("INPUT:    'N' for quit     ISBN for check:\n")
        if isbn == 'N':
            break
        else:
            try:
                count = 0
                # cursor.execute(sqlI, isbn)
                # count += len(cursor.fetchall())
                cursor.execute(sqlII, isbn)
                count += len(cursor.fetchall())
                if count >= 1:
                    logger.info("■■■   OK   ■■■")
                else:
                    logger.info("==||  No Record ||==")
            except:
                logger.info("Failed:\n")



def isbnTosql(path='D:\\Pycharm\\isbnSpider\\data\\testData.txt', cursor=cursor, mkconn=mkconn):
    fTt = open(path, 'r')
    isbnS = []
    sql = 'INSERT INTO preISBN( ISBN ) VALUES ( ? )'
    try:
        for li in fTt:
            cursor.execute(sql, li[:-1])
            isbnS.append(li[:-1])
        # 本表自身去重
        cursor.execute('SELECT DISTINCT ISBN INTO "#t1" FROM preISBN')
        cursor.execute('TRUNCATE TABLE preISBN')
        cursor.execute('INSERT INTO preISBN  SELECT * FROM "#t1"')
        cursor.commit()
    except:
        raise
    return isbnS


"""
#catalog编目库与marc项对照表
catadict['ISBN']='010|a'
catadict['BCid']='690|a'
catadict['Title']='2001|a|h'
catadict['Writer']='2001|f'
catadict['Epitome']='300' or '330'
catadict['Pages']='215|a'
catadict['Price']='010|b' or '010|d'
catadict['PublisDate']='100|a'
catadict['PageMode']='215|d'
catadict['Version']='205 |a'
catadict['extName']='410 0|a'
catadict['translator']=''
catadict['keyword']='6060'
catadict['PubID']='ISBN前5位'
catadict['id']='??'
catadict['publish']='210|c'
catadict['adds']='210|a'
catadict['Caste']=''

"""

if __name__ == '__main__':
    # isbnS = isbnData(path='D:\\桌面\\isbn1.0.txt')
    # isbnS = isbnTosql(path='D:\\桌面\\isbn1.0.txt')
    # isbnS = isbnData()
    # marc(isbnS)
    # delISBN(insertRecord)
    # cursor.commit()
    # isbnIn.closed()
    check()

    # isbnS = sqlData()
    # isbnS = ['9787535479426']
    # isbnS = ['9787215069756']
