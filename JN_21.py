# -*- coding: utf-8 -*-

import re
from urllib import request
import urllib

from collections import deque

Sq = deque()
Vis = set()


urlst = [ "https://www.yandex.com/",
            "http://www.baidu.com",
            "http://www.1688.com",
            "https://www.zhihu.com/question/20271508",
            "http://www.cnblogs.com/wupeiqi/articles/4731930.html",
            "http://www.baidu.com/s?",
            'http://news.dbanotes.net'
            ]

Sq.append( urlst[6] )
cnt = 0
count_Sq = 1
Rurl = open( 'Result_JN_2.txt', '+w' )
Rurl.write( '\n\n' )
S = ''
while Sq:
    url = Sq.popleft()
    Vis = { url }
    count_Sq -= 1

    print( ' Already Sipdered:' + str( cnt ) + '    Spidering ---->   ' + url )
    print( 'Url Numbers In The Q: ', count_Sq )
    if len( url ) > 50:
        print( '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' )
        print( url )
        continue
    try:
        Op = request.urlopen( url )
        cnt += 1
    
        if 'html' not in  Op.getheader( 'Content-Type' ):
            #sf:log >>>>add logging common
            continue
        try:
            Dt_t = Op.read().decode( 'utf-8' )
            Dt = Dt_t.encode( encoding = 'gbk', errors = 'backslashreplace' )
        except Exception as e:
            #sf: log
            continue
        Lkre = re.compile( 'href="(.+?)"' )
        Lkt =  Lkre.findall( Dt_t )   
        for x in Lkt:
            if 'http' in x and x not in Vis:
                Sq.append(x)
                Rurl.write( x + '\n' )
                count_Sq += 1
                if not count_Sq % 100:
                    S = input( 'Press N to STOP:\n' )
                print( 'Adding into the Q---->  ' + x )

        if S == 'N':
            break
    except Exception as e:
        print( e ) 
        Error = input( 'Error Press:\n' )
        #sf: log    
        continue
Rurl.close()

                    



queue = deque( [ 'Eric', 'John', 'Michael' ] )
queue.append( 'Terry' )
queue.append( 'Graham' )
queue.popleft()
queue.popleft()
queue

