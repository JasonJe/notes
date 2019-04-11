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
>>> df.tail() # 展示最后 5 行数据
  first  second  thrid
1     b       1    100
2     b       2    200
3     c       1    200
4     c       2    300
5     c       3    300
>>> df.tail(3) # 展示最后 3 行数据
  first  second  thrid
3     c       1    200
4     c       2    300
5     c       3    300
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

可以将`NumPy`的`ufunc`应用于`Pandas`对象

```python
>>> import pandas as pd
>>> import numpy as np
>>>
>>> df = pd.DataFrame(np.random.randn(4, 3), columns = ['first', 'second', 'thrid'], index = ['one', 'two', 'three', 'four'])
>>> df
          first    second     thrid
one   -0.519511  0.301790 -1.168141
two    0.184956 -1.075827 -0.269703
three -0.347362  0.811374 -0.053796
four  -0.046029  0.031835 -0.160494
>>>
>>> np.abs(df) # 使用 ufunc
          first    second     thrid
one    0.519511  0.301790  1.168141
two    0.184956  1.075827  0.269703
three  0.347362  0.811374  0.053796
four   0.046029  0.031835  0.160494
>>>
>>> f = lambda x: x.max() - x.min()
>>> df.apply(f) # 每列执行一次上述运算
first     0.704466
second    1.887201
thrid     1.114346
dtype: float64
>>> df.apply(f, axis = 'columns') # 对每行进行应用
one      1.469931
two      1.260783
three    1.158735
four     0.192329
dtype: float64
>>>
>>> f = lambda x: '##%.2f' %x 
>>> df.applymap(f) # 每个浮点数进行函数应用
         first   second    thrid
one    ##-0.52   ##0.30  ##-1.17
two     ##0.18  ##-1.08  ##-0.27
three  ##-0.35   ##0.81  ##-0.05
four   ##-0.05   ##0.03  ##-0.16
>>> df['thrid'].map(f) # Series 对应的计算
one      ##-1.17
two      ##-0.27
three    ##-0.05
four     ##-0.16
Name: thrid, dtype: object
```

* 排序和排名

```python
>>> import pandas as pd
>>> import numpy as np
>>>
>>> s = pd.Series([4, np.nan, 7, np.nan, -3, 2], index=['d', 'a', 'b', 'c', 'e', 'f'])
>>> s
d    4.0
a    NaN
b    7.0
c    NaN
e   -3.0
f    2.0
dtype: float64
>>> s.sort_index() # 索引排序
a    NaN
b    7.0
c    NaN
d    4.0
e   -3.0
f    2.0
dtype: float64
>>> s.sort_values() # 值排序，NaN 置后
e   -3.0
f    2.0
d    4.0
b    7.0
a    NaN
c    NaN
dtype: float64
>>>
>>> df = pd.DataFrame(np.arange(12.).reshape((4, 3)), columns = ['first', 'second', 'thrid'], index = ['four', 'three', 'two', 'one'])
>>> df
       first  second  thrid
four     0.0     1.0    2.0
three    3.0     4.0    5.0
two      6.0     7.0    8.0
one      9.0    10.0   11.0
>>> df.sort_index() # 索引排序
       first  second  thrid
four     0.0     1.0    2.0
one      9.0    10.0   11.0
three    3.0     4.0    5.0
two      6.0     7.0    8.0
>>> df.sort_index(axis = 1) # 列排序
       first  second  thrid
four     0.0     1.0    2.0
three    3.0     4.0    5.0
two      6.0     7.0    8.0
one      9.0    10.0   11.0
>>> df.sort_index(axis = 1, ascending = False) # 降序排序
       thrid  second  first
four     2.0     1.0    0.0
three    5.0     4.0    3.0
two      8.0     7.0    6.0
one     11.0    10.0    9.0
>>> df.sort_values(by = 'first') # 根据指定列排序
       first  second  thrid
four     0.0     1.0    2.0
three    3.0     4.0    5.0
two      6.0     7.0    8.0
one      9.0    10.0   11.0
>>> df.sort_values(by = ['first', 'second'])
       first  second  thrid
four     0.0     1.0    2.0
three    3.0     4.0    5.0
two      6.0     7.0    8.0
one      9.0    10.0   11.0
>>>
>>> s = pd.Series([7, -5, 7, 4, 2, 0, 4]) # 为对应元素分组后，分配一个平均排名
>>> s.rank()
0    6.5
1    1.0
2    6.5
3    4.5
4    3.0
5    2.0
6    4.5
dtype: float64
>>> s.rank(method = 'first') # 原始顺序做排名
0    6.0
1    1.0
2    7.0
3    4.0
4    3.0
5    2.0
6    5.0
dtype: float64
>>> s.rank(ascending = False, method = 'max') # 最大排名
0    2.0
1    7.0
2    2.0
3    4.0
4    5.0
5    6.0
6    4.0
dtype: float64
>>> s.rank(ascending = False, method = 'min') # 最小排名
0    1.0
1    7.0
2    1.0
3    3.0
4    5.0
5    6.0
6    3.0
dtype: float64
>>> s.rank(ascending = False, method = 'average') # 同组进行平均排名
0    1.5
1    7.0
2    1.5
3    3.5
4    5.0
5    6.0
6    3.5
dtype: float64
>>> s.rank(ascending = False, method = 'dense') # 排名在组件增加 1
0    1.0
1    5.0
2    1.0
3    2.0
4    3.0
5    4.0
6    2.0
dtype: float64
>>>
>>> df = pd.DataFrame(np.arange(12.).reshape((4, 3)), columns = ['first', 'second', 'thrid'], index = ['four', 'three', 'two', 'one'])
>>> df.rank(axis='columns')
       first  second  thrid
four     1.0     2.0    3.0
three    1.0     2.0    3.0
two      1.0     2.0    3.0
one      1.0     2.0    3.0
```

