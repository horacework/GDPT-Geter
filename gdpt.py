from tkinter import *
import tkinter.messagebox as messagebox
import requests
from html.parser import HTMLParser
import os
# from config import cookies
import PIL.Image
import PIL.ImageTk
import json


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        # 主窗体大小，标题
        self.master.title('GDPT内网获取器')
        self.master.geometry('800x660')
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
        # 搜索框
        self.searchInput = Entry(self)
        self.searchInput.grid(row=0, column=2, sticky=E, pady=10)
        # 搜索按钮
        self.searchBtn = Button(self, text='搜索', command=searchKey)
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
        self.listBox = Listbox(self, width=100, height=28)
        self.listBox.bind('<Double-Button-1>', printList)
        self.listBox.grid(row=2, column=0, columnspan=4, padx=45)
        # 刷新按钮
        self.flashBtn = Button(self, text='刷新', command=change)
        self.flashBtn.grid(row=3, column=0, sticky=W + E + N + S, padx=45, pady=10)
        # 退出按钮
        self.quitBtn = Button(self, text='离开', command=cleanAndQuit)
        self.quitBtn.grid(row=3, column=3, sticky=W + E + N + S, padx=45, pady=10)

    def clearListBox(self):
        self.listBox.delete(0, END)

    def flashListBox(self, data):
        if len(data) != 0:
            self.clearListBox()
            for i in range(len(data)):
                app.listBox.insert(END, data[i])
                if not i % 2:
                    app.listBox.itemconfig(i, bg='#f0f0ff')
        else:
            messagebox.showinfo('提示', '获取数据失败')

    def hide(self):
        self.master.withdraw()

    def show(self):
        self.master.update()
        self.master.deiconify()

    def openLogin(self):
        self.hide()
        subFrame = LoginFrame()


class LoginFrame(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master)
        # self.master.geometry('1200x300')
        self.session = requests.session()

        self.master.title('Login')

        self.createWidgets()



    def createWidgets(self):
        Label(self, text="账号名：").grid(sticky=E)
        Label(self, text="密码：").grid(sticky=E)
        Label(self, text="验证码：").grid(sticky=E)

        self.userInput = Entry(self)
        self.userInput.grid(row=0, column=1)
        self.passInput = Entry(self)
        self.passInput.grid(row=1, column=1)
        self.codeInput = Entry(self)
        self.codeInput.grid(row=2, column=1)

        im = PIL.Image.open('code.png')
        photo = PIL.ImageTk.PhotoImage(im)
        label = Label(self, image=photo)
        label.image = photo
        label.grid(row=0, column=2, columnspan=2, rowspan=2, sticky=W + E + N + S, padx=0, pady=0)

        button1 = Button(self, text='登录', command=self.getVCodeAndSessionId)
        button1.grid(row=3, column=2)

        button2 = Button(self, text='退出', command=self.exitPro)
        button2.grid(row=3, column=3)

    def loginAction(self):
        userInfo = {
            'account': self.userInput,
            'passwd': self.passInput,
            'vcode': self.codeInput
        }
        r = self.session.post('http://pt.gdut.edu.cn/v2/login/', userInfo)

        print(r.text)


    def exitPro(self):
        quit()

    def getVCodeAndSessionId(self):
        # TODO 获取验证码png和当前sessionID
        r = self.session.get('http://pt.gdut.edu.cn/v2/login/')
        # kv = requests.utils.dict_from_cookiejar(r.cookies)
        r.encoding = 'utf-8'
        print(r.text)



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
                    self.dataID.append(j.split('=')[1].split('&')[0])

        if self.inZfkdItem == 'inside' and tag == 'br':
            self.titleReady = 'checked'

    def handle_data(self, data):
        if self.inZfkdItem == 'inside' and self.titleReady == 'checked':
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


