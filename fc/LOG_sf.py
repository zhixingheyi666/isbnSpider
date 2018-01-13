# -*- coding: utf-8 -*-
#写一个通用的 日志 函数，返回一个日志实例
#函数的作用就是通过传递参数来定制个性化的 日志实例，精细的控制日志行为来满足需要
#比如多久日志清空一次，日志的路径等等
#默认参数包括日志的名称和路径，是否启用文件日志，日志标志符等
#当然，是否可以通过自定义 logging.Logger 类,来实现同样的功能，测试一下看看
#记得还有 装饰器 的用法来着

import logging
from logging import getLogger
from logging import FileHandler 
from logging import StreamHandler 
from logging import Formatter 

#code for log
#Using:     logger.info( 'Some information' ) to replace print( 'Some information' )
logger = getLogger( 'SF:' )
logger.setLevel( logging.DEBUG)
#logging.basicConfig( level = logging.INFO )

#LOG_FILE = 'Log_test.log'

fh = FileHandler( 'Log-test.log' )
fh.setLevel( logging.INFO )

ch = StreamHandler()
#ch.setLevel( logging.WARN)
ch.setLevel( logging.DEBUG)

formatter = Formatter( '%(asctime)s - %(name)s - %(levelname)s:\n%(message)s\n' )
formatter_ch = Formatter( '%(name)s:     %(message)s' )
fh.setFormatter( formatter )
ch.setFormatter( formatter_ch )

logger.addHandler(fh)
logger.addHandler(ch)

"""
The code below is a test for module logging.
"""
tts = '0'
ttn = int(tts) 
logger.info( 'ttn = %d ' % ttn )
logger.debug( 'Debug:ttn = %d ' % ttn )
ldebug = logger.debug
linfo = logger.info
ldebug( 'LDB\n\n rename loggger.debug to ldebug!!' )
try:
    print( 10 / ttn )
except Exception as e:
    ldebug( e )
