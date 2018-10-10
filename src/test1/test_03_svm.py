# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from sklearn.model_selection import GridSearchCV
from sklearn import svm


def drawPic(arr):

    x = arr[:,0]
    y = arr[:,1]
    z = arr[:,2]

    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    ax.set_xlabel('C')
    ax.set_ylabel('gamma')
    ax.set_zlabel('f1 score')
    ax.set_title("svm")
    ax.plot_trisurf(x,y,z,linewidth=0.2,antialiased = True )
    plt.savefig("../../data/svm_img.png")

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


svr = svm.SVC()
C = [1, 10, 100, 1000]
Gamma = [1e-1,1e-2,1e-3,1e-4] #[0.125, 0.25, 0.5 ,1, 2, 4]
parameter_space = {
    'kernel':('linear', 'rbf'), 
    'C':C, 
    'gamma':Gamma
}
score = 'f1'
grid = GridSearchCV(svr, parameter_space, cv=3, scoring='%s' % score,verbose=1)
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
path = "./result_svm/"
mkdir(path)

means = grid.cv_results_['mean_test_score']
stds = grid.cv_results_['std_test_score']
params = grid.cv_results_['params']

for mean, stdev, param in zip(means, stds, params):
    params_min_samples_leaf_x.append(param['C'])
    params_max_depth_y.append(param['gamma'])
    result_z.append(mean)
    print("%0.3f (+/-%0.03f) for %r" % (mean, stdev*2, param))

arr.append(params_min_samples_leaf_x)
arr.append(params_max_depth_y)
arr.append(result_z)

np.savetxt(path + "arr1.txt", np.transpose(arr))
arr_s = np.loadtxt(path + 'arr1.txt')
drawPic(arr_s);

