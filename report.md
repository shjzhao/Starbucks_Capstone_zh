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

以下是文件中每个变量的类型和解释 ：

**portfolio.json**
* id (string) – 推送的id
* offer_type (string) – 推送的种类，例如 BOGO、打折（discount）、信息（informational）
* difficulty (int) – 满足推送的要求所需的最少花费
* reward (int) – 满足推送的要求后给与的优惠
* duration (int) – 推送持续的时间，单位是天
* channels (字符串列表)

||channels|difficulty|duration|id|offer_type|reward|
|-:|-:|-:|-:|-:|-:|-:|
|0|[email, mobile, social]|10|7|ae264e3637204a6fb9bb56bc8210ddfd|bogo|10|
|1|[web, email, mobile, social]|10|5|4d5c57ea9a6940dd891ad53e9dbe8da0|bogo|10|
|2|[web, email, mobile]|0|4|3f207df678b143eea3cee63160fa8bed|informational|0|
|3|[web, email, mobile]|5|7|9b98b8c7a33c4b65b9aebfe6a799e6d9|bogo|5|
|4|[web, email]|20|10|0b1e1539f2cc45b7b9fa7c272da2e1d7|discount|5|
|5|[web, email, mobile, social]|7|7|2298d6c36e964ae4a3e7e9706d1fb8c2|discount|3|
|6|[web, email, mobile, social]|10|10|fafdcd668e3743c1bb461111dcafc2a4|discount|2|
|7|[email, mobile, social]|0|3|5a8bc65990b245e5a138643cd4eb9837|informational|0|
|8|[web, email, mobile, social]|5|5|f19421c1d4aa40978ebb69ca19b0e20d|bogo|5|
|9|[web, email, mobile]|10|7|2906b810c7d4411798c6938adc9daaa5|discount|2|

**profile.json**
* age (int) – 顾客的年龄 
* became_member_on (int) – 该顾客第一次注册app的时间
* gender (str) – 顾客的性别（注意除了表示男性的 M 和表示女性的 F 之外，还有表示其他的 O）
* id (str) – 顾客id
* income (float) – 顾客的收入

||age|became_member_on|gender|id|income|
|-:|-:|-:|-:|-:|-:|
|0|118|20170212|None|68be06ca386d4c31939f3a4f0e3dd783|NaN|
|1|55|20170715|F|0610b486422d4921ae7d2bf64640c50b|112000.0|
|2|118|20180712|None|38fe809add3b4fcf9315a9694bb96ff5|NaN|
|3|75|20170509|F|78afa995795e4d85b5d9ceeca43f5fef|100000.0|
|4|118|20170804|None|a03223e636434f42ac4c3df47e8bac43|NaN|

**transcript.json**
* event (str) – 记录的描述（比如交易记录、推送已收到、推送已阅）
* person (str) – 顾客id
* time (int) – 单位是小时，测试开始时计时。该数据从时间点 t=0 开始
* value - (dict of strings) – 推送的id 或者交易的数额

||event|person|time|value|
|-:|-:|-:|-:|-:|
|0|offer received|78afa995795e4d85b5d9ceeca43f5fef|0|{'offer id': '9b98b8c7a33c4b65b9aebfe6a799e6d9'}|
|1|offer received|a03223e636434f42ac4c3df47e8bac43|0|{'offer id': '0b1e1539f2cc45b7b9fa7c272da2e1d7'}|
|2|offer received|e2127556f4f64592b11af22de27a7932|0|{'offer id': '2906b810c7d4411798c6938adc9daaa5'}|
|3|offer received|8ec6ce2a7e7949b1bf142def7d0e0586|0|{'offer id': 'fafdcd668e3743c1bb461111dcafc2a4'}|
|4|offer received|68617ca6246f4fbc85e91a2a49552598|0|{'offer id': '4d5c57ea9a6940dd891ad53e9dbe8da0'}|
|12654|transaction|02c083884c7d45b39cc68e1314fec56c|0|{'amount': 0.8300000000000001}|
|12657|transaction|9fa9ae8f57894cc9a3b8a9bbe0fc1b2f|0|{'amount': 34.56}|
|12659|transaction|54890f68699049c2a04d415abc25e717|0|{'amount': 13.23}|
|12670|transaction|b2f1cd155b864803ad8334cdf13c4bd2|0|{'amount': 19.51}|
|12671|transaction|fe97aa22dd3e48c8b143116a8403dd52|0|{'amount': 18.97}|

