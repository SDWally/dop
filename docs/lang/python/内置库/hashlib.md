# hashlib

## md5

- MD5 是最常见的摘要算法，速度很快，生成结果是固定的 128 bit 字节，通常用一个 32 位的 16 进制字符串表示。 

##　sha1 sha256

- 调用 SHA1 和调用 MD5 完全类似，SHA1 的结果是160 bit 字节，通常用一个 40 位的 16 进制字符串表示。

## sha512

- SHA256 算法比 SHA1 算法更安全，SHA512 算法比 SHA1 算法更安全，越安全的算法计算速度越慢，摘要更长

## pbkdf2_hmac

```

import hashlib
import binascii
import os

x = hashlib.pbkdf2_hmac("sha256", b"I_love_python", b"", 1)
print("x_1 = " + binascii.hexlify(x).decode())

x = hashlib.pbkdf2_hmac("sha256", b"I_love_python", b"", 1)  # 相同盐值
print("x_2 = " + binascii.hexlify(x).decode())

x = hashlib.pbkdf2_hmac("sha256", b"I_love_python", b"", 10)  # 相同盐值，不同迭代次数
print("x_3 = " + binascii.hexlify(x).decode())

x = hashlib.pbkdf2_hmac("sha256", b"I_love_python", b"dsa", 1)  # 不同盐值，相同迭代次数
print("x_4 = " + binascii.hexlify(x).decode())

y = hashlib.pbkdf2_hmac("sha256", b"I_love_python", os.urandom(16), 1)  # 随机生成盐值
print("y_1 = " + binascii.hexlify(y).decode())
```

## PBKDF2 函数原理

- PBKDF2(Password-Based Key Derivation Function) 是一个用来导出密钥的函数，常用于生成加密的密码。
- 通过一个伪随机函数（例如 HMAC 函数），把明文和一个盐值作为输入参数，然后重复进行运算，并最终产生密钥。
- 如果重复的次数足够大，破解的成本就会变得很高。而盐值的添加也会增加“彩虹表”攻击的难度。
- 


## 长度问题

    import hashlib
    m = hashlib.sha512()
    h1 = hashlib.pbkdf2_hmac('sha512', b'pass', b'salt', 100, m.block_size)   # 128
    h2 = hashlib.pbkdf2_hmac('sha512', b'pass', b'salt', 100) # default 64
    print(h1)
    print(h2)

##

- from https://vimsky.com/examples/detail/python-method-hashlib.pbkdf2_hmac.html
- https://blog.csdn.net/happyjacob/article/details/110771794