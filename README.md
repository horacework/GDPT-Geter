# GDPT-Geter

GDPT内网资源获取器

项目入口文件： [gdpt.py](https://github.com/horacework/GDPT-Geter/blob/master/gdpt.py)

**已实现功能：**

* 获取数据检测

* 类型筛选

* 关键字搜索

* 双击即可下载并打开种子

* 离开按钮可清空缓存种子

**待完善功能：**

* 登录获取cookies功能

**注意** 登录功能开发受阻,无法模拟正常登录，多次试验皆被警告，为保实验室IP不被封，暂时不开发此功能


**使用方法：**   （暂时）

* 根据GDPT规定，安装 [uTorrent](http://www.utorrent.com/intl/zh/) 软件，并将设为系统默认打开.torrent文件的软件

* 将config-example.json重命名为config.json

* 补全config.json内cookies信息(在浏览器内登录一次，之后提取cookies)

* 运行gdpt.py（运行环境：Python 3.5.0，各类依赖库的安装请自理）