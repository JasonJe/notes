## 5.5 MongoDB

>date: 2019-02-21

![](../assets/images/55.jpg)

### 5.5.1 `NoSQL`和`MongoDB`

#### `NoSQL`

`NoSQL`(`NoSQL = Not Only SQL`)，意即"不仅仅是`SQL`"。指的是非关系型的数据库，是对不同于传统的关系数据库管理系统(`RDBMS`)的统称。

`NoSQL`用于超大规模数据的存储。（例如谷歌或`Facebook`每天为他们的用户收集万亿比特的数据）。这些类型的数据存储不需要固定的模式，无需多余操作就可以横向扩展。

* `RDBMS vs NoSQL`

`RDBMS`：高度组织化结构化数据、结构化查询语言（`SQL`）、数据和关系都存储在单独的表中、数据操纵语言，数据定义语言、严格的一致性、基础事务

`NoSQL`：代表着不仅仅是`SQL`、没有声明性查询语言、没有预定义的模式、键 - 值对存储，列存储，文档存储，图形数据库、最终一致性，而非`ACID`属性、非结构化和不可预知的数据、`CAP`定理、高性能，高可用性和可伸缩性

* 分布式系统

在介绍`CAP`定理前先介绍下什么是分布式系统。

分布式系统（`distributed system`）由多台计算机和通信的软件组件通过计算机网络连接（本地网络或广域网）组成。

分布式系统是建立在网络之上的软件系统。正是因为软件的特性，所以分布式系统具有高度的内聚性和透明性。

因此，网络和分布式系统之间的区别更多的在于高层软件（特别是操作系统），而不是硬件。

1) 分布式计算的优点

可靠性（容错）：分布式计算系统中的一个重要的优点是可靠性。一台服务器的系统崩溃并不影响到其余的服务器；

可扩展性：在分布式计算系统可以根据需要增加更多的机器；

资源共享：共享数据是必不可少的应用，如银行，预订系统；

灵活性：由于该系统是非常灵活的，它很容易安装，实施和调试新的服务；

更快的速度：分布式计算系统可以有多台计算机的计算能力，使得它比其他系统有更快的处理速度；

开放系统：由于它是开放的系统，本地或者远程都可以访问到该服务；

更高的性能：相较于集中式计算机网络集群可以提供更高的性能（及更好的性价比）。

2) 分布式计算的缺点

故障排除：故障排除和诊断问题；

软件：更少的软件支持是分布式计算系统的主要缺点；

网络：网络基础设施的问题，包括：传输问题，高负载，信息丢失等；

安全性：开放系统的特性让分布式计算系统存在着数据的安全性和共享的风险等问题。

* `CAP`定理

在计算机科学中, CAP定理（`CAP theorem`）, 又被称作 布鲁尔定理（`Brewer's theorem`）, 它指出对于一个分布式计算系统来说，不可能同时满足以下三点:

1) 一致性(`Consistency`)：所有节点在同一时间具有相同的数据；

2) 可用性(`Availability`)：保证每个请求不管成功或者失败都有响应；

3) 分隔容忍(`Partition tolerance`)：系统中任意信息的丢失或失败不会影响系统的继续运作。

`CAP`理论的核心是：一个分布式系统不可能同时很好的满足一致性，可用性和分区容错性这三个需求，最多只能同时较好的满足两个。

因此，根据 `CAP` 原理将 `NoSQL` 数据库分成了满足 `CA` 原则、满足 `CP` 原则和满足 `AP` 原则三 大类：

1) `CA` - 单点集群，满足一致性，可用性的系统，通常在可扩展性上不太强大；

2) `CP` - 满足一致性，分区容忍性的系统，通常性能不是特别高；

3) `AP` - 满足可用性，分区容忍性的系统，通常可能对一致性要求低一些。

![](../assets/images/551_01.png)

* NoSQL的优点/缺点

1) 优点：高可扩展性、分布式计算、低成本、架构的灵活性，半结构化数据、没有复杂的关系

2) 缺点：没有标准化、有限的查询功能（到目前为止）、最终一致是不直观的程序

* `BASE`(`Basically Available`, `Soft-state`, `Eventually Consistent`)

`BASE`是`NoSQL`数据库通常对可用性及一致性的弱要求原则：

`Basically Availble`：基本可用；

