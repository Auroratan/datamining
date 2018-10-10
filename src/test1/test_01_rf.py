import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

def drawPic(arr):

    x = arr[:,0]
    y = arr[:,1]
    z = arr[:,2]

    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    ax.set_xlabel('min_samples_leaf')
    ax.set_ylabel('n_estimators')
    ax.set_zlabel('f1 score')
    ax.plot_trisurf(x,y,z,linewidth=0.2,antialiased = True )
    plt.savefig("../../data/rf_img.png")

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

rf = RandomForestClassifier(random_state=10, criterion="entropy", max_depth=10, min_samples_split=50)
n_estimators = [i for i in range(10, 100, 5)]
min_samples_leaf = [i for i in range(2, 30, 2)]

parameter_space = {
    "n_estimators": n_estimators,
    "min_samples_leaf": min_samples_leaf,
}

score = 'f1'
grid = GridSearchCV(rf, parameter_space, cv=3, scoring='%s' % score,verbose=1)
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
path = "./result_rf/"
mkdir(path)

means = grid.cv_results_['mean_test_score']
stds = grid.cv_results_['std_test_score']
params = grid.cv_results_['params']

for mean, stdev, param in zip(means, stds, params):
    params_min_samples_leaf_x.append(param['min_samples_leaf'])
    params_max_depth_y.append(param['n_estimators'])
    result_z.append(mean)
    print("%0.3f (+/-%0.03f) for %r" % (mean, stdev*2, param))

arr.append(params_min_samples_leaf_x)
arr.append(params_max_depth_y)
arr.append(result_z)

np.savetxt(path + "arr1.txt", np.transpose(arr))
arr_s = np.loadtxt(path + 'arr1.txt')
drawPic(arr_s);

