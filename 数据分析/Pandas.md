## 7.4 `Pandas`

>date: 2019-04-09

![](../assets/images/74.jpg)

### 7.4.1 基本数据结构

* `Series`

```python
>>> import pandas as pd
>>> import numpy as np
>>>
>>> s = pd.Series([1, 3, -2, 4]) # 创建一个 Series 对象
>>> s
0    1
1    3
2   -2
3    4
dtype: int64
>>> s.values # 获取值数组
array([ 1,  3, -2,  4], dtype=int64)
>>> s.index # 获取索引数组
RangeIndex(start=0, stop=4, step=1)
>>> s.index = ['a', 'b', 'c', 'd'] # 修改索引数组
>>> s
a    1
b    3
c   -2
d    4
dtype: int64
>>>
>>> s = pd.Series([1, 3, -2, 4], index = ['a', 'b', 'c', 'd']) # 创建时指定索引数组
>>> s
a    1
b    3
c   -2
d    4
dtype: int64
>>> s.values
array([ 1,  3, -2,  4], dtype=int64)
>>> s.index
Index(['a', 'b', 'c', 'd'], dtype='object')
>>>
>>> s['a'] # 类似字典方式索引取值
1
>>> s['b'] = 5 # 修改值
>>> s[['b', 'c', 'd']]
b    5
c   -2
d    4
dtype: int64
>>>
>>> s[s > 0] # 根据数值取值
a    1
b    5
d    4
dtype: int64
>>> s * 2 # 标量乘法
a     2
b    10
c    -4
d     8
dtype: int64
>>> np.exp(s) # 数学计算
a      2.718282
b    148.413159
c      0.135335
d     54.598150
dtype: float64
>>>
>>> 'a' in s # 可看作字典进行处理
True
>>> 'e' in s
False
>>>
>>> s = pd.Series({'a': 1, 'b': 3, 'c': -2, 'd': 4}) # 以字典的方式创建
>>> s
a    1
b    3
c   -2
d    4
dtype: int64
>>>
>>> s1 = pd.Series(s, index = ['a', 'b', 'c', 'e'])
>>> s1 # 不存在于 s 的索引，其值为 NaN
a    1.0
b    3.0
c   -2.0
e    NaN
dtype: float64
>>> pd.isnull(s1) # 检测缺失数据
a    False
b    False
c    False
e     True
dtype: bool
>>> s1.isnull()
a    False
b    False
c    False
e     True
dtype: bool
>>> pd.notnull(s1) # 检测非缺失数据
a     True
b     True
c     True
e    False
dtype: bool
>>> s1.notnull()
a     True
b     True
c     True
e    False
dtype: bool
>>>
>>> s + s1 # 根据索引进行计算，其中一方有，而另一方无的数据置为 NaN
a    2.0
b    6.0
c   -4.0
d    NaN
e    NaN
dtype: float64
>>>
>>> s1.name = 'series_name' # Series 名称
>>> s1.index.name = 'series_index_name' # 索引名称
>>>
>>> s1
series_index_name
a    1.0
b    3.0
c   -2.0
e    NaN
Name: series_name, dtype: float64
```

* `DataFrame`

