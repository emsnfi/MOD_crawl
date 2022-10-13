import time
import threading


class MyThread(threading.Thread):
    def __init__(self, target=None, args=(), **kwargs):
        super(MyThread, self).__init__()
        self._target = target
        self._args = args
        self._kwargs = kwargs

    def run(self):
        if self._target == None:
            return
        self.__result__ = self._target(*self._args, **self._kwargs)

    def get_result(self):
        self.join() #當需要取得結果值的時候阻塞等待子執行緒完成
        return self.__result__

    


# class MyThread (threading.Thread):
 
#     def __init__(self,x):
#         self.__x = x
#         threading.Thread.__init__(self)
 
#     def run (self):
#           print (str(self.__x))

# def te(a, b=2, c=3):
#     print(a, b, c)
#     time.sleep(1)
#     return 1


# st = MyThread(target=te, args=(1,), c=4)
# st.start()
# print('result:',st.get_result())