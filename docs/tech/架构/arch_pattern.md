# 架构模式篇

## 架构模式分类

- 从混乱到有序
- 分布式系统
- 交互式系统
- 可适应系统

### 从混乱到有序

- 避免组件过多
- 分解子任务

- Layer
- Pipe and Filters
- Blackboard

- Layer 网络协议 OSI七层模型

#### 细化分层架构的方法

- 定义将任务划分到不同层的抽象准则-离平台的概念距离/通用程度/概念复杂度
- 根据抽象准则确定抽象层级数-层数太多会加大开销，层数太少会结构不清晰
- 给每层命名并分派任务-最高层完成整个系统要完成的任务，其他各层的任务是辅佐上一层
- 规范服务-倒置的重用金字塔
- 完善层次划分-反复执行前四步骤
- 规范每层的接口
- 确定各层的结构
- 规范相邻层之间的通信
- 将相邻层解耦合-上一层知道下一层，下一层不知道其用户的身份，只存在单向耦合
- 制定错误处理策略-

#### Layer模式的优点

- 各层可重用
- 支持标准化
- 限制了依赖关系的范围
- 可更换性

#### Layer模式的缺点

- 行为变化可能引发雪崩效应
- 效率低下
- 不必要的工作
- 难以确定正确的层次粒度

#### Pipes and Filters模式

- 将任务分为多个依次执行的处理步骤
- 每个步骤均由过滤器组件实现
- 过滤器一边使用数据一边提供数据
- 数据源/过滤器/数据接收器通过管道依次相连
- 由管道连接的过滤器序列成为处理流水线

##### 过滤器组件

- 流水线处理单元
- 计算和添加信息来充实数据，浓缩或提取信息来提炼数据，改变表示方式来转换数据
- 触发机制： 下游拉取输出/上游推送输入/不间断循环，拉取输入，推送输出

##### 实现

- 将任务划分为一系列处理阶段，每个阶段都只依赖于前一个阶段的输出
- 定义沿管道传递的数据的格式
- 确定如何实现每条管道连接
- 设计并实现过滤器
- 设计错误处理机制
- 搭建处理流水线

##### 变种

- tee and join 流水线系统-允许过滤器有多个入口或多个出口-流水线升级为有向图，甚至可包含反馈回路-一般是有向无环图

#### PAF模式的优点

- 不需要中间文件，但也可以使用
- 可更换过滤器
- 可重组过滤器
- 可重用过滤器组件
- 可快速创建流水线原型
- 效率因并行处理得以提高

#### PAF模式的缺点

- 共享状态信息的开销高昂或缺乏灵活性
- 通过并行处理提高效率的初衷常常成为泡影
- 数据转换开销
- 错误处理-对于必须可靠运行的系统，Layer模式更适合


