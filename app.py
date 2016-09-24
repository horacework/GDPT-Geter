import sys
import requests
from html.parser import HTMLParser

url = 'http://pt.gdut.edu.cn'
url2 = 'http://pt.gdut.edu.cn/torrents.php?inclbookmarked=0&picktype=0&incldead=1&spstate=0&page=0'
url3 = 'http://pt.gdut.edu.cn/download.php?id=62116'
url4 = 'http://pt.gdut.edu.cn/torrents.php?search=%E4%BA%BA%E7%B1%BB%E6%B8%85%E9%99%A4%E8%AE%A1%E5%88%92&notnewword=1'

cookies = {'c_secure_login': 'bm9wZQ%3D%3D',
           'c_secure_pass': '4823182438a4c337f72a62a84f2518e1',
           'c_secure_ssl': 'bm9wZQ%3D%3D',
           'c_secure_tracker_ssl': 'bm9wZQ%3D%3D',
           'c_secure_uid': 'NzI2Nw%3D%3D'}


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inZfkdItem = None
        self.titleReady = None

    def handle_starttag(self, tag, attrs):
        # print("start: ",tag)
        if tag == 'td':
            for k, v in attrs:
                if k == 'id' and v == 'zfkd':
                    self.inZfkdItem = 'inside'

        if self.inZfkdItem == 'inside' and tag == 'a':
            for i, j in attrs:
                if i == 'title':
                    print('英文标题：', j)
                if i ==  'href':
                    print('详细链接：', j)
                    print('id: ',j.split('=')[1].split('&')[0])

        if self.inZfkdItem == 'inside' and tag == 'br':
            self.titleReady = 'checked'

    def handle_data(self, data):
        if self.inZfkdItem == 'inside' and self.titleReady == 'checked':
            print('中文标题：', data)
            self.titleReady = None

    def handle_endtag(self, tag):
        # print("end: ",tag)
        if tag == 'td':
            self.inZfkdItem = None


# r = requests.get(url, cookies=cookies)
# r.encoding = 'utf-8'

r2 = requests.get(url2, cookies=cookies)
r2.encoding = 'utf-8'

# print(r.text)
# print(r.headers['content-type'])
# print(r.text)

parser = MyHTMLParser()
# parser.feed("<html><head><title>Test</title></head><body><h1>Parse me!</h1></body></html>")
parser.feed(r2.text)
