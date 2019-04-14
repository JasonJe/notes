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

```python
>>> import pandas as pd
>>> import numpy as np
>>>
>>> # 层次化索引
>>> s = pd.Series(np.random.randn(9), index=[['a', 'a', 'a', 'b', 'b', 'c', 'c', 'd', 'd'], [1, 2, 3, 1, 3, 1, 2, 2, 3]])
>>> s # 多层索引
a  1   -0.479523
   2   -1.895419
   3    0.634754
b  1    0.761861
   3   -0.256956
c  1    0.255096
   2    0.393600
d  2    0.838809
   3   -0.474474
dtype: float64
>>> s.index
MultiIndex(levels=[['a', 'b', 'c', 'd'], [1, 2, 3]],
           labels=[[0, 0, 0, 1, 1, 2, 2, 3, 3], [0, 1, 2, 0, 2, 0, 1, 1, 2]])
>>> s['b'] # 取一级索引的值
1    0.761861
3   -0.256956
dtype: float64
>>> s['b':'c']
b  1    0.761861
   3   -0.256956
c  1    0.255096
   2    0.393600
dtype: float64
>>> s.loc[:, 2] # 取第二级索引的值
a   -1.895419
c    0.393600
d    0.838809
dtype: float64
>>>
>>> s.unstack() # 生成透视表
          1         2         3
a -0.479523 -1.895419  0.634754
b  0.761861       NaN -0.256956
c  0.255096  0.393600       NaN
d       NaN  0.838809 -0.474474
>>> s.unstack().stack() # 逆运算
a  1   -0.479523
   2   -1.895419
   3    0.634754
b  1    0.761861
   3   -0.256956
c  1    0.255096
   2    0.393600
d  2    0.838809
   3   -0.474474
dtype: float64
>>>
>>> df = pd.DataFrame(np.arange(12).reshape((4, 3)), index=[['a', 'a', 'b', 'b'], [1, 2, 1, 2]], columns=[['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']])
>>> df
     Ohio     Colorado
    Green Red    Green
a 1     0   1        2
  2     3   4        5
b 1     6   7        8
  2     9  10       11
>>> df.index.names = ['key1', 'key2'] # 指定索引名称
>>> df.columns.names = ['state', 'color'] # 指定列名称
>>>
>>> df['Ohio'] # 一级列组的数据
color      Green  Red
key1 key2
a    1         0    1
     2         3    4
b    1         6    7
     2         9   10
>>> 
>>> # 重排和分级索引
>>> df.swaplevel('key1', 'key2') # 调整索引顺序
state      Ohio     Colorado
color     Green Red    Green
key2 key1
1    a        0   1        2
2    a        3   4        5
1    b        6   7        8
2    b        9  10       11
>>> df.sort_index(level = 1) # 按照指定级别的索引排序
state      Ohio     Colorado
color     Green Red    Green
key1 key2
a    1        0   1        2
b    1        6   7        8
a    2        3   4        5
b    2        9  10       11
>>> df.swaplevel(0, 1).sort_index(level = 0)
state      Ohio     Colorado
color     Green Red    Green
key2 key1
1    a        0   1        2
     b        6   7        8
2    a        3   4        5
     b        9  10       11
>>>
>>> # 根据级别汇总统计
>>> df.sum(level = 'key2') # 汇总指定索引的值
state  Ohio     Colorado
color Green Red    Green
key2
1         6   8       10
2        12  14       16
>>> df.sum(level = 'color', axis = 1) # 汇总指定列的值
color      Green  Red
key1 key2
a    1         2    1
     2         8    4
b    1        14    7
     2        20   10
>>>
>>> # 使用列进行索引
>>> df = pd.DataFrame({'a': range(7), 'b': range(7, 0, -1), 'c': ['one', 'one', 'one', 'two', 'two', 'two', 'two'], 'd': [0, 1, 2, 0, 1, 2, 3]})
>>> df
   a  b    c  d
0  0  7  one  0
1  1  6  one  1
2  2  5  one  2
3  3  4  two  0
4  4  3  two  1
5  5  2  two  2
6  6  1  two  3
>>> df1 = df.set_index(['c', 'd']) # 指定列作为索引
>>> df1
       a  b
c   d
one 0  0  7
    1  1  6
    2  2  5
two 0  3  4
    1  4  3
    2  5  2
    3  6  1
>>> df.set_index(['c', 'd'], drop = False) # 不移除列
       a  b    c  d
c   d
one 0  0  7  one  0
    1  1  6  one  1
    2  2  5  one  2
two 0  3  4  two  0
    1  4  3  two  1
    2  5  2  two  2
    3  6  1  two  3
>>> df1.reset_index() # 恢复原来的索引
     c  d  a  b
0  one  0  0  7
1  one  1  1  6
2  one  2  2  5
3  two  0  3  4
4  two  1  4  3
5  two  2  5  2
6  two  3  6  1
>>>
>>> # DataFrame合并
>>> df1 = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'a', 'b'], 'data1': range(7)})
>>> df2 = pd.DataFrame({'key': ['a', 'b', 'd'], 'data2': range(3)})
>>> df1
  key  data1
0   b      0
1   b      1
2   a      2
3   c      3
4   a      4
5   a      5
6   b      6
>>> df2
  key  data2
0   a      0
1   b      1
2   d      2
>>> pd.merge(df1, df2) # 拼接两个DataFrame，仅仅索引相同的参与，并且形成多对一的合并
  key  data1  data2
0   b      0      1
1   b      1      1
2   b      6      1
3   a      2      0
4   a      4      0
5   a      5      0
>>> pd.merge(df1, df2, on = 'key') # 指定使用那个列进行连接，默认使用重叠的列
  key  data1  data2
0   b      0      1
1   b      1      1
2   b      6      1
3   a      2      0
4   a      4      0
5   a      5      0
>>>
>>> df3 = pd.DataFrame({'lkey': ['b', 'b', 'a', 'c', 'a', 'a', 'b'], 'data1': range(7)})
>>> df4 = pd.DataFrame({'rkey': ['a', 'b', 'd'], 'data2': range(3)})
>>>
>>> pd.merge(df3, df4, left_on = 'lkey', right_on = 'rkey') # 默认进行内连接，连接相同的索引，内连接组合键的交集
  lkey  data1 rkey  data2
0    b      0    b      1
1    b      1    b      1
2    b      6    b      1
3    a      2    a      0
4    a      4    a      0
5    a      5    a      0
>>> pd.merge(df1, df2, how = 'outer') # 使用两个表的所有键，外连接组合键的并集
  key  data1  data2
0   b    0.0    1.0
1   b    1.0    1.0
2   b    6.0    1.0
3   a    2.0    0.0
4   a    4.0    0.0
5   a    5.0    0.0
6   c    3.0    NaN
7   d    NaN    2.0
>>>
>>> df1 = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b'], 'data1': range(6)})
>>> df2 = pd.DataFrame({'key': ['a', 'b', 'a', 'b', 'd'], 'data2': range(5)})
>>> df1
  key  data1
0   b      0
1   b      1
2   a      2
3   c      3
4   a      4
5   b      5
>>> df2
  key  data2
0   a      0
1   b      1
2   a      2
3   b      3
4   d      4
>>>
>>> pd.merge(df1, df2, on = 'key', how = 'left') # 基于 key 这一列，使用 left 连接
   key  data1  data2
0    b      0    1.0
1    b      0    3.0
2    b      1    1.0
3    b      1    3.0
4    a      2    0.0
5    a      2    2.0
6    c      3    NaN
7    a      4    0.0
8    a      4    2.0
9    b      5    1.0
10   b      5    3.0
>>> pd.merge(df1, df2, how = 'inner') # 内连接，昌盛笛卡尔积，df1 有 3 个 b， df2 有 2 个 b 结果有 6 个 b
  key  data1  data2
0   b      0      1
1   b      0      3
2   b      1      1
3   b      1      3
4   b      5      1
5   b      5      3
6   a      2      0
7   a      2      2
8   a      4      0
9   a      4      2
>>>
>>> left = pd.DataFrame({'key1': ['foo', 'foo', 'bar'], 'key2': ['one', 'two', 'one'],  'lval': [1, 2, 3]})
>>> right = pd.DataFrame({'key1': ['foo', 'foo', 'bar', 'bar'], 'key2': ['one', 'one', 'one', 'two'], 'rval': [4, 5, 6, 7]})
>>> pd.merge(left, right, on = ['key1', 'key2'], how = 'outer') # 通过多个列进行合并
  key1 key2  lval  rval
0  foo  one   1.0   4.0
1  foo  one   1.0   5.0
2  foo  two   2.0   NaN
3  bar  one   3.0   6.0
4  bar  two   NaN   7.0
>>> pd.merge(left, right, on = 'key1') # 多个列重叠时候，只指定一个列，其余列会重命名
  key1 key2_x  lval key2_y  rval
0  foo    one     1    one     4
1  foo    one     1    one     5
2  foo    two     2    one     4
3  foo    two     2    one     5
4  bar    one     3    one     6
5  bar    one     3    two     7
>>> pd.merge(left, right, on = 'key1', suffixes = ('_left', '_right')) # 指定重名的后缀
  key1 key2_left  lval key2_right  rval
0  foo       one     1        one     4
1  foo       one     1        one     5
2  foo       two     2        one     4
3  foo       two     2        one     5
4  bar       one     3        one     6
5  bar       one     3        two     7
>>>
>>> # 索引上的合并
>>> left1 = pd.DataFrame({'key': ['a', 'b', 'a', 'a', 'b', 'c'], 'value': range(6)})
>>> right1 = pd.DataFrame({'group_val': [3.5, 7]}, index=['a', 'b'])
>>> left1
  key  value
0   a      0
1   b      1
2   a      2
3   a      3
4   b      4
5   c      5
>>> right1
   group_val
a        3.5
b        7.0
>>> pd.merge(left1, right1, left_on = 'key', right_index = True) # 基于 key 列和 right1的索引进行内连接
  key  value  group_val
0   a      0        3.5
2   a      2        3.5
3   a      3        3.5
1   b      1        7.0
4   b      4        7.0
>>> pd.merge(left1, right1, left_on = 'key', right_index = True, how = 'outer') # 外连接
  key  value  group_val
0   a      0        3.5
2   a      2        3.5
3   a      3        3.5
1   b      1        7.0
4   b      4        7.0
5   c      5        NaN
>>>
>>> lefth = pd.DataFrame({'key1': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'], 'key2': [2000, 2001, 2002, 2001, 2002], 'data': np.arange(5.)})
>>> righth = pd.DataFrame(np.arange(12).reshape((6, 2)), index=[['Nevada', 'Nevada', 'Ohio', 'Ohio', 'Ohio', 'Ohio'], [2001, 2000, 2000, 2000, 2001, 2002]], columns=['event1', 'event2'])
>>> lefth
     key1  key2  data
0    Ohio  2000   0.0
1    Ohio  2001   1.0
2    Ohio  2002   2.0
3  Nevada  2001   3.0
4  Nevada  2002   4.0
>>> righth
             event1  event2
Nevada 2001       0       1
       2000       2       3
Ohio   2000       4       5
       2000       6       7
       2001       8       9
       2002      10      11
>>> pd.merge(lefth, righth, left_on = ['key1', 'key2'], right_index = True )
     key1  key2  data  event1  event2
0    Ohio  2000   0.0       4       5
0    Ohio  2000   0.0       6       7
1    Ohio  2001   1.0       8       9
2    Ohio  2002   2.0      10      11
3  Nevada  2001   3.0       0       1
>>> pd.merge(lefth, righth, left_on = ['key1', 'key2'], right_index = True, how = 'outer')
     key1  key2  data  event1  event2
0    Ohio  2000   0.0     4.0     5.0
0    Ohio  2000   0.0     6.0     7.0
1    Ohio  2001   1.0     8.0     9.0
2    Ohio  2002   2.0    10.0    11.0
3  Nevada  2001   3.0     0.0     1.0
4  Nevada  2002   4.0     NaN     NaN
4  Nevada  2000   NaN     2.0     3.0
>>>
>>> left2 = pd.DataFrame([[1., 2.], [3., 4.], [5., 6.]], index=['a', 'c', 'e'], columns=['Ohio', 'Nevada'])
>>> right2 = pd.DataFrame([[7., 8.], [9., 10.], [11., 12.], [13, 14]], index=['b', 'c', 'd', 'e'], columns=['Missouri', 'Alabama'])
>>> left2
   Ohio  Nevada
a   1.0     2.0
c   3.0     4.0
e   5.0     6.0
>>> right2
   Missouri  Alabama
b       7.0      8.0
c       9.0     10.0
d      11.0     12.0
e      13.0     14.0
>>> pd.merge(left2, right2, how = 'outer', left_index = True, right_index = True) # 基于所有df的索引
   Ohio  Nevada  Missouri  Alabama
a   1.0     2.0       NaN      NaN
b   NaN     NaN       7.0      8.0
c   3.0     4.0       9.0     10.0
d   NaN     NaN      11.0     12.0
e   5.0     6.0      13.0     14.0
>>> left2.join(right2, how = 'outer') # 效果同上，left2 与 right2的键的并集，默认使用左连接，保留左边表的行索引
   Ohio  Nevada  Missouri  Alabama
a   1.0     2.0       NaN      NaN
b   NaN     NaN       7.0      8.0
c   3.0     4.0       9.0     10.0
d   NaN     NaN      11.0     12.0
e   5.0     6.0      13.0     14.0
>>> left1.join(right1, on = 'key') # 指定列名
  key  value  group_val
0   a      0        3.5
1   b      1        7.0
2   a      2        3.5
3   a      3        3.5
4   b      4        7.0
5   c      5        NaN
>>>
>>> another = pd.DataFrame([[7., 8.], [9., 10.], [11., 12.], [16., 17.]], index=['a', 'c', 'e', 'f'], columns=['New York', 'Oregon'])
>>> another
   New York  Oregon
a       7.0     8.0
c       9.0    10.0
e      11.0    12.0
f      16.0    17.0
>>> left2.join([right2, another]) # 连接多个表
   Ohio  Nevada  Missouri  Alabama  New York  Oregon
a   1.0     2.0       NaN      NaN       7.0     8.0
c   3.0     4.0       9.0     10.0       9.0    10.0
e   5.0     6.0      13.0     14.0      11.0    12.0
>>> left2.join([right2, another], how = 'outer')
C:\ProgramData\Miniconda3\lib\site-packages\pandas\core\frame.py:6369: FutureWarning: Sorting because non-concatenation axis is not aligned. A future version
of pandas will change to not sort by default.

To accept the future behavior, pass 'sort=False'.

To retain the current behavior and silence the warning, pass 'sort=True'.

  verify_integrity=True)
   Ohio  Nevada  Missouri  Alabama  New York  Oregon
a   1.0     2.0       NaN      NaN       7.0     8.0
b   NaN     NaN       7.0      8.0       NaN     NaN
c   3.0     4.0       9.0     10.0       9.0    10.0
d   NaN     NaN      11.0     12.0       NaN     NaN
e   5.0     6.0      13.0     14.0      11.0    12.0
f   NaN     NaN       NaN      NaN      16.0    17.0
>>>
>>> # 轴向连接
>>> arr = np.arange(12).reshape((3, 4))
>>> arr
array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11]])
>>> np.concatenate([arr, arr], axis=1)
array([[ 0,  1,  2,  3,  0,  1,  2,  3],
       [ 4,  5,  6,  7,  4,  5,  6,  7],
       [ 8,  9, 10, 11,  8,  9, 10, 11]])
>>>
>>> s1 = pd.Series([0, 1], index=['a', 'b'])
>>> s2 = pd.Series([2, 3, 4], index=['c', 'd', 'e'])
>>> s3 = pd.Series([5, 6], index=['f', 'g'])
>>> pd.concat([s1, s2, s3]) # 纵向拼接
a    0
b    1
c    2
d    3
e    4
f    5
g    6
dtype: int64
>>> pd.concat([s1, s2, s3], axis=1) # 横向拼接
__main__:1: FutureWarning: Sorting because non-concatenation axis is not aligned. A future version
of pandas will change to not sort by default.

To accept the future behavior, pass 'sort=False'.

To retain the current behavior and silence the warning, pass 'sort=True'.

     0    1    2
a  0.0  NaN  NaN
b  1.0  NaN  NaN
c  NaN  2.0  NaN
d  NaN  3.0  NaN
e  NaN  4.0  NaN
f  NaN  NaN  5.0
g  NaN  NaN  6.0
>>>
>>> s4 = pd.concat([s1, s3])
>>> s4
a    0
b    1
f    5
g    6
dtype: int64
>>> pd.concat([s1, s4], axis=1)
     0  1
a  0.0  0
b  1.0  1
f  NaN  5
g  NaN  6
>>> pd.concat([s1, s4], axis=1, join='inner')
   0  1
a  0  0
b  1  1
>>> pd.concat([s1, s4], axis=1, join_axes = [['a', 'c', 'b', 'e']]) # 指定拼接使用的索引
     0    1
a  0.0  0.0
c  NaN  NaN
b  1.0  1.0
e  NaN  NaN
>>>
>>> result = pd.concat([s1, s1, s3], keys = ['one','two', 'three']) # 使用一个层次化索引
>>> result
one    a    0
       b    1
two    a    0
       b    1
three  f    5
       g    6
dtype: int64
>>> result.unstack()
         a    b    f    g
one    0.0  1.0  NaN  NaN
two    0.0  1.0  NaN  NaN
three  NaN  NaN  5.0  6.0
>>>
>>> pd.concat([s1, s2, s3], axis = 1, keys = ['one','two', 'three']) # 横向拼接，keys 变成列名
   one  two  three
a  0.0  NaN    NaN
b  1.0  NaN    NaN
c  NaN  2.0    NaN
d  NaN  3.0    NaN
e  NaN  4.0    NaN
f  NaN  NaN    5.0
g  NaN  NaN    6.0
>>>
>>> df1 = pd.DataFrame(np.arange(6).reshape(3, 2), index=['a', 'b', 'c'], columns=['one', 'two'])
>>> df2 = pd.DataFrame(5 + np.arange(4).reshape(2, 2), index=['a', 'c'], columns=['three', 'four'])
>>> df1
   one  two
a    0    1
b    2    3
c    4    5
>>> df2
   three  four
a      5     6
c      7     8
>>> pd.concat([df1, df2], axis=1, keys=['level1', 'level2'])
  level1     level2
     one two  three four
a      0   1    5.0  6.0
b      2   3    NaN  NaN
c      4   5    7.0  8.0
>>> pd.concat({'level1': df1, 'level2': df2}, axis = 1)
  level1     level2
     one two  three four
a      0   1    5.0  6.0
b      2   3    NaN  NaN
c      4   5    7.0  8.0
>>> pd.concat([df1, df2], axis=1, keys = ['level1', 'level2'], names = ['upper', 'lower']) # 命名指定轴级别索引名称
upper level1     level2
lower    one two  three four
a          0   1    5.0  6.0
b          2   3    NaN  NaN
c          4   5    7.0  8.0
>>>
>>> df1 = pd.DataFrame(np.random.randn(3, 4), columns=['a', 'b', 'c', 'd'])
>>> df2 = pd.DataFrame(np.random.randn(2, 3), columns=['b', 'd', 'a'])
>>> df1
          a         b         c         d
0  0.540245 -1.432206  1.282044  0.489050
1  0.318615  0.790511  2.567630 -0.390115
2  1.156002  0.164498  0.846345 -1.135219
>>> df2
          b         d         a
0 -0.162024 -1.082169  0.775074
1  0.428736  1.947893  0.962349
>>>
>>> pd.concat([df1, df2], ignore_index=True) # 不保留连接轴上的索引，产生一组新的索引
          a         b         c         d
0  0.540245 -1.432206  1.282044  0.489050
1  0.318615  0.790511  2.567630 -0.390115
2  1.156002  0.164498  0.846345 -1.135219
3  0.775074 -0.162024       NaN -1.082169
4  0.962349  0.428736       NaN  1.947893
>>>
>>> # 合并重叠数据
>>> a = pd.Series([np.nan, 2.5, np.nan, 3.5, 4.5, np.nan], index=['f', 'e', 'd', 'c', 'b', 'a'])
>>> b = pd.Series(np.arange(len(a), dtype=np.float64), index=['f', 'e', 'd', 'c', 'b', 'a'])
>>> b[-1] = np.nan
>>> a
f    NaN
e    2.5
d    NaN
c    3.5
b    4.5
a    NaN
dtype: float64
>>> b
f    0.0
e    1.0
d    2.0
c    3.0
b    4.0
a    NaN
dtype: float64
>>> np.where(pd.isnull(a), b, a) # 三目运算
array([0. , 2.5, 2. , 3.5, 4.5, nan])
>>> b[:-2].combine_first(a[2:]) # 效果同上，用传递对象中的数据为调用对象的缺失数据“打补丁”
a    NaN
b    4.5
c    3.0
d    2.0
e    1.0
f    0.0
dtype: float64
>>>
>>> df1 = pd.DataFrame({'a': [1., np.nan, 5., np.nan], 'b': [np.nan, 2., np.nan, 6.], 'c': range(2, 18, 4)})
>>> df2 = pd.DataFrame({'a': [5., 4., np.nan, 3., 7.], 'b': [np.nan, 3., 4., 6., 8.]})
>>> df1
     a    b   c
0  1.0  NaN   2
1  NaN  2.0   6
2  5.0  NaN  10
3  NaN  6.0  14
>>> df2
     a    b
0  5.0  NaN
1  4.0  3.0
2  NaN  4.0
3  3.0  6.0
4  7.0  8.0
>>> df1.combine_first(df2)
     a    b     c
0  1.0  NaN   2.0
1  4.0  2.0   6.0
2  5.0  4.0  10.0
3  3.0  6.0  14.0
4  7.0  8.0   NaN
>>>
>>> # 重塑层次化索引
>>> df = pd.DataFrame(np.arange(6).reshape((2, 3)), index = pd.Index(['Ohio','Colorado'], name='state'), columns=pd.Index(['one', 'two', 'three'], name='number'))
>>> df
number    one  two  three
state
Ohio        0    1      2
Colorado    3    4      5
>>> result = df.stack() # 将数据的列“旋转”为行
>>> result
state     number
Ohio      one       0
          two       1
          three     2
Colorado  one       3
          two       4
          three     5
dtype: int32
>>> result.unstack() # 将数据的行“旋转”为列
number    one  two  three
state
Ohio        0    1      2
Colorado    3    4      5
>>> result.unstack(0)
state   Ohio  Colorado
number
one        0         3
two        1         4
three      2         5
>>> result.unstack('state') # 指定层级
state   Ohio  Colorado
number
one        0         3
two        1         4
three      2         5
>>>
>>> s1 = pd.Series([0, 1, 2, 3], index=['a', 'b', 'c', 'd'])
>>> s2 = pd.Series([4, 5, 6], index=['c', 'd', 'e'])
>>> df1 = pd.concat([s1, s2], keys=['one', 'two'])
>>> df1
one  a    0
     b    1
     c    2
     d    3
two  c    4
     d    5
     e    6
dtype: int64
>>> df1.unstack()
       a    b    c    d    e
one  0.0  1.0  2.0  3.0  NaN
two  NaN  NaN  4.0  5.0  6.0
>>> df1.unstack().stack()
one  a    0.0
     b    1.0
     c    2.0
     d    3.0
two  c    4.0
     d    5.0
     e    6.0
dtype: float64
>>> df1.unstack().stack(dropna = False) # stack默认会滤除缺失数据，因此该运算是可逆的
one  a    0.0
     b    1.0
     c    2.0
     d    3.0
     e    NaN
two  a    NaN
     b    NaN
     c    4.0
     d    5.0
     e    6.0
dtype: float64
>>>
>>> df = pd.DataFrame({'left': result, 'right': result + 5}, columns = pd.Index(['left', 'right'], name = 'side'))
>>> df
side             left  right
state    number
Ohio     one        0      5
         two        1      6
         three      2      7
Colorado one        3      8
         two        4      9
         three      5     10
>>> df.unstack('state') # 在对DataFrame进行unstack操作时，作为旋转轴的级别将会成为结果中的最低级别
side   left          right
state  Ohio Colorado  Ohio Colorado
number
one       0        3     5        8
two       1        4     6        9
three     2        5     7       10
>>> df.unstack('state').stack('side')
state         Colorado  Ohio
number side
one    left          3     0
       right         8     5
two    left          4     1
       right         9     6
three  left          5     2
       right        10     7
```

