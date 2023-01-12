# Mysql索引相关知识

from https://blog.csdn.net/weixin_51123079/article/details/125546028

- MySQL中索引的存储类型有两种，即 BTree 和 Hash。
- 索引是在存储引擎中实现的
- MySQL 的存储引擎有：InnoDB、MyISAM、Memory、Heap
- InnoDB / MyISAM 只支持 BTree 索引
- Memory / Heap 都支持 BTree 和 Hash 索引
- 存储引擎就是指 表的类型 以及 表在计算机上的存储方式

### 索引优点

- 提高数据的查询的效率（类似于书的目录）
- 可以保证数据库表中每一行数据的唯一性（唯一索引）
- 减少分组和排序的时间（使用分组和排序子句进行数据查询）
- 被索引的列会自动进行分组和排序

### 索引缺点

- 占用磁盘空间
- 降低更新表的效率（不仅要更新表中的数据，还要更新相对应的索引文件）

## 索引分类

1、普通索引 和 唯一索引

普通索引：MySQL 中的基本索引类型，允许在定义索引的列中插入 重复值 和 空值

唯一索引：要求索引列的值必须 唯一，但允许 有空值

如果是组合索引，则列值的组合必须 唯一
主键索引是一种特殊的唯一索引，不允许 有空值
2、单列索引 和 组合索引

单列索引：一个索引只包含单个列，一个表可以有多个单列索引
组合索引：在表的 多个字段 组合上 创建的 索引
只有在查询条件中使用了这些字段的 左边字段 时，索引才会被使用（最左前缀原则）
3、全文索引

全文索引 的类型为 fulltext
在定义索引的 列上 支持值的全文查找，允许在这些索引列中插入 重复值 和 空值
全文索引 可以在 char、varchar 和 text 类型的 列 上创建
4、空间索引

空间索引 是对 空间数据类型 的字段 建立的索引

MySQL中的空间数据类型有4种，分别是 Geometry、Point、Linestring 和 Polygon

MySQL 使用 Spatial 关键字进行扩展，使得能够用创建正规索引类似的语法创建空间索引

创建空间索引的列，不允许为空值，且只能在 MyISAM 的表中创建。

5、前缀索引

在 char、varchar 和 text 类型的 列 上创建索引时，可以指定索引 列的长度

## 索引数据结构

 MySQL 索引 的数据结构可以分为 BTree 和 Hash 两种，BTree 又可分为 BTree 和 B+Tree。

###　Hash

Hash：使用 Hash 表存储数据，Key 存储索引列，Value 存储行记录或行磁盘地址。

 Hash 只支持等值查询（“=”，“IN”，“<=>”），不支持任何范围查询（原因在于 Hash 的每个键之间没有任何的联系），Hash 的查询效率很高，时间复杂度为 O(1)。


### BTree

BTree：属于多叉树，又名多路平衡查找树。

性质：

- BTree 的节点存储多个元素（ 键值 - 数据 / 子节点 的地址）
- BTree 节点的键值按 非降序 排列
- BTree 所有叶子节点都位于同一层（具有相同的深度）

BTree 的不足：

不支持范围查询的快速查找（每次查询都得从根节点重新进行遍历）
节点都存储数据会导致磁盘数据存储比较分散，查询效率有所降低

B+Tree：在 BTree 的基本上，对 BTree 进行了优化：只有叶子节点才会存储 键值 - 数据，非叶子节点只存储 键值 和 子节点 的地址；叶子节点之间使用双向指针进行连接，形成一个双向有序链表。

B+Tree 的优点：

保证了等值查询和范围查询的快速查找
单一节点存储更多的元素，减少了查询的 IO 次数

##　索引实现

### MyISAM 索引

- MyISAM 的 数据文件（.myd） 和 索引文件（.myi） 是分开存储的
- MyISAM（B+Tree）叶子节点中存储的键值为索引列的值，数据为索引所在行的磁盘地址
- MyISAM 的 主键索引（Primary key）和 辅助索引（Secondary key）在结构上没有任何区别，只是 主键索引 要求 键值唯一，而 辅助索引 键值 可以重复


### InnoDB 索引

数据和索引都存储在一个文件中（.ibd）

一般情况下，聚簇索引等同于主键索引；除 聚簇索引 外的所有索引 均称为 辅助索引

InnoDB（B+Tree）叶子节点中存储的键值为索引列的值

如果是聚簇索引，数据为整行记录（除了主键值）
如果是辅助索引，数据为该行的主键值
每一张表都有一个聚簇索引