## 数据理解与数据清理

### 1 portfolio 数据

* 将channels转化为one-hot形式
* 将offer_type转化为one-hot形式

得到结果如下：

||difficulty|duration|id|reward|mobile|social|web|email|offer_type_bogo|offer_type_discount|offer_type_informational|
|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|
|0|10|7|ae264e3637204a6fb9bb56bc8210ddfd|10|1|1|0|1|1|0|0|
|1|10|5|4d5c57ea9a6940dd891ad53e9dbe8da0|10|1|1|1|1|1|0|0|
|2|0|4|3f207df678b143eea3cee63160fa8bed|0|1|0|1|1|0|0|1|
|3|5|7|9b98b8c7a33c4b65b9aebfe6a799e6d9|5|1|0|1|1|1|0|0|
|4|20|10|0b1e1539f2cc45b7b9fa7c272da2e1d7|5|0|0|1|1|0|1|0|
|5|7|7|2298d6c36e964ae4a3e7e9706d1fb8c2|3|1|1|1|1|0|1|0|
|6|10|10|fafdcd668e3743c1bb461111dcafc2a4|2|1|1|1|1|0|1|0|
|7|0|3|5a8bc65990b245e5a138643cd4eb9837|0|1|1|0|1|0|0|1|
|8|5|5|f19421c1d4aa40978ebb69ca19b0e20d|5|1|1|1|1|1|0|0|
|9|10|7|2906b810c7d4411798c6938adc9daaa5|2|1|0|1|1|0|1|0|

### 2 profile 数据

#### 2.1 数据量

profile中有17000*5条数据

#### 2.2 缺失数据

|列名|           缺失值数量|
|-:|                    -:|
|age|                    0|
|became_member_on|       0|
|gender|              2175|
|id||0|
|income|              2175|

#### 2.3 数据统计

* 年龄

|统计项|            数值|
|-:|                 -:|
|count|    17000.000000|
|mean|        62.531412|
|std|         26.738580|
|min|         18.000000|
|25%|         45.000000|
|50%|         58.000000|
|75%|         73.000000|
|max|        118.000000|

![年龄分布直方图](./imgs/output_17_1.png '年龄分布直方图')

年龄118岁的顾客人数最多，这显然不合理，可能是年龄选项的上限是118，许多顾客随意填写了上限值，数据处理时，应排除这些年龄数据。

* 会员注册日

最早会员注册日：20130729；

最晚会员注册日：20180726。

* 用户性别

|性别|    人数|
|-:|       -:|
|M |     8484|
|F |     6129|
|NaN |   2175|
|O|       212|

* 用户收入

|统计项|             数值|
|-:|                  -:|
|count|     14825.000000|
|mean |     65404.991568|
|std |      21598.299410|
|min |      30000.000000|
|25% |      49000.000000|
|50% |      64000.000000|
|75% |      80000.000000|
|max|      120000.000000|

![收入分布直方图](./imgs/output_24_1.png '收入分布直方图')

不同性别用户收入情况

|gender|count|mean|std|min|25%|50%|75%|max|
|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|
|F|6129.0|71306.412139|22338.353773|30000.0|54000.0|71000.0|88000.0|120000.0|
|M|8484.0|61194.601603|20069.517615|30000.0|45000.0|59000.0|73000.0|120000.0|
|O|212.0|63287.735849|18938.594726|30000.0|51000.0|62000.0|79250.0|100000.0|

![不同性别收入分布直方图](./imgs/output_26_0.png '不同性别收入分布直方图')

#### 2.4 数据清理

* 缺失值数据处理

数据浏览时发现性别缺失的，同样其收入也缺失，且其年龄为118。这部分无效数据需特别处理。首先将年龄为118的更改为None。

* 处理age数据

将年龄按10岁间隔分组，转化为one-hot形式。

* 处理became_member_on数据

将became_member_on转化为datetime类型后新增became_member_yeaer列，记录用户加入会员的年份。然后将became_member_yeaer转换为one-hot形式。

* 将gender转化为one-hot形式

当gender_F，gender_M，gender_O均为0时，代表None。

* 将income转化为one-hot形式

将收入按10000间隔分组，转化为one-hot形式。如果income各列均为0，代表None。

最终得到结果如下所示：

