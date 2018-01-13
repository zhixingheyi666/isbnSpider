The urllib.request module defines functions and classes which help in opening URLs (mostly HTTP) in a complex world — basic and digest authentication, redirections, cookies and more.

urllib.request模块定义函数和类帮你以复杂的方式打开url，包括基本和摘要的认证，重定向，cookie和其他。

For ftp, file, and data urls and requests explicity handled by legacy URLopener and FancyURLopener classes, this function returns a urllib.response.addinfourl object which can work as context manager and has methods such as

对于ftp,file和 data url ，request对象将被继承的 URLopener 和 FancyURLopener类来处理。这个函数返回一个 urllib.response.addinfourl 对象，此对象将作为一个上下文管理器来工作，并且包括以下的函数：

with open( 'zhihu.html', 'wb' ) as f:
    f.write(str.encode(data))
