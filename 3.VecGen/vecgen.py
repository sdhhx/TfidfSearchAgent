# -*- coding: utf-8 -*-
import csv
import math
import jieba

#����ÿһ����Ϣ�ı�
class wooyun_serialize(object):
	#��ʼ��
	def __init__(self,row):
		self.date = row['date'].decode("utf-8")
		self.url = row['url'].decode("utf-8")
		self.title = row['title'].decode("utf-8")
		self.words = row['wordcut'].decode("utf-8").split("|")
	#ÿ�������������Ĵ���
	def get_words(self):
		words = {} 
		for word in self.words:
			if not words.has_key(word):
				words[word] = True
		return words
	#����ÿ�������еĹؼ��ʵ�TFֵ����Ƶ/�ʵ���Ŀ)
	def tf_cal(self):
		words = {} 
		for word in self.words:
			if not words.has_key(word):
				words[word] = 1
			else:
				words[word] += 1
		for word in words:
			words[word] = float(words[word]) / float(len(words))
		return words

#����IDFֵ		
class idf_cal(object):
	def __init__(self):
		self.idf = {}
	#����IDFֵ -- log(N/(n+1)) ������N���ĵ�������n��ÿ��������ֵ��ĵ���Ŀ
	def calculate(self):
		with open('wordcut.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			rowNum = 0
			for row in reader:
				wooyun_unit = wooyun_serialize(row)
				rowNum += 1
				wordcut = wooyun_unit.get_words()
				for word in wordcut:
					if not word in self.idf:
						self.idf[word] = 2
					else:
						self.idf[word] += 1
		for word in self.idf:
			self.idf[word] = math.log(rowNum/self.idf[word])
		return self.idf

#�������ɣ�������ʽ�� ����,tf-idfֵ| ... |����,if-idfֵ		
class vector_gen(object):
	def __init__(self):
		self.idf = idf_cal().calculate()
		
		filename1 = "wordvec.csv"
		f1 = file(filename1,"wb")
		self.writer1 = csv.writer(f1)
		self.writer1.writerow(['date','url','title','wordvec'])
		
		filename2 = "wordidf.csv"
		f2 = file(filename2,"wb")
		self.writer2 = csv.writer(f2)
		self.writer2.writerow(['word','idf'])
	
	tf-idf����: tf*idf
	def calculate(self):
		with open('wordcut.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				wooyun_unit = wooyun_serialize(row)
				date = wooyun_unit.date.encode('utf-8')
				url = wooyun_unit.url.encode('utf-8')
				title = wooyun_unit.title.encode('utf-8')
				
				tf = wooyun_unit.tf_cal()
				tfidf = {}				
				for word in tf:
					tfidf[word] = tf[word] * self.idf[word]
				idf_str = ""
				for word in tfidf:
					idf_str += word
					idf_str += ","
					idf_str += str(round(tfidf[word],4))
					idf_str += "|"
				idf_str = idf_str[:-1].encode('utf-8')
				
				self.writer1.writerow([date,url,title,idf_str])
	
	def idf_output(self):
		for word in self.idf:
			self.writer2.writerow([word.encode('utf-8') , str(round(self.idf[word],4)) ])

ana = vector_gen()
ana.calculate()
ana.idf_output()

		