### 7.4.3 汇总和计算描述统计

* 常见统计方法

```python
>>> import pandas as pd
>>> import numpy as np
>>>
>>> df = pd.DataFrame([[1.4, np.nan], [7.1, -4.5], [np.nan, np.nan], [0.75, -1.3]], index=['a', 'b', 'c', 'd'], columns=['one', 'two'])
>>> df
    one  two
a  1.40  NaN
b  7.10 -4.5
c   NaN  NaN
d  0.75 -1.3
>>>
>>> df.count() # 非 NaN 数量
one    3
two    2
dtype: int64
>>> df.describe() # 汇总统计
            one       two
count  3.000000  2.000000
mean   3.083333 -2.900000
std    3.493685  2.262742
min    0.750000 -4.500000
25%    1.075000 -3.700000
50%    1.400000 -2.900000
75%    4.250000 -2.100000
max    7.100000 -1.300000
>>> df.min() # 最小值
one    0.75
two   -4.50
dtype: float64
>>> df.min(axis =1) # 列的最小值计算
a    1.4
b   -4.5
c    NaN
d   -1.3
dtype: float64
>>> df.min(skipna = False) # 不排除缺失值进行计算，默认是排除缺失值后进行计算的
one   NaN
two   NaN
dtype: float64
>>> df.max() # 最大值
one    7.1
two   -1.3
dtype: float64
>>> df['one'].argmin() # 最小值索引位置
'd'
>>> df['one'].argmax() # 最大值索引位置
'b'
>>> df.idxmin() # 最小值索引位置
one    d
two    b
dtype: object
>>> df.idxmax() # 最大值索引位置
one    b
two    d
dtype: object
>>> df.quantile() # 分位数
one    1.4
two   -2.9
Name: 0.5, dtype: float64
>>> df.sum() # 总和，自动排除缺失值
one    9.25
two   -5.80
dtype: float64
>>> df.mean() # 平均数
one    3.083333
two   -2.900000
dtype: float64
>>> df.mad() # 根据平均值计算平均绝对离差
one    2.677778
two    1.600000
dtype: float64
>>> df.var() # 方差
one    12.205833
two     5.120000
dtype: float64
>>> df.std() # 标准差
one    3.493685
two    2.262742
dtype: float64
>>> df.skew() # 偏度
one    1.664846
two         NaN
dtype: float64
>>> df.kurt() # 峰度
one   NaN
two   NaN
dtype: float64
>>> df.cumsum() # 累计和
    one  two
a  1.40  NaN
b  8.50 -4.5
c   NaN  NaN
d  9.25 -5.8
>>> df.cummin() # 累计最小值
    one  two
a  1.40  NaN
b  1.40 -4.5
c   NaN  NaN
d  0.75 -4.5
>>> df.cummax() # 累计最大值
   one  two
a  1.4  NaN
b  7.1 -4.5
c  NaN  NaN
d  7.1 -1.3
>>> df.cumprod() # 累计积
     one   two
a  1.400   NaN
b  9.940 -4.50
c    NaN   NaN
d  7.455  5.85
>>> df.diff() # 一阶差分
   one  two
a  NaN  NaN
b  5.7  NaN
c  NaN  NaN
d  NaN  NaN
>>> df.pct_change() # 百分数变化
        one       two
a       NaN       NaN
b  4.071429       NaN
c  0.000000  0.000000
d -0.894366 -0.711111
```

* 相关系数与协方差

```python
>>> s1 = pd.Series(np.random.randn(4), index = ['four', 'three', 'two', 'one'])
>>> s2 = pd.Series(np.random.randn(4), index = ['four', 'three', 'two', 'one'])
>>> s1
four    -1.570356
three    1.330038
two     -0.015304
one     -1.049489
dtype: float64
>>> s2
four     0.953147
three   -0.259151
two      0.026956
one     -0.211236
dtype: float64
>>> s1.corr(s2) # 计算 s1 和 s2 的相关系数
-0.6709803173456137
>>> s1.cov(s2) # 计算 s1 和 s2 的协方差
-0.48462481328586904
>>>
>>> df = pd.DataFrame(np.random.randn(4, 3), columns = ['first', 'second', 'thrid'], index = ['four', 'three', 'two', 'one'])
>>> df.corr() # DataFrame 的相关系数矩阵
           first    second     thrid
first   1.000000 -0.448123  0.690295
second -0.448123  1.000000 -0.791210
thrid   0.690295 -0.791210  1.000000
>>> df.cov() # DataFrame 的协方差矩阵
           first    second     thrid
first   1.413201 -0.546178  0.554683
second -0.546178  1.051160 -0.548321
thrid   0.554683 -0.548321  0.456896
>>> df.corrwith(s1) # 针对每列的相关系数
first    -0.056426
second   -0.586744
thrid    -0.020669
dtype: float64
```