|age|became_member_on|id|income|age_1.0|age_2.0|...|age_10.0|became_member_year_2013|became_member_year_2014|...|became_member_year_2018|gender_F|gender_M|gender_O|income_3.0|income_4.0|...|income_12.0|
|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|
|0|NaN|2017-02-12|68be06ca386d4c31939f3a4f0e3dd783|NaN|0|0|...|0|0|...|0|0|0|0|0|0|...|0|
|1|55.0|2017-07-15|0610b486422d4921ae7d2bf64640c50b|112000.0|0|0|...|0|0|...|0|1|0|0|0|0|...|0|
|2|NaN|2018-07-12|38fe809add3b4fcf9315a9694bb96ff5|NaN|0|0|...|0|0|...|1|0|0|0|0|0|...|0|
|3|75.0|2017-05-09|78afa995795e4d85b5d9ceeca43f5fef|100000.0|0|0|...|0|0|...|0|1|0|0|0|0|...|0|
|4|NaN|2017-08-04|a03223e636434f42ac4c3df47e8bac43|NaN|0|0|...|0|0|...|0|0|0|0|0|0|...|0|

### 3 transcript 数据

#### 3.1 数据量

transcript中有306534*4条数据。

#### 3.2 缺失数据

无。

#### 3.3 数据统计

不同类别数据量如下：
|类型|数量|
|-:|-:|
|transaction|138953|
|offer received|76277|
|offer viewed|57725|
|offer completed|33579|

![事件数量统计](./imgs/output_31_1.png '事件数量统计')

事件涉及顾客人数：17000。

#### 3.4 数据清理

* 提取除transaction外其他类型事件数据。
* 新增offerId列，从value列中提取offer id值填入，注意value中有部分key是‘offer_id’而不是‘offer id’。
* 删除value列。
* 检查offerId是否有空值，并将推送的id数与portfolio中推送id比较，可知推送的id与portfolio中一致。
* 将同一用户的同一个offerID的接收、浏览、完成情况合并到一行中。增加列'time_btw_rec_view'记录收到推送到阅读推送之间的时间间隔。增加列'time_btw_rec_cmpt'记录收到推送到完成推送之间的时间间隔。
* 增加'offer_viewed'列，标记该条推送是否被浏览。
* 增加'offer_completed'列，标记该条推送是否被完成。
* 增加'time_btw_rec_cmpt_valid'列，计算offer_completed到offer_received的时间是否在有效期内。
* 增加'time_btw_rec_view_valid'列，计算offer_viewed到offer_received的时间是否在有效期内。
* 增加'viewed_before_completed'列，标记该条推送完成前是否别浏览。
注意：
    1. 用户查看、完成的推送，一定在其接收的推送中，但是接收的推送不一定会被用户查看和完成；
    2. 用户完成的推送不一定被用户查看过，用户查看和完成推送也不一定在有效期内；
    3. 同一用户可能收到同一offer多次，如果多个同一ID的offer都在有效期内，处理时默认用户浏览和完成的是最新收到的offer。

### 4 整合数据
* 将portfolio合并入整理好的事件数据中。
* 将profile合并入整理好的事件数据中。
* 删除合并产生的冗余的列。

整合后的数据，取出一条示例如下：

| | |
|-:|-:|
|person| 78afa995795e4d85b5d9ceeca43f5fef|
|offer_received_time|                   0|
|offerId|9b98b8c7a33c4b65b9aebfe6a799e6d9|
|time_btw_rec_view|6|
|time_btw_rec_cmpt|                   132|
|offer_viewed|     1|
|offer_completed|  1|
|time_btw_rec_cmpt_valid|               1|
|time_btw_rec_view_valid|               1|
|viewed_before_completed|               1|
|difficulty|       5|
|duration|         7|
|reward|           5|
|mobile|           1|
|social|           0|
|web|              1|
|email|            1|
|offer_type_bogo|  1|
|offer_type_discount|                   0|
|offer_type_informational|              0|
|age|             75|
|became_member_on|    2017-05-09 00:00:00|
|income|      100000|
|age_1.0|          0|
|age_2.0|          0|
|age_3.0|          0|
|age_4.0|          0|
|age_5.0|          0|
|age_6.0|          0|
|age_7.0|          1|
|age_10.0|         0|
|became_member_year_2013|               0|
|became_member_year_2014|               0|
|became_member_year_2015|               0|
|became_member_year_2016|               0|
|became_member_year_2017|               1|
|gender_F|         1|
|gender_M|         0|
|gender_O|         0|
|income_3.0|       0|
|income_4.0|       0|
|income_5.0|       0|
|income_6.0|       0|
|income_7.0|       0|
|income_8.0|       0|
|income_10.0|      1|
|income_11.0|      0|
|income_12.0|      0|

