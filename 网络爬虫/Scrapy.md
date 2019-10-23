## 3.5 `Scrapy`

>date: 2019-02-11

![](../assets/images/35.jpg)

### 3.5.1 `Scrapy`架构

`Scrapy`是一个为了爬取网站数据，提取结构性数据而编写的爬虫框架，使用了`Twisted`异步网络库来处理网络通讯。相较于`Requests` + `BeautifulSoup`组合成爬虫流水线，`Scrapy`更像是一个开箱即用的流水线。它更加偏向于生产环境下的爬虫，包含了下载器，解析器，日志，异常处理等等模块。它实现了更加高级的定制化，更加方便管理，灵活，可配置。

![Scrapy架构图](../assets/images/351_01.png)

`Scrapy Engine`: 这是引擎，负责`Spiders`、`ItemPipeline`、`Downloader`、`Scheduler`中间的通讯，信号、数据传递等等！

`Scheduler`(调度器): 它负责接受引擎发送过来的`requests`请求，并按照一定的方式进行整理排列，入队、并等待`Scrapy Engine`(引擎)来请求时，交给引擎。

`Downloader`（下载器）：负责下载`Scrapy Engine`(引擎)发送的所有`Requests`请求，并将其获取到的`Responses`交还给`Scrapy Engine`(引擎)，由引擎交给`Spiders`来处理，

`Spiders`：它负责处理所有`Responses`,从中分析提取数据，获取`Item`字段需要的数据，并将需要跟进的URL提交给引擎，再次进入`Scheduler`(调度器)，

`Item Pipeline`：它负责处理`Spiders`中获取到的`Item`，并进行处理，比如去重，持久化存储（存数据库，写入文件，总之就是保存数据用的）

`Downloader Middlewares`（下载中间件）：你可以当作是一个可以自定义扩展下载功能的组件

`Spider Middlewares`（`Spider`中间件）：你可以理解为是一个可以自定扩展和操作引擎和`Spiders`中间‘通信‘的功能组件（比如进入`Spiders`的`Responses`;和从`Spiders`出去的`Requests`）

**数据流过程：**

1) 引擎打开一个网站，找到处理该网站的`Spider`并向该`Spider`请求第一个要爬取的`URL(s)`。

2) 引擎从`Spider`中获取到第一个要爬取的`URL`并在调度器(`Scheduler`)以`Request`调度。

3) 引擎向调度器请求下一个要爬取的`URL`。

4) 调度器返回下一个要爬取的`URL`给引擎，引擎将`URL`通过下载中间件(请求`request`方向)转发给下载器(`Downloader`)。

5) 一旦页面下载完毕，下载器生成一个该页面的`Response`，并将其通过下载中间件(返回`response`方向)发送给引擎。

6) 引擎从下载器中接收到`Response`并通过`Spider`中间件(输入方向)发送给`Spider`处理。

7) `Spider`处理`Response`并返回爬取到的`Item`及(跟进的)新的`Request`给引擎。

8) 引擎将(`Spider`返回的)爬取到的`Item`给`Item Pipeline`，将(`Spider`返回的)`Request`给调度器。

9) (从第二步)重复直到调度器中没有更多的`request`，引擎关闭该网站。

### 3.5.2 `Scrapy`简明教程

* 项目结构

安装完`Scrapy`后，在命令行中输入`scrapy startproject demo`，输入`cd demo`进入项目文件夹。

项目目录结构如下：

```shell
├── demo
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── __pycache__
│   ├── settings.py
│   └── spiders
│       ├── __init__.py
│       └── __pycache__
└── scrapy.cfg
```

在上面的目录结构中，`demo`是一个模块，所有的项目代码都在这个模块内定义并添加。

1) `items.py`是定义存储对象的文件，决定爬取哪些项目；

2) `middlewares.py`是中间件，一般不进行修改，主要负责组件之间的请求和响应；

3) `pipelines.py`是管道文件，决定爬取后的数据处理和存储；

4) `settings.py`是项目的设置文件，设置项目管道数据的处理文件、爬虫频率等。

5) `spiders`文件夹主要防止爬虫主题文件，用于实现爬虫逻辑。

6) `scrapy.cfg`是这个项目的配置文件，包括与项目设置的项目名称：