```python
>>> data = {'first': ['a', 'b', 'b', 'c', 'c', 'c'], 'second': [1, 1, 2, 1, 2, 3], 'thrid': [100, 100, 200, 200, 300, 300]}
>>>
>>> df = pd.DataFrame(data) # 以字典方式创建 DataFrame 对象，其中 key 为列名， index 自动变为有序序列
>>> df
  first  second  thrid
0     a       1    100
1     b       1    100
2     b       2    200
3     c       1    200
4     c       2    300
5     c       3    300
>>>
>>> df.head() # 展示前 5 行数据
  first  second  thrid
0     a       1    100
1     b       1    100
2     b       2    200
3     c       1    200
4     c       2    300
>>> df.head(3) # 指定展示前 3 行数据
  first  second  thrid
0     a       1    100
1     b       1    100
2     b       2    200
>>>
>>> pd.DataFrame(data, columns = ['thrid', 'second', 'first']) # 指定列顺序
   thrid  second first
0    100       1     a
1    100       1     b
2    200       2     b
3    200       1     c
4    300       2     c
5    300       3     c
>>>
>>> df1 = pd.DataFrame(data, columns = ['fourth', 'thrid', 'second', 'first'], index = ['one', 'two', 'three', 'four', 'five', 'six']) # 指定 index，传入列在数据中找不到，结果产生缺失值
>>> df1
      fourth  thrid  second first
one      NaN    100       1     a
two      NaN    100       1     b
three    NaN    200       2     b
four     NaN    200       1     c
five     NaN    300       2     c
six      NaN    300       3     c
>>> df1.columns # 获取列数组
Index(['fourth', 'thrid', 'second', 'first'], dtype='object')
>>> df1['second'] # 索引列
one      1
two      1
three    2
four     1
five     2
six      3
Name: second, dtype: int64
>>> df1.first # 类似字典索引列
<bound method NDFrame.first of       fourth  thrid  second first
one      NaN    100       1     a
two      NaN    100       1     b
three    NaN    200       2     b
four     NaN    200       1     c
five     NaN    300       2     c
six      NaN    300       3     c>
>>>
>>> df1.loc['three'] # 索引指定行
fourth    NaN
thrid     200
second      2
first       b
Name: three, dtype: object
>>> df1['fourth'] = 10.01 # 修改指定列
>>> df1['fourth'] = np.arange(6)
>>>
>>> s = pd.Series([-1, -2, -3], index = ['one', 'three', 'five'])
>>> df1['fourth'] = s # 传入 Series 修改指定列，匹配 index
>>> df1
       fourth  thrid  second first
one      -1.0    100       1     a
two       NaN    100       1     b
three    -2.0    200       2     b
four      NaN    200       1     c
five     -3.0    300       2     c
six       NaN    300       3     c
>>>
>>> df1['fifth'] = df1.second < 2 # 逻辑运算增加一列
>>> df1
       fourth  thrid  second first  fifth
one      -1.0    100       1     a   True
two       NaN    100       1     b   True
three    -2.0    200       2     b  False
four      NaN    200       1     c   True
five     -3.0    300       2     c  False
six       NaN    300       3     c  False
>>>
>>> del df1['fifth'] # 删除指定列
>>> df1
       fourth  thrid  second first
one      -1.0    100       1     a
two       NaN    100       1     b
three    -2.0    200       2     b
four      NaN    200       1     c
five     -3.0    300       2     c
six       NaN    300       3     c
>>>
>>> data = {'first': {'one': 'a', 'two': 'b', 'three': 'b'}, 'second': {'one': 1, 'two': 1, 'three': 2, 'four': 1}}
>>> df2 = pd.DataFrame(data) # 外层键作为列，内层键作为索引
>>> df2
      first  second
four    NaN       1
one       a       1
three     b       2
two       b       1
>>> df2.T # 转置
       four one three two
first   NaN   a     b   b
second    1   1     2   1
>>>
>>> pd.DataFrame(data, index = pd.Series(['five', 'two', 'three'])) # 指定索引，内层键不起作用，即不会被合并，排序成最终索引
      first  second
five    NaN     NaN
two       b     1.0
three     b     2.0
>>>
>>> df1.index.name = 'index_name' # 指定索引名称
>>> df1.columns.name = 'columns_name' # 指定列名称
>>> df1
columns_name  fourth  thrid  second first  fifth
index_name
one             -1.0    100       1     a   True
two              NaN    100       1     b   True
three           -2.0    200       2     b  False
four             NaN    200       1     c   True
five            -3.0    300       2     c  False
six              NaN    300       3     c  False
>>> df1.values # 以二维 ndarray 的返回数据
array([[-1.0, 100, 1, 'a', True],
       [nan, 100, 1, 'b', True],
       [-2.0, 200, 2, 'b', False],
       [nan, 200, 1, 'c', True],
       [-3.0, 300, 2, 'c', False],
       [nan, 300, 3, 'c', False]], dtype=object)
```

* 索引对象

