# 星巴克毕业项目

## 简介

用户画像和用户行为分析是数据分析中常见的内容，在商业活动中我们可以通过APP注册等方式收集用户信息，通过在APP中进行埋点收集用户行为。

本项目的数据集是一些模拟 Starbucks rewards 移动 app 上用户行为的数据。每隔几天，星巴克会向 app 的用户发送一些推送。这个推送可能仅仅是一条饮品的广告或者是折扣券或 BOGO（买一送一）。一些顾客可能一连几周都收不到任何推送。 

顾客收到的推送可能是不同的，这就是这个数据集的挑战所在。

这个数据集是从星巴克 app 的真实数据简化而来。因为下面的这个模拟器仅产生了一种饮品， 实际上星巴克的饮品有几十种。

每种推送都有有效期。例如，买一送一（BOGO）优惠券推送的有效期可能只有 5 天。你会发现数据集中即使是一些消息型的推送都有有效期，哪怕这些推送仅仅是饮品的广告，例如，如果一条消息型推送的有效期是 7 天，你可以认为是该顾客在这 7 天都可能受到这条推送的影响。

数据集中还包含 app 上支付的交易信息，交易信息包括购买时间和购买支付的金额。交易信息还包括该顾客收到的推送种类和数量以及看了该推送的时间。顾客做出了购买行为也会产生一条记录。 

同样需要记住有可能顾客购买了商品，但没有收到或者没有看推送。

举个例子，一个顾客在周一收到了满 10 美元减 2 美元的优惠券推送。这个推送的有效期从收到日算起一共 10 天。如果该顾客在有效日期内的消费累计达到了 10 美元，该顾客就满足了该推送的要求。

然而，这个数据集里有一些地方需要注意。即，这个推送是自动生效的；也就是说，顾客收到推送后，哪怕没有看到，满足了条件，推送的优惠依然能够生效。比如，一个顾客收到了"满10美元减2美元优惠券"的推送，但是该用户在 10 天有效期内从来没有打开看到过它。该顾客在 10 天内累计消费了 15 美元。数据集也会记录他满足了推送的要求，然而，这个顾客并没被受到这个推送的影响，因为他并不知道它的存在。

## 任务

我们将搭建一个模型来预测某顾客是否会完成推送的活动，以及顾客是否会在完成活动前浏览该推送。如果顾客在完成活动前并没有浏览该推送，则无论是否进行该推送顾客都会完成该消费，则对其推送该促销没有意义。从商业角度出发，如果顾客无论是否收到推送都打算花 10 美元，你并不希望给他发送满 10 美元减 2 美元的优惠券推送。


## 数据集

一共有三个数据文件：

* portfolio.json – 包括推送的 id 和每个推送的元数据（持续时间、种类等等）
* profile.json – 每个顾客的人口统计数据
* transcript.json – 交易、收到的推送、查看的推送和完成的推送的记录

| |channels|	difficulty|	duration|	id|	offer_type|	reward|
| -: | -: | -: | -: | -:|-:|-:|
|0|	[email, mobile, social]|	10|	7|	ae264e3637204a6fb9bb56bc8210ddfd|	bogo|	10|
|1|	[web, email, mobile, social]|	10	|5|	4d5c57ea9a6940dd891ad53e9dbe8da0|	bogo|	10|
|2|	[web, email, mobile]|	0|	4|	3f207df678b143eea3cee63160fa8bed|	informational|	0|
|3|	[web, email, mobile]|	5|	7|	9b98b8c7a33c4b65b9aebfe6a799e6d9|	bogo|	5|
|4|	[web, email]|	20|	10|	0b1e1539f2cc45b7b9fa7c272da2e1d7|	discount|	5|
|5|	[web, email, mobile, social]|	7|	7|	2298d6c36e964ae4a3e7e9706d1fb8c2|	discount|	3|
|6|	[web, email, mobile, social]|	10|	10|	fafdcd668e3743c1bb461111dcafc2a4|	discount|	2|
|7|	[email, mobile, social]|	0|	3|	5a8bc65990b245e5a138643cd4eb9837|	informational|	0|
|8|	[web, email, mobile, social]|	5|	5|	f19421c1d4aa40978ebb69ca19b0e20d|	bogo|	5|
|9|	[web, email, mobile]|	10|	7|	2906b810c7d4411798c6938adc9daaa5|	discount|	2|

