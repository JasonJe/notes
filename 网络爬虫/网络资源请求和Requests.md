## 3.2 网络资源请求和Requests

>date: 2019-02-05

![](../assets/images/32.jpg)

### 3.2.1 “让HTTP服务于人类”

虽然`Python`标准库中的`urllib`模块已经包含了平常平常我们使用的大多数`HTTP`功能，但是它的`API`使用起来并不自然。[`Kenneth Reitz`](https://www.kennethreitz.org/)大神帮我们准备了一个优雅而简单的`HTTP`库——[`Requests`](https://github.com/requests/requests)。

![Requests库](../assets/images/321_01.png)

互联网的发展让人类获取数据更加地方便，但在繁杂的数据背景下，人类需要自己去组织获取这些繁杂的数据是一件工作量颇大的事情，网络爬虫就是为了解决这种事情而出现的。

`Requests`库旨在简化`HTTP`请求的过程，针对抓取目标的描述和定义，我们利用其制定规则去爬取，然后对获得的数据和网页进行分析与过滤，得到的数据最终能用于其它用途。

### 3.2.2 Requests简明教程

* `get`请求

```python
import requests

r = requests.get('http://httpbin.org/ip')
```

* 构造`url`

>http://httpbin.org/get?key1=value1&key2=value2

构造`url`的请求参数，即`?`后的`query string`。

```python
import requests

d = {'key1': 'value1', 'key2': 'value2'}
r = requests.get('http://httpbin.org/get', params=d)
print(r.url)
```

* 响应正文文本

```python
import requests

r = requests.get('http://httpbin.org/ip')

print(r.text)
print(r.encoding)
```

* 二进制响应对象

```python
import requests

r = requests.get('http://httpbin.org/ip')

print(r.content)
```

* `JSON`响应正文

```python
import requests

r = requests.get('http://httpbin.org/ip')

print(r.json())
print(type(r.json()))
```

* 响应状态

```python
import requests

r = requests.get('http://httpbin.org/ip')

print(r.status_code)
print(r.raise_for_status()) # 响应返回404，使用该语句抛出异常
```

* 响应头

```python
import requests

r = requests.get('http://httpbin.org/ip')

print(r.headers)
```

* 定制请求头

```python
import requests

url = 'http://httpbin.org/headers'

headers = {'user-agent': 'test/0.0.1'}

r = requests.get(url, headers = headers)
print(r.text)
```

* `post`请求——`form`表单形式

```python
import requests

url = 'http://httpbin.org/post'
d = {'key1': 'value1', 'key2': 'value2'}
r = requests.post(url, data = d)
print(r.text)
```

* `post`请求——`JSON`字符串形式

```python
import requests

url = 'http://httpbin.org/post'
s = json.dumps({'key1': 'value1', 'key2': 'value2'})
r = requests.post(url, data = s)
print(r.text)
```

* `post`请求——`multipart`形式

```python
import requests

url = 'http://httpbin.org/post'
files = {'file': open('report.txt', 'rb')}
r = requests.post(url, files = files)
print(r.text)
```

* 获取`cookies`

```python
import requests

url = 'http://httpbin.org/post'
r = requests.get(url)
print(r.cookies)
```

* 带`cookies`请求

```python
import requests

url = 'http://httpbin.org/cookies'
cookies = {'cookies_are': 'test'}
r = requests.get(url, cookies = cookies)
print(r.text)
```

* 设置请求超时

```python
import requests

url = 'http://httpbin.org/get'
r = requests.get(url, timeout = 0.001)
print(r.raise_for_status())
```

* 常见异常

1) `ConnectionError` 由于网络原因，无法建立连接。

2) `HTTPError` 如果响应的状态码不为200，`Response.raise_for_status()`会抛出`HTTPError`异常。

3) `Timeout` 超时异常。

4) `TooManyRedirects` 若请求超过了设定的最大重定向次数，则会抛出一个 TooManyRedirects 异常。

所有requests抛出的异常都继承自`requests.exceptions.RequestException`类。
