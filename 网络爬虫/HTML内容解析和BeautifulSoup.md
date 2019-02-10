## 3.3 HTML内容解析和BeautifulSoup

>date: 2019-02-05

![](../assets/images/33.jpg)

### 3.3.1 `HTML`解析器

解析`HTML`是一项自动化的工作，由（所谓的）HTML解析器执行。它们有两个主要目的：

* `HTML`遍历：为程序员提供一个接口，来轻松地访问和修改“HTML代码”。

* `HTML`清理：修正有语法错误的HTML，改善结果标记的布局和缩进样式。

|解析器|使用方法|优势|劣势|
|:--:|:--:|:--:|:--:|
|`Python`标准库|`BeautifulSoup(markup, "html.parser")`|执行速度适中；文档容错能力强|`Python 2.7.3`或`3.2.2`前的版本中文文档的容错能力差|
|`lxml HTML`解析器|`BeautifulSoup(markup, "lxml")`|速度快，文档容错能力强|需要安装`C`语言库|
|`lxml XML`解析器|`BeautifulSoup(markup, ["lxml-xml"])；`<br>`BeautifulSoup(markup, "xml")`|速度快，唯一支持`XML`的解析器|需要安装`C`语言库|
|`html5lib`|`BeautifulSoup(markup, "html5lib")`|最好的容错性，以浏览器的方式解析文档，生成`HTML5`格式的文档|速度慢，不依赖外部扩展|

`BeautifulSoup`支持`Python`标准库中的`HTML`解析器，还支持上述的及清洗器。

### 3.3.2 `BeautifulSoup`简明教程

`BeautifulSoup` 是一个可以从`HTML`或`XML`文件中提取数据的`Python`库.它能够通过你喜欢的转换器实现惯用的文档导航,查找,修改文档的方式.`BeautifulSoup`会帮你节省数小时甚至数天的工作时间.

* `HTML`结构

`HTML`页面是由基本元素及属性组成的，其基本结构由文档类型声明、`html`标签对、`head`标签对、`body`标签对组成

1) 文档类型声明`<!DOCTYPE html>`是用来说明该文档是`HTML`文档，所有`HTML`文档开始于文档声明之后，说明了文档的类型以及其遵守的标准规范集。

2) `html`标签对是由成对的`<html></html>`组成的，其中`<html>`位于文档最前面，用来表示`HTML`文档的开始；`</html>`位于文档最后面，用来表示`HTML`文档的结束；中间的部分是文档的头部和主题。

3) `<head>`标签对包含有关`HTML`文档的信息，可以包含一些辅助性标签，如`<title>`、`<base>`、`<link>`、`<meta>`、`<style>`、`<script>`等。

4) `<body>`标签对是`HTML`文档的主体部分，在此标签中可以包含`<p>`、`<h1>`、`<br>`等众多标签，`<body>`标签出现在`</head>`标签之后，且必须在闭标签`</html>`之前闭合。`<body>`标签中还有很多属性，用于设置文档的背景颜色、文本颜色、链接颜色、边距等。

```html
<!DOCTYPE html> 
<html>
    <head>
        <meta charset="utf-8"/>
        <title>标题</title>
    </head>
    <body>
        <p>段落</p>
    </body>
</html>
```

* `BeautifulSoup`对象

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc, 'html.parser') # BeautifulSoup 对象

tag = soup.b # Tag 对象
type(tag) # <class 'bs4.element.Tag'>

tag.name # Tag 对象名称

tag['class'] # Tag 的属性
tag.attrs

tag.string # NavigableString 对象
type(tag.string) # <class 'bs4.element.NavigableString'>
unicode_string = unicode(tag.string) # 将 NavigableString 对象转换成Unicode字符串
tag.string.replace_with("No longer bold") # 替换成其它的字符串

markup = "<b><!--Hey, buddy. Want to buy a used parser?--></b>"
soup = BeautifulSoup(markup)
comment = soup.b.string # Comment 对象，特殊类型的 NavigableString 对象
type(comment) # <class 'bs4.element.Comment'>
```

* 指定文档解析器

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc, 'html.parser')
soup = BeautifulSoup(html_doc, 'lxml')
soup = BeautifulSoup(html_doc, 'html5lib')
```

* 标准缩进格式输出

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.prettify())
```

* 编码

```python
from bs4 import BeautifulSoup

markup = "<h1>Sacr\xc3\xa9 bleu!</h1>"
soup = BeautifulSoup(markup)
soup.h1 # <h1>Sacré bleu!</h1>
soup.h1.string # u'Sacr\xe9 bleu!'
soup.original_encoding # 'utf-8' 获取自动编码的结果

soup = BeautifulSoup(markup, from_encoding="iso-8859-8") # 指定编码方式

soup = BeautifulSoup(markup, exclude_encodings=["ISO-8859-7"]) # 排除自动使用编码的格式

# 通过Beautiful Soup输出文档时,不管输入文档是什么编码方式,输出编码均为UTF-8编码

print(soup.prettify("latin-1")) # 指定编码方式输出
print(soup.p.encode("latin-1"))
```

* 浏览`HTML`结构

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc, 'html.parser')

soup.title

soup.title.name

soup.title.string

soup.title.parent.name

soup.p

soup.p['class']

soup.a

soup.find_all('a')

soup.find(id="link3")

for link in soup.find_all('a'):
    print(link.get('href'))

soup.get_text()
soup.get_text("|") # 指定tag内容的分隔符，u'\nI linked to |example.com|\n'
soup.stripped_strings # 文本列表生成器
```

参考链接：

* [BeautifulSoup 文档](https://beautifulsoup.readthedocs.io/zh_CN/latest/)