```python
>>> import pandas as pd
>>> import numpy as np
>>>
>>> df = pd.Series(range(3), index = ['a', 'b', 'c'])
>>> index = df.index
>>> index
Index(['a', 'b', 'c'], dtype='object')
>>> index[1:]
Index(['b', 'c'], dtype='object')
>>> index[1] = 'd' # Index 对象不可变，故不能进行修改
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\ProgramData\Miniconda3\lib\site-packages\pandas\core\indexes\base.py", line 2051, in __setitem__
    raise TypeError("Index does not support mutable operations")
TypeError: Index does not support mutable operations
>>>
>>> labels = pd.Index(np.arange(3))
>>> labels
Int64Index([0, 1, 2], dtype='int64')
>>>
>>> df1 = pd.Series([1.5, -2.5, 0], index = labels)
>>> df1
0    1.5
1   -2.5
2    0.0
dtype: float64
>>>
>>> df1.index is labels # 其不可变的特性能在多个数据结构中安全共享
True
>>>
>>> 1 in df1.index # 不可变对象的原因，内存地址不通
False
>>>
>>> labels1 = pd.Index(np.arange(3))
>>> labels2 = pd.Index(np.arange(2, 4))
>>> labels1
Int64Index([0, 1, 2], dtype='int64')
>>> labels2
Int64Index([2, 3], dtype='int64')
>>>
>>>
>>> labels1.append(labels2) # 连接两个 Index
Int64Index([0, 1, 2, 2, 3], dtype='int64')
>>> labels1.difference(labels2) # 计算差集
Int64Index([0, 1], dtype='int64')
>>> labels1.intersection(labels2) # 计算交集
Int64Index([2], dtype='int64')
>>> labels1.union(labels2) # 计算并集
Int64Index([0, 1, 2, 3], dtype='int64')
>>> labels1.isin(labels2) # 计算 labels1 值是否在 labels2 中
array([False, False,  True])
>>> labels1.delete(0) # 删除索引 0 处的元素
Int64Index([1, 2], dtype='int64')
>>> labels1.drop(1) # 删除值为 1 的元素
Int64Index([0, 2], dtype='int64')
>>> labels1.insert(0, 1) # 在索引 0 的位置插入元素
Int64Index([1, 0, 1, 2], dtype='int64')
>>> labels1.is_monotonic # 各个元素均大于等于迁移元素时，返回 True
True
>>> labels1.is_unique # 没有重复值时，返回 True
True
>>> labels1.unique() # 返回唯一值数组
Int64Index([0, 1, 2], dtype='int64')
```

### 7.4.2 基本操作

* 重新索引

`DataFrame.reindex(labels=None, index=None, columns=None, axis=None, method=None, copy=True, level=None, fill_value=nan, limit=None, tolerance=None)`

`index` 新序列

`method` 插值方式

`fill_value` 指定填充的值

`limit` 向前或向后填充的最大填充量

`tolerance` 向前或向后填充是，填充不确定匹配项的最大间距

`level` 在`MultiIndex`的指定级别上匹配简单索引，否则选取其子集

`copy` 默认为`True`，是否进行复制

```python
>>> import pandas as pd
>>> import numpy as np
>>>
>>> s = pd.Series([1, 3, -2, 4], index = ['a', 'b', 'c', 'd'])
>>> s
a    1
b    3
c   -2
d    4
dtype: int64
>>>
>>> s1 = s.reindex(['e', 'd', 'c', 'b', 'a']) # 根据索引值重排
>>> s1
e    NaN
d    4.0
c   -2.0
b    3.0
a    1.0
dtype: float64
>>>
>>> s2 = s.reindex(['a', 'b', 'c', 'd', 'e'], method = 'ffill') # 不存在的索引，向前补充缺失值
>>> s2
a    1
b    3
c   -2
d    4
e    4
dtype: int64
>>>
>>> data = {'first': ['a', 'b', 'b', 'c', 'c', 'c'], 'second': [1, 1, 2, 1, 2, 3], 'thrid': [100, 100, 200, 200, 300, 300]}
>>>
>>> df1 = pd.DataFrame(data, columns = ['thrid', 'second', 'first'], index = ['one', 'two', 'three', 'four', 'five', 'six'])
>>> df1
       thrid  second first
one      100       1     a
two      100       1     b
three    200       2     b
four     200       1     c
five     300       2     c
six      300       3     c
>>>
>>> df1.reindex(['one', 'two', 'three', 'four', 'five', 'six', 'seven']) # 重新索引 DataFrame
       thrid  second first
one    100.0     1.0     a
two    100.0     1.0     b
three  200.0     2.0     b
four   200.0     1.0     c
five   300.0     2.0     c
six    300.0     3.0     c
seven    NaN     NaN   NaN
>>>
>>> df1.reindex(columns = ['fourth', 'thrid', 'second']) # 对 columns 重新索引
       fourth  thrid  second
one       NaN    100       1
two       NaN    100       1
three     NaN    200       2
four      NaN    200       1
five      NaN    300       2
six       NaN    300       3
>>> df1
       thrid  second first
one      100       1     a
two      100       1     b
three    200       2     b
four     200       1     c
five     300       2     c
six      300       3     c
```

