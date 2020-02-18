
# coding: utf-8

# # 目录
# [1. 加载数据](#1)<br>
# [2. 描述性统计](#2)<br>
# [3. 数据预处理](#3)<br>
# [4. 特征工程](#4)<br>
# [5. 训练模型及模型评估](#5)<br>
# [6. 模型应用--预测新数据](#6)<br>

# <div id="1"></div>
# # 一、加载数据

# In[2]:

import pandas as pd
import numpy as np


# In[461]:

# 加载产品实例信息
prd_data = pd.read_csv('prd_data.csv',encoding='utf-8')


# In[28]:

prd_data.head()


# In[4]:

# 加载通话信息、个人信息、DPI信息、终端信息和训练集标签数据
call_data = pd.read_csv('call_data.csv',encoding='utf-8')
cust_data = pd.read_csv('cust_data.csv',encoding='utf-8')
dpi_data = pd.read_csv('dpi_data.csv',encoding='utf-8')
trmnl_data = pd.read_csv('trmnl_data_update.csv',encoding='utf-8')
train_label = pd.read_csv('train_result.csv',encoding='utf-8')


# In[28]:

# 以产品实例信息为主表，关联其余信息表，生成原始数据宽表
all_data = pd.merge(prd_data, call_data, how='left', on='user')


# In[30]:

all_data = pd.merge(all_data, cust_data, how='left', on='user')
all_data = pd.merge(all_data, dpi_data, how='left', on='user')
all_data = pd.merge(all_data, trmnl_data, how='left', on='user')
all_data = pd.merge(all_data, train_label, how='left', on='user')


# In[31]:

#查看数据表前5行
all_data.head()


# In[3]:

all_data.to_csv('all_data.csv',index=None)
#all_data = pd.read_csv('all_data.csv',encoding = 'utf-8')


# <div id="2"></div>
# # 二、描述性统计

# ## 2.1 基本信息

# In[44]:

# 查看宽表大小
all_data.shape


# In[35]:

# 查看宽表基本信息
all_data.info()


# ## 2.2 查看缺失值

# In[39]:

# 统计有缺失值的列，及缺失记录数
all_data.isnull().sum()[all_data.isnull().sum()>0]
# all_data.apply(lambda col: round(float(sum(col.isnull()))/col.size, 3))  #统计缺失值占比


# ## 2.3 数据的分布情况

# In[369]:

#查看目标变量数据的分布  离散型变量的数据分布都可以用这种方式来统计
all_data['label'].value_counts(dropna=False)


# In[41]:

#连续型变量的数据分布  统计记录条数、均值、标准差、最小值、最大值和三个分位点值  此处仅为演示做了简化处理，实际有些列需要先做处理再统计其分布
all_data.describe()


# <div id="3"></div>
# # 三、数据预处理

# ## 3.1缺失值处理

# In[370]:

# 列出存在缺失值的列
all_data.isnull().columns


# In[5]:

# 缺失值处理应该结合数据分布及对数据的理解来进行。
#为简化，本次演示中把APP访问次数类的字段缺失值都填充为0，其余都处理为-1，。
col_fill0 = ['app1_visits', 'app2_visits', 'app3_visits', 'app4_visits', 'app5_visits', 'app6_visits', 'app7_visits', 'app8_visits']
for col in col_fill0:
    all_data[col].fillna(0, inplace=True)
    
all_data = all_data.fillna(-1)


# In[467]:

#再次确认缺失值情况
all_data.isnull().sum()[all_data.isnull().sum()>0]


# ## 3.2 异常值处理

# In[468]:

# 以开通日期为例
# 开通日期及对应条数，按开通日期倒序排序，看前10个
all_data['open_date'].value_counts().sort_index(ascending=False).head(10)


# In[470]:

# 统计异常值条数
all_data[prd_data['open_date']>20190930].shape


# In[471]:

# 简化起见，把开通日期在20190930以后的异常值替换为该列中位数
all_data.loc[all_data['open_date']>20190930,'open_date']=all_data['open_date'].median()


# <div id="4"></div>
# # 四、特征工程

# ## 4.1特征转换——日期特征转化为时长特征

# In[303]:

