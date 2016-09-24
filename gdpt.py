from tkinter import *
import tkinter.messagebox as messagebox
import requests
from html.parser import HTMLParser


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        # checkButton控件的值
        self.movieCheckVar = IntVar()
        self.tvCheckVar = IntVar()
        self.cartoonCheckVar = IntVar()
        self.showCheckVar = IntVar()

        self.grid()
        self.createWidgets()

    def createWidgets(self):
        # 控件初始化
        # 标题
        self.btTitle = Label(self, text='资源列表')
        self.btTitle.grid(row=0, column=0, sticky=W, padx=45, pady=10)
        #搜索框
        self.searchInput = Entry(self)
        self.searchInput.grid(row=0, column=2, sticky=E, pady=10)
        #搜索按钮
        self.searchBtn = Button(self, text='搜索', command=self.quit)
        self.searchBtn.grid(row=0, column=3, sticky=W, padx=5, pady=10)
        # 分类筛选
        self.movieCheck = Checkbutton(self, variable=self.movieCheckVar, text='电影', command=printCheckButton)
        self.movieCheck.grid(row=1, column=1, sticky=W)
        self.tvCheck = Checkbutton(self, variable=self.tvCheckVar, text='电视剧', command=printCheckButton)
        self.tvCheck.grid(row=1, column=1, sticky=E)
        self.cartoonCheck = Checkbutton(self, variable=self.cartoonCheckVar, text='动漫', command=printCheckButton)
        self.cartoonCheck.grid(row=1, column=2, sticky=W)
        self.showCheck = Checkbutton(self, variable=self.showCheckVar, text='综艺', command=printCheckButton)
        self.showCheck.grid(row=1, column=2)

        self.selectTitle = Label(self, text='分类选择')
        self.selectTitle.grid(row=1, column=0, sticky=W, padx=45, pady=10)
        # 显示列表
        self.listBox = Listbox(self, width=100,height=28)
        self.listBox.bind('<Double-Button-1>', printList)
        self.listBox.grid(row=2, column=0, columnspan=4, padx=45)
        # 刷新按钮
        self.flashBtn = Button(self, text='刷新', command=self.quit)
        self.flashBtn.grid(row=3, column=0, sticky=W+E+N+S, padx=45, pady=10)
        # 退出按钮
        self.quitBtn = Button(self, text='离开', command=self.quit)
        self.quitBtn.grid(row=3, column=3, sticky=W+E+N+S, padx=45, pady=10)

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inZfkdItem = None
        self.titleReady = None
        self.dataCH = []
        self.dataID = []

    def handle_starttag(self, tag, attrs):
        # print("start: ",tag)
        if tag == 'td':
            for k, v in attrs:
                if k == 'id' and v == 'zfkd':
                    self.inZfkdItem = 'inside'

        if self.inZfkdItem == 'inside' and tag == 'a':
            for i, j in attrs:
                if i == 'title':
                    # print('英文标题：', j)
                    pass
                if i == 'href':
                    # print('详细链接：', j)
                    print('id: ', j.split('=')[1].split('&')[0])
                    self.dataID.append(j.split('=')[1].split('&')[0])

        if self.inZfkdItem == 'inside' and tag == 'br':
            self.titleReady = 'checked'

    def handle_data(self, data):
        if self.inZfkdItem == 'inside' and self.titleReady == 'checked':
            print('中文标题：', data)
            self.dataCH.append(data)
            self.titleReady = None

    def handle_endtag(self, tag):
        # print("end: ",tag)
        if tag == 'td':
            self.inZfkdItem = None


class MyData():
    def __init__(self):
        self.dataCH = None
        self.dataID = None


def printList(event):
    print(app.listBox.curselection())
    print('s:', app.listBox.get(app.listBox.curselection()))

def printCheckButton():
    print(app.movieCheckVar.get())
    print(app.tvCheckVar.get())
    print(app.cartoonCheckVar.get())
    print(app.showCheckVar.get())


app = Application()
# 设置窗口标题:
app.master.title('GDPT内网获取器')
app.master.geometry('800x630')


newestUrl = 'http://pt.gdut.edu.cn/torrents.php?inclbookmarked=0&picktype=0&incldead=1&spstate=0&page=0'
cookies = {'c_secure_login': 'bm9wZQ%3D%3D',
           'c_secure_pass': '4823182438a4c337f72a62a84f2518e1',
           'c_secure_ssl': 'bm9wZQ%3D%3D',
           'c_secure_tracker_ssl': 'bm9wZQ%3D%3D',
           'c_secure_uid': 'NzI2Nw%3D%3D'}

r = requests.get(newestUrl, cookies=cookies)
r.encoding = 'utf-8'

parser = MyHTMLParser()
parser.feed(r.text)

result = MyData()
result.dataID = parser.dataID
result.dataCH = parser.dataCH


for item in result.dataCH:  # 第一个小部件插入数据
    app.listBox.insert(END, item)

# 主消息循环:
app.mainloop()
