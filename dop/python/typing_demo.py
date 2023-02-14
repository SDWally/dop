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

# fails
user_c = get_user_name(UserId(42351)+UserId(42351))

# 仅仅是不通过类型检查，不代表不可以运行

# from typing import NewType
#
# UserId = NewType('UserId', int)
#
# # Fails at runtime and does not pass type checking
# class AdminUserId(UserId):
#     pass

from typing import NewType

UserId = NewType('UserId', int)

ProUserId = NewType('ProUserId', UserId)


#　Generics can be parameterized by using a factory available in typing called TypeVar.

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar('T')      # Declare type variable

def first(l: Sequence[T]) -> T:   # Generic function
    return l[0]

from typing import Any

def hash_a(item: object) -> int:
    # Fails type checking; an object does not have a 'magic' method.
    item.magic()
    ...

def hash_b(item: Any) -> int:
    # Passes type checking
    item.magic()
    ...

# Passes type checking, since ints and strs are subclasses of object
hash_a(42)
hash_a("foo")

# Passes type checking, since Any is compatible with all types
hash_b(42)
hash_b("foo")

# Use object to indicate that a value could be any type in a typesafe manner. Use Any to indicate that a value is dynamically typed.

"""
Nominal vs structural subtyping
"""