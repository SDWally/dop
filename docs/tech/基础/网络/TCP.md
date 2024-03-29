# TCP协议

- from https://baike.baidu.com/item/TCP/33012?fr=aladdin

- 面向连接的、可靠的、基于字节流的传输层通信协议
- 主计算机中的成对进程之间依靠TCP提供可靠的通信服务
- TCP假设它可以从较低级别的协议获得简单的，可能不可靠的数据报服务。（如何将数据组合成数据块，在数据链路层中称这种数据块为帧）
- 传输控制协议（TCP，Transmission Control Protocol）是为了在不可靠的互联网络上提供可靠的端到端字节流而专门设计的一个传输协议。
- 不同主机的应用层之间经常需要可靠的、像管道一样的连接，但是IP层不提供这样的流机制，而是提供不可靠的包交换。

## TCP

- 应用层向TCP层发送用于网间传输的、用8位字节表示的数据流，
- 然后TCP把数据流分区成适当长度的报文段（通常受该计算机连接的网络的数据链路层的最大传输单元（MTU）的限制）
- TCP把结果包传给IP层，由它来通过网络将包传送给接收端实体的TCP层。TCP为了保证不发生丢包，就给每个包一个序号，同时序号也保证了传送到接收端实体的包的按序接收。
- 然后接收端实体对已成功收到的包发回一个相应的确认（ACK）；如果发送端实体在合理的往返时延（RTT）内未收到确认，那么对应的数据包就被假设为已丢失将会被进行重传。
- TCP用一个校验和函数来检验数据是否有错误；在发送和接收时都要计算校验和。

## TCP传输实体

- 每台支持TCP的机器都有一个TCP传输实体。TCP实体可以是一个库过程、一个用户进程，或者内核的一部分。在所有这些情形下，它管理TCP流，以及与IP层之间的接口。
- TCP传输实体接受本地进程的用户数据流，将它们分割成不超过64KB（实际上去掉IP和TCP头，通常不超过1460数据字节）的分段，每个分段以单独的IP数据报形式发送。
- 当包含TCP数据的数据报到达一台机器时，它们被递交给TCP传输实体，TCP传输实体重构出原始的字节流。

## TCP拥塞控制

在拥塞控制上，采用广受好评的TCP拥塞控制算法（也称AIMD算法）。该算法主要包括四个主要部分：

###　慢启动

－　每当建立一个TCP连接时或一个TCP连接发生超时重传后，该连接便进入慢启动阶段。进入慢启动后，TCP实体将拥塞窗口的大小初始化为一个报文段，即：cwnd=1。
－　此后，每收到一个报文段的确认（ACK），cwnd值加1，即拥塞窗口按指数增加。
－　当cwnd值超过慢启动阈值（ssthresh）或发生报文段丢失重传时，慢启动阶段结束。前者进入拥塞避免阶段，后者重新进入慢启动阶段。 

### 拥塞避免

- 在慢启阶段，当cwnd值超过慢启动阈值（ssthresh）后，慢启动过程结束，TCP连接进入拥塞避免阶段。
- 在拥塞避免阶段，每一次发送的cwnd个报文段被完全确认后，才将cwnd值加1。在此阶段，cwnd值线性增加。

### 快速重传

- 快速重传是对超时重传的改进。
- 当源端收到对同一个报文的三个重复确认时，就确定一个报文段已经丢失，因此立刻重传丢失的报文段，而不必等到重传定时器（RTO）超时。以此减少不必要的等待时间。

### 快速恢复

- 快速恢复是对丢失恢复机制的改进。在快速重传之后，不经过慢启动过程而直接进入拥塞避免阶段。
- 每当快速重传后，置ssthresh=cwnd/2、cwnd=ssthresh+3。
- 此后，每收到一个重复确认，将cwnd值加1，直至收到对丢失报文段和其后若干报文段的累积确认后，置cwnd=ssthresh，进入拥塞避免阶段。

###　特点

（1）基于流的方式；
（2）面向连接；
（3）可靠通信方式；
（4）在网络状况不佳的时候尽量降低系统由于重传带来的带宽开销；
（5）通信连接维护是面向通信的两个端点的，而不考虑中间网段和节点。

### 规定

为满足TCP协议的这些特点，TCP协议做了如下的规定： [10] 
①数据分片：在发送端对用户数据进行分片，在接收端进行重组，由TCP确定分片的大小并控制分片和重组；
②到达确认：接收端接收到分片数据时，根据分片数据序号向发送端发送一个确认；
③超时重发：发送方在发送分片时启动超时定时器，如果在定时器超时之后没有收到相应的确认，重发分片；
④滑动窗口：TCP连接每一方的接收缓冲空间大小都固定，接收端只允许另一端发送接收端缓冲区所能接纳的数据，TCP在滑动窗口的基础上提供流量控制，防止较快主机致使较慢主机的缓冲区溢出；
⑤失序处理：作为IP数据报来传输的TCP分片到达时可能会失序，TCP将对收到的数据进行重新排序，将收到的数据以正确的顺序交给应用层；
⑥重复处理：作为IP数据报来传输的TCP分片会发生重复，TCP的接收端必须丢弃重复的数据；
⑦数据校验：TCP将保持它首部和数据的检验和，这是一个端到端的检验和，目的是检测数据在传输过程中的任何变化。如果收到分片的检验和有差错，TCP将丢弃这个分片，并不确认收到此报文段导致对端超时并重发。