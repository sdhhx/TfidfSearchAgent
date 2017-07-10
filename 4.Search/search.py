# -*- coding: utf-8 -*-
import csv
import math
import jieba

#查询数据生成
class queryvec_gen(object):
	def __init__(self,input):
		self.input = input
		self.vec = {}
	
	#计算查询词，主要为计算查询词的权重
	def vector_cal(self):
		wordcut = list(jieba.cut(self.input,cut_all=False))
		maxfreq = 0
		for word in wordcut:
			if not word in self.vec:
				self.vec[word] = 1
			else:
				self.vec[word] += 1
			if self.vec[word] > maxfreq:
				maxfreq = self.vec[word]
		with open('wordidf.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				word = row['word'].decode("utf-8")
				idf = float(row['idf'].decode("utf-8"))
				if self.vec.has_key(word):
					self.vec[word] = (0.5 + 0.5 * float(self.vec[word]) / float(maxfreq) ) * idf
		return self.vec
	
	#计算向量的模值
	def vecnorm_cal(self):
		norm = 0
		for word in self.vec:
			norm += self.vec[word] * self.vec[word]
		norm = math.sqrt(norm)
		return norm
					
class search(object):
	def __init__(self):
		print u"请输入你想搜索的信息:",
		self.query = raw_input()
		self.query = self.query
		self.query = queryvec_gen(self.query)
		self.queryvec = self.query.vector_cal()
		self.queryvecNorm = self.query.vecnorm_cal()
		self.result_list = []
	
	#计算向量的模值
	def vecnorm_cal(self,vec):
		norm = 0
		for word in vec:
			norm += vec[word] * vec[word]
		norm = math.sqrt(norm)
		return norm
	
	#向量相似度计算，主要是余弦值计算
	def similarity_cal(self,vec1,vec2,vec1Norm,vec2Norm):
		similarity = 0
		for word in vec1:
			if vec2.has_key(word):
				similarity += vec1[word] * vec2[word]
		similarity = similarity / (vec1Norm * vec2Norm)
		return similarity
	
	#计算查询词与文档的相似度，然后按照相似度进行排行，完成检索操作
	def input_search(self):
		with open('wordvec.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				date = row['date'].decode("utf-8")
				url = row['url'].decode("utf-8")
				title = row['title'].decode("utf-8")
				info = [date,url,title]
				
				title_vec = {}
				tmp = row['wordvec'].decode("utf-8").split("|")
				for word in tmp:
					word = word.split(",")
					title_vec[ word[0] ] = float(word[1])
				similarity = self.similarity_cal(title_vec,self.queryvec,self.vecnorm_cal(title_vec),self.queryvecNorm)
				self.result_list.append([info, similarity])
		#list的排序函数
		self.result_list.sort(key = lambda x:float(x[1]),reverse = True)
		self.show_result()
	
	#展示检索结果
	def show_result(self):
		count = 0
		for info in self.result_list:
			if info[1] >= 0.01:
				count += 1
		print u"共检索到",str(count),u"条记录。"
		i = 1
		string = ""
		for info in self.result_list:
			if info[1] >= 0.01:
				print u"发布日期:",info[0][0]
				print u"标题:",info[0][2]
				print u"链接:",info[0][1]
				print ""
				#print str(info[1])
				if i == 20:
					break
				i += 1

ser = search()
ser.input_search()
