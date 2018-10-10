# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier


def drawPic(arr):

    x = arr[:,0]
    y = arr[:,1]
    z = arr[:,2]

    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    ax.set_xlabel('n_neighbors')
    ax.set_ylabel('leaf_size')
    ax.set_zlabel('f1 score')
    ax.plot_trisurf(x,y,z,linewidth=0.2,antialiased = True )
    plt.savefig("../../data/knn_img.png")

    plt.show()

def mkdir(path):

    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


datapath = "../../data/"
train_data = np.loadtxt(datapath + "Test1_features.dat", delimiter=',')
print("训练数据集(shape):")
print(train_data.shape)

train_label = np.loadtxt(datapath + "Test1_labels.dat", delimiter=',')
print("训练数据标签(shape):")
print(train_label.shape)

#开始调优使用GridSearchCV找到,最优参数
knn = KNeighborsClassifier()
#设置k的范围
k_range = list(range(1,5))
leaf_range = list(range(1,4))

#weight_options = ['uniform','distance']
#algorithm_options = ['auto','ball_tree','kd_tree','brute']

weight_options = ['uniform']


parameter_space = dict(
        n_neighbors = k_range,
        weights = weight_options,
        #algorithm=algorithm_options,
        leaf_size=leaf_range)

score = 'f1'
grid = GridSearchCV(knn, parameter_space, cv=3, scoring='%s' % score,verbose=1)
grid.fit(train_data, train_label)
print("Best parameters set found on development set:")
print()
print(grid.best_params_)
print()
print("Grid scores on development set:")
print()
print("best_score_")
print(grid.best_score_)
print()
arr = [];
params_min_samples_leaf_x = [];
params_max_depth_y = [];
result_z = [];
path = "./result_knn/"
mkdir(path)

means = grid.cv_results_['mean_test_score']
stds = grid.cv_results_['std_test_score']



params = grid.cv_results_['params']

for mean, stdev, param in zip(means, stds, params):
    params_min_samples_leaf_x.append(param['n_neighbors'])
    params_max_depth_y.append(param['leaf_size'])
    result_z.append(mean)
    print("%0.3f (+/-%0.03f) for %r" % (mean, stdev*2, param))

arr.append(params_min_samples_leaf_x)
arr.append(params_max_depth_y)
arr.append(result_z)

np.savetxt(path + "arr1.txt", np.transpose(arr))
arr_s = np.loadtxt(path + 'arr1.txt')
drawPic(arr_s);