* 唯一值、值计数以及成员资格

```python
>>> s = pd.Series(['c', 'a', 'd', 'a', 'a', 'b', 'b', 'c', 'c'])
>>> s.unique() # 唯一值数组
array(['c', 'a', 'd', 'b'], dtype=object)
>>> s.value_counts() # 计数数组，降序排列
a    3
c    3
b    2
d    1
dtype: int64
>>> pd.value_counts(s.values, sort = False)
b    2
c    3
a    3
d    1
dtype: int64
>>> s.isin(['b', 'c']) # 是否包含的该值的数组
0     True
1    False
2    False
3    False
4    False
5     True
6     True
7     True
8     True
dtype: bool
>>> s[s.isin(['b', 'c'])]
0    c
5    b
6    b
7    c
8    c
dtype: object
```

### 7.4.4 `IO`操作

* `csv`

```python
>>> df = pd.read_csv('examples/ex1.csv') # 读csv文件
>>> df
   a   b   c   d message
0  1   2   3   4   hello
1  5   6   7   8   world
2  9  10  11  12     foo
>>> pd.read_table('examples/ex1.csv', sep = ',') # 指定分隔符为 ,
   a   b   c   d message
0  1   2   3   4   hello
1  5   6   7   8   world
2  9  10  11  12     foo
>>> list(open('examples/ex3.txt'))
['            A         B         C\n',
 'aaa -0.264438 -1.026059 -0.619500\n',
 'bbb  0.927272  0.302904 -0.032399\n',
 'ccc -0.264273 -0.386314 -0.217601\n',
 'ddd -0.871858 -0.348382  1.100491\n']
>>> pd.read_table('examples/ex3.txt', sep='\s+') # 使用正则表达式作为分隔符号
            A         B         C
aaa -0.264438 -1.026059 -0.619500
bbb  0.927272  0.302904 -0.032399
ccc -0.264273 -0.386314 -0.217601
ddd -0.871858 -0.348382  1.100491
>>>
>>> pd.read_csv('examples/ex2.csv', header = None) # 不读列名
   0   1   2   3      4
0  1   2   3   4  hello
1  5   6   7   8  world
2  9  10  11  12    foo
>>> pd.read_csv('examples/ex2.csv', names = ['a', 'b', 'c', 'd', 'message']) # 指定列名
   a   b   c   d message
0  1   2   3   4   hello
1  5   6   7   8   world
2  9  10  11  12     foo
>>> pd.read_csv('examples/ex2.csv', names = ['a', 'b', 'c', 'd', 'message'], index_col='message') # 指定索引列
         a   b   c   d
message               
hello    1   2   3   4
world    5   6   7   8
foo      9  10  11  12
>>>
>>> list(open('csv_mindex.csv'))
['key1,key2,value1,value2\n',
 'one,a,1,2\n',
 'one,b,3,4\n',
 'one,c,5,6\n',
 'one,d,7,8\n',
 'two,a,9,10\n',
 'two,b,11,12\n',
 'two,c,13,14\n',
 'two,d,15,16\n']
>>> parsed = pd.read_csv('examples/csv_mindex.csv', index_col = ['key1', 'key2']) # 指定索引数组，进行层次索引
>>> parsed
           value1  value2
key1 key2                
one  a          1       2
     b          3       4
     c          5       6
     d          7       8
two  a          9      10
     b         11      12
     c         13      14
     d         15      16
>>>
>>> pd.read_csv('examples/ex4.csv', skiprows=[0, 2, 3]) # 跳过 0， 2， 3 行
   a   b   c   d message
0  1   2   3   4   hello
1  5   6   7   8   world
2  9  10  11  12     foo
>>>
>>> result = pd.read_csv('examples/ex5.csv', na_values=['NULL']) # 指定将读到的 NULL 定义为空值，默认还有 NA 和 空字符串
>>> result
  something  a   b     c   d message
0       one  1   2   3.0   4     NaN
1       two  5   6   NaN   8   world
2     three  9  10  11.0  12     foo
>>> pd.read_csv('examples/ex5.csv', na_values = {'message': ['foo', 'NA'], 'something': ['two']}) # 利用字典将识别到对应列中的值置为空值
something  a   b     c   d message
0       one  1   2   3.0   4     NaN
1       NaN  5   6   NaN   8   world
2     three  9  10  11.0  12     NaN
>>>
>>> pd.options.display.max_rows = 10 # 最大显示行数
>>> pd.read_csv('examples/ex6.csv')
           one       two     three      four key
0     0.467976 -0.038649 -0.295344 -1.824726   L
1    -0.358893  1.404453  0.704965 -0.200638   B
2    -0.501840  0.659254 -0.421691 -0.057688   G
3     0.204886  1.074134  1.388361 -0.982404   R
4     0.354628 -0.133116  0.283763 -0.837063   Q
...        ...       ...       ...       ...  ..
9995  2.311896 -0.417070 -1.409599 -0.515821   L
9996 -0.479893 -0.650419  0.745152 -0.646038   E
9997  0.523331  0.787112  0.486066  1.093156   K
9998 -0.362559  0.598894 -1.843201  0.887292   G
9999 -0.096376 -1.012999 -0.657431 -0.573315   0
[10000 rows x 5 columns]
If you want to only read a small
>>> pd.read_csv('examples/ex6.csv', nrows = 5) # 只显示 5 行
        one       two     three      four key
0  0.467976 -0.038649 -0.295344 -1.824726   L
1 -0.358893  1.404453  0.704965 -0.200638   B
2 -0.501840  0.659254 -0.421691 -0.057688   G
3  0.204886  1.074134  1.388361 -0.982404   R
4  0.354628 -0.133116  0.283763 -0.837063   Q
>>>
>>> chunker = pd.read_csv('examples/ex6.csv', chunksize = 1000) # 分块读取
>>> chunker
<pandas.io.parsers.TextParser at 0x8398150>
>>> tot = pd.Series([])
>>> for piece in chunker:
        tot = tot.add(piece['key'].value_counts(), fill_value=0)
>>> tot = tot.sort_values(ascending=False)
>>> tot[:10]
E    368.0
X    364.0
L    346.0
O    343.0
Q    340.0
M    338.0
J    337.0
F    335.0
K    334.0
H    330.0
dtype: float64
>>>
>>> data.to_csv('examples/out.csv') # 保存成 csv
>>> 
>>> import sys
>>> data.to_csv(sys.stdout, sep='|') # 指定保存的分隔符
>>> 
>>> data.to_csv(sys.stdout, na_rep='NULL')
,something,a,b,c,d,message
0,one,1,2,3.0,4,NULL
1,two,5,6,NULL,8,world
2,three,9,10,11.0,12,foo
>>>
>>> data.to_csv(sys.stdout, index = False, header = False) # 不保存列名和索引
one,1,2,3.0,4,
two,5,6,,8,world
three,9,10,11.0,12,foo
>>>
>>> data.to_csv(sys.stdout, index = False, columns = ['a', 'b', 'c']) # 保存指定列名
a,b,c
1,2,3.0
5,6,
9,10,11.0
>>>
>>> s = pd.Series(np.arange(7)) # 序列进行保存
>>> s.to_csv('examples/series.csv')
```