`Soft-state`：软状态/柔性事务。"Soft state" 可以理解为"无连接"的, 而 "Hard state" 是"面向连接"的；

`Eventual Consistency`：最终一致性， 也是是 ACID 的最终目的。

#### `MongoDB`

`MongoDB` 是由`C++`语言编写的，是一个基于分布式文件存储的开源数据库系统。

`MongoDB` 是一个介于关系数据库和非关系数据库之间的产品，是非关系数据库当中功能最丰富，最像关系数据库的。他支持的数据结构非常松散，是类似 `json` 的 `bjson` 格式，因此可以存储比较复杂的数据类型。

1) 面向集合（Collenction-Orented）；
2) 模式自由（schema-free)；
3) 文档型。

* `SQL`与`MongoDB`概念对照

|SQL概念|MongoDB概念|说明|
|:--:|:--:|:--:|
|database|database|数据库|
|table|collection|数据表/集合|
|row|document|数据记录行/文档|
|column|field|数据字段/域|
|index|index|索引|
|table joins| |表连接,MongoDB不支持|
|primary key|primary key|主键,MongoDB自动将_id字段设置为主键|

* 特点、功能和适用场合

1) 特点：

> * 面向集合存储，易于存储对象类型的数据；
>
> * 模式自由；
>
> * 支持动态查询；
>
> * 支持完全索引，包含内部对象；
>
> * 支持查询；支持复制和故障恢复；
>
> * 使用高效的二进制数据存储，包括大型对象（如视频等）；
>
> * 自动处理碎片，以支持云计算层次的扩展性；
>
> * 支持 `Python`，`PHP`，`Ruby`，`Java`，`C`，`C#`，`Javascript`，`Perl` 及 `C++`语言的驱动程序，社区也提供了对 `Erlang` 及`.NET` 等平台的驱动程序；
>
> * 文件存储格式为 `BSON`（一种 `JSON` 的扩展）；
>
> * 可通过网络访问。
>

2) 功能

> * 面向集合的存储：适合存储对象及 `JSON` 形式的数据；
>
> * 动态查询：`MongoDB` 支持丰富的查询表达式。查询指令使用 `JSON` 形式的标记，可轻易；
>
> * 查询文档中内嵌的对象及数组；
>
> * 完整的索引支持：包括文档内嵌对象及数组。MongoDB 的查询优化器会分析查询表达式，并生成一个高效的查询计划；
>
> * 查询监视：`MongoDB` 包含一系列监视工具用于分析数据库操作的性能；
>
> * 复制及自动故障转移：`MongoDB` 数据库支持服务器之间的数据复制，支持主-从模式及服务器之间的相互复制。复制的主要目标是提供冗余及自动故障转移；
>
> * 高效的传统存储方式：支持二进制数据及大型对象（如照片或图片）；
>
> * 自动分片以支持云级别的伸缩性：自动分片功能支持水平的数据库集群，可动态添加额外的机器。
>

3) 适用场合

> * 网站数据：`MongoDB` 非常适合实时的插入，更新与查询，并具备网站实时数据存储所需的复制及高度伸缩性；
>
> * 缓存：由于性能很高，`MongoDB` 也适合作为信息基础设施的缓存层。在系统重启之后，由 `MongoDB` 搭建的持久化缓存层可以避免下层的数据源过载；
>
> * 大尺寸，低价值的数据：使用传统的关系型数据库存储一些数据时可能会比较昂贵，在此之前，很多时候程序员往往会选择传统的文件进行存储；
>
> * 高伸缩性的场景：`MongoDB` 非常适合由数十或数百台服务器组成的数据库。`MongoDB`的路线图中已经包含对 `MapReduce` 引擎的内置支持；
>
> * 用于对象及 `JSON` 数据的存储：`MongoDB` 的 `BSON` 数据格式非常适合文档化格式的存储及查询。
>

* 数据类型