from datetime import datetime,timedelta
import time
def months(str1,str2):
    if len(str2)==6:
        str1_d = datetime.strptime(str1, "%Y%m")
        str2_d = datetime.strptime(str2, "%Y%m")
        num=(str1_d.year-str2_d.year)*12+(str1_d.month-str2_d.month)
    elif len(str2)==7:
        str1_d = datetime.strptime(str1, "%Y%m")
        str2_d = datetime.strptime(str2, "%Y-%m")
        num = (str1_d.year-str2_d.year)*12+(str1_d.month-str2_d.month)
    else:
        num=-1
    return num


# In[483]:

# 对客户入网时间、出生日期、终端自注册短信发送时间、用户的开通日期做此类处理。
all_data['cust_access_net_dt']=all_data['cust_access_net_dt'].apply(lambda x:months('201910',str(x)[0:6]))
all_data['birth_date']=all_data['birth_date'].apply(lambda x:months('201910',str(x)[0:6]))
all_data['register_date']=all_data['register_date'].apply(lambda x:months('201910',str(x)[0:7]))
all_data['open_date']=all_data['open_date'].apply(lambda x:months('201910',str(x)[0:6]))


# In[484]:

all_data['register_date'].head()


# ## 4.2 特征转换——对类别变量进行编码
# 

# ### 4.2.1 独热编码（One-hot encoding）

# In[136]:

#统计终端品牌分布，按记录数排序
all_data[['user','pro_brand']].groupby(['pro_brand']).size().sort_values(ascending=False)


# In[376]:

pro_brand = pd.DataFrame({'total':all_data[['user','pro_brand']].groupby('pro_brand').size().sort_values(ascending=False)})


# In[377]:

pro_brand.head() #此时pro_brand是索引，total是列


# In[378]:

#重置索引
pro_brand.reset_index(inplace=True)


# In[379]:

pro_brand.head(10)


# In[485]:

pro_brand_list=pro_brand.iloc[:8,0].tolist()
pro_brand_list


# In[486]:

all_data['pro_brand']=all_data['pro_brand'].apply(lambda x:x if x in pro_brand_list else '其他')


# In[487]:

all_data['pro_brand'].head(10)


# In[489]:

all_data = pd.get_dummies(all_data,columns=['pro_brand'],prefix="pro_brand")


# In[490]:

all_data.head()


# In[491]:

all_data.columns


# In[492]:

all_data.to_csv('all_data1.csv',index=None)


# In[ ]:

#all_data = pd.read_csv('all_data1.csv',encoding = 'utf-8')


# ### 4.2.2 标签编码（Label Encoding）

# In[316]:

#标签编码直接将类别转换为数字  
#统计信用度等级分布
all_data['credit_level'].value_counts()


# In[98]:

from sklearn.preprocessing import LabelEncoder


# In[493]:

le_credit_level = LabelEncoder().fit(all_data['credit_level'])
all_data['credit_level'] = le_credit_level.transform(all_data['credit_level'])


# In[494]:

all_data['credit_level'].value_counts()


# In[495]:

#会员等级、星级级别做同样处理
le_membership_level = LabelEncoder().fit(all_data['membership_level'])
all_data['membership_level'] = le_membership_level.transform(all_data['membership_level'])

le_star_level = LabelEncoder().fit(all_data['star_level'])
all_data['star_level'] = le_star_level.transform(all_data['star_level'])

# all_data['membership_level'] = LabelEncoder().fit_transform(all_data['membership_level'])


# In[496]:

all_data['star_level'].value_counts()


# In[6]:

#对目标变量做同样处理
all_data['label'].value_counts()


# In[498]:

le_label = LabelEncoder().fit(all_data['label'][all_data['label']!= -1])   #可能需要把-1改成'-1'


# In[223]:

le_label.classes_


# In[500]:

all_data.loc[all_data['label']!= -1,'label'] = le_label.transform(all_data['label'][all_data['label']!= -1])
#all_data.loc[all_data['label']!= -1,'label'] = LabelEncoder().fit_transform(all_data['label'][all_data['label']!= -1])


# In[112]:

le_label.inverse_transform([0,1,2,3,4])


# In[501]:

