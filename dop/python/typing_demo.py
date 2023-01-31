# coding=utf8
# typing demo
# python org
# https://docs.python.org/3/library/typing.html

from typing import NewType

UserId = NewType('UserId', int)
some_id = UserId(524313)


def get_user_name(user_id: UserId) -> str:
    print(type(user_id))


# passes type checking
user_a = get_user_name(UserId(42351))

# fails type checking; an int is not a UserId
user_b = get_user_name(-1)

# 仅仅是不通过类型检查，不代表不可以运行

