# encoding:UTF-8
#import urllib.request
from urllib import request

urlst = [ "https://www.yandex.com/", "http://www.baidu.com", "http://www.1688.com"]
uf = [2]
openre = request.urlopen(urlst[2])
data = openre.read()
try:
    data = data.decode('UTF-8')
    Dco = data.encode( encoding = 'gbk', errors = 'backslashreplace' ) 
except Exception as e:
    print(e)
    Dco = 'Error'
F = open( 'recordt.txt', 'w' )
#UnicodeEncodeError:gbk codec can’t encode character ...
# to avoid the above case ,use the function encode with parameter errors = 'backslashreplace'
print( Dco )
F.write( str(Dco) )
F.close()
