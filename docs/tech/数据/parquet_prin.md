# parquet 原理

## 索引部分列时，parquet 内部发生了什么？？？





## 文件构成

这里存储模型又可以理解为存储格式或文件格式，Parquet 的存储模型主要由行组（Row Group）、列块（Column Chuck）、页（Page）组成。

1、行组，Row Group：Parquet 在水平方向上将数据划分为行组，默认行组大小与 HDFS Block 块大小对齐，Parquet 保证一个行组会被一个 Mapper 处理。

2、列块，Column Chunk：行组中每一列保存在一个列块中，一个列块具有相同的数据类型，不同的列块可以使用不同的压缩。

3、页，Page：Parquet 是页存储方式，每一个列块包含多个页，一个页是最小的编码的单位，同一列块的不同页可以使用不同的编码方式。

## 字段存储

每个记录由一个或多个字段组成。
每个字段可以是atomic字段或者group字段（嵌套）。

每个字段有3个属性：重复性（repetition）、类型（type）和名称（name）

### 类型


### 重复性

required(1次)、optional(0或者1次)、repeated（0次或大于1次）

为了编码嵌套列，parquet 使用 dremel 通过 definition levels 和 repetition levels 来实现

- 用以表示在该字段路径上哪个节点进行了重复
- Definition Levels：用以表示该字段路径上有多少可选的字段实际进行了定义

- 1）比如：嵌套a.b.c三个3字段。字段path就是a.b.c
- 2）Repetition levels用来表示path中哪个部分是重复的。如果在a上重复了，那么level是1，b上重复level是2，c上重复level是3.
- 3）definition levels用来看下字段path中多少可选字段部分（optional和repeated）是定义的（即有值），求个和

## 资料

1. 列式存储引擎-内核机制-Parquet格式 https://cloud.tencent.com/developer/article/2325393
2. 