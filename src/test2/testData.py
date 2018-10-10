import numpy as np
import pandas as pd
import src.file as file
df=pd.read_csv("../../data/Test2_Data.csv")
print(df.head())
print(df.info())
print(df.describe())
print(np.shape(df.values))
print(df.values[:5,:])
row,col=np.shape(df.values)
print(row,col)
listArr=[]
for i in range(row):
    arr=[]
    for j in range(col):
        if(j==(col-1)):
            if(df.values[i,j]==False):
                arr.append(2000)
            else:
                arr.append(5000)
        else:
            if(df.values[i,j]!=0):
                arr.append(j+1)
        print(i,j)
    listArr.append(arr)
print(listArr)
count=0;
path="./item/"
file.mkdir(path)


for item in listArr:   
    np.savetxt(path+str(count)+"_item.txt",item)
    count=count+1