|Type|Number|String|Notes|
|:--:|:--:|:--:|:--:|
|Double|1|"double"|-----|
|字符串|2|"string"|存储数据常用的数据类型。在 MongoDB 中，UTF-8 编码的字符串才是合法的。|
|对象|3|"object"|-----|
|数组|4|"array"|-----|
|二进制数据|5|"binData"|-----|
|未定义|6|"undefined"|已过期|
|对象 ID|7|"objectId"|用于创建文档的 ID。|
|布尔值|8|"bool"|-----|
|日期|9|"date"|-----|
|空|10|"null"|-----|
|正则表达式|11|"regex"|-----|
|DBPointer|12|"dbPointer"|已过期|
JavaScript(代码)|13|"javascript"|此数据类型用于将JavaScript代码存储到文档中|
|符号|14|"symbol"|已过期|
|JavaScript(带范围)|15|"javascriptWithScope"|-----|
|32位整数|16|"int"|根据你所采用的服务器，可分为 32 位或 64 位。|
|时间戳|17|"timestamp"|记录文档修改或添加的具体时间|
|64位整数|18|"long"|-----|
|Decimal128|19|"decimal"|New in version 3.4|
|Min key|-1|"minKey"|将一个值与 BSON（二进制的 JSON）元素的最低值和最高值相对比。|
|Max key|127|"maxKey"|将一个值与 BSON（二进制的 JSON）元素的最低值和最高值相对比。|

### 5.5.2 常用命令

* 数据库连接

```bash
mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]] # 标准连接语法

$ mongo
MongoDB shell version v4.0.3
connecting to: mongodb://127.0.0.1:27017
MongoDB server version: 4.0.3
> mongodb://admin:123456@localhost/test
```

* 数据库操作

```bash
use DATABASE_NAME

> use test # 创建数据库
switched to db test
> db # 当前使用的数据库
test
> show dbs # 查看所有的数据库。刚创建的数据库并不在数据库的列表中，要显示它，需要向其插入一些数据
> db.dropDatabase() # 删除数据库
{ "dropped" : "test", "ok" : 1 }
```

* 集合操作

```bash
db.createCollection(name, options)

# options 参数：

# capped（可选）：如果为 true，则创建固定集合。固定集合是指有着固定大小的集合，当达到最大值时，它会自动覆盖最早的文档。当该值为 true 时，必须指定 size 参数。默认为 false。
# autoIndexId（可选）：如为 true，自动在 _id 字段创建索引。默认为 false。
# size数值（可选）：为固定集合指定一个最大值（以字节计）。
# max数值（可选）：指定固定集合中包含文档的最大数量。

> use test # 切换数据库
switched to db test
> db.createCollection("set_test") # 创建集合
{ "ok" : 1 }
> db.createCollection("set_test_2", { capped : true, autoIndexId : true, size : 6142800, max : 10000 } ) # 带参数创建集合
{ "ok" : 1 }
> show collections # 显示存在的集合
set_test
set_test_2
> db.set_test_2.drop() # 上传集合
> true
```

* 文档操作

