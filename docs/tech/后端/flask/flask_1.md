## Flask源码学习

## 类型检查控制

typing.TYPE_CHECKING

A special constant that is assumed to be True by 3rd party static type checkers. It is False at runtime.

运行时关闭，平时开启，以适应静态类型检查

## 额外技术资料

- 弱引用 https://zhuanlan.zhihu.com/p/478369875

### 弱引用

- 四层双向循环链表
- GC是以引用计数为主，分代回收优化下的标记清除为辅的技术实现的
- 被确定为要消除的变量并不会立刻释放占用的内存，而且转入对应类型的free_list进行缓存
- 节省了申请malloc，free服务的额外开支
- del方法只会删除栈空间中的引用变量，而不会删除堆空间上的变量
- 想要真正删除一个变量指向的堆空间对象，那就必须让这个对象的引用计数器归零（不考虑循环引用时）
- sys.getrefcount(a) 查看引用计数
- b = weakref.ref(a) 弱引用
- 存在free_list缓存机制的基本数据类型不能被直接弱引用
```
>>> class MyList(list):
...     ...
...
>>> a = MyList([1,2,3])
>>> a
[1, 2, 3]
>>> b = weakref.ref(a)
# 这里的list数据类型不可以直接被弱引用，必须用MyList来继承，变成新的数据类型后，才可以进行弱引用
```
- 直接使用weakref.proxy(a)获取a指向的堆变量的代理对象
- weakref还提供了方法WeakMethod来允许你只弱引用用一个类中的某个方法：
```
import weakref
import array

class MyObj:
    def func1(self):
        print("I am func1")
    def func2(self):
        print("I am func2")

a = MyObj()

method = weakref.WeakMethod(a.func1)
method()()
```
- 可以很好地限制引用变量对对象本身的访问权限。而且由于调用是不可被赋值的，所以外界无法轻易通过猴子补丁等方法覆盖原类的方法
- weakref.getweakrefcount(object)：返回指向 object 的弱引用和代理的数量。
- weakref.getweakrefs(object)：返回由指向 object 的所有弱引用和代理构成的列表。
- 弱引用哈希表WeakSet
- weakref还提供了WeakKeyDictionary和WeakValueDictionary，能够让dict在不污染对象计数的情况下去装载它们
- 
```
>>> import array
>>> a = array.array('i', [1,2,3])
>>> fin = weakref.finalize(a, lambda : print("a is dead!"))
>>> del a
a is dead!
``` 
  
- 终结器会在绑定的对象指向的堆变量被销毁时被调用。
- 你可以随时调用它，但是终结器在它的生命周期中必定且只能被调用一次，这是对象实际空间被销毁的信号
- 可以为一个对象绑定多个终结器，从而在生命周期的不同时刻定义不同行为。
- 通过终结器可以间接反映对象的存活情况。
- 基于终结器的回调比__del__更加健壮
- 为什么说终结器的回调比__del__更加健壮呢？因为__del__受到运行环境影响，在有的Python解释器实现中，对象被销毁时并不会调用__del__，且__del__也会受到循环引用的影响。

### 