* 分组

```python
>>> import pandas as pd
>>> import numpy as np
>>>
>>> df = pd.DataFrame({'key1' : ['a', 'a', 'b', 'b', 'a'], 'key2' : ['one', 'two', 'one', 'two', 'one'], 'data1' : np.random.randn(5), 'data2' : np.random.randn(5)})
>>> df
  key1 key2     data1     data2
0    a  one -0.296159 -1.964854
1    a  two  0.490876  0.484856
2    b  one -0.047975  1.882631
3    b  two  1.206025  0.174956
4    a  one -1.639627 -0.715221
>>> grouped = df['data1'].groupby(df['key1']) # 指定某列按照 key1 分组
>>> grouped.mean()
key1
a   -0.481637
b    0.579025
Name: data1, dtype: float64
>>> df['data1'].groupby([df['key1'], df['key2']]).mean() # 按照指定的两个列分组后求均值
key1  key2
a     one    -0.967893
      two     0.490876
b     one    -0.047975
      two     1.206025
Name: data1, dtype: float64
>>>
>>> states = np.array(['Ohio', 'California', 'California', 'Ohio', 'Ohio'])
>>> years = np.array([2005, 2005, 2006, 2005, 2006])
>>> df['data1'].groupby([states, years]).mean() # 指定每行对应的索引后进行分组
California  2005    0.490876
            2006   -0.047975
Ohio        2005    0.454933
            2006   -1.639627
Name: data1, dtype: float64
>>>
>>> df.groupby('key1').mean() # 指定表按照 key1 分组
         data1     data2
key1
a    -0.481637 -0.731740
b     0.579025  1.028793
>>> df.groupby(['key1', 'key2']).mean()
              data1     data2
key1 key2
a    one  -0.967893 -1.340037
     two   0.490876  0.484856
b    one  -0.047975  1.882631
     two   1.206025  0.174956
>>> df.groupby(['key1', 'key2']).size() # 求分组后每组的大小
key1  key2
a     one     2
      two     1
b     one     1
      two     1
dtype: int64
>>>
>>> # 分组迭代
>>> for name, group in df.groupby('key1'):
...     print(name)
...     print(group)
...
a
  key1 key2     data1     data2
0    a  one -0.296159 -1.964854
1    a  two  0.490876  0.484856
4    a  one -1.639627 -0.715221
b
  key1 key2     data1     data2
2    b  one -0.047975  1.882631
3    b  two  1.206025  0.174956
>>> for (k1, k2), group in df.groupby(['key1', 'key2']):
...     print((k1, k2))
...     print(group)
...
('a', 'one')
  key1 key2     data1     data2
0    a  one -0.296159 -1.964854
4    a  one -1.639627 -0.715221
('a', 'two')
  key1 key2     data1     data2
1    a  two  0.490876  0.484856
('b', 'one')
  key1 key2     data1     data2
2    b  one -0.047975  1.882631
('b', 'two')
  key1 key2     data1     data2
3    b  two  1.206025  0.174956
>>> pieces = dict(list(df.groupby('key1'))) # 将分组当成一个字典
>>> pieces
{'a':   key1 key2     data1     data2
0    a  one -0.296159 -1.964854
1    a  two  0.490876  0.484856
4    a  one -1.639627 -0.715221, 'b':   key1 key2     data1     data2
2    b  one -0.047975  1.882631
3    b  two  1.206025  0.174956}
>>>
>>> df.dtypes
key1      object
key2      object
data1    float64
data2    float64
dtype: object
>>> grouped = df.groupby(df.dtypes, axis=1) # 按照类型分组
>>> for dtype, group in grouped:
...     print(dtype)
...     print(group)
...
float64
      data1     data2
0 -0.296159 -1.964854
1  0.490876  0.484856
2 -0.047975  1.882631
3  1.206025  0.174956
4 -1.639627 -0.715221
object
  key1 key2
0    a  one
1    a  two
2    b  one
3    b  two
4    a  one
>>>
>>> # 选取某列的子集
>>> df.groupby(['key1', 'key2'])[['data2']].mean()
              data2
key1 key2
a    one  -1.340037
     two   0.484856
b    one   1.882631
     two   0.174956
>>> s_grouped  = df.groupby(['key1', 'key2'])['data2']
>>> s_grouped.mean()
key1  key2
a     one    -1.340037
      two     0.484856
b     one     1.882631
      two     0.174956
Name: data2, dtype: float64
>>>
>>> # 通过字典或 Series 分组
>>> people = pd.DataFrame(np.random.randn(5, 5), columns=['a', 'b', 'c', 'd', 'e'], index=['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])
>>> people.iloc[2:3, [1, 2]] = np.nan
>>> people
               a         b         c         d         e
Joe     0.424557 -0.005562  0.644771 -1.527423 -1.763429
Steve  -0.511867 -1.825093  0.970510  0.926331  0.317576
Wes    -1.030695       NaN       NaN  0.341934 -0.056919
Jim     0.356591  0.369781  0.566692  0.167915  0.454313
Travis -0.380479 -0.115895  1.095088 -1.042988  1.356148
>>>
>>> mapping = {'a': 'red', 'b': 'red', 'c': 'blue', 'd': 'blue', 'e': 'red', 'f' : 'orange'}
>>> by_column = people.groupby(mapping, axis = 1)
>>> by_column.sum()
            blue       red
Joe    -0.882651 -1.344434
Steve   1.896841 -2.019384
Wes     0.341934 -1.087615
Jim     0.734607  1.180685
Travis  0.052100  0.859774
>>>
>>> map_series = pd.Series(mapping)
>>> map_series
a       red
b       red
c      blue
d      blue
e       red
f    orange
dtype: object
>>> people.groupby(map_series, axis = 1).count() # 计算数量
        blue  red
Joe        2    3
Steve      2    3
Wes        1    2
Jim        2    3
Travis     2    3
>>>
>>> # 通过函数分组
>>> people.groupby(len).sum()
          a         b         c         d         e
3 -0.249547  0.364219  1.211464 -1.017574 -1.366036
5 -0.511867 -1.825093  0.970510  0.926331  0.317576
6 -0.380479 -0.115895  1.095088 -1.042988  1.356148
>>> key_list = ['one', 'one', 'one', 'two', 'two']
>>> people.groupby([len, key_list]).min()
              a         b         c         d         e
3 one -1.030695 -0.005562  0.644771 -1.527423 -1.763429
  two  0.356591  0.369781  0.566692  0.167915  0.454313
5 one -0.511867 -1.825093  0.970510  0.926331  0.317576
6 two -0.380479 -0.115895  1.095088 -1.042988  1.356148
>>>
>>> # 
>>> columns = pd.MultiIndex.from_arrays([['US', 'US', 'US', 'JP', 'JP'], [1, 3, 5, 1, 3]], names = ['cty', 'tenor'])
>>> hier_df = pd.DataFrame(np.random.randn(4, 5), columns = columns)
>>> hier_df
cty          US                            JP
tenor         1         3         5         1         3
0      0.119116  1.243414  0.325555  0.790014 -1.194997
1      1.135141  1.890262  1.196081 -0.345959 -1.271117
2     -0.242083  0.860681  0.646477  1.889308 -0.299354
3     -0.123762 -0.011193  1.084885 -1.488621  0.199857
>>>
>>> hier_df.groupby(level='cty', axis = 1).count() # 指定某一等级进行分组
cty  JP  US
0     2   3
1     2   3
2     2   3
3     2   3
```

