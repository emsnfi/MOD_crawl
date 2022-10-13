from asyncio import threads

from tkinter import *
from thread import *;
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
        # currentThreaname = thread.currentThread()
        self.__result__ = self._target(*self._args, **self._kwargs)

    def get_result(self):
        self.join() #當需要取得結果值的時候阻塞等待子執行緒完成
        return self.__result__



def fun():
    for i in range(10):
        time.sleep(1)
        print("sdfsdf")
        
        
def fun2(ss):
    for i in range(20):
        time.sleep (1)
        print(ss)

def threading1():
    # Call work function
    t1=MyThread(target=fun)
    t1.start()
def threading2(ss):
    # Call work function
    t1=MyThread(target=fun2,args=(ss,))
    t1.start()
root = Tk()
root.geometry('400x500+250+50')
root.title('Test Log Compiler')

toolLabel = Label(root, justify=LEFT, text='Test Log Compiler', font=("Arial",12), height=2, width=200)
toolLabel.pack()
T = Label(root, text="instructions", height=14, width=40, bg='white', font=("Arial",9), relief=SUNKEN, bd=4, justify=LEFT)
T.pack()      
t3 = threading.Thread(target = fun)
t4 = threading.Thread(target = fun2)

t = MyThread(fun)
t2 = MyThread(fun2)
button = Button(root, text = 'Start', command= threading1, width = 8, height = 3, fg = 'black' )
button2 = Button(root, text = 'clik2', command= lambda: threading2("2d"), width = 8, height = 3, fg = 'black' )
# button2 = Button(root, text = 'clik2', command= MyThread(target=fun2).start, width = 8, height = 3, fg = 'black' )
# buttonStop = Button(root, text = 'stop', command = exit , width = 4, height = 2, fg = 'black' )
button.pack(padx = 10, pady = 10)
button2.pack(padx = 20, pady = 10)
root.mainloop()