* `JSON`

```python
>>> import json
>>> result = json.loads(obj)
>>> result
{'name': 'Wes', 'pet': None, 'places_lived': ['United States', 'Spain', 'Germany'], 'siblings': [{'age': 30, 'name': 'Scott', 'pets': ['Zeus', 'Zuko']}, {'age': 38, 'name': 'Katie', 'pets': ['Sixes', 'Stache', 'Cisco']}]}
>>> siblings = pd.DataFrame(result['siblings'], columns=['name', 'age'])
>>> siblings
    name  age
0  Scott   30
1  Katie   38
>>>
>>> pd.read_json('examples/example.json')
   a  b  c
0  1  2  3
1  4  5  6
2  7  8  9
>>> print(data.to_json())
{"a":{"0":1,"1":4,"2":7},"b":{"0":2,"1":5,"2":8},"c":{"0":3,"1":6,"2":9}}
>>> print(data.to_json(orient='records'))
[{"a":1,"b":2,"c":3},{"a":4,"b":5,"c":6},{"a":7,"b":8,"c":9}]
```

* `pickle`

```python
>>> df = pd.read_csv('examples/ex1.csv')
>>> df
   a   b   c   d message
0  1   2   3   4   hello
1  5   6   7   8   world
2  9  10  11  12     foo
>>> df.to_pickle('examples/frame_pickle')
>>> pd.read_pickle('examples/frame_pickle')
   a   b   c   d message
0  1   2   3   4   hello
1  5   6   7   8   world
2  9  10  11  12     foo
```

* `excel`

```python
>>> xlsx = pd.ExcelFile('examples/ex1.xlsx')
>>> pd.read_excel(xlsx, 'Sheet1')
   a   b   c   d message
0  1   2   3   4   hello
1  5   6   7   8   world
2  9  10  11  12     foo
>>> df = pd.read_excel('examples/ex1.xlsx', 'Sheet1')
>>> df
   a   b   c   d message
0  1   2   3   4   hello
1  5   6   7   8   world
2  9  10  11  12     foo
>>> writer = pd.ExcelWriter('examples/ex2.xlsx')
>>> df.to_excel(writer, 'Sheet1')
>>> writer.save()
>>>
>>> df.to_excel('examples/ex2.xlsx')
```

### 7.4.5 数据准备

* 缺失数据处理