如果表中有定义主键，主键索引用作聚簇索引
如果表中没有定义主键，选择第一个不为 NULL 的唯一索引列用作聚簇索引
如果以上都没有，使用一个 6 字节长整形的隐式字段 ROWID （自增）用作聚簇索引
根据在 辅助索引树 中获取的 主键id，再到 主键索引树 查询数据的过程 称为 回表 查询

#### 组合索引

遵循 最左匹配（最左前缀）原则：
使用 组合索引 查询时，MySQL 会一直向右匹配直至遇到范围查询（>、<、between、like）就停止匹配。
只有第一列是有序的，其它列都是无序的（最左匹配原则的原因）

#### 覆盖索引：

覆盖索引不是一种索引结构，而是一种优化手段
我们只需要查询 组合索引 中的字段，而不需要表中的其它字段，在这过程中不会产生回表现象，这种情况称为 覆盖索引

## 是否加索引

加索引：

- 数据本身具有某种的性质，如：唯一性、非空性…
- 频繁进行 分组或排序 的列；如果待排序的列有多个，可以建立 组合索引

不加索引：

- 经常更新的列
- 列 的值类型 很少，如 性别
- where 条件中用不到的列
- 参与计算的列
- 数据量小的表

## 判断索引是否生效

 使用 explain 关键字。

possible_keys：MySQL 在搜索数据记录时可选用的各个索引
key：MySQL 实际选用的索引

## 避免索引失效

- 使用组合索引时，遵循 最左匹配 原则
- 不在索引列上进行任何操作，如：计算、函数、类型转换
- 尽量使用覆盖索引
- 索引列 尽量不使用 不等于（!= / <>）条件、通配符开头的模糊查询（like %abc）、or 作为连接条件
- 字符串加单引号（不加可能会发生索引列的隐式转换，导致索引失效）

## in操作是否走索引

- IN 通常是走索引的，当IN后面的数据在数据表中超过30%的匹配时是全表的扫描，不会走索引，因此IN走不走索引与后面的数据量有关系！
- 使用 IN 查询的参数如果是固定时;SELECT * FROM 表名 WHERE ( 查询字段 = 固定参数1 OR 查询字段 = 固定参数2 ) 这样的效率是最高的；
- 如果查询的参数集合比较大时建议使用 EXISTS 代替 IN 查询，效率会高很多

## 使用EXISTS代替IN

- from https://blog.csdn.net/S_ZaiJiangHu/article/details/119417926

　　假如有一个表user，它有两个字段id和name，我们要查询名字中带a的用户信息：
　　最简单的SQL：select * from user where name like ‘%a%’;
　　使用IN的SQL：select u.* from user u where u.id in (select uu.id from user uu where uu.name like ‘%a%’);
　　我们现在将使用IN的SQL修改为使用EXISTS的SQL该怎么写呢？
　　一开始我直接将u.id in 替换为EXISTS，获得如下语句 ：
　　　　select u.* from user u where exists(select uu.id from user uu where uu.name like ‘%a%’);
　　经过测试发现输出结果错误，该语句将所有的用户全部一个不漏的查询出来了，相信你也发现了问题，后来我对上述语句做了修改如下：
　　　　select u.* from user u where exists (select uu.id from user uu where uu.name like ‘%a%’ and uu.id=u.id);

## 何时使用exists代替in

- from https://www.cnblogs.com/xianlei/p/8862313.html

mysql中的in语句是把外表和内表作hash 连接，而exists语句是对外表作loop循环，每次loop循环再对内表进行查询。一直大家都认为exists比in语句的效率要高，这种说法其实是不准确的。这个是要区分环境的。
 

如果查询的两个表大小相当，那么用in和exists差别不大。 
如果两个表中一个较小，一个是大表，则子查询表大的用exists，子查询表小的用in： 
例如：表A（小表），表B（大表）
 
1：
select * from A where cc in (select cc from B) 效率低，用到了A表上cc列的索引；
 
select * from A where exists(select cc from B where cc=A.cc) 效率高，用到了B表上cc列的索引。 
相反的
 
2：
select * from B where cc in (select cc from A) 效率高，用到了B表上cc列的索引；
 
select * from B where exists(select cc from A where cc=B.cc) 效率低，用到了A表上cc列的索引。
 
 
not in 和not exists如果查询语句使用了not in 那么内外表都进行全表扫描，没有用到索引；而not extsts 的子查询依然能用到表上的索引。所以无论那个表大，用not exists都比not in要快。 
in 与 =的区别 
select name from student where name in ('zhang','wang','li','zhao'); 
与 
select name from student where name='zhang' or name='li' or name='wang' or name='zhao' 
的结果是相同的。