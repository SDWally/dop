# 使用Python生成自由长度的uuid，并兼容python2.7和python3.6

## 业务背景

需要对新闻进行唯一性标记，新闻标记的uuid生成，需要满足16定长的字符串，寻找一种hash算法。

## 技术设计

查看hashlib相关包后，考虑性能及实现，决定使用BLAKE2哈希函数，使用BLAKE2b函数进行。
官方文档有提及，
```
BLAKE2 支持 keyed mode (HMAC 的更快速更简单的替代), salted hashing, personalization 和 tree hashing
```

## 示例代码

python2.7

```
content = "测试文本标题等内容加密"
from pyblake2 import blake2b
blk2b = blake2b(digest_size=8, person="wally")
blk2b.update(content)
print(blk2b.hexdigest())
```

python3.6

```
content = "测试文本标题等内容加密"
import hashlib
blk2b = hashlib.blake2b(content.encode(), digest_size=8, person=b"wally")
print(blk2b.hexdigest())
```

## 参考

1. https://docs.python.org/zh-cn/3.6/library/hashlib.html
2. https://pythonhosted.org/pyblake2/