## 搭建机器学习模型

搭建一个模型来预测某顾客是否会完成推送的活动，以及顾客是否会在完成活动前浏览该推送。

### 1 导入数据
 将'age_1.0', 'age_10.0', 'age_2.0', 'age_3.0', 'age_4.0', 'age_5.0', 'age_6.0', 'age_7.0', 'age_8.0', 'age_9.0', 'became_member_year_2013',
 'became_member_year_2014', 'became_member_year_2015', 'became_member_year_2016', 'became_member_year_2017', 'became_member_year_2018',
 'difficulty', 'duration', 'email', 'gender_F', 'gender_M', 'gender_O', 'income_10.0', 'income_11.0', 'income_12.0', 'income_3.0', 'income_4.0',
  'income_5.0', 'income_6.0', 'income_7.0', 'income_8.0', 'income_9.0', 'mobile', 'offer_type_bogo', 'offer_type_discount',
 'offer_type_informational', 'reward', 'social', 'web' 字段作为输入X，
 将'offer_completed', 'viewed_before_completed'字段作为输出y。

### 2 创建机器学习管道
* 使用MinMaxScaler()，将数值缩放到0~1范围内
* 创建多目标分类器，并使用k邻近算法。

### 3 训练管道
* 将数据分割成训练和测试集
* 训练管道

### 4 测试模型
报告数据集中每个输出类别的 f1 得分、准确度和召回率。

### 5 优化模型
使用网格搜索来找到最优的参数组合。

### 6 再次测试模型
报告数据集中每个输出类别的 f1 得分、准确度和召回率。

### 7 尝试更多算法
使用随机森林和adaboost算法并使用网格搜索寻找最优参数。


##  结果讨论

1. k邻近、随机森林和adaboost三种算法准确率相差不大，可能主要因为数据量不大的原因。
三种算法中使用adaboost算法得到的精度在3种分类器中最高，为77.2%。
[Adaboost](https://scikit-learn.org/stable/modules/ensemble.html#adaboost)是一种集成方法。集成方法的目标是将使用给定学习算法构建的几个基本分类器的预测结合起来，以提高单个分类器的通用性/鲁棒性。通常有两种集成方法：1.平均方法，原理是独立建立多个分类器，然后平均其预测。平均而言，由于组合分类器的方差减小了，因此组合分类器通常比任何单个基础分类器都要好，随机森林法属于该类。2.增强方法，基本分类器是按顺序构建一系列分类器，然后尝试减小组合分类器的偏差。这样做的动机是将几个弱分类器结合起来以产生一个强大的整体，adaboost属于该类。AdaBoost的核心原则是构建一系列弱分类器，这些弱分类器比随机猜测仅仅稍微好一点(如小决策树)。在每次迭代中不断更新权重，然后通过加权多数投票(或求和)将所有预测组合起来，得出最终预测。

2. 使用网格搜索得出了最优参数{'clf__estimator__learning_rate': 1.0, 'clf__estimator__n_estimators': 300}。

3. 限于时间和机器性能，没有进行更多尝试，后续可以尝试更多不同算法，以比对时间花销和精度。

4. 关于算法选择，sklearn提供了一个[cheatsheet](https://scikit-learn.org/stable/tutorial/machine_learning_map/index.html)值得参考。

5. 后续可以继续研究顾客消费金额同用户信息和推送信息间的关系，来预测不同顾客的消费金额和推送对消费金额的影响。

## 应用程序
### 预测
在input.json中包含一名顾客的信息，在命令行中使用python run.py model.pickle input.json result.txt
命令，即可使用model.pickle中保存的模型，预测input.json中的顾客对于推送的预测结果，并将结果保存到result.txt中。
### 数据处理
原始数据处理可使用命令python process_data.py data/ data/cleaned_data.pickle，即可处理data文件夹中的portfolio.json 
、profile.json 、transcript.json文件，并将清理好的数据保存到data文件夹下的cleaned_data.pickle文件中。
### 训练模型
可使用命令python train_classifier.py ./data/clean_data.pickle model.pickle，即可使用data文件夹中处理好的数据clean_data.pickle训练模型，并将模型保存至model.pickle文件中。
