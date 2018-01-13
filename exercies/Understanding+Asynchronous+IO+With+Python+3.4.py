
# coding: utf-8

# http://python.jobbole.com/87431/
# http://sahandsaba.com/understanding-asyncio-node-js-python-3-4.html
# 在这里也使用了一个 log_execution_time 装饰器来统计斐波那契函数的计算时间。
# 
# 程序中采用的 斐波那契算法 是故意使用最慢的一种的(指数复杂度)。这是因为这篇文章的主题不是关于斐波那契的(可以参考我的这篇文章,这是一个关于斐波那契对数复杂度的算法)，同时因为比较慢，我可以更容易地展示一些概念。下面是Python的做法，它将使用数倍的时间。

# In[5]:


from functools import wraps
from threading import Thread
from time import sleep
from time import time
import pdb


# In[6]:


def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        return_value = func(*args, **kwargs)
        message = "Executing {} took {:.03} seconds. ".format(func.__name__,time() - start)
        print(message)
        return return_value
    return wrapper


# In[7]:


def fib(n):
    return fib(n - 1) + fib(n - 2) if n > 1 else n


# In[8]:


timed_fib = log_execution_time(fib)


# In[9]:


def print_hello():
    print("{} - Hello World!".format(int(time())))
    sleep(3)
    
def read_and_process_input():
    while True:
        try:
            n = int(input())
            #if not isinstance(n,int):
            #    continue
        except:
            pass
        print("fib({}) = {}".format(n, timed_fib(n)))


# In[10]:


def main():
    # Second thread will print the hello message. Starting as a daemon means
    # the thread will not prevent the process from exiting.
    t = Thread(target = print_hello)
    #pdb.set_trace()
    t.daemon = True
    t.start()
    # Main thread will read and process input
    read_and_process_input()


# In[12]:


if __name__ == '__main__':
    main()

