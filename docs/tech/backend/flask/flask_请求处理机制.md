# 

## WSGI （web service gateway interface）

- 一般来说http服务器和框架需要进行解耦，http专门负责接受HTTP请求、解析HTTP请求、发送HTTP，响应请求等；而web框架负责处理请求的逻辑，和数据库的交互等等，那么它们之间需要约定一套接口使得http服务器能够调用web框架的处理逻辑，这个协议就是WSGI协议。
- 一个是请求数据封装的字典environ，另一个是需要框架回调的方法start_response。

##　

在flask框架中，服务器对每个请求调用一次app的wsgi_app方法返回结果，而wsgi_app方法的执行过程就是请求的处理流程。

```python
    def wsgi_app(self, environ: dict, start_response: t.Callable) -> t.Any:
        """The actual WSGI application. This is not implemented in
        :meth:`__call__` so that middlewares can be applied without
        losing a reference to the app object. Instead of doing this::

            app = MyMiddleware(app)

        It's a better idea to do this instead::

            app.wsgi_app = MyMiddleware(app.wsgi_app)

        Then you still have the original application object around and
        can continue to call methods on it.

        .. versionchanged:: 0.7
            Teardown events for the request and app contexts are called
            even if an unhandled error occurs. Other events may not be
            called depending on when an error occurs during dispatch.
            See :ref:`callbacks-and-errors`.

        :param environ: A WSGI environment.
        :param start_response: A callable accepting a status code,
            a list of headers, and an optional exception context to
            start the response.
        """
        ctx = self.request_context(environ)
        error: t.Optional[BaseException] = None
        try:
            try:
                ctx.push()
                response = self.full_dispatch_request()
            except Exception as e:
                error = e
                response = self.handle_exception(e)
            except:  # noqa: B001
                error = sys.exc_info()[1]
                raise
            return response(environ, start_response)
        finally:
            if "werkzeug.debug.preserve_context" in environ:
                environ["werkzeug.debug.preserve_context"](_cv_app.get())
                environ["werkzeug.debug.preserve_context"](_cv_request.get())

            if error is not None and self.should_ignore_error(error):
                error = None

            ctx.pop(error)

    def __call__(self, environ: dict, start_response: t.Callable) -> t.Any:
        """The WSGI server calls the Flask application object as the
        WSGI application. This calls :meth:`wsgi_app`, which can be
        wrapped to apply middleware.
        """
        return self.wsgi_app(environ, start_response)
```

## 服务器启动

- 服务器启动后，假设服务器是基于线程的，此时app对象被创建，加载了相关的初始化参数，这时代理对象如current_app、g、session、request等会被创建，但是它们目前并没有代理任何的对象，如果此时使用它们会报错，需要在第一次接收到请求后才会真正地代理上下文。

## 接收请求，创建上下文，入栈

服务器收到一个http请求后，使用app上下文和请求数据创建一个线程，调用app的request_context(self, environ)方法，将解包后封装的http请求数据当做environ参数传入，返回一个RequestContext实例对象，每一个请求都有一个RequestContext实例对象，同时他们都拥有各自的app上下文，也就是说在本线程中的app应用是服务器初始化app的一个引，因此我们可以动态修改app的属性。

将RequestContext对象push进_request_ctx_stack里面，_request_ctx_stack是一个栈对象，此时代理对象request指向栈顶的RequestContext对象的request属性，该request是一个Request对象，而session此时指向栈顶的RequestContext对象的session属性。

判断_app_ctx_stack栈顶是否存在应用上下文对象AppContext，不存在就创建，同时将AppContext推送到_app_ctx_stack栈对象中，此时current_app指向栈顶AppContext对象的app属性，而g变量指向栈顶AppContext对象的g属性，本质上是一个_AppCtxGlobals对象，数据结构是一个字典。

##　请求分派

分发请求并执行处理逻辑的函数为full_dispatch_request，其返回一个Response对象。处理的过程为：

先执行app对象before_first_request_funcs列表中的所有方法，这是针对app的第一次请求需要的预处理方法，执行该列表中的所有方法是一个原子操作，被加了线程锁，如果不是第一次请求就跳过；

然后执行app对象的url_value_preprocessors字典中对应蓝图的列表中的所有方法，对所有的URL进行预处理；

执行app对象的before_request_funcs列表中的所有方法，其会按照加载的顺序链执行，并且如果中间有任何一个方法返回的结果不是None，那么执行中断，直接返回结果，不再执行视图函数。这是针对app所有的请求都会执行的方法，当然也可以通过蓝图来进行管理；

通过request对象的url_rule(Rule)找到app中的url_map中对应的视图函数执行，返回一个元组的结果rv，就是我们平时写视图函数时返回的元组；

调用make_response函数，以返回的结果rv作为参数构建一个Response对象；

执行app对象中的after_request_funcs列表的所有方法，以构建的Response对象作为参数，每个方法必须都返回Response类型的对象，最后调用session保存本次的状态信息；

## 出栈

先执行app对象的teardown_request_funcs列表中的所有的方法，其方法和after_request_funcs中的一样，只不过是在出栈前才触发，这意味着即使处理逻辑的部分出错，这里方法也会执行，然后从_request_ctx_stack中弹出RequestContext请求上下文，然后执行app对象中的teardown_appcontext_funcs列表的所有方法，最后从_app_ctx_stack中弹出AppContext应用上下文。