```python
>>> import pandas as pd
>>> import numpy as np
>>>
>>> s = pd.Series(['aardvark', 'artichoke', np.nan, 'avocado'])
>>> s
0     aardvark
1    artichoke
2          NaN
3      avocado
dtype: object
>>> s.isnull() # 判断是否为空，返回一个布尔型数组
0    False
1    False
2     True
3    False
dtype: bool
>>>
>>> s[0] = None # None对象可作为NaN使用
>>> s
0         None
1    artichoke
2          NaN
3      avocado
dtype: object
>>> s.isnull()
0     True
1    False
2     True
3    False
dtype: bool
>>>
>>> s = pd.Series([1, np.nan, 3.5, np.nan, 7])
>>> s
0    1.0
1    NaN
2    3.5
3    NaN
4    7.0
dtype: float64
>>> s.dropna() # 删除NaN
0    1.0
2    3.5
4    7.0
dtype: float64
>>> s[s.notnull()] # 同上
0    1.0
2    3.5
4    7.0
dtype: float64
>>>
>>> df = pd.DataFrame([[1., 6.5, 3.], [1., np.nan, np.nan],[np.nan, np.nan, np.nan], [np.nan, 6.5, 3.]])
>>> df
     0    1    2
0  1.0  6.5  3.0
1  1.0  NaN  NaN
2  NaN  NaN  NaN
3  NaN  6.5  3.0
>>> df.dropna()
     0    1    2
0  1.0  6.5  3.0
>>> df.dropna(how = 'all') # 删除整行为空的
     0    1    2
0  1.0  6.5  3.0
1  1.0  NaN  NaN
3  NaN  6.5  3.0
>>> df[4] = np.nan
>>> df.dropna(axis = 1, how = 'all') # 删除整列为空
     0    1    2
0  1.0  6.5  3.0
1  1.0  NaN  NaN
2  NaN  NaN  NaN
3  NaN  6.5  3.0
>>>
>>> df = pd.DataFrame(np.random.randn(7, 3))
>>> df.iloc[:4, 1] = np.nan
>>> df.iloc[:2, 2] = np.nan
>>> df
          0         1         2
0 -1.835056       NaN       NaN
1 -0.622418       NaN       NaN
2 -0.917339       NaN -1.705462
3  1.877966       NaN -0.969041
4 -0.306760  1.169494 -1.275661
5 -0.566569  0.828514  0.425309
6 -1.006299 -2.028990  0.216853
>>> df.dropna()
          0         1         2
4 -0.306760  1.169494 -1.275661
5 -0.566569  0.828514  0.425309
6 -1.006299 -2.028990  0.216853
>>> df.dropna(thresh = 2) # 保留至少有 2 个非 NaN 的行
          0         1         2
2 -0.917339       NaN -1.705462
3  1.877966       NaN -0.969041
4 -0.306760  1.169494 -1.275661
5 -0.566569  0.828514  0.425309
6 -1.006299 -2.028990  0.216853
>>>
>>> df.fillna(0) # 填充空值为 0 
          0         1         2
0 -1.835056  0.000000  0.000000
1 -0.622418  0.000000  0.000000
2 -0.917339  0.000000 -1.705462
3  1.877966  0.000000 -0.969041
4 -0.306760  1.169494 -1.275661
5 -0.566569  0.828514  0.425309
6 -1.006299 -2.028990  0.216853
>>> df.fillna({1: 0.5, 2: 0}) # 指定列填充对应值
          0         1         2
0 -1.835056  0.500000  0.000000
1 -0.622418  0.500000  0.000000
2 -0.917339  0.500000 -1.705462
3  1.877966  0.500000 -0.969041
4 -0.306760  1.169494 -1.275661
5 -0.566569  0.828514  0.425309
6 -1.006299 -2.028990  0.216853
>>> df.fillna(0, inplace = True) # 原地修改
>>> df
          0         1         2
0 -1.835056  0.000000  0.000000
1 -0.622418  0.000000  0.000000
2 -0.917339  0.000000 -1.705462
3  1.877966  0.000000 -0.969041
4 -0.306760  1.169494 -1.275661
5 -0.566569  0.828514  0.425309
6 -1.006299 -2.028990  0.216853
>>>
>>> df = pd.DataFrame(np.random.randn(6, 3))
>>> df.iloc[2:, 1] = np.nan
>>> df.iloc[4:, 2] = np.nan
>>> df
          0         1         2
0 -1.497591  0.565268  0.000782
1 -0.651188 -1.774130  0.187381
2  0.148992       NaN -0.045827
3 -0.349998       NaN  0.184382
4  2.078643       NaN       NaN
5 -0.980509       NaN       NaN
>>> df.fillna(method='ffill') # 前向补充
          0         1         2
0 -1.497591  0.565268  0.000782
1 -0.651188 -1.774130  0.187381
2  0.148992 -1.774130 -0.045827
3 -0.349998 -1.774130  0.184382
4  2.078643 -1.774130  0.184382
5 -0.980509 -1.774130  0.184382
>>> df.fillna(method='ffill', limit=2) # 至少补充 2 行
          0         1         2
0 -1.497591  0.565268  0.000782
1 -0.651188 -1.774130  0.187381
2  0.148992 -1.774130 -0.045827
3 -0.349998 -1.774130  0.184382
4  2.078643       NaN  0.184382
5 -0.980509       NaN  0.184382
>>>
>>> s = pd.Series([1., np.nan, 3.5, np.nan, 7])
>>> s.fillna(s.mean()) # 补充对应的均值
0    1.000000
1    3.833333
2    3.500000
3    3.833333
4    7.000000
dtype: float64
>>>
```

