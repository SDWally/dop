Python性能分析的几种方法
++++++++++++++++++++++++

几种常用的性能分析方法
---------------------

- print 装饰器模式
- timeit python -m ; timeit -n 5 -r 5 -s "import ..."
- %timeit
- /usr/bin/time -p python xx.py
- python -m cprofile -s cumulative xx.py
- python -m cprofile -o profile.stats xx.py
- runsnakerun
- line_profiler
- cprofile+pstat+gprof2dot
- perf


line_profiler
--------------

主要用于对某个函数，进行逐行分析。

- 安装：　pip install line_profiler

- 装饰器：　使用＠profile 标记选中的函数。要注意，它不会对函数中调用的子函数进行逐行分析。

- 用kernprof.py来运行代码： kernpref -l -v xxx.py

memory_profiler
----------------

用于逐行测量内存占用率

- 安装：　pip install memory_profiler (可选装　psutil　来提高分析速度)

- 装饰器：　使用＠profile 标记选中的函数

- 使用：　python -m memory_profiler xxx.py

profile可视化
--------------

安装
~~~~~

- pstats
- gprof2dot

使用
~~~~~

- 将sd_profiile装饰在要分析的函数前。

代码如下：

:: 
    # -*- coding: utf-8 -*-
    # !/usr/bin/env python

    import sys
    import cProfile
    import pstats
    import os


    Do_Profiling = True


    def sd_profile(filename):
        def wrapper(func):
            def profiled_func(*args, **kwargs):
                #Do_Profiling = os.getenv("PROFILING")
                if Do_Profiling:
                    profile = cProfile.Profile()
                    profile.enable()
                    result = func(*args, **kwargs)
                    profile.disable()
                    sortby = "tottime"
                    ps = pstats.Stats(profile).sort_stats(sortby)
                    #dump to stat file
                    ps.dump_stats(filename)
                    #dump to png file
                    os.system("gprof2dot -f pstats %s | dot -Tpng -o %s.png"%(filename, filename))
                else:
                    result = func(*args, **kwargs)
                return result
            return profiled_func
        return wrapper



更深层次的分析（仅供参考）
------------------------

冯诺伊曼瓶颈
~~~~~~~~~~~~~~

- 冯诺伊曼结构、哈佛结构
- 由于指令与数据放在同一内存带来的CPU利用率（吞吐率）降低

pref
~~~~~

linux上的一个工具

- 安装　sudo apt install linux-source sudo apt install linux-tools-generic

- 运行分析　perf stat -e cycles,stalled-cycles-fronted,stalled-cycles-backend,instructions,cache-references,cache-misses,branches,branch-misses,task-clock,faults,minor-faults,cs,migrations -r 3 python xxx.py

- perf list 可查看可使用事件

perf结果解释
~~~~~~~~~~~

task-clock 时钟周期数　单位　ｍｓ
context-switches 被挂起次数　等待内核操作时（如IO）
CPU-migrations　被挂起次数　CPU迁移时
page-faults 缺页小中断次数　发生在内存分配后第一次被使用（延迟分配系统）
cache-references 引用缓存数据
cache-miss　缓存失效
instructions　执行指令数
insns per cycle 一个时钟周期执行指令数
stalled-cycles-frontend 等待流水线前端填满指令时钟周期数
stalled-cycles-backend　等待流水线后端填满指令时钟周期数
branch　代码执行流程变化
stalled-cycles　分支预测失效
branch-miss　分支预测失效


补充
-----

矢量操作和非矢量操作使用的是不同的CPU计算单元和指令集。numpy有极其优化的ｃ代码来使用CPU矢量操作。

减少缓存失效，以及将问题重新描述，往往是比较有效而且足够的优化手段。