## flask请求处理最简代码模型

假设服务器使用的是多进程模式。

from multiprocessing import Process, Pool
class Flask(object):
    def __call__(self, environ, start_response):
        """定义app对请求的处理过程"""
        pass

def listen_port():
    """假设这是端口监听并解析http请求的方法"""
    pass

def run_web():
    """假设这是程序主循环"""
    app = Flask() # 创建一个app，这是app初始化做的
    pool = Pool(10)
    while True:
        # 获取一个http请求的数据
        environ, start_response = listen_port()
        # 调用app处理请求
        pool.apply_async(app, args=(environ, start_response))

if __name__ == '__main__':
    run_web()
## 总结

- 无论是gunicorn服务器还是uwsgi服务器，其启动后加载了app对象；
- 当收到http请求后，按照http协议解析数据，将数据打包成一个字典(environ)，将其和响应函数（start_response）一起作为参数调用app对象的wsgi_app方法；
- wsgi_app方法按照A接收请求，B创建上下文，C入栈，D请求分发，E出栈的步骤处理完业务逻辑返回响应数据；

## 个人总结

- 每一个请求都是一个 RequestContext
- RequestContext 对象 push 到 _request_ctx_stack 中
- 代理对象request指向栈顶的RequestContext对象的request属性，该request是一个Request对象，而session此时指向栈顶的RequestContext对象的session属性
- 判断_app_ctx_stack栈顶是否存在应用上下文对象AppContext，不存在就创建，同时将AppContext推送到_app_ctx_stack栈对象中，此时current_app指向栈顶AppContext对象的app属性，而g变量指向栈顶AppContext对象的g属性，本质上是一个_AppCtxGlobals对象，数据结构是一个字典。
- 

## 核心信号

template_rendered = _signals.signal("template-rendered")
before_render_template = _signals.signal("before-render-template")
request_started = _signals.signal("request-started")
request_finished = _signals.signal("request-finished")
request_tearing_down = _signals.signal("request-tearing-down")
got_request_exception = _signals.signal("got-request-exception")
appcontext_tearing_down = _signals.signal("appcontext-tearing-down")
appcontext_pushed = _signals.signal("appcontext-pushed")
appcontext_popped = _signals.signal("appcontext-popped")
message_flashed = _signals.signal("message-flashed")

##  

- 分发请求并执行处理逻辑的函数为full_dispatch_request
- 执行 before_first_request_funcs 中的所有方法
- 执行 preprocess_request， 包括 url_value_preprocessors （所有的URL进行预处理） before_request_funcs（）
- 通过request对象的url_rule(Rule)找到app中的url_map中对应的视图函数执行，返回一个元组的结果rv，就是我们平时写视图函数时返回的元组
- 执行 dispatch_request，即执行url对应的视图函数
- 执行 finalize_request， 调用make_response函数，以返回的结果rv作为参数构建一个Response对象  process_response-> _after_request_functions 返回Response类型的对象

##　出栈代码

```
    def pop(self, exc: t.Optional[BaseException] = _sentinel) -> None:  # type: ignore
        """Pops the request context and unbinds it by doing that.  This will
        also trigger the execution of functions registered by the
        :meth:`~flask.Flask.teardown_request` decorator.

        .. versionchanged:: 0.9
           Added the `exc` argument.
        """
        clear_request = len(self._cv_tokens) == 1

        try:
            if clear_request:
                if exc is _sentinel:
                    exc = sys.exc_info()[1]
                self.app.do_teardown_request(exc)

                request_close = getattr(self.request, "close", None)
                if request_close is not None:
                    request_close()
        finally:
            ctx = _cv_request.get()
            token, app_ctx = self._cv_tokens.pop()
            _cv_request.reset(token)

            # get rid of circular dependencies at the end of the request
            # so that we don't require the GC to be active.
            if clear_request:
                ctx.request.environ["werkzeug.request"] = None

            if app_ctx is not None:
                app_ctx.pop(exc)

            if ctx is not self:
                raise AssertionError(
                    f"Popped wrong request context. ({ctx!r} instead of {self!r})"
                )
```

- 执行do_teardown_request  -> teardown_request_funcs
- do_teardown_appcontext -> teardown_appcontext_funcs

##　上下文

Flask的上下文对象
Flask有两种Context(上下文)，分别是

RequestContext 请求上下文
Request 请求的对象，封装了Http请求(environ)的内容
Session 根据请求中的cookie，重新载入该访问者相关的会话信息。

AppContext 程序上下文
g 处理请求时用作临时存储的对象。每次请求都会重设这个变量
current_app 当前激活程序的程序实例

生命周期：

current_app的生命周期最长，只要当前程序实例还在运行，都不会失效。
Request和g的生命周期为一次请求期间，当请求处理完成后，生命周期也就完结了
Session就是传统意义上的session了。只要它还未失效（用户未关闭浏览器、没有超过设定的失效时间），那么不同的请求会共用同样的session。

## 整体处理步骤

- 创建上下文（请求上下文 应用上下文）
- 入栈 （_request_ctx_stack _app_ctx_stack ）
- 请求分发 （full_dispatch_request->response）
- 出栈()
- 响应wsgi (执行WSGI服务器传入的start_response()函数 发送状态码和HTTP报文头)
