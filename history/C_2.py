from urllib import request


urlst = [ "https://www.yandex.com/",
            "http://www.baidu.com",
            "http://www.1688.com",
            "https://www.zhihu.com/question/20271508"
            ]
uf = [2]
#page = request.Request( urlst[3] )
#page.add_header( 'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'  )
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}  
page = request.Request( urlst[3], headers = headers )

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
with open( 'zhihu.html', 'wb' ) as f:
    f.write(str.encode(data))
F.write( str(Dco) )
F.close()
