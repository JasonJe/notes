## 5.2 `SQL`

>date: 2019-02-16

![](../assets/images/52.jpg)

### 5.2.1 数据操纵

`SELECT * FROM celebs;` 提取celebs表中的全部数据

* 数据类型

*integer* 整数类型
*text* 文本字符串类型
*date* 日期类型
*real* 实数类型

* 创建表

```sql
CREATE TABLE table_name (
    column_1 data_type, 
    column_2 data_type, 
    column_3 data_type
  );
```

* 插入数据

```sql
INSERT INTO celebs (id, name, age)
VALUES (1, 'Justin Bieber', 21);
```

* 选取某一列

```sql
SELECT name FROM celebs;
```

* 更新数据

```sql
UPDATE celebs
SET age = 22
WHERE id = 1;
```

* 修改数据表

增加一列数据定义

```sql
ALTER TABLE celebs ADD COLUMN twitter_handle TEXT;
```

* 删除数据

```sql
DELETE FROM celebs WHERE twitter_handle IS NULL;
```

* 清空表

```sql
TRUNCATE TABLE celebs;
```

* 删除表

```sql
DROP TABLE celebs;
```

### 5.2.2 数据查询

* 单表查询

```sql
SELECT name, imdb_rating FROM movies;
```

【`DISINCT` 操作符 保证查询结果为唯一值】
```sql
SELECT DISTINCT genre FROM movies;
```

【`WHERE` 操作符 过滤查询/条件查询】
```sql
SELECT * FROM movies WHERE imdb_rating > 8;
```

`WHERE` 条件运算符有

`=` 等于

`!=` 不等于

`>` 大于

`<` 小于

`>=` 大于等于

`<=` 小于等于

【`LIKE` 操作符 模糊查询】

```sql
SELECT * FROM movies
WHERE name LIKE 'Se_en';
```

```sql
SELECT * FROM movies
WHERE name LIKE 'a%';

SELECT * FROM movies
WHERE name LIKE '%man%'
```

`LIKE` 通配符
`_` 通配单个字符
`%` 通配零个或多个字符

`A%` 匹配所有开头为'A'的字符
`%a` 匹配所有结尾为'a'的字符

【`BETWEEN ... AND ...` 操作符 匹配范围内的记录】

```sql
SELECT * FROM movies
WHERE name BETWEEN 'A' AND 'J';
```

```sql
SELECT * FROM movies
WHERE year BETWEEN 1990 AND 2000
AND genre = 'comedy';
```

【`AND & OR` 操作符 逻辑过滤】

如果第一个条件和第二个条件都成立，则 AND 运算符显示一条记录
如果第一个条件和第二个条件中只要有一个成立，则 OR 运算符显示一条记录

```sql
SELECT * FROM movies
WHERE genre = 'comedy'
OR year < 1980;
```

【`ORDER BY DESC/ASC` 操作符 排序】

`ASC` 升序排序
`DESC` 降序排序

```sql
SELECT * FROM movies
ORDER BY imdb_rating DESC;
```

【`LIMIT` 操作符 限制记录数量】

```sql
SELECT * FROM movies
ORDER BY imdb_rating ASC
LIMIT 3;
```

### 5.2.3 聚合函数

【`COUNT(...)` 计数函数】

```sql
SELECT COUNT(*) FROM fake_apps;
```

【`GROUP BY` 分组函数】

```sql
SELECT price, COUNT(*) FROM fake_apps
GROUP BY price;
```

```sql
SELECT price, COUNT(*) FROM fake_apps
WHERE downloads > 20000
GROUP BY price;
```

【`SUM(...)` 求和函数】

```sql
SELECT SUM(downloads) FROM fake_apps;
```

```sql
SELECT category, SUM(downloads) FROM fake_apps
GROUP BY category;
```

【`MAX(...)` 最大值函数】

```sql
SELECT MAX(downloads) FROM fake_apps;
```

```sql
SELECT name, category, MAX(downloads) FROM fake_apps
GROUP BY category;
```

【`MIN(...)` 最小值函数】

```sql
SELECT MIN(downloads) FROM fake_apps;
```

【`AVG(...)` 平均函数】

```sql
SELECT AVG(downloads) FROM fake_apps;
```

```sql
SELECT price, AVG(downloads) FROM fake_apps
GROUP BY price;
```

【`ROUND(...)` 舍入为指定小数位数函数】

```sql
SELECT price, ROUND(AVG(downloads), 2) FROM fake_apps
GROUP BY price;
```

### 5.2.4 多表

【`PRIMARY KEY` 主键】

定义为主键的一列不为NULL值，都是唯一值