* 聚合

```python
>>> df = pd.DataFrame({'key1' : ['a', 'a', 'b', 'b', 'a'], 'key2' : ['one', 'two', 'one', 'two', 'one'], 'data1' : np.random.randn(5), 'data2' : np.random.randn(5)})
>>> df
  key1 key2     data1     data2
0    a  one -0.247505  0.839460
1    a  two -1.737265 -1.131199
2    b  one  1.383777 -0.376133
3    b  two  0.113274  0.592628
4    a  one -0.690304 -0.867604
>>> grouped = df.groupby('key1')
>>> grouped['data1'].quantile(0.9) # 计算90% 分位数
key1
a   -0.336065
b    1.256727
Name: data1, dtype: float64
>>> def peak_to_peak(arr):
...     return arr.max() - arr.min()
...
>>> grouped.agg(peak_to_peak) # 自定义聚合函数
         data1     data2
key1
a     1.489760  1.970659
b     1.270503  0.968761
>>> grouped.describe() # 分组进行描述函数
     data1                                            ...        data2
     count      mean       std       min       25%    ...          min       25%       50%       75%       max
key1                                                  ...
a      3.0 -0.891691  0.765025 -1.737265 -1.213784    ...    -1.131199 -0.999401 -0.867604 -0.014072  0.839460
b      2.0  0.748525  0.898381  0.113274  0.430900    ...    -0.376133 -0.133942  0.108248  0.350438  0.592628

[2 rows x 16 columns]
>>>
>>> tips = pd.DataFrame({'total_bill': [16.99, 10.34, 21.01, 23.68, 24.59, 25.29], 'tip': [1.01, 1.66, 3.50, 3.31, 3.61, 4.71], 'smoker': ['No', 'No', 'No', 'No', 'No', 'No'], 'day': ['Sun', 'Sun', 'Sun', 'Sun', 'Sun', 'Sun'], 'time': ['Dinner', 'Dinner', 'Dinner', 'Dinner', 'Dinner', 'Dinner'], 'size': [2, 3, 3, 2, 4, 4]})
>>> tips
   total_bill   tip smoker  day    time  size
0       16.99  1.01     No  Sun  Dinner     2
1       10.34  1.66     No  Sun  Dinner     3
2       21.01  3.50     No  Sun  Dinner     3
3       23.68  3.31     No  Sun  Dinner     2
4       24.59  3.61     No  Sun  Dinner     4
5       25.29  4.71     No  Sun  Dinner     4
>>> tips['tip_pct'] = tips['tip'] / tips['total_bill']
>>> tips
   total_bill   tip smoker  day    time  size   tip_pct
0       16.99  1.01     No  Sun  Dinner     2  0.059447
1       10.34  1.66     No  Sun  Dinner     3  0.160542
2       21.01  3.50     No  Sun  Dinner     3  0.166587
3       23.68  3.31     No  Sun  Dinner     2  0.139780
4       24.59  3.61     No  Sun  Dinner     4  0.146808
5       25.29  4.71     No  Sun  Dinner     4  0.186240
>>> grouped = tips.groupby(['day', 'smoker']) # 按照 day smoker 分组
>>> grouped_pct = grouped['tip_pct'] # 选取指定列
>>> grouped_pct.agg('mean') # 求均值
day  smoker
Sun  No        0.143234
Name: tip_pct, dtype: float64
>>> grouped_pct.agg(['mean', 'std', peak_to_peak]) # 求mean std peak_to_peak
                mean       std  peak_to_peak
day smoker
Sun No      0.143234  0.044135      0.126793
>>> grouped_pct.agg([('foo', 'mean'), ('bar', np.std)]) # 对聚合函数进行重命名
                 foo       bar
day smoker
Sun No      0.143234  0.044135
>>>
>>> functions = ['count', 'mean', 'max']
>>> result = grouped['tip_pct', 'total_bill'].agg(functions) # 对列应用函数组计算
>>> result
           tip_pct                    total_bill
             count      mean      max      count       mean    max
day smoker
Sun No           6  0.143234  0.18624          6  20.316667  25.29
>>> result['tip_pct']
            count      mean      max
day smoker
Sun No          6  0.143234  0.18624
>>>
>>> ftuples = [('Durchschnitt', 'mean'),('Abweichung', np.var)]
>>> grouped['tip_pct', 'total_bill'].agg(ftuples) # 指定自定义名称
                tip_pct              total_bill
           Durchschnitt Abweichung Durchschnitt Abweichung
day smoker
Sun No         0.143234   0.001948    20.316667  33.077747
>>> grouped.agg({'tip' : np.max, 'size' : 'sum'})
             tip  size
day smoker
Sun No      4.71    18
>>> grouped.agg({'tip_pct' : ['min', 'max', 'mean', 'std'], 'size' : 'sum'})
             tip_pct                              size
                 min      max      mean       std  sum
day smoker
Sun No      0.059447  0.18624  0.143234  0.044135   18
>>>
>>> tips.groupby(['day', 'smoker'], as_index = False).mean() # 聚合数据都有由唯一的分组键组成的索引（可能还是层次化的）。可以向groupby传入as_index=False以禁用该功能
   day smoker  total_bill       tip  size   tip_pct
0  Sun     No   20.316667  2.966667     3  0.143234
>>>
>>> def top(df, n = 5, column='tip_pct'):
...     return df.sort_values(by=column)[-n:]
...
>>> top(tips, n = 6)
   total_bill   tip smoker  day    time  size   tip_pct
0       16.99  1.01     No  Sun  Dinner     2  0.059447
3       23.68  3.31     No  Sun  Dinner     2  0.139780
4       24.59  3.61     No  Sun  Dinner     4  0.146808
1       10.34  1.66     No  Sun  Dinner     3  0.160542
2       21.01  3.50     No  Sun  Dinner     3  0.166587
5       25.29  4.71     No  Sun  Dinner     4  0.186240
>>> tips.groupby('smoker').apply(top) # 对每个分组调用这个函数
          total_bill   tip smoker  day    time  size   tip_pct
smoker
No     3       23.68  3.31     No  Sun  Dinner     2  0.139780
       4       24.59  3.61     No  Sun  Dinner     4  0.146808
       1       10.34  1.66     No  Sun  Dinner     3  0.160542
       2       21.01  3.50     No  Sun  Dinner     3  0.166587
       5       25.29  4.71     No  Sun  Dinner     4  0.186240
>>> tips.groupby(['smoker', 'day']).apply(top, n = 1, column = 'total_bill') # 指定函数的参数
              total_bill   tip smoker  day    time  size  tip_pct
smoker day
No     Sun 5       25.29  4.71     No  Sun  Dinner     4  0.18624
>>> result = tips.groupby('smoker')['tip_pct'].describe() # 指定分组的列进行函数
>>> result
        count      mean       std       min       25%       50%       75%      max
smoker
No        6.0  0.143234  0.044135  0.059447  0.141537  0.153675  0.165076  0.18624
>>> result.unstack('smoker')
       smoker
count  No        6.000000
mean   No        0.143234
std    No        0.044135
min    No        0.059447
25%    No        0.141537
50%    No        0.153675
75%    No        0.165076
max    No        0.186240
dtype: float64
>>>
>>> grouped.apply(lambda x: x.describe()) # 匿名函数
                  total_bill       tip      size   tip_pct
day smoker
Sun No     count    6.000000  6.000000  6.000000  6.000000
           mean    20.316667  2.966667  3.000000  0.143234
           std      5.751326  1.370499  0.894427  0.044135
           min     10.340000  1.010000  2.000000  0.059447
           25%     17.995000  2.072500  2.250000  0.141537
           50%     22.345000  3.405000  3.000000  0.153675
           75%     24.362500  3.582500  3.750000  0.165076
           max     25.290000  4.710000  4.000000  0.186240
>>> tips.groupby('smoker', group_keys = False).apply(top) # 禁用分组键
   total_bill   tip smoker  day    time  size   tip_pct
3       23.68  3.31     No  Sun  Dinner     2  0.139780
4       24.59  3.61     No  Sun  Dinner     4  0.146808
1       10.34  1.66     No  Sun  Dinner     3  0.160542
2       21.01  3.50     No  Sun  Dinner     3  0.166587
5       25.29  4.71     No  Sun  Dinner     4  0.186240
>>>
>>> # 分位数和桶分析
>>> df = pd.DataFrame({'data1': np.random.randn(1000), 'data2': np.random.randn(1000)})
>>> quartiles = pd.cut(df.data1, 4) # 按照样本分位数分成 4 个片，每个片长度相等
>>>
>>> def get_stats(group):
...     return {'min': group.min(), 'max': group.max(), 'count': group.count(), 'mean': group.mean()}
...
>>> grouped = df.data2.groupby(quartiles)
>>> grouped.apply(get_stats).unstack()
                   count       max      mean       min
data1
(-3.126, -1.602]    60.0  2.198863  0.117761 -2.136785
(-1.602, -0.0846]  418.0  3.620271 -0.063688 -2.881248
(-0.0846, 1.433]   441.0  3.494448 -0.044065 -2.521566
(1.433, 2.951]      81.0  2.616863  0.106218 -2.036658
>>>
>>> grouping = pd.qcut(df.data1, 10, labels = False) # 按照样本分位数进行分片，每个片长度不等
>>> grouped = df.data2.groupby(grouping)
>>> grouped.apply(get_stats).unstack()
       count       max      mean       min
data1
0      100.0  2.675240  0.027128 -2.314295
1      100.0  1.806032 -0.103512 -2.457887
2      100.0  3.620271 -0.003968 -2.881248
3      100.0  2.254870 -0.094208 -2.026318
4      100.0  1.978568 -0.021608 -2.000379
5      100.0  3.031282 -0.040011 -2.301995
6      100.0  1.753286 -0.180444 -2.153139
7      100.0  3.494448  0.035509 -2.356695
8      100.0  2.597087  0.012859 -2.521566
9      100.0  2.616863  0.064407 -2.036658
>>>
>>> # 透视表和交叉表
>>> tips.pivot_table(index=['day', 'smoker']) # 按照指定列进行透视表
            size       tip   tip_pct  total_bill
day smoker
Sun No         3  2.966667  0.143234   20.316667
>>> tips.pivot_table(['tip_pct', 'size'], index=['time', 'day'], columns = 'smoker') # 聚合tip_pct和size，根据time, day进行分组，smoker作为列
           size   tip_pct
smoker       No        No
time   day
Dinner Sun    3  0.143234
>>> tips.pivot_table(['tip_pct', 'size'], index=['time', 'day'], columns='smoker', margins=True)
           size       tip_pct
smoker       No All        No       All
time   day
Dinner Sun    3   3  0.143234  0.143234
All           3   3  0.143234  0.143234
>>> tips.pivot_table('tip_pct', index = ['time', 'smoker'], columns='day', aggfunc = len, margins = True) # 使用指定的聚合函数
day            Sun  All
time   smoker
Dinner No      6.0  6.0
All            6.0  6.0
>>> tips.pivot_table('tip_pct', index=['time', 'size', 'smoker'], columns='day', aggfunc='mean', fill_value = 0) # 前冲空值后进行聚合
day                      Sun
time   size smoker
Dinner 2    No      0.099614
       3    No      0.163564
       4    No      0.166524
>>> # 交叉表
>>> df
   Sample Nationality    Handedness
0       1         USA  Right-handed
1       2       Japan   Left-handed
2       3         USA  Right-handed
3       4       Japan  Right-handed
4       5       Japan   Left-handed
5       6       Japan  Right-handed
6       7         USA  Right-handed
7       8         USA   Left-handed
8       9       Japan  Right-handed
9      10         USA  Right-handed
>>> pd.crosstab(df.Nationality, df.Handedness, margins = True)
Handedness   Left-handed  Right-handed  All
Nationality
Japan                  2             3    5
USA                    1             4    5
All                    3             7   10
>>> pd.crosstab([tips.time, tips.day], tips.smoker, margins=True)
smoker        No  Yes  All
time   day                
Dinner Fri     3    9   12
       Sat    45   42   87
       Sun    57   19   76
       Thur    1    0    1
Lunch  Fri     1    6    7
       Thur   44   17   61
All          151   93  244
```

