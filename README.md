# Spacecraft-orbiting-simulator
This is a python project, also a physics engine, using pygame library to simulate the orbit of the spacecraft

事情的起源，还要回到2020年的9月。高二的我，无心学术。高中的知识对我来说就是totally boring。于是我在课外寻求解脱。那个时候恰逢我们市举办了某个“拖方块编程”比赛。我抱着玩玩的心态参加了。我编写的程序是一个物理仿真模型，针对于人造天体。（人话：照抄坎巴拉太空计划，做了一个二维版的火箭模拟器）。我每天花了大量的时间去编写代码（屎山），融进了很多心血，做到了很多我现在看起来都认为不可思议的事情。


我先来简单说明一下，中心天体的参数我是参考了坎巴拉中的Kerbin。这样做，方便了我配置火箭的参数，也优化了仿真体验。毕竟坎星的质量和半径都比较小，低轨道运行周期比较小。现在看到的是第一版的程序，bug特别多，我们先来运行一下。现在是有飞行指引的。对于小白来说，只要按照步骤操作，100%能把这个小火箭送上轨道。同时我们可以来分析一下代码。pygame提供了一个渲染线程，而我又实现了一个100Hz刷新率的物理计算线程（保证计算精度）以及跟随渲染线程进行的并行粒子计算和物理物体轨道推算（瞎扯中...所谓的并行粒子计算，就是发动机喷出来的那些小球的运动学计算。轨道推算，就是利用万有引力公式，从当前点开始暴力的动力学计算，直到运行一周后终止，并返回所得的物体位移点集。）我用了面向对象编程。火箭对象继承了PhyObject对象，因此自带对空气阻力的计算。空气阻力的公式我参考了坎巴拉官方wiki，虽然他们站点的公式显示全都有问题。计算空气阻力需要大气密度还有某些magic的系数等参数。我搞定了那些magic的参数，至于大气的ρ，我用pV=nRT貌似能够推导出来，这个时候计算大气密度的工作就只需要得到当前高度的大气平均摩尔质量、大气压、以及气温即可完成。大气平均摩尔质量，我使用了29进行近似。大气压我使用了某个指数函数完成了计算。至于大气温度，我直接照抄USSA的数据，这是一个分段的函数。总的来说，我目前也无法评判空气动力学系统实现的怎么样。不过至少目前看来，基本与坎巴拉数据是吻合的。PhyObject有个UserForcesCompute，我在火箭对象重写了这个函数，加入了燃料消耗改变质量、节流阀输出控制等功能。我这边有两种模式。火箭模式是看火箭的，轨道模式是看轨道的。在轨道模式我们可以看到当前物体的运行轨迹，有点时候，你还可以观察到Ap（轨道远点）与Pe（轨道近点）的分布情况。这个轨道如此奇形怪状是因为加速的时候方向没有调整好。轨道顺向显示了物体在轨道某一点上，轨道切向的绝对方向。

我们可以看到，这个程序目前只存在着飞行指引模式，没有自由飞行模式。其实一开始是有的，为了参加比赛我才把他砍掉，但那个时候太不成熟，我应该打上注释的，我却全部把那些代码给删了，所以现在只能够重写。辛亏当初留下来的代码还是比较容易调整的，重写自由模式的工作量比较小。

增大节流阀，准备起飞。怎么不动？哪有bug？原来我被自己坑了。引擎根本就没打开。我保留这个鸡肋的功能，可能就是致敬坎巴拉吧。bug真多。。我也不知道为什么会这样。先随便玩玩吧。

增加一点热键的说明。并修复一个特别nt的问题。轨道模式下地表那里，显示的单位应该是米，而我不知道为什么把它变成了m/s。。史上无敌了。

最后让我们试试着陆。我们可以按U一键入轨。

着陆失败，火箭怎么炸了？？我觉得应该是我没把火箭速度和地面标志指示好的问题。唉 就这样吧。

现在回头看，我挺后悔当初没有好好学习文化科，来做这个东西。在我这个年龄段，说点心里话，学了编程也没什么用。缺着数学基础、算法基础以及进阶的、成体系的CS知识，我做的那些都无异于简单、重复的劳动，换句话说，我做的工作就都是笨功夫。这些功夫都是简单的，python语言那么容易上手，不管在哪，简单培训下谁都学得会，掌握高中范围内的万有引力公式，这样的仿真程序谁都能做得出来。对于一个人的发展，普通高考永远是最好走的路。考上一个好的大学，完成系统有效的本科学习，收获的永远比我高中时期不务“正业”学来的技术多。最后提一嘴，这个程序只在我们市拿了二等奖。



