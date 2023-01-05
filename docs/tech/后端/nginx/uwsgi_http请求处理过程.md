# Nginx到框架的http请求处理过程

## 整体请求过程 

1. Nginx收到HTTP请求（这部分就是标准的TCP监听）
2. 通过ngx_http_uwsgi_module模块，把HTTP请求转化为uwsgi请求
3. 通过TCP socket 或者 unix domain socket 连接到 uwsgi 服务器进程，把请求转发给该进程
4. uwsgi server 进程收到uwsgi请求后， 调用进程内运行的flask（Django）框架接口代码，生成uwsgi响应
5. 原路返回给Nginx的ngx_http_uwsgi_module模块，module模块把uwsgi响应，转化成HTTP响应，通过Nginx返回到浏览器

## WSGI规范

- 进程内代码调用规范，而非进程间通信协议
- 调用者端，成为server/gateway;被调用者端，称为 application/framework

## uWSGI server

- uWSGI Server 是一个应用服务器
- uwsgi协议是一个协议
- WSGI是一个进程内代码调用规范（接口定义规范）
- Flask： 一个实现了WSGI规范的Python应用程序