```bash
db.COLLECTION_NAME.insert(document) # 插入文档

> db.set_test.insert({
        set: 'test',
        test: 'test'
})
WriteResult({ "nInserted" : 1 })

> db.set_test.find()
{ "_id" : ObjectId("56064886ade2f21f36b03134"), "set" : "test", "test" : "test" }
> db.set_test.find().pretty()
> document=({
        set: 'test',
        test: 'test'
});
> db.set_test.insert(document)
WriteResult({ "nInserted" : 1 })

db.COLLECTION_NAME.update() # 更新文档

> db.set_test.update({'set':'test'},{$set:{'set':'test2'}},{multi:true}) # 只会修改第一条发现的文档，如果要修改多条相同的文档，则需要设置 multi 参数为 true

db.COLLECTION_NAME.save( # 替换已有文档
   <document>,
   {
     writeConcern: <document>
   }
)

> db.set_test.save({
    "_id" : ObjectId("56064886ade2f21f36b03134"),
    "set" : "test3",
    "test" : "test2"
})
> db.set_test.find().pretty()
{
    "_id" : ObjectId("56064886ade2f21f36b03134"),
    "set" : "test3",
    "test" : "test2"
}

db.COLLECTION_NAME.remove(
   <query>,
   {
     justOne: <boolean>,
     writeConcern: <document>
   }
)

# 参数说明：
# 
# query（可选）：删除的文档的条件。
# justOne（可选）：如果设为 true 或 1，则只删除一个文档，如果不设置该参数，或使用默认值 false，则删除所有匹配条件的文档。
# writeConcern（可选）：抛出异常的级别。

> db.set_test.remove({'set':'test3'})
WriteResult({ "nRemoved" : 1 })
> db.set_test.find()
>
> db.set_test.remove({}) # 删除全部数据
>

db.COLLECTION_NAME.find(query, projection)

# 参数说明：
# 
# query（可选）：使用查询操作符指定查询条件
# projection（可选）：使用投影操作符指定返回的键。查询时返回文档中所有键值， 只需省略该参数即可（默认省略）。

> db.set_test.find({"set":"test3", "test":"test2"}).pretty() # 实现AND运算，传入多个键即可
{
    "_id" : ObjectId("56064886ade2f21f36b03134"),
    "set" : "test3",
    "test" : "test2"
}
> db.set_test.find({$or:[{"set":"test3"},{"test": "test2"}]}).pretty() # 使用$or关键字实现OR运算
{
    "_id" : ObjectId("56064886ade2f21f36b03134"),
    "set" : "test3",
    "test" : "test2"
}
> db.set_test.find({"set":"test"}).pretty() # 等于条件 WHERE set = "test"
> db.set_test.find({"set":{$lt:50}}).pretty() # 小于 WHERE set < 50
> db.set_test.find({"set":{$lte:50}}).pretty() # 小于等于 WHERE set <= 50
> db.set_test.find({"set":{$gt:50}}).pretty() # 大于 WHERE set > 50
> db.set_test.find({"set":{$gte:50}}).pretty() # 大于等于 WHERE set >= 50
> db.set_test.find({"set":{$ne:50}}).pretty() # 不等于 WHERE set != 50
> db.set_test.find({"set":{$lt:200,$gt:100}}).pretty() # WHERE set > 100 AND set < 200
> db.set_test.find({"set":{$type:'string'}}).pretty() # 找set为字符串的数据
> db.set_test.find({"set":{$type:2}}).pretty() # 两句相同


db.COLLECTION_NAME.find().limit(NUMBER) # 指定从MongoDB中读取的记录条数
> db.set_test.find({},{"set":1,_id:0}).limit(2) # LIMIT  

db.COLLECTION_NAME.find().limit(NUMBER).skip(NUMBER) # 跳过指定数量的数据
> db.set_test.find({},{"title":1,_id:0}).limit(1).skip(1)


db.COLLECTION_NAME.find().sort({KEY:1}) # 排序，其中 1 为升序排列，而 -1 是用于降序排列。
> db.set_test.find({},{"set":1,_id:0}).sort({"test":-1})
```

* 索引

