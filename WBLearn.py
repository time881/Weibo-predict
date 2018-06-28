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
import sklearn as skl
from sklearn.ensemble import RandomForestRegressor as rfr
from sklearn.externals import joblib

jb.suggest_freq(('http://'), True)
jb.suggest_freq(('http'), True)
jb.suggest_freq(('.net'), True)
jb.suggest_freq(('╮ (￣ 3￣) ╭'), True)
jb.suggest_freq(('.com'), True)
jb.suggest_freq(('大数据'), True)
jb.suggest_freq(('发红包'), True)
jb.suggest_freq(('雾霾'), True)

def RFTLearn(learnStruct, learnLabel, fileName):
	rf2 = rfr(n_estimators=50,max_depth=4);
	rf2.fit(learnStruct, learnLabel)
	joblib.dump(rf2, fileName)
	pass


#Row:用户转发总数，ContentDict 用户转发Detial
def learnByUser(ContentDict, UserWordDictCollect, row, type=1):
	
	UselessPro = {'f','uj','x', 'c', 'r','p', 'h','d','ul','e','y','k','o','m','u','ud'
	,"ug"
	,"uj"
	,"ul"
	,"uv"
	,"uz"}

	dropword = {'http','t',"cn",'是',"有","到","我","我们"}
	ContentDict = np.array(ContentDict)
	idex=np.lexsort([ContentDict[:, 1+type]])
	ContentDict_sort=ContentDict[idex,:]
	del ContentDict
	#ContentDict = collections.OrderedDict(sorted(ContentDict.items(), key = lambda t:t[1][1+type],reverse = False))
	
	learnStruct = []#以ContentID 为单位，文章权值时间为内容的训练结构
	learnLabel = []

	UserWordDict={}#用户的词汇表和词汇权值
	for i in ContentDict_sort:
		TempInfo = []
		Strflag = pseg.lcut(i[-1])
		weight = (int)(i[1+type])
		index = 0
		weightCount=0
		for word, flag in Strflag:
			if not word in UserWordDict and not word in dropword and not flag in UselessPro:
				index += 1
				weightCount += weight
				UserWordDict[word] = weight
			elif word in UserWordDict and (word in dropword or flag in UselessPro):
				del UserWordDict[word]

		aveWeight = weightCount/(index+0.00001)
		Week, Time = dtool.Timetransf(i[1])
		TempInfo.append(aveWeight)
		TempInfo.append(Time)
		TempInfo.append(Week)
		learnStruct.append(TempInfo)
		learnLabel.append(weight)

	UserWordDictCollect[row['userid']] = UserWordDict

	fileName = dtool.RFTModulefileName(row['userid'], type)

	RFTLearn(learnStruct, learnLabel, fileName)
	pass