```sql
CREATE TABLE artists(id INTEGER PRIMARY KEY, name TEXT)
```

【`FOREIGN KEY` 外键】

* 多表查询

```sql
SELECT albums.name, albums.year, artists.name FROM albums, artists;
```

【`INNER JOIN` 内连接】

```sql
SELECT
*
FROM
albums
JOIN artists ON
albums.artist_id = artists.id;
```

【`LEFT JOIN` 左连接】

```sql
SELECT
*
FROM
albums
LEFT JOIN artists ON
albums.artist_id = artists.id;
```

【`AS` 关键字 重命名列名】

```sql
SELECT
albums.name AS 'Album',
albums.year,
artists.name AS 'Artist'
FROM
albums
JOIN artists ON
albums.artist_id = artists.id
WHERE
albums.year > 1980;
```

### 5.2.5 子查询

* 非关联子查询

【嵌套查询】

```sql
SELECT *
FROM flights
WHERE origin in (
SELECT code
FROM airports
WHERE elevation < 2000);
```

```sql
SELECT a.dep_month,
    a.dep_day_of_week,
    AVG(a.flight_distance) AS average_distance
FROM (
    SELECT dep_month,
            dep_day_of_week,
            dep_date,
            sum(distance) AS flight_distance
    FROM flights
    GROUP BY 1,2,3
    ) a
GROUP BY 1,2
ORDER BY 1,2;
```

* 关联子查询

【外部查询取出一行后，再对内部查询中的每一行内进行运算，TRUE时候返回查询结果】

```sql
SELECT id
FROM flights AS f
WHERE distance < (
SELECT AVG(distance)
FROM flights
WHERE carrier = f.carrier
);
```

### 5.2.6 集合操作

【`UNION` 并集】

```sql
SELECT column_name(s) FROM table1
UNION
SELECT column_name(s) FROM table2;
```

`UNION ALL` 会列出所有的值，即不去重

【`INTERSECT` 交集】

```sql
SELECT category FROM new_products
INTERSECT
SELECT category FROM legacy_products;
```

【`EXCEPT` 差集】

```sql
SELECT category FROM new_products
EXCEPT
SELECT category FROM legacy_products;
```

### 5.2.7 条件聚合

`IS NULL` 值为空
`IS NOT NULL` 值不为空

【`CASE` 控制结构】

```sql
SELECT
CASE
    WHEN elevation < 250 THEN 'Low'
    WHEN elevation BETWEEN 250 AND 1749 THEN 'Medium'
    WHEN elevation >= 1750 THEN 'High'
    ELSE 'Unknown'
END AS elevation_tier
, COUNT(*)
FROM airports
GROUP BY 1;
```

【`COUNT(CASE WHEN)`】

```sql
SELECT    state, 
COUNT(CASE WHEN elevation >= 2000 THEN 1 ELSE NULL END) as count_high_elevation_aiports 
FROM airports 
GROUP BY state;
```

【`SUM(CASE WHEN)`】

```sql
SELECT origin, sum(distance) as total_flight_distance, sum(CASE WHEN carrier = 'DL' THEN distance ELSE 0 END) as total_delta_flight_distance 
FROM flights 
GROUP BY origin;
```

```sql
SELECT origin, 100.0*(sum(CASE WHEN carrier = 'UN' THEN distance ELSE 0 END)/sum(distance)) as percentage_flight_distance_from_united 
FROM flights 
GROUP BY origin;
```

```sql
SELECT state,
100.0 * sum(CASE WHEN elevation >= 2000 THEN 1 ELSE 0 END) / count(*)  as percentage_high_elevation_airports
FROM airports
GROUP BY state;
```

### 5.2.8 日期，数字和字符串函数

【`Dates` 时间函数】

```sql
SELECT DATETIME(manufacture_time)
FROM baked_goods;
```

```sql
SELECT DATE(manufacture_time), count(*) as count_baked_goods
FROM baked_goods
GROUP BY DATE(manufacture_time);
```

```sql
SELECT TIME(manufacture_time), count(*) as count_baked_goods
FROM baked_goods
GROUP BY TIME(manufacture_time);
```

在当前时间进行时间的增加，下述例子在当前时间上增加了1天2小时30分钟

```sql
SELECT DATETIME(manufacture_time, '+2 hours', '30 minutes', '1 day') as inspection_time
FROM baked_goods;
```

【`Numbers` 数字函数】

```sql
SELECT ROUND(ingredients_cost, 4) as rounded_cost
FROM baked_goods;
```