```shell
# Automatically created by: scrapy startproject
#
# For more information about the [deploy] section see:
# https://scrapyd.readthedocs.io/en/latest/deploy.html

[settings]
default = demo.settings # 项目的设置文件名

[deploy]
#url = http://localhost:6800/
project = demo # 项目名称
```

* 命令行

```shell
scrapy startproject project_name # 创建新的项目

cd  project_name # 进入项目文件夹

scrapy genspider mydomain mydomain.com # 创建一个spider

scrapy fetch # 使用Scrapy下载器获取URL

scrapy runspider # 运行独立的蜘蛛而不创建项目

scrapy settings # 指定项目设置值

scrapy shell # 给定URL的交互式抓取模块

scrapy startproject # 创建一个新的Scrapy项目

scrapy version # 显示Scrapy版本

scrapy view # 使用Scrapy下载器获取URL并在浏览器中显示内容

scrapy crawl # 用于抓取使用蜘蛛的数据

scrapy check # 检查爬行命令返回的项目

scrapy list # 显示项目中可用蜘蛛的列表

scrapy edit # 可以使用编辑器编辑蜘蛛

scrapy parse # 解析蜘蛛给定的URL

scrapy bench # 用于运行快速基准测试（Benchmark指出Scrapy每分钟可以抓取多少页面）

scrapy -h # 查看帮助
```

* 定义存储对象

打开`./demo/items.py`文件，在其中定义抓取的数据容器。它的工作像简单的`Python`，类似定义数据库中的栏位，来结构化、细化数据的归属。

```python
import scrapy

class DemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    create_time = scrapy.Field()
```

例如在批量爬取文章的时候，在里面定义`scrapy.Field()`来指定对应的文章标题、文章内容、作者、创建时间、阅读量等等的定义，同时也能对未定义的字段提供填充功能防止出错。

* 定义爬虫

以及通过`scrapy genspider mydomain mydomain.com`命令创建了一个爬虫类，进入`spides`文件夹后，打开`./spiders/mydomain.py`文件。

```python
# -*- coding: utf-8 -*-
import scrapy

class MydomainSpider(scrapy.Spider):
    name = 'mydomain'
    allowed_domains = ['mydomain.com']
    start_urls = ['http://mydomain.com/']

    def parse(self, response):
        pass
```

要建立一个爬虫，必须使用`scrapy.Spider`创建一个子类，并必须确定单个强制的属性`name, allowed_domains, start_urls`和一个方法`parse()`。

1) `name`是爬虫的名称，其它爬虫不能与其相同；

2) `allowed_domains`是搜索的域名范围，亦即爬虫的约束范围，规定只能爬取该域名下的网页，不存在的页面会被忽略掉；

3) `start_urls`需要爬取的`URL`的元祖/列表，爬虫从这里开始爬取，其他的子`URL`会从这些起始`URL`中生成；

4) `parse()`定义解析的方法，解析`response`，提取结构化数据，即生成`item`；同时生成下一页`URL`请求。

由上添加`parse_item()`方法。

```python
# -*- coding: utf-8 -*-
import scrapy
from ..items import DemoItem

class MydomainSpider(scrapy.Spider):
    name = 'mydomain'
    allowed_domains = ['mydomain.com']
    start_urls = ['http://mydomain.com/']

    def parse(self, response):
        urls = response.xpath('')
        for url in urls:
            yield scrapy.Request(url, callback = self.parse_item) # 发送请求。回调给parse_item处理

    def parse_item(self, response):
        item = DemoItem()
        item['title'] = response.xpath('')
        item['content'] = response.xpath('')
        item['author'] = response.xpath('')
        item['create_time'] = response.xpath('')
```

命令行键入`scrapy crawl mydomain -o mydomain.csv`即可以开始进行采集。

* 定义存储

当`item`在`Spider`中被手机后，会被传递给`pipeline`，其按照定义的顺序处理`item`。

`pipeline`大多数用于验证爬取的数据，对数据进行查重，将数据进行持久化等。

```python
# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem

class MydomainPipeline(object):
    def process_item(self, item, spider):
        if item['author']:
            # processing
            return item
        else:
            raise DropItem("Missing author in %s" % item)
```

