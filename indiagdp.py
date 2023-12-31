# -*- coding: utf-8 -*-
"""INDIAGDP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SHGlNG32YqCtuUI44mvKXDY0OKzynLnw
"""

import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn.model_selection as train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from mpl_toolkits import mplot3d
import statsmodels.api as sm
from sklearn import metrics
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
plt.style.use('seaborn-darkgrid')

data = pd.read_csv("India_GDP_Data.csv")

data

"""# **EDA**"""

data.shape

data.info

data.isna().sum()

data.describe

"""# **Visualization Analysis**"""

plt.figure(figsize=(25,5))
plt.style.use('dark_background')
sns.lineplot(data=data.iloc[:,1:])

data.iloc[:,1:].hist(figsize=(20,5),layout=(1,4))
plt.style.use('dark_background')

data.iloc[:,1:].plot(kind='kde',subplots=True,figsize=(20,5),layout=(1,4))
plt.style.use('dark_background')

sns.pairplot(data,hue='GDP_In_Billion_USD',height=2.5)

"""# **checking for correlation**"""

data.corr()

plt.figure(figsize=(8,6))
sns.heatmap(data.iloc[:, 1:].corr(), annot=True, cmap=plt.cm.CMRmap_r)

data.corr()['GDP_In_Billion_USD']

"""# **insight**"""

plt.style.use('dark_background')
plt.plot(data['Year'],data['GDP_In_Billion_USD'],linewidth=4,linestyle='--',marker='.', markerfacecolor='m',color='b',markersize=12)
plt.xlabel('Year')
plt.ylabel('GDP_In_Billion_USD')
plt.title('GDP GROWTH RATE')

pd.plotting.lag_plot(data['GDP_In_Billion_USD'])
plt.style.use('dark_background')

sm.graphics.tsa.plot_pacf(data.GDP_In_Billion_USD)
plt.style.use('dark_background')

plt.style.use('dark_background')
plt.plot(data['Year'],data['Per_Capita_in_USD'],linewidth=4,linestyle='--',marker='.', markerfacecolor='m',color='k',markersize=12)
plt.xlabel('Year')
plt.ylabel('Per_Capita_in_USD')
plt.title('GDP GROWTH RATE')

pd.plotting.lag_plot(data['Per_Capita_in_USD'])
plt.style.use('dark_background')

sm.graphics.tsa.plot_pacf(data.Per_Capita_in_USD)
plt.style.use('dark_background')

plt.style.use('dark_background')
plt.plot(data['Per_Capita_in_USD'],data['GDP_In_Billion_USD'],linewidth=4,linestyle='--',marker='.', markerfacecolor='m',color='g',markersize=12)
plt.xlabel('Per_Capita_in_USD')
plt.ylabel('GDP_In_Billion_USD')
plt.title('GDP GROWTH RATE')

data.diff().plot(figsize=(8,4),kind='scatter',x = 'Per_Capita_in_USD', y = 'GDP_In_Billion_USD',color='m')
plt.style.use('dark_background')

ax = plt.axes(projection='3d')
ydata = data['Year']
xdata = data['Per_Capita_in_USD']
zdata = data['GDP_In_Billion_USD']
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='gist_rainbow_r');
plt.style.use('dark_background')

"""# **Linear Regression**"""

lr=LinearRegression().fit(X_train,Y_train)
Y_Predict=lr.predict(X_test)

print('r2 score :',r2_score(Y_test,Y_Predict))
print('\n')
print('MAE:',mean_absolute_error(Y_test,Y_Predict))
print('\n')
print('MSE:',mean_squared_error(Y_test,Y_Predict))
print('\n')
print('RSME:',mean_squared_error(Y_test,Y_Predict,squared=False))

X = data.drop('Year', axis=1)
Y = data['Year']

from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans

data = data.copy()
data.drop(columns=['Year'], inplace=True)
data

values = Normalizer().fit_transform(data.values)
print(values)

def clustering_algorithm(n_clusters, dataset):
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, max_iter=300)
    labels = kmeans.fit_predict(dataset)
    s = metrics.silhouette_score(dataset, labels, metric='euclidean')
    dbs = metrics.davies_bouldin_score(dataset, labels)
    calinski = metrics.calinski_harabasz_score(dataset, labels)
    return s, dbs, calinski

for i in range(3, 11):
    s, dbs, calinski = clustering_algorithm(i, values)
    print(i, s, dbs, calinski)

random_data = np.random.rand(167,9)
s_random, dbs_random, calinski_random = clustering_algorithm(3, random_data)
s, dbs, calinski = clustering_algorithm(3, values)

print(s_random, dbs_random, calinski_random)
print(s, dbs, calinski)

set1, set2, set3 = np.array_split(values, 3)
s1, dbs1, calinski1 = clustering_algorithm(3, set1)
s2, dbs2, calinski2 = clustering_algorithm(3, set2)
s3, dbs3, calinski3 = clustering_algorithm(3, set3)
print(s1, dbs1, calinski1)
print(s2, dbs2, calinski2)
print(s3, dbs3, calinski3)

kmeans = KMeans(n_clusters=3, n_init=10, max_iter=300)
y_pred = kmeans.fit_predict(values)
labels = kmeans.labels_

data['labels'] = labels

sns.catplot(x='labels', kind='count', data=data)

centroids = kmeans.cluster_centers_
print(centroids)

max = len(centroids[0])
for i in range(max):
    print(data.columns.values[i],"\n{:.4f}".format(centroids[:, i].var()))

data_0 = data[data['labels'] == 0]
data_1 = data[data['labels'] == 1]
data_2 = data[data['labels'] == 2]

plt.figure(figsize=(8, 6), dpi=80)
plt.scatter(data_0['GDP_In_Billion_USD'], data_0['Per_Capita_in_USD'], c='blue', s=10, label='Cluster A')
plt.scatter(data_1['GDP_In_Billion_USD'], data_1['Per_Capita_in_USD'], c='red', s=10, label='Cluster B')
plt.scatter(data_2['GDP_In_Billion_USD'], data_2['Per_Capita_in_USD'], c='green', s=10, label='Cluster C')

plt.xlabel('GDP_In_Billion_USD')
plt.ylabel('Per_Capita_in_USD')
plt.legend(),
plt.show

description = data.groupby("labels")['GDP_In_Billion_USD', 'Per_Capita_in_USD','labels']
n_clients = description.size()
description = description.mean()
description['n_clients'] = n_clients
print(description)