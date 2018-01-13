# -*- coding:utf-8 -*-
import pdb, time

from urllib.request import urlopen
from bs4 import BeautifulSoup

try:
    from .LOG_sf import logger
    from .conn_SQL import mkcon
except:
    from LOG_sf import logger
    from conn_SQL import mkcon


def bMrktsql( htmlpath ):
    try:
        html = urlopen(htmlpath)
        pdb.set_trace()
        bsObj = BeautifulSoup(html, 'html.parser')
        uList = bsObj.find_all('a')
        logger.info('Numbers of Url : %r', str(len(uList)))
    except:
        logger.exception('Parsing Failure:')
        logger.info('Parsing Failure')
        return None
    ulist = []
    ulistl = []
    uerr = []
    for ui in uList:
        try:
            url = []
            tmark = True
            thref = ui.attrs['href']
            if len(thref) > 255:
                tmark = False
            url.append(ui.attrs['href'])
            if len(ui.text) <= 255:
                url.append(ui.text)
            else:
                url.append(ui.text[0:255])
            exd = { key: ui.attrs[key] for key in ui.attrs.keys() - {'href', 'add_date', 'last_modified'}}
            exmsg = ''
            for k, v in exd.items():
                exmsg += k + '\n' + v + '\n'
            url.append(exmsg)
            adtm = time.strftime( '%Y-%m-%d %H:%M:%S',time.localtime(int(ui.attrs['add_date'])))
            mdftm = time.strftime( '%Y-%m-%d %H:%M:%S',time.localtime(int(ui.attrs['last_modified'])))
            url.append(adtm)
            url.append(mdftm)
            if tmark: 
                ulist.append(tuple(url))
            else:
                ulistl.append(tuple(url))
        except:
            logger.exception('urlMark Parsing Error:\n')
            logger.info('urlMark Parsing Error:\n' + str(ui))
            uerr.append(ui)
    cursor, mconn = mkcon()
    cursor.execute('''use fortest''')
#需添加url重复检查措施，或者数据库中添加也可
    try:
        cursor.executemany('''insert into bookmurl( url, urll, utext, exmsg, tags, addtm, mdftm )
                                values( %s, '', %s, %s, '', %s, %s)''', ulist)
        cursor.executemany('''insert into bookmurl( url, urll, utext, exmsg, tags, addtm, mdftm )
                                values( '', %s, %s, %s, '', %s, %s)''', ulistl)
        mconn.commit()
    except:
        logger.exception('SQL Failure!\n')
        logger.warn('SQL Failure!\n')
    return (ulist, ulistl, uerr)
    
    
    
    
if __name__ == '__main__':
    tUrl = bMrktsql('file:///D:/python_learn/spider/data/FireFox_bookmarks.html')
    