* 丢弃项

```python
>>> import pandas as pd
>>> import numpy as np
>>>
>>> s = pd.Series([1, 3, -2, 4], index = ['a', 'b', 'c', 'd'])
>>> s
a    1
b    3
c   -2
d    4
dtype: int64
>>>
>>> s.drop('c') # 删除索引 c 行
a    1
b    3
d    4
dtype: int64
>>> s.drop(['b', 'c']) # 数组方式删除
a    1
d    4
dtype: int64
>>>
>>> data = {'first': ['a', 'b', 'b', 'c', 'c', 'c'], 'second': [1, 1, 2, 1, 2, 3], 'thrid': [100, 100, 200, 200, 300, 300]}
>>>
>>> df = pd.DataFrame(data, columns = ['thrid', 'second', 'first'], index = ['one', 'two', 'three', 'four', 'five', 'six'])
>>> df.drop(['three', 'four']) # 删除指定索引行
      thrid  second first
one     100       1     a
two     100       1     b
five    300       2     c
six     300       3     c
>>> df.drop('thrid', axis = 1) # 指定轴向删除
       second first
one         1     a
two         1     b
three       2     b
four        1     c
five        2     c
six         3     c
>>> df.drop('thrid', axis = 'columns') # 同上
       second first
one         1     a
two         1     b
three       2     b
four        1     c
five        2     c
six         3     c
>>> df.drop('three', inplace = True) # 就地修改
>>> df
      thrid  second first
one     100       1     a
two     100       1     b
four    200       1     c
five    300       2     c
six     300       3     c
```

* 索引，选取和过滤

