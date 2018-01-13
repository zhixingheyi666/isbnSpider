
from urllib import request
import urllib


urlst = [ "https://www.yandex.com/",
            "http://www.baidu.com",
            "http://www.1688.com",
            "https://www.zhihu.com/question/20271508",
            "http://www.cnblogs.com/wupeiqi/articles/4731930.html",
            "http://www.baidu.com/s?" 
            ]
uf = [2]
#page = request.Request( urlst[5] )
#page.add_header( 'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'  )
utail = {}
#data['word'] = '课表'
utail['word'] = 'Jecvay Notes'
urtail = urllib.parse.urlencode( utail )
full_url = urlst[5] + urtail
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}  
page = request.Request( full_url, headers = headers )

#function urlopen accept real url or request instance
#the request module make you  visit web site like a browser
#page is a request instance
openre = request.urlopen( page )
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
#print( Dco )
with open( 'JecvayNotes.html', 'wb' ) as f:
    f.write(str.encode(data))
F.write( str(Dco) )
F.close()
#a test for urllib.parse.libencode( ** )
print( 'a test for url.parse.encode( ** )\n' )
uphrase_encode = utail
uphrase_encode['name'] = 'junjun'
uphrase_encode['Content-Type'] = 'Charset:UTF-8'
uphrase_encode['Big attr'] = 'generator list iterator'
print( uphrase_encode )
print(  urllib.parse.urlencode( uphrase_encode ) )


from urllib.parse import urlparse
upl = [ 'http://www.cwi.nl:80/%7Eguido/Python.html',
        'http://www.baidu.com/index.php?username=guol' ]
upls = []
for u in upl:
    upls.append( urlparse ( u ) )
    print( u,'\n',upls[ -1 ] )