* 选择器

在定义`spider`时候，需要在`HTML`提取数据，`Scarpy`是基于`lxml`构建选择器的，它提供了下面四个基本方法：

1) `xpath()`传入[`xpath`](http://www.w3school.com.cn/xpath/index.asp)表达式，返回该表达式所对应的所有节点的列表；

2) `extract()`序列化该节点为`Unicode`字符串并返回列表；

3) `css()`传入`CSS`表达式，返回表达式对应所有节点的列表；

4) `re()`传入正则表达式，返回`Unicode`字符串并返回列表。

* 设置文件

对于整个爬虫工程，`Scrapy`使用`settings.py`进行配置，常见的配置项如下：

```python
# -*- coding: utf-8 -*-
 
BOT_NAME = 'demo' # Scrapy项目的名字,这将用来构造默认 User-Agent,同时也用来log,当您使用 startproject 命令创建项目时其也被自动赋值。
 
SPIDER_MODULES = ['demo.spiders'] # Scrapy搜索spider的模块列表 默认: [xxx.spiders]
NEWSPIDER_MODULE = 'demo.spiders' # 使用 genspider 命令创建新spider的模块。默认: 'xxx.spiders'

USER_AGENT = 'demo (+http://www.mydomain.com)' # 爬取的默认User-Agent，除非被覆盖

ROBOTSTXT_OBEY = True # 如果启用, Scrapy将会采用 robots.txt 策略 (https://baike.baidu.com/item/robots%E5%8D%8F%E8%AE%AE/2483797?fr=aladdin&fromid=9518761&fromtitle=robots.txt)
 
CONCURRENT_REQUESTS = 32 # Scrapy downloader 并发请求(concurrent requests)的最大值,默认: 16

DOWNLOAD_DELAY = 3 # 为同一网站的请求配置延迟（默认值：0）。下载器在下载同一个网站下一个页面前需要等待的时间,该选项可以用来限制爬取速度,减轻服务器压力。同时也支持小数:0.25 以秒为单位

# 下载延迟设置只有一个有效
CONCURRENT_REQUESTS_PER_DOMAIN = 16 # 对单个网站进行并发请求的最大值。
CONCURRENT_REQUESTS_PER_IP = 16 # 对单个IP进行并发请求的最大值。如果非0,则忽略 CONCURRENT_REQUESTS_PER_DOMAIN 设定,使用该设定。也就是说,并发限制将针对IP,而不是网站。该设定也影响 DOWNLOAD_DELAY: 如果 CONCURRENT_REQUESTS_PER_IP 非0,下载延迟应用在IP而不是网站上。

COOKIES_ENABLED = False # 禁用Cookie（默认情况下启用）

TELNETCONSOLE_ENABLED = False # 禁用Telnet控制台（默认启用）

DEFAULT_REQUEST_HEADERS = { # 覆盖默认请求标头：
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
}

SPIDER_MIDDLEWARES = { # 启用或禁用蜘蛛中间件
   'demo.middlewares.DemoSpiderMiddleware': 543,
}

DOWNLOADER_MIDDLEWARES = { # 启用或禁用下载器中间件
   'demo.middlewares.MyCustomDownloaderMiddleware': 543,
}

EXTENSIONS = { # 启用或禁用扩展程序
   'scrapy.extensions.telnet.TelnetConsole': None,
}

ITEM_PIPELINES = { # 配置项目管道
   'demo.pipelines.MydomainPipeline': 300,
}

AUTOTHROTTLE_ENABLED = True # 启用和配置AutoThrottle扩展（默认情况下禁用）

AUTOTHROTTLE_START_DELAY = 5 # 初始下载延迟

AUTOTHROTTLE_MAX_DELAY = 60 # 在高延迟的情况下设置的最大下载延迟

AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0 # Scrapy请求的平均数量应该并行发送每个远程服务器

AUTOTHROTTLE_DEBUG = False # 启用显示所收到的每个响应的调节统计信息：
 
# 启用和配置HTTP缓存（默认情况下禁用）
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
```

参考链接：

* [Scrapy 文档](https://scrapy-chs.readthedocs.io/zh_CN/latest/intro/overview.html)