以下是文件中每个变量的类型和解释 ：

**portfolio.json**
* id (string) – 推送的id
* offer_type (string) – 推送的种类，例如 BOGO、打折（discount）、信息（informational）
* difficulty (int) – 满足推送的要求所需的最少花费
* reward (int) – 满足推送的要求后给与的优惠
* duration (int) – 推送持续的时间，单位是天
* channels (字符串列表)

**profile.json**
* age (int) – 顾客的年龄 
* became_member_on (int) – 该顾客第一次注册app的时间
* gender (str) – 顾客的性别（注意除了表示男性的 M 和表示女性的 F 之外，还有表示其他的 O）
* id (str) – 顾客id
* income (float) – 顾客的收入

**transcript.json**
* event (str) – 记录的描述（比如交易记录、推送已收到、推送已阅）
* person (str) – 顾客id
* time (int) – 单位是小时，测试开始时计时。该数据从时间点 t=0 开始
* value - (dict of strings) – 推送的id 或者交易的数额

# 数据分析与模型建立

请查看[Starbucks_Capstone_notebook-zh.ipynb](,/Starbucks_Capstone_notebook-zh.ipynb)，
详细记录了数据分析和模型建立的过程。

###  结果讨论

1. k邻近、随机森林和adaboost三种算法准确率相差不大，可能主要因为数据量不大的原因。
三种算法中使用adaboost算法得到的精度在3种分类器中最高，为77.2%。
[Adaboost](https://scikit-learn.org/stable/modules/ensemble.html#adaboost)是一种集成方法。集成方法的目标是将使用给定学习算法构建的几个基本分类器的预测结合起来，以提高单个分类器的通用性/鲁棒性。通常有两种集成方法：1.平均方法，原理是独立建立多个分类器，然后平均其预测。平均而言，由于组合分类器的方差减小了，因此组合分类器通常比任何单个基础分类器都要好，随机森林法属于该类。2.增强方法，基本分类器是按顺序构建一系列分类器，然后尝试减小组合分类器的偏差。这样做的动机是将几个弱分类器结合起来以产生一个强大的整体，adaboost属于该类。AdaBoost的核心原则是构建一系列弱分类器，这些弱分类器比随机猜测仅仅稍微好一点(如小决策树)。在每次迭代中不断更新权重，然后通过加权多数投票(或求和)将所有预测组合起来，得出最终预测。

2. 使用网格搜索得出了最优参数{'clf__estimator__learning_rate': 1.0, 'clf__estimator__n_estimators': 300}。

3. 限于时间和机器性能，没有进行更多尝试，后续可以尝试更多不同算法，以比对时间花销和精度。

4. 关于算法选择，sklearn提供了一个[cheatsheet](https://scikit-learn.org/stable/tutorial/machine_learning_map/index.html)值得参考。

5. 后续可以继续研究顾客消费金额同用户信息和推送信息间的关系，来预测不同顾客的消费金额和推送对消费金额的影响。

# 应用程序
### 预测
在input.json中包含一名顾客的信息，在命令行中使用python run.py model.pickle input.json result.txt
命令，即可使用model.pickle中保存的模型，预测input.json中的顾客对于推送的预测结果，并将结果保存到result.txt中。
### 数据处理
原始数据处理可使用命令python process_data.py data/ data/cleaned_data.pickle，即可处理data文件夹中的portfolio.json 
、profile.json 、transcript.json文件，并将清理好的数据保存到data文件夹下的cleaned_data.pickle文件中。
### 训练模型
可使用命令python train_classifier.py ./data/clean_data.pickle model.pickle，即可使用data文件夹中处理好的
数据clean_data.pickle训练模型，并将模型保存至model.pickle文件中。
