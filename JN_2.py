# -*- coding: utf-8 -*-

#from fc.conn_SQL import cursor, mconn 
from fc.conn_SQL import mkcon 
from fc.LOG_sf import logger
import re
from urllib import request
import urllib

from collections import deque

Sq = deque()
Vis = set()
sql = 'insert into originurl( url ) values( %s )'
cursor, mconn = mkcon()

urlst = [ "https://www.yandex.com/",
            "http://www.baidu.com",
            "http://www.1688.com",
            "https://www.zhihu.com/question/20271508",
            "http://www.cnblogs.com/wupeiqi/articles/4731930.html",
            "http://www.baidu.com/s?",
            'http://news.dbanotes.net',
            'http://www.sina.com.cn/',
            'http://k1.youxi.com/360meiti.html'
            ]

Sq.append( urlst[8] )
cnt = 0
count_Sq = 1
#Rurl = open( 'Result_JN_2.txt', '+w' )
#Rurl.write( '\n\n' )
S = ''
while Sq:
    url = Sq.popleft()
    #Vis.add(url) 
    logger.warn( str(len(Vis)) + 'len( Vis )     ' +  str(count_Sq) )
    count_Sq -= 1

    #logger.info( ' Already Sipdered:' + str( cnt ) + '    Spidering ---->   ' + url )
    logger.info( 'Url Numbers In The Q: ' +  str(count_Sq) )
    if len( url ) > 50:
        logger.info( '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' )
        logger.info( url )
        continue
    try:
        Op = request.urlopen( url, timeout = 2 )
        cnt += 1
    
        if 'html' not in  Op.getheader( 'Content-Type' ):
            #sf:log >>>>add logging common
            logger.debug( 'NO html:' + url)
            continue
        try:
            Dt_t = Op.read().decode( 'utf-8' )
            Dt = Dt_t.encode( encoding = 'gbk', errors = 'backslashreplace' )
        except Exception as e:
            #sf: log
            logger.warn( 'Encode:' )
            logger.warn(e)
            continue
        #Lkre = re.compile( 'href="(.+?)"' )
        Lkre = re.compile( r'class="title".+?href="(.+?)"' )
        Lkt =  Lkre.findall( Dt_t )   
        for x in Lkt:
            if 'http' in x and x not in Vis:
                Sq.append(x)
                Vis.add(x) 
                cursor.execute( sql, [x] )
                #Rurl.write( x + '\n' )
                count_Sq += 1
                if not count_Sq % 100:
                    #S = input( 'Press N to STOP:\n' )
                    mconn.commit()
                    logger.info( 'Sql Commit!' )
                    pass
                logger.info( 'Adding into the Q---->  ' + x )


        if S == 'N':
            mconn.commit()
            break
    except Exception as e:
        logger.error( 'urlopen:' ) 
        logger.error(e) 
        if  count_Sq % 100 > 95:
            S = input( 'Press N to STOP:\n' )
        #Error = input( 'Error Press:\n' )
        #sf: log    
        continue
#Rurl.close()
logger.info( 'Success Commplete!' )


"""
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
queue = deque( [ 'Eric', 'John', 'Michael' ] )
queue.append( 'Terry' )
queue.append( 'Graham' )
queue.popleft()
queue.popleft()
queue
"""


"""
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
The code below is a test for module logging.
tts = '0'
ttn = int(tts) 
logger.info( 'ttn = %d ' % ttn )
logger.debug( 'Debug:ttn = %d ' % ttn )
ldebug = logger.debug
linfo= logger.info
ldebug( 'LDB\n\n rename loggger.debug to ldebug!!' )
try:
    print( 10 / ttn )
except:
    pass
"""



"""
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
import logging
from logging import getLogger
from logging import FileHandler 
from logging import StreamHandler 
from logging import Formatter 

#code for log
#Using:     logger.info( 'Some information' ) to replace print( 'Some information' )
logger = getLogger( 'SF' )
logger.setLevel( logging.DEBUG)
#logging.basicConfig( level = logging.INFO )

#LOG_FILE = 'JN.log'


fh = FileHandler( 'JN.log' )
#fh.setLevel( logging.INFO )
fh.setLevel( logging.DEBUG)

ch = StreamHandler()
#ch.setLevel( logging.INFO)
ch.setLevel( logging.DEBUG)
#ch.setLevel( logging.WARN)

formatter = Formatter( '%(asctime)s - %(name)s - %(levelname)s:\n%(message)s\n' )
formatter_ch = Formatter( '%(name)s:     %(message)s' )
fh.setFormatter( formatter )
ch.setFormatter( formatter_ch )

logger.addHandler(fh)
logger.addHandler(ch)

linfo = logger.info
ldebug = logger.debug
"""