### 7.4.7 时间序列

```python
>>> import pandas as pd
>>> import numpy as np
>>> from datetime import datetime
>>>
>>> now = datetime.now()
>>> now
datetime.datetime(2019, 4, 14, 14, 57, 2, 607604) # datetime以毫秒形式存储日期和时间
>>> now.year
2019
>>> now.month
4
>>> now.day
14
>>> delta = datetime(2011, 1, 7) - datetime(2008, 6, 24, 8, 15) # 求时间差
>>> delta
datetime.timedelta(926, 56700)
>>> delta.days
926
>>> delta.seconds
56700
>>> value = '2011-01-03'
>>> datetime.strptime(value, '%Y-%m-%d') # 字符串转换成时间对象
datetime.datetime(2011, 1, 3, 0, 0)
>>> datestrs = ['7/6/2011', '8/6/2011']
>>> [datetime.strptime(x, '%m/%d/%Y') for x in datestrs] # 针对格式化编码键字符串转换为时间
[datetime.datetime(2011, 7, 6, 0, 0), datetime.datetime(2011, 8, 6, 0, 0)]
>>>
>>> from dateutil.parser import parse # 常见的时间编码格式解析的库
>>>
>>> parse('2011-01-03')
datetime.datetime(2011, 1, 3, 0, 0)
>>> parse('Jan 31, 1997 10:45 PM')
datetime.datetime(1997, 1, 31, 22, 45)
>>> parse('6/12/2011', dayfirst=True)
datetime.datetime(2011, 12, 6, 0, 0)
>>>
>>> datestrs = ['2011-07-06 12:00:00', '2011-08-06 00:00:00']
>>> pd.to_datetime(datestrs) # to_datetime方法可以解析多种不同的日期表示形式
DatetimeIndex(['2011-07-06 12:00:00', '2011-08-06 00:00:00'], dtype='datetime64[ns]', freq=None)
>>>
>>> idx = pd.to_datetime(datestrs + [None]) # 还可以处理缺失值
>>> idx
DatetimeIndex(['2011-07-06 12:00:00', '2011-08-06 00:00:00', 'NaT'], dtype='datetime64[ns]', freq=None)
>>> idx[2]
NaT
>>> pd.isnull(idx)
array([False, False,  True])
>>>
>>> # 时间序列基础
>>> from datetime import datetime
>>> dates = [datetime(2011, 1, 2), datetime(2011, 1, 5), datetime(2011, 1, 7), datetime(2011, 1, 8), datetime(2011, 1, 10), datetime(2011, 1, 12)] # 最基本的时间序列类型就是以时间戳
>>> ts = pd.Series(np.random.randn(6), index=dates)
>>> ts
2011-01-02    0.333535
2011-01-05   -0.075027
2011-01-07    1.124325
2011-01-08    0.125570
2011-01-10   -0.306823
2011-01-12    0.428457
dtype: float64
>>> ts.index
DatetimeIndex(['2011-01-02', '2011-01-05', '2011-01-07', '2011-01-08', '2011-01-10', '2011-01-12'], dtype='datetime64[ns]', freq=None)
>>> ts + ts[::2] # 不同索引的时间序列之间的算术运算会自动按日期对齐
2011-01-02    0.667071
2011-01-05         NaN
2011-01-07    2.248650
2011-01-08         NaN
2011-01-10   -0.613646
2011-01-12         NaN
dtype: float64
>>> ts.index.dtype # 用NumPy的datetime64数据类型以纳秒形式存储时间戳
dtype('<M8[ns]')
>>>
>>> stamp = ts.index[0]
>>> stamp
Timestamp('2011-01-02 00:00:00')
>>>
>>> stamp = ts.index[0]
>>> stamp
Timestamp('2011-01-02 00:00:00')
>>>
>>> stamp = ts.index[2]
>>> ts[stamp]
1.1243249102150383
>>> ts['1/10/2011'] # 传入一个可以被解释为日期的字符串索引选取数据
-0.3068230768613339
>>> ts['20110110']
-0.3068230768613339
>>>
>>> longer_ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
>>> longer_ts
2000-01-01    1.222843
2000-01-02   -0.271132
2000-01-03   -1.501011
2000-01-04   -0.644345
2000-01-05   -0.704011
2000-01-06    0.050380
2000-01-07   -0.737766
2000-01-08   -2.021776
2000-01-09    1.385572
2000-01-10   -0.454104
2000-01-11    0.688225
2000-01-12    0.637390
2000-01-13    1.719199
2000-01-14   -0.002724
2000-01-15   -0.903036
2000-01-16    0.756754
2000-01-17    0.392026
2000-01-18   -0.706296
2000-01-19    1.151165
2000-01-20    0.079625
2000-01-21   -0.472052
2000-01-22   -1.477105
2000-01-23    0.358813
2000-01-24   -0.184131
2000-01-25   -0.041601
2000-01-26   -0.479601
2000-01-27    0.881606
2000-01-28   -0.951334
2000-01-29   -0.037862
2000-01-30    0.167141
                ...
2002-08-28   -0.258072
2002-08-29   -0.414740
2002-08-30    1.230950
2002-08-31    0.125225
2002-09-01    0.501439
2002-09-02   -0.167500
2002-09-03    0.451182
2002-09-04    0.225198
2002-09-05    0.360042
2002-09-06   -0.311505
2002-09-07   -0.173966
2002-09-08   -0.905943
2002-09-09   -0.079419
2002-09-10    0.793470
2002-09-11   -0.683641
2002-09-12   -0.096508
2002-09-13   -1.188629
2002-09-14   -1.750932
2002-09-15   -0.880764
2002-09-16   -0.555012
2002-09-17    0.272917
2002-09-18   -0.102776
2002-09-19    0.425911
2002-09-20   -1.197386
2002-09-21    0.424416
2002-09-22   -0.538048
2002-09-23    0.087369
2002-09-24   -1.502346
2002-09-25    0.198375
2002-09-26   -0.530859
Freq: D, Length: 1000, dtype: float64
>>> longer_ts['2001'] # 对于较长的时间序列，只需传入“年”或“年月”即可轻松选取数据的切片
2001-01-01   -0.882748
2001-01-02   -3.371471
2001-01-03   -0.693397
2001-01-04   -1.486200
2001-01-05   -1.312219
2001-01-06   -1.149771
2001-01-07    0.610819
2001-01-08    0.699712
2001-01-09    0.420111
2001-01-10    0.639840
2001-01-11   -0.403378
2001-01-12   -1.194900
2001-01-13   -1.284597
2001-01-14   -0.114514
2001-01-15    0.513225
2001-01-16   -0.277911
2001-01-17    0.933601
2001-01-18    1.385059
2001-01-19    0.108851
2001-01-20    0.985631
2001-01-21   -0.927034
2001-01-22    0.946125
2001-01-23    0.878829
2001-01-24    1.167784
2001-01-25   -0.233972
2001-01-26    0.493551
2001-01-27    1.629848
2001-01-28    0.052982
2001-01-29   -0.609424
2001-01-30   -0.510213
                ...
2001-12-02    1.123397
2001-12-03    0.660333
2001-12-04   -1.801672
2001-12-05   -0.205906
2001-12-06   -0.535307
2001-12-07   -0.732763
2001-12-08   -0.451930
2001-12-09   -1.479985
2001-12-10   -0.518113
2001-12-11    1.239788
2001-12-12    0.878961
2001-12-13   -0.283507
2001-12-14    0.298770
2001-12-15   -1.218034
2001-12-16   -0.788832
2001-12-17    0.139006
2001-12-18   -0.721656
2001-12-19   -0.911452
2001-12-20    0.767588
2001-12-21    0.827079
2001-12-22    0.819848
2001-12-23   -0.836723
2001-12-24   -0.426866
2001-12-25    0.405659
2001-12-26   -0.463876
2001-12-27   -0.713284
2001-12-28   -1.389079
2001-12-29   -0.488248
2001-12-30    0.047046
2001-12-31    1.900386
Freq: D, Length: 365, dtype: float64
>>> longer_ts['2001-05'] # 指定月也同样奏效
2001-05-01    1.042674
2001-05-02    1.031177
2001-05-03   -0.438955
2001-05-04    4.044227
2001-05-05   -0.598783
2001-05-06   -0.406856
2001-05-07   -1.898497
2001-05-08    0.113137
2001-05-09    1.378242
2001-05-10    0.989399
2001-05-11   -1.362318
2001-05-12   -0.043546
2001-05-13   -1.072461
2001-05-14    0.109050
2001-05-15   -0.887780
2001-05-16   -0.663451
2001-05-17   -1.112314
2001-05-18   -1.122386
2001-05-19    0.862525
2001-05-20    0.701046
2001-05-21    1.697688
2001-05-22   -0.033784
2001-05-23   -0.147078
2001-05-24   -0.782681
2001-05-25   -1.196842
2001-05-26   -0.576644
2001-05-27   -1.066685
2001-05-28    1.804850
2001-05-29   -0.612760
2001-05-30   -1.106360
2001-05-31   -0.939074
Freq: D, dtype: float64
>>> ts[datetime(2011, 1, 7):] # 也可以进行切片
2011-01-07    1.124325
2011-01-08    0.125570
2011-01-10   -0.306823
2011-01-12    0.428457
dtype: float64
>>> ts
2011-01-02    0.333535
2011-01-05   -0.075027
2011-01-07    1.124325
2011-01-08    0.125570
2011-01-10   -0.306823
2011-01-12    0.428457
dtype: float64
>>> ts['1/6/2011':'1/11/2011'] # 范围查询
2011-01-07    1.124325
2011-01-08    0.125570
2011-01-10   -0.306823
dtype: float64
>>> ts.truncate(after='1/9/2011') # 截取两个日期之间TimeSeries
2011-01-02    0.333535
2011-01-05   -0.075027
2011-01-07    1.124325
2011-01-08    0.125570
dtype: float64
>>>
>>> dates = pd.date_range('1/1/2000', periods=100, freq='W-WED') # 对DataFrame也有效
>>> long_df = pd.DataFrame(np.random.randn(100, 4), index=dates, columns=['Colorado', 'Texas', 'New York', 'Ohio'])
>>> long_df.loc['5-2001']
            Colorado     Texas  New York      Ohio
2001-05-02 -0.282713 -0.943762 -0.826692  1.307700
2001-05-09  1.112437  0.617931  0.608714 -0.487003
2001-05-16  2.121348 -0.365944 -0.340720  0.080809
2001-05-23  1.354461  0.048902  0.694478  1.330714
2001-05-30 -1.724245 -0.722224  0.356464 -0.312777
>>>
>>> # 带有重复索引的时间序列
>>> dates = pd.DatetimeIndex(['1/1/2000', '1/2/2000', '1/2/2000', '1/2/2000', '1/3/2000'])
>>> dup_ts = pd.Series(np.arange(5), index=dates)
>>> dup_ts
2000-01-01    0
2000-01-02    1
2000-01-02    2
2000-01-02    3
2000-01-03    4
dtype: int32
>>> dup_ts.index.is_unique
False
>>> dup_ts['1/3/2000'] # 要么产生标量值
4
>>> dup_ts['1/2/2000'] # 要么产生切片
2000-01-02    1
2000-01-02    2
2000-01-02    3
dtype: int32
>>>
>>> grouped = dup_ts.groupby(level=0) # 对具有非唯一时间戳的数据进行聚合，一个办法是使用groupby，并传入level=0
>>> grouped.mean()
2000-01-01    0
2000-01-02    2
2000-01-03    4
dtype: int32
>>> grouped.count()
2000-01-01    1
2000-01-02    3
2000-01-03    1
dtype: int64
>>>
>>> # 日期的范围、频率以及移动
>>> ts
2011-01-02    0.333535
2011-01-05   -0.075027
2011-01-07    1.124325
2011-01-08    0.125570
2011-01-10   -0.306823
2011-01-12    0.428457
dtype: float64
>>> resampler = ts.resample('D')
>>> index = pd.date_range('2012-04-01', '2012-06-01') # 生成日期范围
>>> index
DatetimeIndex(['2012-04-01', '2012-04-02', '2012-04-03', '2012-04-04',
               '2012-04-05', '2012-04-06', '2012-04-07', '2012-04-08',
               '2012-04-09', '2012-04-10', '2012-04-11', '2012-04-12',
               '2012-04-13', '2012-04-14', '2012-04-15', '2012-04-16',
               '2012-04-17', '2012-04-18', '2012-04-19', '2012-04-20',
               '2012-04-21', '2012-04-22', '2012-04-23', '2012-04-24',
               '2012-04-25', '2012-04-26', '2012-04-27', '2012-04-28',
               '2012-04-29', '2012-04-30', '2012-05-01', '2012-05-02',
               '2012-05-03', '2012-05-04', '2012-05-05', '2012-05-06',
               '2012-05-07', '2012-05-08', '2012-05-09', '2012-05-10',
               '2012-05-11', '2012-05-12', '2012-05-13', '2012-05-14',
               '2012-05-15', '2012-05-16', '2012-05-17', '2012-05-18',
               '2012-05-19', '2012-05-20', '2012-05-21', '2012-05-22',
               '2012-05-23', '2012-05-24', '2012-05-25', '2012-05-26',
               '2012-05-27', '2012-05-28', '2012-05-29', '2012-05-30',
               '2012-05-31', '2012-06-01'],
              dtype='datetime64[ns]', freq='D')
>>> pd.date_range(start='2012-04-01', periods=20)
DatetimeIndex(['2012-04-01', '2012-04-02', '2012-04-03', '2012-04-04',
               '2012-04-05', '2012-04-06', '2012-04-07', '2012-04-08',
               '2012-04-09', '2012-04-10', '2012-04-11', '2012-04-12',
               '2012-04-13', '2012-04-14', '2012-04-15', '2012-04-16',
               '2012-04-17', '2012-04-18', '2012-04-19', '2012-04-20'],
              dtype='datetime64[ns]', freq='D')
>>> pd.date_range(end='2012-06-01', periods=20)
DatetimeIndex(['2012-05-13', '2012-05-14', '2012-05-15', '2012-05-16',
               '2012-05-17', '2012-05-18', '2012-05-19', '2012-05-20',
               '2012-05-21', '2012-05-22', '2012-05-23', '2012-05-24',
               '2012-05-25', '2012-05-26', '2012-05-27', '2012-05-28',
               '2012-05-29', '2012-05-30', '2012-05-31', '2012-06-01'],
              dtype='datetime64[ns]', freq='D')
>>> pd.date_range('2000-01-01', '2000-12-01', freq='BM') # 指定起始和结束日期
DatetimeIndex(['2000-01-31', '2000-02-29', '2000-03-31', '2000-04-28',
               '2000-05-31', '2000-06-30', '2000-07-31', '2000-08-31',
               '2000-09-29', '2000-10-31', '2000-11-30'],
              dtype='datetime64[ns]', freq='BM')
>>> pd.date_range('2012-05-02 12:56:31', periods=5)
DatetimeIndex(['2012-05-02 12:56:31', '2012-05-03 12:56:31',
               '2012-05-04 12:56:31', '2012-05-05 12:56:31',
               '2012-05-06 12:56:31'],
              dtype='datetime64[ns]', freq='D')
>>> pd.date_range('2012-05-02 12:56:31', periods=5, normalize=True)
DatetimeIndex(['2012-05-02', '2012-05-03', '2012-05-04', '2012-05-05',
               '2012-05-06'],
              dtype='datetime64[ns]', freq='D')
>>> # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects 时间序列频率列表
>>>
>>> pd.date_range('2012-05-02 12:56:31', periods=5)
DatetimeIndex(['2012-05-02 12:56:31', '2012-05-03 12:56:31',
               '2012-05-04 12:56:31', '2012-05-05 12:56:31',
               '2012-05-06 12:56:31'],
              dtype='datetime64[ns]', freq='D')
>>> pd.date_range('2012-05-02 12:56:31', periods=5, normalize=True)
DatetimeIndex(['2012-05-02', '2012-05-03', '2012-05-04', '2012-05-05',
               '2012-05-06'],
              dtype='datetime64[ns]', freq='D')
>>>
>>> pd.date_range('2000-01-01', '2000-01-03 23:59', freq='4h')
DatetimeIndex(['2000-01-01 00:00:00', '2000-01-01 04:00:00',
               '2000-01-01 08:00:00', '2000-01-01 12:00:00',
               '2000-01-01 16:00:00', '2000-01-01 20:00:00',
               '2000-01-02 00:00:00', '2000-01-02 04:00:00',
               '2000-01-02 08:00:00', '2000-01-02 12:00:00',
               '2000-01-02 16:00:00', '2000-01-02 20:00:00',
               '2000-01-03 00:00:00', '2000-01-03 04:00:00',
               '2000-01-03 08:00:00', '2000-01-03 12:00:00',
               '2000-01-03 16:00:00', '2000-01-03 20:00:00'],
              dtype='datetime64[ns]', freq='4H')
>>> pd.date_range('2000-01-01', periods=10, freq='1h30min') # 传入频率字符串
DatetimeIndex(['2000-01-01 00:00:00', '2000-01-01 01:30:00',
               '2000-01-01 03:00:00', '2000-01-01 04:30:00',
               '2000-01-01 06:00:00', '2000-01-01 07:30:00',
               '2000-01-01 09:00:00', '2000-01-01 10:30:00',
               '2000-01-01 12:00:00', '2000-01-01 13:30:00'],
              dtype='datetime64[ns]', freq='90T')
>>> rng = pd.date_range('2012-01-01', '2012-09-01', freq='WOM-3FRI') # “每月第3个星期五”的日期
>>> list(rng)
[Timestamp('2012-01-20 00:00:00', freq='WOM-3FRI'), Timestamp('2012-02-17 00:00:00', freq='WOM-3FRI'), Timestamp('2012-03-16 00:00:00', freq='WOM-3FRI'), Timestamp('2012-04-20 00:00:00', freq='WOM-3FRI'), Timestamp('2012-05-18 00:00:00', freq='WOM-3FRI'), Timestamp('2012-06-15 00:00:00', freq='WOM-3FRI'), Timestamp('2012-07-20 00:00:00', freq='WOM-3FRI'), Timestamp('2012-08-17 00:00:00', freq='WOM-3FRI')]
>>>
>>> ts = pd.Series(np.random.randn(4), index=pd.date_range('1/1/2000', periods=4, freq='M'))
>>> ts
2000-01-31   -1.006966
2000-02-29   -1.195399
2000-03-31   -0.836660
2000-04-30    0.527456
Freq: M, dtype: float64
>>> ts.shift(2) # 前移2
2000-01-31         NaN
2000-02-29         NaN
2000-03-31   -1.006966
2000-04-30   -1.195399
Freq: M, dtype: float64
>>> ts.shift(-2) # 后移2
2000-01-31   -0.836660
2000-02-29    0.527456
2000-03-31         NaN
2000-04-30         NaN
Freq: M, dtype: float64
>>> ts / ts.shift(1) - 1
2000-01-31         NaN
2000-02-29    0.187129
2000-03-31   -0.300099
2000-04-30   -1.630430
Freq: M, dtype: float64
>>> ts.shift(2, freq='M') # 对时间戳进行位移
2000-03-31   -1.006966
2000-04-30   -1.195399
2000-05-31   -0.836660
2000-06-30    0.527456
Freq: M, dtype: float64
>>> ts.shift(3, freq='D')
2000-02-03   -1.006966
2000-03-03   -1.195399
2000-04-03   -0.836660
2000-05-03    0.527456
dtype: float64
>>> ts.shift(1, freq='90T')
2000-01-31 01:30:00   -1.006966
2000-02-29 01:30:00   -1.195399
2000-03-31 01:30:00   -0.836660
2000-04-30 01:30:00    0.527456
Freq: M, dtype: float64
>>>
>>> # 通过偏移量对日期进行位移
>>> from pandas.tseries.offsets import Day, MonthEnd
>>> now = datetime(2011, 11, 17)
>>> now + 3 * Day()
Timestamp('2011-11-20 00:00:00')
>>> now + MonthEnd()
Timestamp('2011-11-30 00:00:00')
>>> now + MonthEnd(2) # 移动两个偏移量
Timestamp('2011-12-31 00:00:00')
>>> offset = MonthEnd()
>>> offset.rollforward(now) # 向前滚动
Timestamp('2011-11-30 00:00:00')
>>> offset.rollback(now)
Timestamp('2011-10-31 00:00:00') # 向后滚动
>>>
>>> ts = pd.Series(np.random.randn(20), index=pd.date_range('1/15/2000', periods=20, freq='4d'))
>>> ts
2000-01-15   -0.022910
2000-01-19    2.192282
2000-01-23   -0.005369
2000-01-27   -0.793929
2000-01-31    0.163929
2000-02-04   -1.208727
2000-02-08   -0.128358
2000-02-12    0.660290
2000-02-16   -0.642933
2000-02-20   -0.270957
2000-02-24    1.035243
2000-02-28   -0.714663
2000-03-03    0.228718
2000-03-07    0.543422
2000-03-11   -0.738712
2000-03-15    0.581632
2000-03-19    0.921999
2000-03-23   -0.326011
2000-03-27    0.974065
2000-03-31    0.475992
Freq: 4D, dtype: float64
>>> ts.groupby(offset.rollforward).mean()
2000-01-31    0.306800
2000-02-29   -0.181443
2000-03-31    0.332638
dtype: float64
>>> ts.resample('M').mean()
2000-01-31    0.306800
2000-02-29   -0.181443
2000-03-31    0.332638
Freq: M, dtype: float64
>>>
>>> # 时区处理
>>> rng = pd.date_range('3/9/2012 9:30', periods=6, freq='D')
>>> ts = pd.Series(np.random.randn(len(rng)), index=rng)
>>> ts
2012-03-09 09:30:00    0.377668
2012-03-10 09:30:00    2.023474
2012-03-11 09:30:00    0.540420
2012-03-12 09:30:00    0.417883
2012-03-13 09:30:00    0.729287
2012-03-14 09:30:00   -1.252820
Freq: D, dtype: float64
>>> print(ts.index.tz)
None
>>> pd.date_range('3/9/2012 9:30', periods=10, freq='D', tz='UTC') # 指定时区
DatetimeIndex(['2012-03-09 09:30:00+00:00', '2012-03-10 09:30:00+00:00',
               '2012-03-11 09:30:00+00:00', '2012-03-12 09:30:00+00:00',
               '2012-03-13 09:30:00+00:00', '2012-03-14 09:30:00+00:00',
               '2012-03-15 09:30:00+00:00', '2012-03-16 09:30:00+00:00',
               '2012-03-17 09:30:00+00:00', '2012-03-18 09:30:00+00:00'],
              dtype='datetime64[ns, UTC]', freq='D')
>>> ts
2012-03-09 09:30:00    0.377668
2012-03-10 09:30:00    2.023474
2012-03-11 09:30:00    0.540420
2012-03-12 09:30:00    0.417883
2012-03-13 09:30:00    0.729287
2012-03-14 09:30:00   -1.252820
Freq: D, dtype: float64
>>> ts_utc = ts.tz_localize('UTC')
>>> ts_utc.tz_convert('America/New_York') # 时区转换
2012-03-09 04:30:00-05:00    0.377668
2012-03-10 04:30:00-05:00    2.023474
2012-03-11 05:30:00-04:00    0.540420
2012-03-12 05:30:00-04:00    0.417883
2012-03-13 05:30:00-04:00    0.729287
2012-03-14 05:30:00-04:00   -1.252820
Freq: D, dtype: float64
>>> ts_eastern = ts.tz_localize('America/New_York')
>>> ts_eastern.tz_convert('UTC')
2012-03-09 14:30:00+00:00    0.377668
2012-03-10 14:30:00+00:00    2.023474
2012-03-11 13:30:00+00:00    0.540420
2012-03-12 13:30:00+00:00    0.417883
2012-03-13 13:30:00+00:00    0.729287
2012-03-14 13:30:00+00:00   -1.252820
Freq: D, dtype: float64
>>> ts_eastern.tz_convert('Europe/Berlin')
2012-03-09 15:30:00+01:00    0.377668
2012-03-10 15:30:00+01:00    2.023474
2012-03-11 14:30:00+01:00    0.540420
2012-03-12 14:30:00+01:00    0.417883
2012-03-13 14:30:00+01:00    0.729287
2012-03-14 14:30:00+01:00   -1.252820
Freq: D, dtype: float64
>>> ts.index.tz_localize('Asia/Shanghai')
DatetimeIndex(['2012-03-09 09:30:00+08:00', '2012-03-10 09:30:00+08:00',
               '2012-03-11 09:30:00+08:00', '2012-03-12 09:30:00+08:00',
               '2012-03-13 09:30:00+08:00', '2012-03-14 09:30:00+08:00'],
              dtype='datetime64[ns, Asia/Shanghai]', freq='D')
>>>
>>> stamp = pd.Timestamp('2011-03-12 04:00')
>>> stamp_utc = stamp.tz_localize('utc')
>>> stamp_utc.tz_convert('America/New_York')
Timestamp('2011-03-11 23:00:00-0500', tz='America/New_York')
>>>
>>> stamp_moscow = pd.Timestamp('2011-03-12 04:00', tz='Europe/Moscow')
>>> stamp_moscow
Timestamp('2011-03-12 04:00:00+0300', tz='Europe/Moscow')
>>>
>>> stamp_utc.value
1299902400000000000
>>> stamp_utc.tz_convert('America/New_York').value
1299902400000000000
>>>
>>> from pandas.tseries.offsets import Hour
>>> stamp = pd.Timestamp('2012-03-12 01:30', tz='US/Eastern')
>>> stamp
Timestamp('2012-03-12 01:30:00-0400', tz='US/Eastern')
>>> stamp + Hour()
Timestamp('2012-03-12 02:30:00-0400', tz='US/Eastern')
>>>
>>> stamp = pd.Timestamp('2012-11-04 00:30', tz='US/Eastern')
>>> stamp
Timestamp('2012-11-04 00:30:00-0400', tz='US/Eastern')
>>> stamp + 2 * Hour()
Timestamp('2012-11-04 01:30:00-0500', tz='US/Eastern')
>>>
>>> rng = pd.date_range('3/7/2012 9:30', periods=10, freq='B')
>>> ts = pd.Series(np.random.randn(len(rng)), index=rng)
>>> ts1 = ts[:7].tz_localize('Europe/London')
>>> ts2 = ts1[2:].tz_convert('Europe/Moscow')
>>> result = ts1 + ts2 # 如果两个时间序列的时区不同，在将它们合并到一起时，最终结果就会是UTC
>>> result.index
DatetimeIndex(['2012-03-07 09:30:00+00:00', '2012-03-08 09:30:00+00:00',
               '2012-03-09 09:30:00+00:00', '2012-03-12 09:30:00+00:00',
               '2012-03-13 09:30:00+00:00', '2012-03-14 09:30:00+00:00',
               '2012-03-15 09:30:00+00:00'],
              dtype='datetime64[ns, UTC]', freq='B')
>>>
>>> p = pd.Period(2007, freq='A-DEC')
>>> p
Period('2007', 'A-DEC')
>>>
>>> p + 5
Period('2012', 'A-DEC')
>>> p - 2
Period('2005', 'A-DEC')
>>>
>>> pd.Period('2014', freq='A-DEC') - p
7
>>>
>>> # 时期及其算术运算
>>> rng = pd.period_range('2000-01-01', '2000-06-30', freq='M') # period_range 创建规则的时期范围
>>> rng
PeriodIndex(['2000-01', '2000-02', '2000-03', '2000-04', '2000-05', '2000-06'], dtype='period[M]', freq='M')
>>> pd.Series(np.random.randn(6), index=rng)
2000-01   -1.733429
2000-02    0.185838
2000-03   -0.013668
2000-04   -0.372594
2000-05    0.451437
2000-06    0.429816
Freq: M, dtype: float64
>>>
>>> values = ['2001Q3', '2002Q2', '2003Q1']
>>> index = pd.PeriodIndex(values, freq='Q-DEC')
>>> index
PeriodIndex(['2001Q3', '2002Q2', '2003Q1'], dtype='period[Q-DEC]', freq='Q-DEC')
>>>
>>> p = pd.Period('2007', freq='A-DEC')
>>> p
Period('2007', 'A-DEC')
>>> # asfreq 转换为当年年初或年末的一个月度时期
>>> p.asfreq('M', how='start')
Period('2007-01', 'M')
>>> p.asfreq('M', how='end')
Period('2007-12', 'M')
>>>
>>> p = pd.Period('2007', freq='A-JUN')
>>> p
Period('2007', 'A-JUN')
>>>
>>> p.asfreq('M', 'start')
Period('2006-07', 'M')
>>> p.asfreq('M', 'end')
Period('2007-06', 'M')
>>>
>>> p = pd.Period('Aug-2007', 'M')
>>> p
Period('2007-08', 'M')
>>> p.asfreq('A-JUN')
Period('2008', 'A-JUN')
>>>
>>> rng = pd.period_range('2006', '2009', freq='A-DEC')
>>> ts = pd.Series(np.random.randn(len(rng)), index=rng)
>>> ts.asfreq('M', how='start')
2006-01   -0.772180
2007-01   -0.451701
2008-01   -0.379165
2009-01    0.516530
Freq: M, dtype: float64
>>> ts.asfreq('B', how='end')
2006-12-29   -0.772180
2007-12-31   -0.451701
2008-12-31   -0.379165
2009-12-31    0.516530
Freq: B, dtype: float64
>>> # 按季度计算的时期频率
>>> p = pd.Period('2012Q4', freq='Q-JAN')
>>> p
Period('2012Q4', 'Q-JAN')
>>> p.asfreq('D', 'start')
Period('2011-11-01', 'D')
>>> p.asfreq('D', 'end')
Period('2012-01-31', 'D')
>>>
>>> p4pm = (p.asfreq('B', 'e') - 1).asfreq('T', 's') + 16 * 60
>>> p4pm
Period('2012-01-30 16:00', 'T')
>>> p4pm.to_timestamp()
Timestamp('2012-01-30 16:00:00')
>>>
>>> rng = pd.period_range('2011Q3', '2012Q4', freq='Q-JAN')
>>> ts = pd.Series(np.arange(len(rng)), index=rng)
>>> ts
2011Q3    0
2011Q4    1
2012Q1    2
2012Q2    3
2012Q3    4
2012Q4    5
Freq: Q-JAN, dtype: int32
>>>
>>> new_rng = (rng.asfreq('B', 'e') - 1).asfreq('T', 's') + 16 * 60
>>> ts.index = new_rng.to_timestamp()
>>> ts
2010-10-28 16:00:00    0
2011-01-28 16:00:00    1
2011-04-28 16:00:00    2
2011-07-28 16:00:00    3
2011-10-28 16:00:00    4
2012-01-30 16:00:00    5
dtype: int32
>>> 
>>> # 将Timestamp转换为Period
>>> rng = pd.date_range('2000-01-01', periods=3, freq='M')
>>> ts = pd.Series(np.random.randn(3), index=rng)
>>> ts
2000-01-31    0.729536
2000-02-29    0.448136
2000-03-31    0.882884
Freq: M, dtype: float64
>>> pts = ts.to_period() # 通过使用to_period方法，可以将由时间戳索引的Series和DataFrame对象转换为以时期索引
>>> pts
2000-01    0.729536
2000-02    0.448136
2000-03    0.882884
Freq: M, dtype: float64
>>>
>>> rng = pd.date_range('1/29/2000', periods=6, freq='D') # 指定任何别的频率
>>> ts2 = pd.Series(np.random.randn(6), index=rng)
>>> ts2
2000-01-29   -0.076665
2000-01-30    1.710172
2000-01-31   -0.349030
2000-02-01   -1.055936
2000-02-02   -0.441720
2000-02-03    0.928499
Freq: D, dtype: float64
>>> ts2.to_period('M')
2000-01   -0.076665
2000-01    1.710172
2000-01   -0.349030
2000-02   -1.055936
2000-02   -0.441720
2000-02    0.928499
Freq: M, dtype: float64
>>> pts = ts2.to_period()
>>> pts
2000-01-29   -0.076665
2000-01-30    1.710172
2000-01-31   -0.349030
2000-02-01   -1.055936
2000-02-02   -0.441720
2000-02-03    0.928499
Freq: D, dtype: float64
>>> pts.to_timestamp(how='end') # 转换回时间戳，使用to_timestamp即可
2000-01-29   -0.076665
2000-01-30    1.710172
2000-01-31   -0.349030
2000-02-01   -1.055936
2000-02-02   -0.441720
2000-02-03    0.928499
Freq: D, dtype: float64
>>>
>>> # 通过数组创建PeriodIndex
>>> data = pd.read_csv('examples/macrodata.csv')
>>> data.head(5)
     year  quarter   realgdp  realcons  realinv  realgovt  realdpi    cpi  \
0  1959.0      1.0  2710.349    1707.4  286.898   470.045   1886.9  28.98   
1  1959.0      2.0  2778.801    1733.7  310.859   481.301   1919.7  29.15   
2  1959.0      3.0  2775.488    1751.8  289.226   491.260   1916.4  29.35   
3  1959.0      4.0  2785.204    1753.7  299.356   484.052   1931.3  29.37   
4  1960.0      1.0  2847.699    1770.5  331.722   462.199   1955.5  29.54   
      m1  tbilrate  unemp      pop  infl  realint  
0  139.7      2.82    5.8  177.146  0.00     0.00  
1  141.7      3.08    5.1  177.830  2.34     0.74  
2  140.5      3.82    5.3  178.657  2.74     1.09  
3  140.0      4.33    5.6  179.386  0.27     4.06  
4  139.6      3.50    5.2  180.007  2.31     1.19  
>>> data.year
0      1959.0
1      1959.0
2      1959.0
3      1959.0
4      1960.0
5      1960.0
6      1960.0
7      1960.0
8      1961.0
9      1961.0
        ...  
193    2007.0
194    2007.0
195    2007.0
196    2008.0
197    2008.0
198    2008.0
199    2008.0
200    2009.0
201    2009.0
202    2009.0
Name: year, Length: 203, dtype: float64
>>> data.quarter
0      1.0
1      2.0
2      3.0
3      4.0
4      1.0
5      2.0
6      3.0
7      4.0
8      1.0
9      2.0
      ... 
193    2.0
194    3.0
195    4.0
196    1.0
197    2.0
198    3.0
199    4.0
200    1.0
201    2.0
202    3.0
Name: quarter, Length: 203, dtype: float64
>>>
>>> index = pd.PeriodIndex(year=data.year, quarter=data.quarter, freq='Q-DEC')
>>> index
PeriodIndex(['1959Q1', '1959Q2', '1959Q3', '1959Q4', '1960Q1', '1960Q2',
             '1960Q3', '1960Q4', '1961Q1', '1961Q2',
             ...
             '2007Q2', '2007Q3', '2007Q4', '2008Q1', '2008Q2', '2008Q3',
             '2008Q4', '2009Q1', '2009Q2', '2009Q3'],
            dtype='period[Q-DEC]', length=203, freq='Q-DEC')
>>>
>>> # 重采样及频率转换
>>>
```

### 7.4.8 高级