```bash
db.COLLECTION_NAME.createIndex({KEY:1}, options) # 创建索引，其中 1 为升序排列，而 -1 是用于降序排列。

# 参数说明（都为可选）：

# background：Boolean，建索引过程会阻塞其它数据库操作，background可指定以后台方式创建索引，即增加 "background" 可选参数。 "background" 默认值为false。
# unique：Boolean，建立的索引是否唯一。指定为true创建唯一索引。默认值为false.
# name：string，索引的名称。如果未指定，MongoDB的通过连接索引的字段名和排序顺序生成一个索引名称。
# dropDups：Boolean，3.0+版本已废弃。在建立唯一索引时是否删除重复记录,指定 true 创建唯一索引。默认值为 false.
# sparse：Boolean，对文档中不存在的字段数据不启用索引；这个参数需要特别注意，如果设置为true的话，在索引字段中不会查询出不包含对应字段的文档.。默认值为 false.
# expireAfterSeconds：integer，指定一个以秒为单位的数值，完成 TTL设定，设定集合的生存时间。
# v：index version，索引的版本号。默认的索引版本取决于mongod创建索引时运行的版本。
# weights：document，索引权重值，数值在 1 到 99,999 之间，表示该索引相对于其他索引字段的得分权重。
# default_language：string，对于文本索引，该参数决定了停用词及词干和词器的规则的列表。 默认为英语
# language_override：string，对于文本索引，该参数指定了包含在文档中的字段名，语言覆盖默认的language，默认值为 language.

> db.set_test.createIndex({"set":1,"test":-1},{background: true})

> db.set_test.getIndexes() # 查看集合索引
> db.set_test.totalIndexSize() # 查看集合索引大小
> db.set_test.dropIndexes() # 删除集合所有索引
> db.set_test.dropIndex("index_name") # 删除集合指定索引

# 覆盖查询是指：所有的查询字段是索引的一部分；所有的查询返回字段在同一个索引中
# 由于所有出现在查询中的字段是索引的一部分， MongoDB 无需在整个数据文档中检索匹配查询条件和返回使用相同索引的查询结果。

# 因为索引存在于RAM中，从索引中获取数据比通过扫描文档读取数据要快得多。
{
   "_id": ObjectId("53402597d852426020000002"),
   "contact": "987654321",
   "dob": "01-01-1991",
   "gender": "M",
   "name": "Tom Benzamin",
   "user_name": "tombenzamin"
}

> db.set_test.ensureIndex({gender:1,user_name:1}) # 它会覆盖这个查询： db.set_test.find({gender:"M"},{user_name:1,_id:0})
> db.set_test.find({gender:"M"},{user_name:1}) # 这个查询不会被覆盖

# 针对下面的文档中的tags数组建立索引，会为依次为music、cricket、blogs三个值建立单独的索引。
{
   "address": {
      "city": "Los Angeles",
      "state": "California",
      "pincode": "123"
   },
   "tags": [
      "music",
      "cricket",
      "blogs"
   ],
   "name": "Tom Benzamin"
}
> db.set_test.ensureIndex({"tags":1}) # 创建数组索引，数组索引不能使用覆盖索引查询
> db.set_test.find({tags:"cricket"}).explain() # 验证使用的索引

> db.set_test.ensureIndex({"address.city":1,"address.state":1,"address.pincode":1}) # 为子文档的三个字段创建索引
> db.set_test.find({"address.city":"Los Angeles"}) # 这样就可以使用子文档的字段来检索数据

# 索引限制
# 由于索引是存储在内存(RAM)中，所以应该确保该索引的大小不超过内存的限制。
# 如果索引的大小大于内存的限制，MongoDB会删除一些索引，这将导致性能下降。

# 索引不能被以下的查询使用：

# 正则表达式及非操作符，如 $nin，$not等。
# 算术运算符，如 $mod，等。
# $where 子句

# 检测语句是否使用索引，可以用explain来查看。

# 集合中索引不能超过64个；
# 索引名的长度不能超过128个字符；
# 一个复合索引最多可以有31个字段。
```

* 聚合