* 数据转换

```python
>>> # 重复值处理
>>> df = pd.DataFrame({'k1': ['one', 'two'] * 3 + ['two'], 'k2': [1, 1, 2, 3, 3, 4, 4]})
>>> df
    k1  k2
0  one   1
1  two   1
2  one   2
3  two   3
4  one   3
5  two   4
6  two   4
>>> df.duplicated() # 返回是否重复的布尔型数组
0    False
1    False
2    False
3    False
4    False
5    False
6     True
dtype: bool
>>> df.drop_duplicates() # 删除重复行
    k1  k2
0  one   1
1  two   1
2  one   2
3  two   3
4  one   3
5  two   4
>>>
>>> df['v1'] = range(7)
>>> df.drop_duplicates(['k1']) # 指定列删除重复行
    k1  k2  v1
0  one   1   0
1  two   1   1
>>> df.drop_duplicates(['k1', 'k2'], keep = 'last') # 保留重复行中最后一行
    k1  k2  v1
0  one   1   0
1  two   1   1
2  one   2   2
3  two   3   3
4  one   3   4
6  two   4   6
>>>
>>> # 数据转换
>>> df = pd.DataFrame({'food': ['bacon', 'pulled pork', 'bacon', 'Pastrami', 'corned beef', 'Bacon', 'pastrami', 'honey ham', 'nova lox'], 'ounces': [4, 3, 12, 6, 7.5, 8, 3, 5, 6]})
>>> df
          food  ounces
0        bacon     4.0
1  pulled pork     3.0
2        bacon    12.0
3     Pastrami     6.0
4  corned beef     7.5
5        Bacon     8.0
6     pastrami     3.0
7    honey ham     5.0
8     nova lox     6.0
>>>
>>> df1 = df['food'].str.lower() # Series的str.lower方法转换为小写
>>> df1
0          bacon
1    pulled pork
2          bacon
3       pastrami
4    corned beef
5          bacon
6       pastrami
7      honey ham
8       nova lox
Name: food, dtype: object
>>> meat_to_animal = {'bacon': 'pig', 'pulled pork': 'pig', 'pastrami': 'cow', 'corned beef': 'cow', 'honey ham': 'pig', 'nova lox': 'salmon'}
>>> df['animal'] = df1.map(meat_to_animal) # 增加一列，对应元素转换为对应值
>>> df
          food  ounces  animal
0        bacon     4.0     pig
1  pulled pork     3.0     pig
2        bacon    12.0     pig
3     Pastrami     6.0     cow
4  corned beef     7.5     cow
5        Bacon     8.0     pig
6     pastrami     3.0     cow
7    honey ham     5.0     pig
8     nova lox     6.0  salmon
>>>
>>> df['food'].map(lambda x: meat_to_animal[x.lower()]) # 同上并能进行 Series的str.lower
0       pig
1       pig
2       pig
3       cow
4       cow
5       pig
6       cow
7       pig
8    salmon
Name: food, dtype: object
>>>
>>> # 替换值
>>> s = pd.Series([1., -999., 2., -999., -1000., 3.])
>>> s
0       1.0
1    -999.0
2       2.0
3    -999.0
4   -1000.0
5       3.0
dtype: float64
>>> s.replace(-999, np.nan)
0       1.0
1       NaN
2       2.0
3       NaN
4   -1000.0
5       3.0
dtype: float64
>>> s.replace([-999, -1000], np.nan)
0    1.0
1    NaN
2    2.0
3    NaN
4    NaN
5    3.0
dtype: float64
>>> s.replace([-999, -1000], [np.nan, 0])
0    1.0
1    NaN
2    2.0
3    NaN
4    0.0
5    3.0
dtype: float64
>>> s.replace({-999: np.nan, -1000: 0}) # 同上
0    1.0
1    NaN
2    2.0
3    NaN
4    0.0
5    3.0
dtype: float64
>>>
>>> # 索引处理
>>> df = pd.DataFrame(np.arange(12).reshape((3, 4)), index=['Ohio', 'Colorado', 'New York'], columns=['one', 'two', 'three', 'four'])
>>> df
          one  two  three  four
Ohio        0    1      2     3
Colorado    4    5      6     7
New York    8    9     10    11
>>> df.index.map(lambda x: x[:4].upper()) # 大写
Index(['OHIO', 'COLO', 'NEW '], dtype='object')
>>> df.index = df.index.map(lambda x: x[:4].upper())
>>> df.rename(index = str.title, columns = str.upper) # 同上，指定方法进行转换并重命名
      ONE  TWO  THREE  FOUR
Ohio    0    1      2     3
Colo    4    5      6     7
New     8    9     10    11
>>>
>>> df.rename(index={'OHIO': 'INDIANA'}, columns = {'three': 'peekaboo'}) # 对应元素进行处理
             one  two  peekaboo  four
INDIANA        0    1         2     3
COLO           4    5         6     7
NEW            8    9        10    11
>>> df
      one  two  three  four
OHIO    0    1      2     3
COLO    4    5      6     7
NEW     8    9     10    11
>>> df.rename(index={'OHIO': 'INDIANA'}, inplace = True)
>>> df
             one  two  three  four
INDIANA        0    1      2     3
COLO           4    5      6     7
NEW            8    9     10    11
>>>
>>> # 离散化和面元划分
>>> ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
>>> bins = [18, 25, 35, 60, 100]
>>> cats = pd.cut(ages, bins)
>>> cats # 按照 bins 分成 4 组
[(18, 25], (18, 25], (18, 25], (25, 35], (18, 25], ..., (25, 35], (60, 100], (35, 60], (35, 60], (25, 35]]
Length: 12
Categories (4, interval[int64]): [(18, 25] < (25, 35] < (35, 60] < (60, 100]]
>>> cats.codes # ages 每个元素所属的组索引
array([0, 0, 0, 1, 0, 0, 2, 1, 3, 2, 2, 1], dtype=int8)
>>> cats.categories # 左开右闭的分组数组
IntervalIndex([(18, 25], (25, 35], (35, 60], (60, 100]]
              closed='right',
              dtype='interval[int64]')
>>> pd.value_counts(cats) # 计数
(18, 25]     5
(35, 60]     3
(25, 35]     3
(60, 100]    1
dtype: int64
>>>
>>> pd.cut(ages, [18, 26, 36, 61, 100], right = False) # 左开右开
[[18, 26), [18, 26), [18, 26), [26, 36), [18, 26), ..., [26, 36), [61, 100), [36, 61), [36, 61), [26, 36)]
Length: 12
Categories (4, interval[int64]): [[18, 26) < [26, 36) < [36, 61) < [61, 100)]
>>>
>>> group_names = ['Youth', 'YoungAdult', 'MiddleAged', 'Senior'] # 每组取名
>>> pd.cut(ages, bins, labels = group_names)
[Youth, Youth, Youth, YoungAdult, Youth, ..., YoungAdult, Senior, MiddleAged, MiddleAged, YoungAdult]
Length: 12
Categories (4, object): [Youth < YoungAdult < MiddleAged < Senior]
>>>
>>> pd.cut(np.random.rand(20), 4, precision = 2) # 指定分成四组，保留 2 位小数
[(0.2, 0.37], (0.37, 0.53], (0.04, 0.2], (0.2, 0.37], (0.53, 0.69], ..., (0.2, 0.37], (0.37, 0.53], (0.2, 0.37], (0.53, 0.69], (0.37, 0.53]]
Length: 20
Categories (4, interval[float64]): [(0.04, 0.2] < (0.2, 0.37] < (0.37, 0.53] < (0.53, 0.69]]
>>>
>>> cats = pd.qcut(np.random.randn(1000), 4) # 按照样本分位数进行分组
>>> cats
[(-3.85, -0.635], (0.611, 4.052], (-3.85, -0.635], (0.611, 4.052], (-0.0446, 0.611], ..., (-3.85, -0.635], (-0.0446, 0.611], (0.611, 4.052], (-3.85, -0.635], (-0.0446, 0.611]]
Length: 1000
Categories (4, interval[float64]): [(-3.85, -0.635] < (-0.635, -0.0446] < (-0.0446, 0.611] <
                                    (0.611, 4.052]]
>>> pd.value_counts(cats)
(0.611, 4.052]       250
(-0.0446, 0.611]     250
(-0.635, -0.0446]    250
(-3.85, -0.635]      250
dtype: int64
>>> pd.qcut(np.random.randn(1000), [0, 0.1, 0.5, 0.9, 1.]) # 自定义分位数数组
[(0.0387, 1.246], (-1.285, 0.0387], (-1.285, 0.0387], (1.246, 2.837], (-1.285, 0.0387], ..., (0.0387, 1.246], (-2.897, -1.285], (0.0387, 1.246], (-1.285, 0.0387], (-1.285, 0.0387]]
Length: 1000
Categories (4, interval[float64]): [(-2.897, -1.285] < (-1.285, 0.0387] < (0.0387, 1.246] <
                                    (1.246, 2.837]]
>>>
>>> # 检测和过滤异常值
>>> df = pd.DataFrame(np.random.randn(1000, 4))
>>> df.describe()
                 0            1            2            3
count  1000.000000  1000.000000  1000.000000  1000.000000
mean     -0.003095    -0.044058     0.045726     0.027742
std       0.977519     0.990128     0.973064     1.018610
min      -3.724572    -3.290415    -3.233415    -3.046136
25%      -0.607939    -0.668722    -0.586161    -0.666566
50%       0.000194    -0.072557     0.027244     0.063540
75%       0.632587     0.665414     0.656196     0.669008
max       3.611280     3.606621     3.765902     3.058573
>>> df[(np.abs(df) > 3).any(1)] # ndarry 的 any() 方法，返回 True
            0         1         2         3
93   3.408187 -0.103922 -1.110054  0.567005
103  3.611280  0.406028  0.274605  0.487306
113 -2.102704  2.007313  3.031139 -0.149642
144  0.332747 -0.538448  3.103812 -0.881626
254 -3.436895  0.302619 -1.501830 -0.182301
281 -3.185617  1.103247 -0.803208  1.976911
529  0.273695 -3.290415  0.332741 -0.106494
546 -0.825269  0.531172  1.224454 -3.046136
703  0.983526  0.787115  3.765902 -0.371106
771 -3.724572  0.793264 -0.950179  0.108810
800 -0.916751 -3.104559  0.341853 -0.410846
808  0.972227 -0.453404 -3.233415  0.458490
811  2.051842  3.606621 -0.042653  1.019130
860  0.236864  3.156231 -0.249022  0.935836
900 -0.460253  1.233382 -0.232106  3.058573
902  2.247374 -1.592100 -3.018866 -0.513080
975  1.291065 -0.188662 -3.090970  0.707329
>>> np.sign(df).head() # 根据正负赋值 -1 1
     0    1    2    3
0  1.0  1.0 -1.0 -1.0
1 -1.0 -1.0  1.0 -1.0
2  1.0  1.0  1.0  1.0
3  1.0  1.0  1.0  1.0
4 -1.0 -1.0  1.0  1.0
>>> df[np.abs(df) > 3] = np.sign(df) * 3
>>>
>>> # 随机抽样
>>> df = pd.DataFrame(np.arange(5 * 4).reshape((5, 4)))
>>> sampler = np.random.permutation(5)
>>> sampler
array([4, 2, 0, 1, 3])
>>> df.take(sampler) # 不放回抽样
    0   1   2   3
4  16  17  18  19
2   8   9  10  11
0   0   1   2   3
1   4   5   6   7
3  12  13  14  15
>>> df.sample(n = 3)
    0   1   2   3
4  16  17  18  19
3  12  13  14  15
1   4   5   6   7
>>> df.sample(n = 3, replace = True) # 放回抽样
    0   1   2   3
4  16  17  18  19
4  16  17  18  19
1   4   5   6   7
>>> choices = pd.Series([5, 7, -1, 6, 4])
>>> choices.sample(n = 10, replace = True)
0    5
1    7
2   -1
4    4
4    4
4    4
2   -1
3    6
0    5
4    4
dtype: int64
>>>
>>> # 独热编码
>>> df = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b'], 'data': range(6)})
>>> pd.get_dummies(df['key'])
   a  b  c
0  0  1  0
1  0  1  0
2  1  0  0
3  0  0  1
4  1  0  0
5  0  1  0
>>> dummies = pd.get_dummies(df['key'], prefix='key') # 指定列名前缀
>>> dummies
   key_a  key_b  key_c
0      0      1      0
1      0      1      0
2      1      0      0
3      0      0      1
4      1      0      0
5      0      1      0
>>> df1 = df[['data']].join(dummies) # 拼接列
>>> df1
   data  key_a  key_b  key_c
0     0      0      1      0
1     1      0      1      0
2     2      1      0      0
3     3      0      0      1
4     4      1      0      0
5     5      0      1      0
```

