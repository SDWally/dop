# hashlib

## 长度问题

    import hashlib
    m = hashlib.sha512()
    h1 = hashlib.pbkdf2_hmac('sha512', b'pass', b'salt', 100, m.block_size)
    h2 = hashlib.pbkdf2_hmac('sha512', b'pass', b'salt', 100)
    print(h1)
    print(h2)

##

- from https://vimsky.com/examples/detail/python-method-hashlib.pbkdf2_hmac.html