```bash
db.COLLECTION_NAME.aggregate(AGGREGATE_OPERATION)

> db.set_test.aggregate([{$group:{_id:"$set",num_tutorial:{$sum:"$test"}}}]) # 计算总和。SELECT set, COUNT(test) FROM set_test GROUP BY set;
> db.set_test.aggregate([{$group:{_id:"$set",num_tutorial:{$avg:"$test"}}}]) # 计算平均值。SELECT set, AVG(test) FROM set_test GROUP BY set;
> db.set_test.aggregate([{$group:{_id:"$set",num_tutorial:{$min:"$test"}}}]) # 获取集合中所有文档对应值得最小值。SELECT set, MIN(test) FROM set_test GROUP BY set;
> db.set_test.aggregate([{$group:{_id:"$set",num_tutorial: {$max:"$test"}}}]) # 获取集合中所有文档对应值得最大值。SELECT set, MAX(test) FROM set_test GROUP BY set;

> db.set_test.aggregate([{$group:{_id:"$set",new_set:{$push: "$new_set"}}}]) # 在结果文档中插入值到一个数组中。 SELECT set 
{ "_id" : "test", "new_set" : [ ] }

> db.set_test.aggregate([{$group:{_id:"$set",new_set:{$addToSet:"$new_set"}}}]) # 在结果文档中插入值到一个数组中，但不创建副本。
{ "_id" : "test", "new_set" : [ ] }

> db.set_test.aggregate([{$group:{_id:"$set",first_res:{$first:"$new_set"}}}]) # 根据资源文档的排序获取第一个文档数据。
{ "_id" : "test", "first_res" : null }

> db.set_test.aggregate([{$group:{_id:"$set",last_res:{$last:"$new_set"}}}]) # 根据资源文档的排序获取最后一个文档数据。
{ "_id" : "test", "last_res" : null }


# 聚合管道

# 聚合管道将文档在一个管道处理完毕后将结果传递给下一个管道处理，它的操作是可以重复的。管道表达式处理输入文档并输出，它是无状态的，只能用于计算当前聚合管道的文档，不能处理其它的文档。

> db.set_test.insert({name:'dogOne',age:1,tags:['animal','dog'],type:'dog',money:[{min:100},{norm:200},{big:300}]});
WriteResult({ "nInserted" : 1 })
>
> db.set_test.insert({name:'catOne',age:3,tags:['animal','cat'],type:'cat',money:[{min:50},{norm:100},{big:200}]});
WriteResult({ "nInserted" : 1 })
>
> db.set_test.insert({name:'catTwo',age:2,tags:['animal','cat'],type:'cat',money:[{min:20},{norm:50},{big:100}]});
WriteResult({ "nInserted" : 1 })
>
> db.set_test.insert({name:'dogTwo',age:5,tags:['animal','dog'],type:'dog',money:[{min:300},{norm:500},{big:700}]});
WriteResult({ "nInserted" : 1 })
>
> db.set_test.insert({name:'appleOne',age:0,tags:['fruit','apple'],type:'apple',money:[{min:10},{norm:12},{big:13}]});
WriteResult({ "nInserted" : 1 })
>
> db.set_test.insert({name:'appleTwo',age:0,tags:['fruit','apple'],type:'apple',money:[{min:10},{norm:12},{big:13}]});
WriteResult({ "nInserted" : 1 })
>
> db.set_test.insert({name:'pineapple',age:0,tags:['fruit','pineapple'],type:'pineapple',money:[{min:8},{norm:9},{big:10}]});
WriteResult({ "nInserted" : 1 })
>


# $match：用于过滤数据，只输出符合条件的文档。$match使用MongoDB的标准查询操作。
# $project：修改输入文档的结构。可以用来重命名、增加或删除域，也可以用于创建计算结果以及嵌套文档。
# 提取money中min为100的文档，并且只输出名称和money数组中的min那一项
> db.set_test.aggregate({$match:{'money.min':100}},{$project:{_id:0,name:'$name',minprice:'$money.min'}})
{ "name" : "dogOne", "minprice" : [ 100 ] }

# $limit：用来限制MongoDB聚合管道返回的文档数。
# $skip：在聚合管道中跳过指定数量的文档，并返回余下的文档。
# 提取money中min小于100的文档，并且限制3个文档，跳过一个文档再显示
> db.set_test.aggregate({$match:{'money.min':{$lt:100}}},{$limit:3},{$skip:1},{$project:{_id:0,name:'$name',minprice:'$money.min'}})
{ "name" : "catTwo", "minprice" : [ 20 ] }
{ "name" : "appleOne", "minprice" : [ 10 ] }

# $group：将集合中的文档分组，可用于统计结果。
# 通过type类型来对数据进行分类，并且同时统计他们的年龄age总和
> db.set_test.aggregate({$group:{_id:'$type',sumage:{$sum:'$age'}}})
{ "_id" : "pineapple", "sumage" : 0 }
{ "_id" : "apple", "sumage" : 0 }
{ "_id" : "cat", "sumage" : 5 }
{ "_id" : "dog", "sumage" : 6 }

# $sort：将输入文档排序后输出。1代表升序，-1代表降序。
# 按照年龄对数据进行排序
> db.set_test.aggregate({$group:{_id:'$type',sumage:{$sum:'$age'}}},{$skip:1},{$sort:{sumage:1}})
{ "_id" : "apple", "sumage" : 0 }
{ "_id" : "cat", "sumage" : 5 }
{ "_id" : "dog", "sumage" : 6 }
```

* 权限管理

开启验证：

```bash
# echo "auth = true" >> /root/mongodb/bin/mongodb.conf`
# systemctl restart systemd-mongodb

> db.auth('myuser','password') # 授权
1
> use admin # 切换数据库

> db.createUser({user:'myuser',pwd:'password',roles:[{role:"userAdminAnyDatabase",db:"admin"}]}); # 创建用户
Successfully added user: {
        "user" : "myuser",
        "roles" : [
                {
                        "role" : "userAdminAnyDatabase",
                        "db" : "admin"
                }
        ]
}

