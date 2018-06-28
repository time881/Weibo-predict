import jieba as jb
import jieba.analyse as analyse
import jieba.posseg as pseg
import collections
from collections import Counter
import numpy as np
import pandas as pd
from datetime import datetime
import math
import gc
import DataTool as dtool
import WBLearn as wblearn
import sklearn as skl
from sklearn.ensemble import RandomForestRegressor as rfr
from sklearn.externals import joblib
import os

jb.suggest_freq(('http://'), True)
jb.suggest_freq(('http'), True)
jb.suggest_freq(('.net'), True)
jb.suggest_freq(('╮ (￣ 3￣) ╭'), True)
jb.suggest_freq(('.com'), True)
jb.suggest_freq(('大数据'), True)
jb.suggest_freq(('发红包'), True)
jb.suggest_freq(('雾霾'), True)


def PredictProcess(Content, Numtype=1):
	LoadUserWordDictFileName = "UserDict/UserWordDictCollect"+"_"+(str)(Numtype)+".txt"
	load = open(LoadUserWordDictFileName,"rb")
	UserWordDict = eval(load.read().decode('utf-8'))
	result = []#预测结果
	for each in Content:
		TempInfo = []
		TempInfoCollect = []
		Trainfilename = dtool.RFTModulefileName(each[0], Numtype)
		if os.path.exists(Trainfilename):
			Week, Time = dtool.Timetransf(each[2])
			
			Weight = 0
			index = 0.00001
			TempSentence = jb.lcut(each[-1])
			for i in TempSentence:
				if i in UserWordDict[each[0]]:
					index += 1
					Weight += UserWordDict[each[0]][i]
			Weight = Weight/index
			TempInfo.append(Weight)
			TempInfo.append(Time)
			TempInfo.append(Week)
			TempInfoCollect.append(TempInfo)
			#print(TempInfo)

			clf = joblib.load(Trainfilename) 
			pre1 = clf.predict(TempInfoCollect)
			result.append((int)(round(pre1[0])))
		else:
			result.append(0)

	del UserWordDict
	result = np.array(result).reshape(-1)
	#print(result)
	return result



Content = dtool.OpenWbfileToList("weibo_predict_data/weibo_predict_data.txt", linenumber=0, isTrainData=False)
List1 = PredictProcess(Content, Numtype=1)
print("round1 end")
List2 = PredictProcess(Content, Numtype=2)
print("round2 end")
List3 = PredictProcess(Content, Numtype=3)
print("round3 end")
ResultContent = np.c_[Content[:,:2],np.c_[List1, np.c_[List2, List3]]]
dtool.WriteResultToFile(ResultContent, 'Result/Result.txt')
