##代码目录说明
- doc:是测试说明问题
- data:数据集和生成的图片
	- dt_img.png:dt算法第一题结果图片
	- knn_img.png:knn算法第一题结果图片
	- rf_img.png:rf算法第一题结果图片
	- svm_img.png:dt算法第一题结果图片
	- Test1_features.dat:第一题使用数据
	- Test1_labels.dat:第一题使用数据
	- Test2_Data.csv：第二题的数据
- src:code
	- /src/test1:是第一问的code
		- test_01_rf.py:RandomForestClassifier
		- test_02_dt.py:DecisionTreeClassifier
		- test_03_svm.py:Svm
		- test_04_knn.py:Knn
		- /result_dt:dt算法的绘图的数据
		- /result_knn:knn算法的绘图的数据
		- /result_rf:rf算法的绘图的数据
		- /result_svm:svm算法的绘图的数据	
	- /src/test2:是第二问的code
		- /fpgrowth/:不适合本题和数据集，可以忽视
	    - /aprior/:解决这个问题的code,all.log输出规则的问题
		 - aprior.py:是aprior算法的代码
		 - runap.py:是运行第二问main
		 - MyLogger.py:是记录规则的日志
		 - all.log:记录规则的日志
	- testData.py：将test2的数据集，预处理并且存储在/item目录中


