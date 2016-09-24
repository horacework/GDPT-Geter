from tkinter import *
import tkinter.messagebox as messagebox
import requests
from html.parser import HTMLParser


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        # 控件初始化
        self.btTitle = Label(self, text='资源列表')
        self.btTitle.grid(row=0, column=0, sticky=W, padx=45, pady=10)

        self.listBox = Listbox(self, width=100)
        self.listBox.bind('<Double-Button-1>', printList)
        self.listBox.grid(row=2, column=0, columnspan=4, padx=45)


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
    print('s:', app.listBox.get(app.listBox.curselection()))


app = Application()
# 设置窗口标题:
app.master.title('GDPT内网获取器')
app.master.geometry('800x600')

# li = ['C', 'python', 'php', 'html', 'SQL', 'java', 'aa', 'aa', 'ss', 'C', 'python', 'php', 'html', 'SQL', 'java', 'aa',
#       'aa', 'ss']

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