* 字符串处理

```python
>>> import re
>>>
>>> s = pd.Series({'Dave': 'dave@google.com', 'Steve': 'steve@gmail.com', 'Rob': 'rob@gmail.com', 'Wes': np.nan})
>>> s
Dave     dave@google.com
Steve    steve@gmail.com
Rob        rob@gmail.com
Wes                  NaN
dtype: object
>>> s.isnull()
Dave     False
Steve    False
Rob      False
Wes       True
dtype: bool
>>> s.str.contains('gmail') # Series.str 对象方法
Dave     False
Steve     True
Rob       True
Wes        NaN
dtype: object
>>> pattern =  '([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\\.([A-Z]{2,4})'
>>> s.str.findall(pattern, flags = re.IGNORECASE) # 正则匹配查找
Dave     [(dave, google, com)]
Steve    [(steve, gmail, com)]
Rob        [(rob, gmail, com)]
Wes                        NaN
dtype: object
>>> matches = s.str.match(pattern, flags = re.IGNORECASE)
>>> matches
Dave     True
Steve    True
Rob      True
Wes       NaN
dtype: object
>>>
>>> matches.str.get(1) # 索引指定位置
Dave    NaN
Steve   NaN
Rob     NaN
Wes     NaN
dtype: float64
>>> matches.str[0] # 索引指定位置
Dave    NaN
Steve   NaN
Rob     NaN
Wes     NaN
dtype: float64
>>>
>>> s.str[:5] # 切片
Dave     dave@
Steve    steve
Rob      rob@g
Wes        NaN
dtype: object
```

`Pandas`字符串方法更多可查看官方文档。

### 7.4.6 聚合和分组

### 7.4.7 时间序列

### 7.4.8 高级