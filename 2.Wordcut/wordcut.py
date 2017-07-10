# -*- coding: utf-8 -*-
import csv
import jieba

#处理每一行信息文本(注意:处理用result直接用excel打开会乱码，请用Notepad等工具打开)
class wooyun_serialize(object):
	def __init__(self,row):
		self.date = row['date'].decode("utf-8")
		self.url = row['url'].decode("utf-8")
		self.title = row['title'].decode("utf-8")
		#存储分词结果
		self.words = []
		#读取停用词表，这里存放标点符号，用于过滤分词产生的标点符号
		stop = open("stopword.txt",'r')
		self.stopwords = {}
		for line in stop.readlines():
			line = line[:-1]
			self.stopwords[line] = True
	#分词函数
	def title_cut(self):
		self.words = list(jieba.cut(self.title,cut_all=False))
	#将分词结果转化为字符串
	def get_wordcut(self):
		string = "" 
		for word in self.words:
			if word.encode('gbk','ignore') not in self.stopwords:
				string += word + '|'
		string = string[:-1]
		return string

#分词过程的调度类
class word_cut(object):
	def __init__(self):
		filename = "wordcut.csv"
		f = file(filename,"wb")
		self.writer = csv.writer(f)
		self.writer.writerow(['date','url','title','wordcut'])
	
	#分词执行
	def analysis(self):
		with open('result.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				wooyun_unit = wooyun_serialize(row)
				wooyun_unit.title_cut()
				date = wooyun_unit.date.encode('utf-8')
				url = wooyun_unit.url.encode('utf-8')
				title = wooyun_unit.title.encode('utf-8')
				wordcut = wooyun_unit.get_wordcut().encode('utf-8')
				self.writer.writerow([date,url,title,wordcut])

#执行
ana = word_cut()
ana.analysis()