> db.system.users.find() # 查看用户列表
> db.runCommand({usersInfo:'myuser'}) # 查看某个用户信息
> db.runCommand({updateUser:'myuser',pwd:'newpassword',customData:{title:"xxx"……}}) # 修改用户信息
> db.changeUserPassword('myuser','newpassword'); # 修改用户密码
> db.system.users.remove({user:'myuser'}); # 删除用户
```

### 5.5.3 高级操作

* 副本集

早期的`MongoDB`版本使用`master-slave`，一主一从和`MySQL`类似，但`slave`在此架构中为只读，当主库宕机后，从库不能自动切换为主。目前已经淘汰`master-slave`模式，改为副本集，这种模式下有一个主(`primary`)，和多个从(`secondary`)，只读。

支持给它们设置权重，当主宕掉后，权重最高的从切换为主。在此架构中还可以建立一个仲裁(`arbiter`)的角色，它只负责裁决，而不存储数据。此架构中读写数据都是在主上，要想实现负载均衡的目的需要手动指定读库的目标`server`。

副本集的搭建这边不做介绍，可以参考[手把手教你搭建mongodb副本集](https://juejin.im/post/5be42ab06fb9a049fa0f40c7)或者自行搜索相关文档。

副本集的特征是：`N`个节点的集群，任何节点可作为主节点，所有写入操作都在主节点上，自动故障转移，能够自动恢复。

![副本集集群结构](../assets/images/553_01.png)

* 分片

分片（`Sharding`）是指将数据库拆分，将其分散在不同的机器上的过程。将数据分散到不同的机器上，不需要功能强大的服务器就可以存储更多的数据和处理更大的负载。基本思想就是将集合切成小块，这些块分散到若干片里，每个片只负责总数据的一部分，最后通过一个均衡器来对各个分片进行均衡（数据迁移）。

通过一个名为`mongos`的路由进程进行操作，`mongos`知道数据和片的对应关系（通过配置服务器）。大部分使用场景都是解决磁盘空间的问题，对于写入有可能会变差，查询则尽量避免跨分片查询。

使用分片的时机：

1) 机器的磁盘不够用了。使用分片解决磁盘空间的问题。
2) 单个mongod已经不能满足写数据的性能要求。通过分片让写压力分散到各个分片上面，使用分片服务器自身的资源。
3) 想把大量数据放到内存里提高性能。和上面一样，通过分片使用分片服务器自身的资源。

相关配置搭建的这边不做介绍，可以查阅[MongoDB 分片的原理、搭建、应用](https://www.cnblogs.com/zhoujinyi/p/4635444.html)或自行搜索文档进行。

![分片集群结构](../assets/images/553_02.png)

上图中主要有如下所述三个主要组件：

`Shard`：用于存储实际的数据块，实际生产环境中一个`shard server`角色可由几台机器组个一个`replica set`承担，防止主机单点故障

`Config Server`：mongod实例，存储了整个 `ClusterMetadata`，其中包括 `chunk`信息。

`Query Routers`：前端路由，客户端由此接入，且让整个集群看上去像单一数据库，前端应用可以透明使用。

* 备份和恢复

1) 备份

```bash
$ mongodump -h <hostname><:port> -d <dbname> -o <path>
$ mongodump --host HOST_NAME --port PORT_NUMBER # 备份全部数据
$ mongodump --collection COLLECTION --db DB_NAME # 备份指定数据库的集合
```

2) 恢复

```bash
$ mongorestore -h <hostname><:port> -d <dbname> <path> --drop
```

* 监控

1) 状态检测

```bash
$ mongostat
```

2) 实例跟踪

```bash
$ mongotop
```

* 查询分析

1) 语句性能分析

```bash
> db.set_test.ensureIndex({gender:1,user_name:1})
> db.set_test.find({gender:"M"},{user_name:1,_id:0}).explain()
{
   "cursor" : "BtreeCursor gender_1_user_name_1",
   "isMultiKey" : false,
   "n" : 1,
   "nscannedObjects" : 0,
   "nscanned" : 1,
   "nscannedObjectsAllPlans" : 0,
   "nscannedAllPlans" : 1,
   "scanAndOrder" : false,
   "indexOnly" : true,
   "nYields" : 0,
   "nChunkSkips" : 0,
   "millis" : 0,
   "indexBounds" : {
      "gender" : [
         [
            "M",
            "M"
         ]
      ],
      "user_name" : [
         [
            {
               "$minElement" : 1
            },
            {
               "$maxElement" : 1
            }
         ]
      ]
   }
}

# 字段说明：