all_data['label'].value_counts()


# In[502]:

all_data.to_csv('all_data2.csv',index=None)


# In[ ]:

#all_data = pd.read_csv('all_data2.csv',encoding = 'utf-8')


# ### 4.2.3 频数编码
# + 频数编码（count encoding）  使用频次替换类别，频次根据训练集计算。这个方法对离群值很敏感，所以结果可以归一化或者转换一下，另外有些变量的频次可能是一样的，这将导致碰撞——两个类别编码为相同的值

# In[503]:

all_data['term_model'].head()


# In[504]:

####终端型号（按照终端型号的出现次数）
#这里的处理是在全部数据集上了，应该改为训练集。
term_model = pd.DataFrame({'total':all_data[['user','term_model']].groupby('term_model').size().sort_values(ascending=False)})


# In[398]:

term_model


# In[505]:

all_data['term_model'] = all_data['term_model'].apply(lambda x:term_model.at[x,'total'] if x!=-1 else -1)


# In[506]:

all_data['term_model'].head()


# In[507]:

all_data.to_csv('all_data3.csv',index=None)


# In[366]:

all_data = pd.read_csv('all_data3.csv',encoding = 'utf-8')


# ### 4.2.4 其它编码方式
# + labelcount编码   根据类别在训练集中的频次排序来编码（升序或降序），对离群值不敏感，也不会对不同的值给出同样的编码。
# + 目标编码 （target encoding） 它使用目标变量的均值来编码类别变量，有技巧，但是好用。

# ## 4.3 数据标准化

# 
# 常见的数据标准化方法
# + min-max标准化（离差标准化）
# + Z-score标准化
# + Logistic标准化 
# + 小数定标标准化
# 等

# In[508]:

all_data.info()


# In[509]:

## 选出需要进行标准化的特征
scale_columns = all_data.select_dtypes(include=['float','int64']).columns
scale_columns


# In[510]:

len(scale_columns)


# In[511]:

#删掉其中无需标准化的属性，包括：数据为类别编码类、占比类
scale_columns = scale_columns.drop(['last_year_capture_user_flag','dt_m_1032', 'dt_m_1034', 'dt_m_1035', 'dt_m_1085', 'dt_m_1086', 'dt_m_1087','credit_level','membership_level', 'gender','star_level', 'label'])


# 简单起见，本演示把这些特征都进行min-max标准化

# In[515]:

#定义标准化函数
min_max_scaler = lambda x : (x-np.min(x))/(np.max(x)-np.min(x))


# In[545]:

#在需要进行标准化的列上执行该函数
all_data[scale_columns]=all_data[scale_columns].apply(min_max_scaler)


# In[546]:

all_data[scale_columns].head()


# In[552]:

all_data.to_csv('all_data4.csv',index=None)


# In[3]:

all_data = pd.read_csv('all_data4.csv',encoding = 'utf-8')


# ## 4.4 特征选择&特征提取

# 
# + 特征选择：在原有特征集中通过一定的方法进行选择，不生成新的特征。方法有过滤式（Filter）、包裹式（Wrapper）、嵌入式（Embedding）等；
# + 特征提取（通常所说的降维）：通过一定手段从原始特征集中生成新的特征集，来替代原始特征集。常见方法如主成分分析（PCA）、线性判别分析（LDA）等。

# 介绍一个基础的特征选择工具feature-selector，里面包含了几种常用的特征选择的方法。
# 
# 下面演示下如何使用这个库中的函数对高相关性的特征进行特征选择。

# In[4]:

#拆分数据
train_data = all_data[all_data['label']>-1]
test_data = all_data[all_data['label']==-1]
print(train_data.shape)
print(test_data.shape)


# In[7]:

train_data.columns


# In[5]:

from feature_selector import FeatureSelector


# In[8]:

train_labels = train_data['label']
train_features = train_data.drop(columns=['user', 'product_nbr','last_year_capture_user_flag','label', 'pro_brand_-1', 'pro_brand_Apple', 'pro_brand_三星', 'pro_brand_其他', 'pro_brand_华为', 'pro_brand_小米',
       'pro_brand_未知厂商', 'pro_brand_欧珀', 'pro_brand_维沃'])


