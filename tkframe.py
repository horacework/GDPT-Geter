from tkinter import *
import tkinter.messagebox as messagebox


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        # self.pack()
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.btTitle = Label(self, text='资源列表')
        self.btTitle.grid(row=0, column=0,sticky=W, padx=45, pady=10)
        # self.nameInput = Entry(self)
        # self.nameInput.grid(row=0, column=1)
        # self.alertButton = Button(self, text='Hello', command=self.hello)
        # self.alertButton.grid(row=1, column=0)
        # self.quitButton = Button(self, text='quit', command=self.quit)
        # self.quitButton.grid(row=1, column=1)

    # def hello(self):
    #     name = self.nameInput.get() or 'world'
    #     messagebox.showinfo('Message', 'Hello, %s' % name)
def printList(event):
    print('s:', listb.get(listb.curselection()))

app = Application()
# 设置窗口标题:
app.master.title('GDPT内网获取器')
app.master.geometry('800x600')

li = ['C','python','php','html','SQL','java','aa','aa','ss','C','python','php','html','SQL','java','aa','aa','ss']
movie = ['CSS','jQuery','Bootstrap']
listb = Listbox(app, width=100)          # 创建两个列表组件
listb.bind('<Double-Button-1>', printList)

for item in li:                 # 第一个小部件插入数据
    listb.insert(END, item)

listb.grid(row=2, column=0, columnspan=4, padx=45)           # 将小部件放置到主窗口中

# 主消息循环:
app.mainloop()