```python
>>> import pandas as pd
>>> import numpy as np
>>>
>>> s = pd.Series([1, 3, -2, 4], index = ['a', 'b', 'c', 'd'])
>>> s
a    1
b    3
c   -2
d    4
dtype: int64
>>>
>>> s['a'] # 类似字典方式进行索引，index 为 key
1
>>> s[2] # 位置索引
-2
>>> s[1:3] # 切片索引
b    3
c   -2
dtype: int64
>>> s[[1, 3]] # 位置数组索引
b    3
d    4
dtype: int64
>>> s[s > 2] # 逻辑判断索引
b    3
d    4
dtype: int64
>>> s['b': 'd'] # 切片索引，右边能包含
b    3
c   -2
d    4
dtype: int64
>>> s['b': 'd'] = 0 # 通过索引来修改值
>>> s
a    1
b    0
c    0
d    0
dtype: int64
>>>
>>> data = {'first': ['a', 'b', 'b', 'c', 'c', 'c'], 'second': [1, 1, 2, 1, 2, 3], 'thrid': [100, 100, 200, 200, 300, 300]}
>>>
>>> df = pd.DataFrame(data, columns = ['thrid', 'second', 'first'], index = ['one', 'two', 'three', 'four', 'five', 'six'])
>>>
>>> df['thrid'] # 字典索引
one      100
two      100
three    200
four     200
five     300
six      300
Name: thrid, dtype: int64
>>> df[1:3] # 行切片
       thrid  second first
two      100       1     b
three    200       2     b
>>> df[['thrid', 'first']] # 数组索引
       thrid first
one      100     a
two      100     b
three    200     b
four     200     c
five     300     c
six      300     c
>>> df[df['second'] < 2] # 选定某列进行逻辑索引
      thrid  second first
one     100       1     a
two     100       1     b
four    200       1     c
>>> df[df['second'] < 2] == 1 # 逻辑判断
      thrid  second  first
one   False    True  False
two   False    True  False
four  False    True  False
>>>
>>> df.loc['three', ['second', 'first']] # 选择 three 行的 second first 列
second    2
first     b
Name: three, dtype: object
>>> df.loc[:'four', ['thrid', 'first']] # 切片到 four 行选择 thrid first 列
       thrid first
one      100     a
two      100     b
three    200     b
four     200     c
>>> df.iloc[2] # 选择索引位置第 3 行
thrid     200
second      2
first       b
Name: three, dtype: object
>>> df.iloc[[1, 2], [0, 2, 1]] # 选择索引位置第 1 2 行的第 0 2 1 列 
       thrid first  second
two      100     b       1
three    200     b       2
>>> df.iloc[:, :2][df.second > 1] # 切片索引后逻辑判断
       thrid  second
three    200       2
five     300       2
six      300       3
>>>
>>> s = pd.Series(np.arange(3.), index=['a', 'b', 'c'])
>>> s
a    0.0
b    1.0
c    2.0
dtype: float64
>>> s[-1]
2.0
>>>
>>> s = pd.Series(np.arange(3.))
>>> s
0    0.0
1    1.0
2    2.0
dtype: float64
>>> s[-1] # 纯整数的序列进行整数索引时，会报错
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\ProgramData\Miniconda3\lib\site-packages\pandas\core\series.py", line 767, in __getitem__
    result = self.index.get_value(self, key)
  File "C:\ProgramData\Miniconda3\lib\site-packages\pandas\core\indexes\base.py", line 3104, in get_value
    tz=getattr(series.dtype, 'tz', None))
  File "pandas/_libs/index.pyx", line 106, in pandas._libs.index.IndexEngine.get_value
  File "pandas/_libs/index.pyx", line 114, in pandas._libs.index.IndexEngine.get_value
  File "pandas/_libs/index.pyx", line 162, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/hashtable_class_helper.pxi", line 958, in pandas._libs.hashtable.Int64HashTable.get_item
  File "pandas/_libs/hashtable_class_helper.pxi", line 964, in pandas._libs.hashtable.Int64HashTable.get_item
KeyError: -1
>>> s[:1]
0    0.0
dtype: float64
>>> s.loc[:1] # 推荐使用 loc 标签索引
0    0.0
1    1.0
dtype: float64
>>> s.iloc[:1] # 或者使用 iloc 整数索引
0    0.0
dtype: float64
```

* 数学运算

