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
import json



def ProcessMainfunction(Content, UserGroup, Numtype=1):
	UserWordDictCollect = {}#收集用户的词汇表和词汇权值

	for index, row in UserGroup.iterrows():
		if row['KeyCount'] == 0:
			break;
		else:
			wblearn.learnByUser(ContentDict[row['userid']], UserWordDictCollect, row, Numtype);
	SaveUserWordDictFileName = "UserDict/UserWordDictCollect"+"_"+(str)(Numtype)+".txt"
	with open(SaveUserWordDictFileName,'w', encoding='utf8') as outfile:
		outfile.write(str(UserWordDictCollect))

	"""
	with open("UserDict/UserWordDictCollect.txt","rb") as load:
		p = eval(load.read().decode('utf-8'))
		print(p)
	"""

Content = dtool.OpenWbfileToList("weibo_train_data/weibo_train_data.txt")
ContentDict = dtool.TransftoDict(Content)
for i in [1,2,3]:
	filename = "UserDict/UserDict"+"_"+(str)(i)+".csv"
	UserGroup = dtool.CountUserDict(Content,filename=filename, type=i, rewrite=True)
	ProcessMainfunction(ContentDict, UserGroup, i)


"""
with open("UserDict/UserWordDictCollect.txt","rb") as load:
	p = eval(load.read().decode('utf-8'))
	print(p)
"""