# In[14]:

fs = FeatureSelector(data=train_features, labels=train_labels)
fs.identify_collinear(correlation_threshold = 0.9,one_hot=False)
# 绘制选择的特征的相关性heatmap
fs.plot_collinear()
# 列出要删除的共线特征
collinear_features = fs.ops['collinear']
# 查看共线特征的dataframe
fs.record_collinear


# In[20]:

train_data = train_data.drop(columns=collinear_features)


# In[21]:

train_data.shape


# In[80]:

collinear_features


# <div id="5"></div>
# # 5. 训练模型及模型评估

# ## 5.1 逻辑回归

# In[25]:

# 训练集上需要删除用户标识、产品实例这类的列
train_data.columns


# In[29]:

X=train_data.drop(['label','user','product_nbr'],axis=1)
y=train_data['label']


# In[30]:

from sklearn.linear_model import LogisticRegression
#from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score


# In[32]:

# 分割训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 / 3., random_state=22)


# In[35]:

# penalty:正则化 l2/l1
# C ：正则化强度
# multi_class:多分类时使用 ovr: one vs rest
model = LogisticRegression(penalty='l2', C=100, multi_class='multinomial',solver="newton-cg",n_jobs=-1)
lgr = model.fit(X_train, y_train)


# In[36]:

# 对测试集进行预测
y_pred = lgr.predict(X_test)
#在测试集上的平均精度
print(lgr.score(X_test, y_test))


# In[37]:

#计算P、R、F1
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
f1 = f1_score( y_test, y_pred, average='macro' )


# In[38]:

p = precision_score(y_test, y_pred, average='macro')
r = recall_score(y_test, y_pred, average='macro')
print('f1',f1)
print('p',p)
print('r',r)


# In[50]:

lgr.coef_[0]


# In[58]:

# 特征重要性
feature_importance = X_train.std(axis=0)*(1/X_train.std(axis=0))*lgr.coef_[0]  #lgr.coef_[0]只是重要性的值，乘上前面实际数值等于1的部分是为了对应到特征上。
feature_importance = np.abs(feature_importance)
feature_importance.sort_values(ascending=False)


# ## 5.2 Xgboost

# In[276]:

#基于Scikit-learn接口的xgboost多分类
import xgboost as xgb
import datetime
model = xgb.XGBClassifier(max_depth=10, learning_rate=0.1, n_estimators=200, silent=True, objective='multi:softmax')
starttime = datetime.datetime.now()
xgb_model = model.fit(X_train, y_train)
endtime = datetime.datetime.now()
print("耗时：%d" %(endtime - starttime).seconds +"s")


# In[273]:

# 对测试集进行预测
y_pred = xgb_model.predict(X_test)
f1 = f1_score( y_test, y_pred, average='macro' )
p = precision_score(y_test, y_pred, average='macro')
r = recall_score(y_test, y_pred, average='macro')
print('f1',f1)
print('p',p)
print('r',r)


# <div id="6"></div>
# # 6.模型应用——预测新数据

# In[81]:

pred_data = test_data.drop(columns=collinear_features)
X_pred = pred_data.drop(['label','user','product_nbr'],axis=1)


# In[205]:

X_pred.head()


# In[118]:

y_pred = lgr.predict(X_pred)


# In[247]:

y_pred = xgb_model.predict(X_pred)


# In[211]:

np.unique(y_pred)


# In[295]:

#统计预测结果中每个类别出现的次数
from collections import Counter
print(Counter(y_pred))


# In[298]:

#预测结果反编码
y_pred = le_label.inverse_transform(y_pred)
print(Counter(y_pred))

'''
le_tabel.classes_
array(['0F2E4CC10EDBE80F', '56AFA2A526F96CC9', '7C26FADD409BD4B9',
       '816A9BEBED2D7C99', 'C7E2941B65C6CCD6'], dtype=object)'''


# In[299]:

test_data.loc[:,['pred_label']] = y_pred


# In[251]:

test_data[['user','pred_label']].head()


# In[303]:

test_data[['user','pred_label']].to_csv('pred_20191222_6.csv',encoding = 'utf-8',index = None, header = None)


# In[ ]:



