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
import os

def Timetransf(timeStr):
		return datetime.strptime(timeStr[0:10], "%Y-%m-%d").weekday(), (int)(timeStr[11:13])+(int)(timeStr[14:16])/60

def OpenWbfileToList(filename, linenumber=0, isTrainData=True):

	Wei_file = open(filename, 'rb');
	Content = Wei_file.read().decode('utf-8')#[0:1100]

	if linenumber == 0:
		Content = (Content.strip().split('\n'))#-5000000
	elif linenumber < 0:
		Content = (Content.strip().split('\n')[linenumber:])#-5000000
	elif linenumber > 0:
		Content = (Content.strip().split('\n')[:linenumber])#-5000000

	if isTrainData:
		Content=[[ii.split('\t')[i]
		           for i in range(7)]
		         for ii in Content]
	else:
		Content=[[ii.split('\t')[i]
		           for i in [0,1,2,3]]
		         for ii in Content]

	Content = np.array(Content)
	print ("prepared Content")
	return Content


def CountUserDict(Content, filename = "UserDict/UserDict.csv", type=1, rewrite=False):#转发

	if not os.path.exists(filename) or rewrite == True:

		Users = pd.DataFrame({'userid':Content[:,0], 'KeyCount': Content[:,(int)(type+2)], 'i':1})
		Users[["KeyCount"]] = Users[["KeyCount"]].astype(int)
		Users = Users.groupby('userid').agg({'KeyCount':sum, 'i':sum}).sort_values(by='KeyCount', ascending=False).reset_index()
		UserDict = open(filename,'w', encoding="utf-8")
		UserDict.write(str(Users.to_csv()))
		UserDict.close()
		return Users;
	elif os.path.exists(filename) and rewrite == False:
		Users = pd.read_csv(filename)
		return Users;


def TransftoDict(Content):
	ContentDic = {}
	for i in Content:
		if i[0] in ContentDic:
			ContentDic[i[0]].append(i[1:])
		else: 
			ContentDic[i[0]] = []
			ContentDic[i[0]].append(i[1:])
	return ContentDic

def RFTModulefileName(Userid, Ntype):
	return ("Module/"+Userid+"_"+(str)(Ntype)+".m")


def WriteResultToFile(Content, Result_Path):
	file = open(Result_Path, 'w')
	length = len(Content)
	index = 0
	for ci in Content:
		limite = 0
		index += 1
		for cj in ci:
			limite += 1
			if limite != 5:
				file.write(str(cj)+'\t')  #\r\n为换行符
			elif index != length:
				file.write(str(cj)+'\n')
			elif index == length : file.write(str(cj))
	file.close() 