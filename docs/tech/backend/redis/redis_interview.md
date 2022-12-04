# Redis 面试专用

## 基础

#### Key管理

- del
- dump
- exists
- expire
- keys
- type

- move
- persist
- ttl
- randomkey
- rename/renamenx

### 数据类型及其操作

####　String

- get
- set
- getrange
- getset
- mget
- strlen
- incr

- setex
- setnx
- setrange
- incrby
- decr
- decrby
- append

#### Hash

- hdel
- hexists
- hget
- hgetall
- hkeys 
- hlen
- hmget
- hset

- hincrby
- hsetnx
- hvals

#### List

- blpop
- brpop
- lindex
- linsert
- llen
- lpop
- lpush
- lrange
- rpush
- rpop

- brpoplpush
- lrem
- lset
- ltrim
- rpoplpush
- rpushx

#### Set

- sadd
- scard
- sdiff
- sdiffstore
- sinter
- sismember
- smembers
- smove
- spop
- srandmember
- srem
- sunion
- sunionstore

#### sorted set

- zadd
- zcard
- zcount
- zincrby
- zinterscore
- zlexcount
- zrange
- zrangebylex
- zrangebyscore
- zrank 
- zrem
- zremrangebylex
- zremrangebyrank
- zrevrange
- zrevrangebyscore
- zrevrank
- zscore
- zunionscore


#### HyperLogLog

- pfadd
- pfcount
- pfmerge