# flask-2

## 判断python版本

- sys.version_info

## 判断是否为协程

- inspect.iscoroutinefunction

## 嵌套默认字典设置

- defaultdict(lambda: defaultdict(dict))

## 路径修正剪切

- os.fspath("/a/b/").rstrip(r"\/")

## 值存在检查

    @property
    def has_static_folder(self) -> bool:
        """``True`` if :attr:`static_folder` is set.

        .. versionadded:: 0.5
        """
        return self.static_folder is not None

## 当前文件夹名称获取

        if self.static_folder is not None:
            basename = os.path.basename(self.static_folder)
            return f"/{basename}".rstrip("/")

## 全局配置实用

    def get_send_file_max_age(self, filename: t.Optional[str]) -> t.Optional[int]:
        """Used by :func:`send_file` to determine the ``max_age`` cache
        value for a given file path if it wasn't passed.

        By default, this returns :data:`SEND_FILE_MAX_AGE_DEFAULT` from
        the configuration of :data:`~flask.current_app`. This defaults
        to ``None``, which tells the browser to use conditional requests
        instead of a timed cache, which is usually preferable.

        .. versionchanged:: 2.0
            The default configuration is ``None`` instead of 12 hours.

        .. versionadded:: 0.9
        """
        value = current_app.config["SEND_FILE_MAX_AGE_DEFAULT"]

## 属性缓存的线程安全版

```
class locked_cached_property(werkzeug.utils.cached_property):
    """A :func:`property` that is only evaluated once. Like
    :class:`werkzeug.utils.cached_property` except access uses a lock
    for thread safety.

    .. versionchanged:: 2.0
        Inherits from Werkzeug's ``cached_property`` (and ``property``).
    """

    def __init__(
        self,
        fget: t.Callable[[t.Any], t.Any],
        name: t.Optional[str] = None,
        doc: t.Optional[str] = None,
    ) -> None:
        super().__init__(fget, name=name, doc=doc)
        self.lock = RLock()

    def __get__(self, obj: object, type: type = None) -> t.Any:  # type: ignore
        if obj is None:
            return self

        with self.lock:
            return super().__get__(obj, type=type)

    def __set__(self, obj: object, value: t.Any) -> None:
        with self.lock:
            super().__set__(obj, value)

    def __delete__(self, obj: object) -> None:
        with self.lock:
            super().__delete__(obj)
```

## HTTP方法 patch

- 在 HTTP 协议中，请求方法 PATCH 用于对资源进行部分修改。

- 在 HTTP 协议中， PUT 方法已经被用来表示对资源进行整体覆盖，而 POST 方法则没有对标准的补丁格式的提供支持。不同于 PUT 方法，而与 POST 方法类似，PATCH 方法是非幂等的，这就意味着连续多个的相同请求会产生不同的效果。

- 要判断一台服务器是否支持 PATCH 方法，那么就看它是否将其添加到了响应首部 Allow 或者 Access-Control-Allow-Methods（在跨域访问的场合，CORS）的方法列表中。

## 实例与子类判断

```
        if isinstance(exc_class, Exception):
            raise TypeError(
                f"{exc_class!r} is an instance, not a class. Handlers"
                " can only be registered for Exception classes or HTTP"
                " error codes."
            )

        if not issubclass(exc_class, Exception):
            raise ValueError(
                f"'{exc_class.__name__}' is not a subclass of Exception."
                " Handlers can only be registered for Exception classes"
                " or HTTP error codes."
            )
```

## 警告打印

        import warnings

        warnings.warn(
            "'session_cookie_name' is deprecated and will be removed in Flask 2.3. Use"
            " 'SESSION_COOKIE_NAME' in 'app.config' instead.",
            DeprecationWarning,
            stacklevel=2,
        )

## 不可变字典

from werkzeug.datastructures import ImmutableDict
- ImmutableDict

## chain

- itertools
- 是一个生成器，可以合并多个可迭代对象，变成一个生成器

## werkzeug测试服务器

        from werkzeug.serving import run_simple

        try:
            run_simple(t.cast(str, host), port, self, **options)
        finally:
            # reset the first request information if the development server
            # reset normally.  This makes it possible to restart the server
            # without reloader and that stuff from an interactive shell.
            self._got_first_request = False

## 线程初始化

- 使用线程池处理请求
- 多线程模式下，每个线程有一个初始化动作
- Run before_first_request functions if this is the thread's first request.

## 请求处理核心过程

- request_started.send(self)
- rv = self.preprocess_request() / rv = self.dispatch_request()  
- request_finished.send(self, response=response)

## 同步与异步的转换

- from https://blog.csdn.net/Android_boom/article/details/125000166

- 同步的方式主要是使用多线程的方式来实现并发
- 异步的方式则主要是基于协程的方式来实现并发

- 线程安全或协程安全

- 同步到异步， 在异步主线程中，遇到同步函数，直接新开一个子线程处理同步函数，异步主线程继续运行
- 异步到同步， 把主线程上的是协程函数的调用，转化为一个在子线程中运行的普通函数，并在异步函数处理完成的逻辑之后，返回到同步运行的子线程中

- run_in_executor  被async修饰的异步函数，调用同步函数时，将同步函数放到线程池中执行，让其他任务也可以继续在事件循环中保持执行
- asyncio.run_coroutine_threadsafe  这个是将asyncio包的future对象转化返回一个concurrent.futures包的future对象。
 动态的加入协程，参数为一个回调函数和一个loop对象，返回值为future对象，通过future.result()获取回调函数返回值
- asyncio.to_thread

### 异步变同步

from asgiref.sync import async_to_sync
body = async_to_sync(reques.body)()

async_to_sync需要传入的是一个awaitable，返回是一个函数，所以我们的还需要在函数的后面进行（）进行一个函数的调用处理。

### 同步变异步

- await anyio.to_thread.run_sync

from asgiref.sync import sync_to_async
asds = await sync_to_async(func=getdata)

## 