`SELECT (number1 + number2)` 返回两个数字的和
`SELECT CAST(number1 AS REAL) / number3` CAST()函数用于将某种数据类型的表达式显式转换为另一种数据类型
`SELECT ROUND(number, precision)` 四舍五入数字，precision为精度

返回两列数据中同行的最小值

```sql
SELECT id, MIN(cook_time, cool_down_time)
FROM baked_goods;
```

【`||` 字符串连接运算】

`SELECT string1 || ' ' || string2;` 利用"||"连接string1和一个空格和string2

【`REPLACE()` 字符串替换运算】

`REPLACE(string,from_string,to_string)` 将string列中的"from_string"字符串替换为"to_string"字符串


### 5.2.9 视图

视图是虚拟的表，本身不包含数据，也就不能对其进行索引操作。对视图的操作和对普通表的操作一样。

视图具有如下好处：

1) 简化复杂的 `SQL` 操作，比如复杂的连接；

2) 只使用实际表的一部分数据；

3) 通过只给用户访问视图的权限，保证数据的安全性；

4) 更改数据格式和表示。

```sql
CREATE VIEW myview AS
SELECT CONCAT(col1, col2) AS concat_col, col3*col4 AS compute_col
FROM test
WHERE col5 = val;
```

### 5.2.10 存储过程

存储过程可以看成是对一系列 `SQL` 操作的批处理。

使用存储过程的好处：

1) 代码封装，保证了一定的安全性；

2) 代码复用；

3) 由于是预先编译，因此具有很高的性能。

命令行中创建存储过程需要自定义分隔符，因为命令行是以 `;` 为结束符，而存储过程中也包含了分号，因此会错误把这部分分号当成是结束符，造成语法错误。

包含 `in`、`out` 和 `inout` 三种参数。

给变量赋值都需要用 `select into` 语句。

每次只能给一个变量赋值，不支持集合的操作。

```sql
DELIMITER //

CREATE PROCEDURE myprocedure(out ret int)
    BEGIN
        DECLARE y INT;
        SELELCT SUM(col1)
        FROM mytable
        INTO y;
        SELECT y*y INTO ret;
    END //

DELIMITER;

CALL myprocedure(@ret);
SELECT @ret;
```

### 5.2.11 触发器

触发器会在某个表执行以下语句时而自动执行：`DELETE`、`INSERT`、`UPDATE`。

触发器必须指定在语句执行之前还是之后自动执行，之前执行使用 `BEFORE` 关键字，之后执行使用 `AFTER` 关键字。`BEFORE` 用于数据验证和净化，`AFTER` 用于审计跟踪，将修改记录到另外一张表中。

`INSERT` 触发器包含一个名为 `NEW` 的虚拟表。

```sql
CREATE TRIGGER mytrigger AFTER INSERT ON mytable
FOR EACH ROW SELECT NEW.col into @result;

SELECT @result; -- 获取结果
```

`DELETE` 触发器包含一个名为 `OLD` 的虚拟表，并且是只读的。

`UPDATE` 触发器包含一个名为 `NEW` 和一个名为 `OLD` 的虚拟表，其中 `NEW` 是可以被修改的，而 `OLD` 是只读的。

`MySQL` 不允许在触发器中使用 `CALL` 语句，也就是不能调用存储过程。

### 5.2.12 事务管理

基本术语：

1) 事务（`transaction`）指一组 `SQL` 语句；

2) 回退（`rollback`）指撤销指定 `SQL` 语句的过程；

3) 提交（`commit`）指将未存储的 `SQL` 语句结果写入数据库表；

4)保留点（`savepoint`）指事务处理中设置的临时占位符（`placeholder`），你可以对它发布回退（与回退整个事务处理不同）。

不能回退 `SELECT` 语句，回退 `SELECT` 语句也没意义；也不能回退 `CREATE` 和 `DROP` 语句。

`MySQL` 的事务提交默认是隐式提交，每执行一条语句就把这条语句当成一个事务然后进行提交。当出现 `START TRANSACTION` 语句时，会关闭隐式提交；当 `COMMIT` 或 `ROLLBACK` 语句执行后，事务会自动关闭，重新恢复隐式提交。

通过设置 `autocommit` 为 `0` 可以取消自动提交；`autocommit` 标记是针对每个连接而不是针对服务器的。

如果没有设置保留点，`ROLLBACK` 会回退到 `START TRANSACTION` 语句处；如果设置了保留点，并且在 `ROLLBACK` 中指定该保留点，则会回退到该保留点。

```sql
START TRANSACTION
// ...
SAVEPOINT delete1
// ...
ROLLBACK TO delete1
// ...
COMMIT
```