# indexOnly: 字段为 true ，表示我们使用了索引。

# cursor：因为这个查询使用了索引，MongoDB 中索引存储在B树结构中，所以这是也使用了 BtreeCursor 类型的游标。如果没有使用索引，游标的类型是 BasicCursor。这个键还会给出你所使用的索引的名称，你通过这个名称可以查看当前数据库下的system.indexes集合（系统自动创建，由于存储索引信息，这个稍微会提到）来得到索引的详细信息。

# n：当前查询返回的文档数量。

# nscanned/nscannedObjects：表明当前这次查询一共扫描了集合中多少个文档，我们的目的是，让这个数值和返回文档的数量越接近越好。

# millis：当前查询所需时间，毫秒数。

# indexBounds：当前查询具体使用的索引。
```

2) 强制指定索引

```bash
> db.set_test.find({gender:"M"},{user_name:1,_id:0}).hint({gender:1,user_name:1}).explain()
```

* `GridFS`

`GridFS`用于存储和恢复那些超过`16M`（`BSON`文件限制）的文件(如：图片、音频、视频等)。所以其可以进行文件存储，它会将大文件对象分割成多个小的`chunk`(文件片段)，一般为`256k/个`，每个`chunk`将作为`MongoDB`的一个文档(`document`)被存储在`chunks`集合中。

`GridFS` 用两个集合来存储一个文件：

`fs.files`：存储和文件有关的meta数据(filename,content_type,还有用户自定义的属性)；

`fs.chunks`：存储文件的实际内容(二进制数据)。

```bash
# fs.files
{
   "filename": "test.txt",
   "chunkSize": NumberInt(261120),
   "uploadDate": ISODate("2014-04-13T11:32:33.557Z"),
   "md5": "7b762939321e146569b07f72c62cca4f",
   "length": NumberInt(646)
}

# fs.chunks
{
   "files_id": ObjectId("534a75d19f54bfec8a2fe44b"),
   "n": NumberInt(0),
   "data": "Mongo Binary Data"
}

$ mongofiles <options> <commands> <filename>

<options> 

--host：mongodb地址
--port：端口号
--username：用户名
--password：密码
--db：mongodb 数据库
--local：本地的文件名称 用于 put/get

<commands>

list <prefix>：列出GridFS存储的文件 以<prefix>开头的文件

search <string>：搜索 包含 <string>的文件

put <filename>：将本地文件保存于 GridFS

get <filename>：下载文件

get_id "<ObjectId>"：获取到指定id的文件

delete <filename>：删除指定的文件

delete_id：删除指定id的文件
```

* `Map Reduce`

`Map-Reduce`是一种计算模型，简单的说就是将大批量的工作（数据）分解（`MAP`）执行，然后再将结果合并成最终结果（`REDUCE`）。

`MongoDB`提供的`Map-Reduce`非常灵活，对于大规模数据分析也相当实用。

```bash
db.COLLECTION_NAME.mapReduce(
   function() {emit(key,value);},  # map 函数
   function(key,values) {return reduceFunction},   # reduce 函数
   {
      out: collection,
      query: document,
      sort: document,
      limit: number
   }
)

# Map 函数调用 emit(key, value), 遍历 collection 中所有的记录, 将 key 与 value 传递给 Reduce 函数进行处理。

# 参数说明:

# map：映射函数 (生成键值对序列,作为 reduce 函数参数)。
# reduce：统计函数，reduce函数的任务就是将key-values变成key-value，也就是把values数组变成一个单一的值value。
# out：统计结果存放集合 (不指定则使用临时集合,在客户端断开后自动删除)。
# query：一个筛选条件，只有满足条件的文档才会调用map函数。（query。limit，sort可以随意组合）
# sort：和limit结合的sort排序参数（也是在发往map函数前给文档排序），可以优化分组机制
# limit：发往map函数的文档数量的上限（要是没有limit，单独使用sort的用处不大）
```

在集合 `orders` 中查找 `status:"A"` 的数据，并根据 `cust_id` 来分组，并计算 `amount` 的总和：

![Map-Reduce过程](../assets/images/553_03.jpg)

参考链接：

* [MongoDB 教程](http://www.runoob.com/mongodb/mongodb-tutorial.html)

* [Mongodb介绍](https://www.cnblogs.com/shaosks/p/5644129.html)