class MyUrlConnect():

    def __init__(self, cookiesConfig):
        self.normalUrl = 'http://pt.gdut.edu.cn/torrents.php?inclbookmarked=0&picktype=0&incldead=1&spstate=0&page='
        self.searchUrl = 'http://pt.gdut.edu.cn/torrents.php?notnewword=1&search='
        self.selectUrl = 'http://pt.gdut.edu.cn/torrents.php?'
        self.downloadUrl = 'http://pt.gdut.edu.cn/download.php?id='
        self.cookies = cookiesConfig

    def connectNormalUrl(self, attr):
        r = requests.get(self.normalUrl + str(attr), cookies=self.cookies)
        r.encoding = 'utf-8'
        return r

    def connectSearchUrl(self, keyword):
        r = requests.get(self.searchUrl + keyword, cookies=self.cookies)
        r.encoding = 'utf-8'
        return r

    def connectSelectUrl(self, movie, tv, cartoon, show):
        url = self.selectUrl
        if movie == 1:
            url += "&cat401=1"
        if tv == 1:
            url += "&cat402=1"
        if cartoon == 1:
            url += "&cat405=1"
        if show == 1:
            url += "&cat403=1"
        r = requests.get(url, cookies=self.cookies)
        r.encoding = 'utf-8'
        return r

    def connectDownloadUrl(self, id):
        r = requests.get(self.downloadUrl + str(id), cookies=self.cookies)
        with open('download/[GDPT]' + str(id) + '.torrent', 'wb') as code:
            code.write(r.content)


def printList(event):
    print('s:', app.listBox.get(app.listBox.curselection()))
    print('id:', result.dataID[app.listBox.curselection()[0]])
    torrentID = result.dataID[app.listBox.curselection()[0]]
    # 下载种子
    connection.connectDownloadUrl(torrentID)
    # 系统打开种子
    os.system(os.getcwd() + '\\download\\' + '[GDPT]' + str(torrentID) + '.torrent')


def searchKey():
    # 关键字搜索
    keyword = app.searchInput.get()
    if keyword == '':
        messagebox.showinfo('警告', '请输入正确的搜索关键字')
    else:

        searchText = connection.connectSearchUrl(keyword)
        searchParser = MyHTMLParser()
        searchParser.feed(searchText.text)
        result.dataID = searchParser.dataID
        result.dataCH = searchParser.dataCH
        app.flashListBox(result.dataCH)


def printCheckButton():
    # 筛选搜索
    selectText = connection.connectSelectUrl(app.movieCheckVar.get(), app.tvCheckVar.get(), app.cartoonCheckVar.get(),
                                             app.showCheckVar.get())
    selectParser = MyHTMLParser()
    selectParser.feed(selectText.text)
    result.dataID = selectParser.dataID
    result.dataCH = selectParser.dataCH
    app.flashListBox(result.dataCH)


def cleanAndQuit():
    # 清除种子残留并退出
    currentPath = os.getcwd() + '\\download\\'
    fileList = os.listdir(currentPath)
    for fileName in fileList:
        print(fileName)
        if re.match('^\[GDPT\][0-9]*\.torrent$', fileName) is not None:
            os.remove(currentPath + fileName)
    exit()


def flashAndUpdate():
    # 获取页面信息
    f = connection.connectNormalUrl(0)
    f.encoding = 'utf-8'
    # 解析页面信息
    flashParser = MyHTMLParser()
    flashParser.feed(f.text)
    # 存储页面信息
    result.dataID = flashParser.dataID
    result.dataCH = flashParser.dataCH
    # 刷新控件上的信息
    app.flashListBox(result.dataCH)


def change():
    tl = Toplevel()
    # 设置tl的title
    tl.title('hello Toplevel')
    # 设置tl在宽和高
    tl.geometry('400x300')
    # 为了区别root和tl，我们向tl中添加了一个Label
    Label(tl, text='hello label').pack()
    Button(tl, text='xchange', command=app.show).pack()

    app.hide()

def loadJsonFile(filename):
    # 读取json文件并返回json数组
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

app = Application()

result = MyData()


# TODO 首先判断是否含有cookies信息，没有则登录，有就开始连接
fileName = 'config.json'
#if os.path.exists(fileName):
if False:
    data = loadJsonFile(fileName)
    connection = MyUrlConnect(data)

    flashAndUpdate()
else:
    # TODO 弹出登录窗口，获取cookies
    app.openLogin()
if False:
    # 弹出登录窗口
    pass

else:
    # 直接使用cookies获取资源
    pass


# TODO 其次判断连接是否成功


# r = connection.connectNormalUrl(0)
# r.encoding = 'utf-8'
#
# parser = MyHTMLParser()
# parser.feed(r.text)


# result.dataID = parser.dataID
# result.dataCH = parser.dataCH
#
# app.flashListBox(result.dataCH)



# 主消息循环:
app.mainloop()
