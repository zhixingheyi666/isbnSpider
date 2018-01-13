#! /usr/bin/env python
# -*- coding: utf-8 -*-

import queue

Q = queue.Queue()
S = set([])

StartPoint = "www.1688.com"
Q.put( StartPoint )
S.add( StartPoint )

while( Q.empty() == False ):
    T = Q.get()
    for point in Pageurl(T):
        if point  not in S:
            Q.put(point)
            S.add(point)

