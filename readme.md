# 本文件夹用于证明DQN算法在路由选择对于传统算法的优越性。
***
## [data.py](模拟网络/data.py):
>该文件拥有本网络拓扑仿真的数据包类，
> 其含有的属性如下:
>1. 数据包的大小。
>2. 数据包的状态。
>3. 起止路由器标号。
>4. 最短路径。
>5. 是否为隐私数据。
>6. 每经过一个路由器的记录和它生命周期内的总记录。
>>注：每一条记录是五个元素形成的五元组，按照顺序分
> 别为前一个路由器的序号，下一个路由器的序号，传输
> 所需时间的相反数（用于DQN训练),下一个路由器的
> 序号，数据包是否到达目的地(布尔值)
> 
>实用的方法只有一个，也就是记录数据的方法。

## [link.py](模拟网络/link.py):
> 该文件表示本网络拓扑中的链路类，其中含有的的属性
> 如下：
>1. 一个传输队列。
>2. 数据包经过该链路所需要的时间(DQN和networkx中的权重)。
>3. 链路的全局唯一标号(由两端路由器构成的元组表示)。
>4. 当前状态下信道中数据占用量。
>5. 信道最大传输信息量。
>
>该类含有一些的实用的方法如下:
>1. 获取链路传输队列中的可用数据量。
>2. 将数据发送至链路的传输队列中。
>3. 数据从传输队列出队后，更新链路传输对列数据可用量。

## [router.py](模拟网络/router.py):
> 该文件表示本网络拓扑中的路由器类，其中含有的的属性
> 如下：
> 1. 路由器的序号
> 2. ip地址（暂时无实际意义）
> 3. 队列的最大数据接收量
> 4. 发送队列
> 5. 接收队列
> 6. 路由表
> 7. 用于计算吞吐量的列表，内部元素应该是一个个元组，每一个元组代表着路由器吞吐量的变化 
> 8. 队列标志
>> 注：假如该路由器的序号为5，则接收队列标志为(0,5)
>> 发送队列标志(5,0),该序号用于更新数据包状态
> 
>该类含有一些的实用的方法如下:
> 1. 获取接收队列的可用数据量
> 2. 获取发送队列的可用数据量
> 3. 将数据从接收队列发送到发送队列.(在这个方法中
> 会对数据包的记录进行更新)
> 4. 从发送队列出队之后要修正发送队列的可用数据量
> 5. 将数据发送至接受队列,传输失败返回False,传输成功返回True
>(在这个网络拓扑中的所有丢包都发生在该方法中)

## [net.py](模拟网络/net.py):
> 该类是本网络拓扑中最核心的类，代表了网络本身，上接网络
> 拓扑中三个基础元素类，即路由器，链路，数据包，下启
> 三种算法的具体拓扑网络，即OSPF,RIP,DQN，是实际测试
> 中最常被调用的API的父类，该类的
> 一些主要方法如下:
> 1. 数据包的数量。
> 2. 基于networkx的图，即网络拓扑的数学表示。
> 3. 路由器组，由字典表示，键为路由器的编号，值为所对应的路由器。
> 4. 每一个路由器的路由表。
> 5. 网络连接组，由字典表示，键为起始路由器和终止路由器的元组，值为相对应的网络链路。
> 6. 数据包集合，一共有指定数目个数据包,每个数据包的大小都不同。
> 7. 数据包大小的最小值
> 8. 信息流的记录信息,键为数据包本体，值为数据包在网络中传输的记录"
> 9. 网络开始传输信息时的时间戳，用于计算吞吐量.
> 10. 数据包大小的最大值
>> 注：数据包大小取最小值与最大值之间的随机数。
> 
> 该类含有的一些方法如下：
> 1. 更新数据包内容。
> 2. 利用matplotlib绘制图
> 3. 更新路由器的吞吐量信息。
> 4. 发送数据包（核心方法，数据包从起始路由器发出到
>目标路由器收到或被丢弃的整个生命周期都由这个方法负责）

## [DQN.py](模拟网络/DQN.py)：
>该类含有实现DQN算法的类，该类含有以下属性（超参数）：
> 1. 状态大小 state_size
> 2. 行为大小 action_size
> 3. 经验回放空间（队列）
> 4. 折扣率
> 5. 随机探索率
> 6. 最低随机探索率 
> 7. 探索率下降指数
> 8. 学习率
> 9. 模型
>
>该类含有以下方法：
> 1. 构建模型的函数，该模型共有三层神经网络
> 2. 储存回放缓存
> 3. 进行随机探索
> 4. 取小批量数据优化模型


## [ospf_network.py](模拟网络/ospf_network.py):
>该类含有基于OSPF的通信网络，这个类继承自net.py中的类，
> 且无变化，因为net.py中的网络类就是基于OSPF设计的。

## [rip_network.py](模拟网络/rip_network.py)：
>该类含有基于RIP的通信网络，这个类继承自net.py中的类，
> 与父类唯一的不同即为每条链路的权值都为1，并且同步更新了
> 路由表。

## [dqn_network.py](模拟网络/dqn_network.py)：
>该类继承Net和DQN,继承了两个类的全部属性和方法，此外，
> 它还拥有一个额外的方法，即通过K最短路径算法计算出K条
> 最短路径，用于后期的DQN选路。

## [Test_normal.py](模拟网络/Test_normal.py)：
> 该类是我对构建这个拓扑网络过程中进行的一系列常规测试，可忽略

## [Test_official.py](模拟网络/Test_official.py)：
> 该类是我对这个拓扑网络的正式测试，其完整的实现了数据包在网络中分发的具体情况。

## [dqn_test.py](模拟网络/dqn_train.py)：
> 该类是我对DQN模型进行训练并与常规算法进行对比测试的类，这个类成功地证明了DQN对于
> 寻路算法的优势。