```python
>>> import pandas as pd
>>> import numpy as np
>>>
>>> s1 = pd.Series([7.3, -2.5, 3.4, 1.5], index = ['a', 'c', 'd', 'e'])
>>> s2 = s2 = pd.Series([-2.1, 3.6, -1.5, 4, 3.1], index = ['a', 'c', 'e', 'f', 'g'])
>>> s1
a    7.3
c   -2.5
d    3.4
e    1.5
dtype: float64
>>> s2
a   -2.1
c    3.6
e   -1.5
f    4.0
g    3.1
dtype: float64
>>>
>>> s1 + s2 # 数据对齐，一方存在的而另一方不存在的索引进行运算会置为 NaN
a    5.2
c    1.1
d    NaN
e    0.0
f    NaN
g    NaN
dtype: float64
>>>
>>> df1 = pd.DataFrame(np.arange(9.).reshape((3, 3)), columns = ['first', 'second', 'thrid'], index = ['one', 'two', 'three'])
>>> df2 = pd.DataFrame(np.arange(12.).reshape((4, 3)), columns = ['first', 'second', 'thrid'], index = ['one', 'two', 'three', 'four'])
>>> df1
       first  second  thrid
one      0.0     1.0    2.0
two      3.0     4.0    5.0
three    6.0     7.0    8.0
>>> df2
       first  second  thrid
one      0.0     1.0    2.0
two      3.0     4.0    5.0
three    6.0     7.0    8.0
four     9.0    10.0   11.0
>>>
>>> df1 + df2 # 不存在的行置为 NaN
       first  second  thrid
four     NaN     NaN    NaN
one      0.0     2.0    4.0
three   12.0    14.0   16.0
two      6.0     8.0   10.0
>>>
>>> df1 = pd.DataFrame({'A': [1, 2]})
>>> df2 = pd.DataFrame({'B': [3, 4]})
>>> df1
   A
0  1
1  2
>>> df2
   B
0  3
1  4
>>> df1 + df2 # 没有共用的列或行标签，结果置为 NaN
    A   B
0 NaN NaN
1 NaN NaN
>>>
>>> df1.add(df2, fill_value = 0) # 对没有重叠的位置补充值，然后进行相加的动作
     A    B
0  1.0  3.0
1  2.0  4.0
>>> df1.radd(df2, fill_value = 0) # 右加
     A    B
0  1.0  3.0
1  2.0  4.0
>>> df1.sub(df2, fill_value = 0) # 减法
     A    B
0  1.0 -3.0
1  2.0 -4.0
>>> df1.rsub(df2, fill_value = 0) # 右减
     A    B
0 -1.0  3.0
1 -2.0  4.0
>>> df1.div(df2, fill_value = 0) # 除法
     A    B
0  inf  0.0
1  inf  0.0
>>> df1.rdiv(df2, fill_value = 0) # 右除
     A    B
0  0.0  inf
1  0.0  inf
>>> df1.floordiv(df2, fill_value = 0) # 地板除
    A    B
0 NaN -0.0
1 NaN -0.0
>>> df1.rfloordiv(df2, fill_value = 0) # 右地板除
     A   B
0 -0.0 NaN
1 -0.0 NaN
>>> df1.mul(df2, fill_value = 0) # 乘法
     A    B
0  0.0  0.0
1  0.0  0.0
>>> df1.rmul(df2, fill_value = 0) # 右地板乘
     A    B
0  0.0  0.0
1  0.0  0.0
>>> df1.pow(df2, fill_value = 0) # 平方
     A    B
0  1.0  0.0
1  1.0  0.0
>>> df1.rpow(df2, fill_value = 0) # 右平方
     A    B
0  0.0  1.0
1  0.0  1.0
>>>
>>> df = pd.DataFrame(np.arange(12.).reshape((4, 3)), columns = ['first', 'second', 'thrid'], index = ['one', 'two', 'three', 'four'])
>>> s = df.iloc[0]
>>> df
       first  second  thrid
one      0.0     1.0    2.0
two      3.0     4.0    5.0
three    6.0     7.0    8.0
four     9.0    10.0   11.0
>>> s
first     0.0
second    1.0
thrid     2.0
Name: one, dtype: float64
>>> df - s # 广播机制进行减法
       first  second  thrid
one      0.0     0.0    0.0
two      3.0     3.0    3.0
three    6.0     6.0    6.0
four     9.0     9.0    9.0
>>> s1 = pd.Series(range(3), index=['first', 'second', 'fifth'])
>>> s1
first     0
second    1
fifth     2
dtype: int64
>>> df + s1 # 不存在列变成并集
       fifth  first  second  thrid
one      NaN    0.0     2.0    NaN
two      NaN    3.0     5.0    NaN
three    NaN    6.0     8.0    NaN
four     NaN    9.0    11.0    NaN
>>> s2 = df['first']
>>> s2
one      0.0
two      3.0
three    6.0
four     9.0
Name: first, dtype: float64
>>> df.sub(s2, axis = 'index') # 进行指定列的运算
       first  second  thrid
one      0.0     1.0    2.0
two      0.0     1.0    2.0
three    0.0     1.0    2.0
four     0.0     1.0    2.0
```

* 函数应用和映射

* 排序和排名

### 7.4.3 汇总和计算描述统计

* 相关系数与协方差

* 唯一值、值计数以及成员资格