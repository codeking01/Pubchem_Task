"""
    -- coding: utf-8 --
    @Author: codeking
    @Data : 2022/5/4 16:40
    @File : test.py
"""
import time
from threading import Thread


def printtest():
    def test2():
        for i in range(333333):
            print(i)
    def test3():
        for i in range(333333,333333*2):
            print(i)
    def test4():
        for i in range(333333*2,333333*3):
            print(i)

    func1=Thread(target=test2)
    func2=Thread(target=test3)
    func3=Thread(target=test4)
    func1.start()
    func2.start()
    func3.start()
    func1.join()
    func2.join()
    func3.join()

def printtest2():
    # def test2():
        for i in range(100000):
            print(i)

    # func=Thread(target=test2)

if __name__ == '__main__':
    t1=time.time()
    printtest()
    t2=time.time()
    print('时间：',t2-t1)

    # t3=time.time()
    # printtest2()
    # t4=time.time()
    # print('时间：',t4-t3)
    #  6.283333778381348
