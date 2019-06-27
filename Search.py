import os
import re
import math
import json
import codecs
import collections
from itertools import islice
import threading

def compute_tf_idf_query(path, words, query):

	tf_idf_query = {}
	file = os.listdir(path)
	file_relevance = []
	for item in list(query.lower().split()):
		if(item in words):
			for key in words[item]:
				if(key not in file_relevance):
					file_relevance.append(key)
			x = 0.0
			y = 1.0 + math.log10(float(len(file) / len(words[item])))
			for new in list(query.lower().split()):
				if(new == item):
					x += 1.0
			x /= len(query.split())
			tf_idf_query[item] = x * y
	stopwords = stopword("vietnamese-stopwords.txt")
	stopwords = re.compile(r"\b(" + "|".join(stopwords) + ")\\W")
	cosine = {}
	for filename in file_relevance:
		file1 = codecs.open(path + filename, 'r', 'utf-8')

		fileContent = file1.read()

		fileContentJsonObject = json.loads(fileContent)
		
		jsonObjectContentAttrValue = fileContentJsonObject['content'].lower()
		file1.close()
		jsonObjectContentAttrValue = re.sub(stopwords,r' ', jsonObjectContentAttrValue.lower())
		jsonObjectContentAttrValue = (re.sub(r'[-|?|$|.|!|"|,|(|)|/|_|\'|`|*|+|@|#|%|^|&|[|]|{|}|;|:|<|>|،|、|…|⋯|᠁|ฯ|‹|›|«|»|‘|’|“|”|‱|‰|±|∓|¶|‴|§|‖|¦|©|🄯|℗|®|℠|™|]',r' ', jsonObjectContentAttrValue).split())
		sum = 0.0
		d1 = 0.0
		d2 = 0.0
		
		line = jsonObjectContentAttrValue
		cosine[filename] = []
		
	
		for char in line:
			if(char in query.lower().split()):
				if(filename in words[char]):
					sum += (words[char][filename] * tf_idf_query[char])
					d1 += (words[char][filename]**2)
					d2 += (tf_idf_query[char]**2)
				else:
					d2 += (tf_idf_query[char]**2)
			else:
				
				if(char in words):
					if(filename in words[char]):
						d1 += (words[char][filename]**2)
		if(d1 * d2 != 0.0):
			cosine[filename].append(sum / (math.sqrt(d1) * math.sqrt(d2)))
	cosine = dict(collections.OrderedDict(sorted(cosine.items(), key = lambda kv: kv[1], reverse = True)))
	file_relevance = list(islice(cosine, 100))
	return tf_idf_query, file_relevance

def compute_tf_idf(path, words,tf_idf_filename):
	tf_idf = {}
	file = os.listdir(path)
	for item in words:
		tf_idf[item] = {}
		y = 1.0 + math.log10(float(len(file) / len(words[item])))
		for filename in file:
			if(filename in words[item]):
				link = codecs.open(path + filename, "r", 'utf-8')
				a = link.read().lower()
				link.close()
				a = re.sub(r'[-|?|$|.|!|"|,|(|)|/|_|\'|`|*|+|@|#|%|^|&|[|]|{|}|;|:|<|>|،|、|…|⋯|᠁|ฯ|‹|›|«|»|‘|’|“|”|‱|‰|±|∓|¶|‴|§|‖|¦|©|🄯|℗|®|℠|™|]',r' ', a)
				new = list(a.split())
				tf_idf[item][filename] = (y * (words[item][filename] / len(new)))
	with codecs.open(tf_idf_filename, "w", "UTF-8") as fp:
		json.dump(tf_idf, fp, ensure_ascii=False)

def stopword(data_path):
	stopword_file =  codecs.open(data_path, "r", "UTF-8")
	stopwords = stopword_file.read().split('\n')
	del(stopwords[0])
	stopword_file.close()
	return stopwords

def build_inverted_index(data_path, stopwords,jsonKey,inverted_index_filename):
	file = os.listdir(data_path)
	
	
	dictionary = {}
	non_words = re.compile(r"\b(" + "|".join(stopwords) + ")\\W")
	
	for filename in file:
	
		link = codecs.open(data_path + filename, "r", "UTF-8")
		
		fileContent = link.read()

		fileContentJsonObject = json.loads(fileContent)
		
		split_words = fileContentJsonObject[jsonKey].lower()
	
		link.close()
		split_words = re.sub(non_words,r' ', split_words)

		split_words = re.sub(r'[-|?|$|.|!|"|,|(|)|/|_|\'|`|*|+|@|#|%|^|&|[|]|{|}|;|:|<|>|،|、|…|⋯|᠁|ฯ|‹|›|«|»|‘|’|“|”|‱|‰|±|∓|¶|‴|§|‖|¦|©|🄯|℗|®|℠|™|]',r' ', split_words)
		new = list(split_words.split())
		if(len(new)!=0):

			if(new[-1] in stopwords):
				del(new[-1])
			for word in new:
			
				if(word not in dictionary):
					dictionary[word] = {}
				if(filename not in dictionary[word]):
					dictionary[word][filename] = 1
				else:
					dictionary[word][filename] += 1
		
	with codecs.open(inverted_index_filename, "w", "UTF-8") as fp:
	
		json.dump(dictionary, fp, ensure_ascii=False)

def compute_relevance_cosine(tf_idf, query, tf_idf_query, file, cosine, currentThread):
	if(len(file) >= 100):
		begin = int(len(file) / 100 *(currentThread - 1))
		end = int((len(file) / 100)*currentThread - 1)
	else:
		begin = int(currentThread - 1)
		end = int(currentThread - 1)
	for filename in range(begin,end + 1):
		sum = 0.0
		d1 = 0.0
		d2 = 0.0
		cosine[file[filename]] = []
		for item in tf_idf:
			if(file[filename] in tf_idf[item]):
				if(item in tf_idf_query):
					sum += (tf_idf[item][file[filename]] * tf_idf_query[item])
					d1 += (tf_idf[item][file[filename]]**2)
					d2 += (tf_idf_query[item]**2)
				else:
					d1 += (tf_idf[item][file[filename]]**2)
			else:
				if(item in tf_idf_query):
					d2 += (tf_idf_query[item]**2)
		if(d1 * d2 != 0.0):
			cosine[file[filename]].append(sum / (math.sqrt(d1) * math.sqrt(d2)))
		
def finalCosine(query,idfFile):
	cosine = {}
	f = codecs.open(idfFile, 'r', 'UTF-8')
	tf_idf = json.load(f)
	f.close()
	tf_idf_query, file = compute_tf_idf_query("doc2/", tf_idf, query)
	threads = []
	if(len(file) >= 100):
		for i in range(1, 101):
			t = threading.Thread(target = compute_relevance_cosine, args = (tf_idf, query, tf_idf_query, file, cosine, i))
		
			threads.append(t)
	else:
		for i in range(1, len(file) + 1):
			t = threading.Thread(target = compute_relevance_cosine, args = (tf_idf, query, tf_idf_query, file, cosine, i))
			
			threads.append(t)
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	cosine = dict(collections.OrderedDict(sorted(cosine.items(), key = lambda kv: kv[1], reverse = True)))
	keys = list(islice(cosine, 20))
	sorted_cosine = {}
	for key in keys:
		sorted_cosine[key] = cosine[key]
	
	return sorted_cosine

def finalDistance(query,idfFile):
	distance = {}
	f = codecs.open(idfFile, 'r', 'UTF-8')
	tf_idf = json.load(f)
	f.close()
	tf_idf_query, file = compute_tf_idf_query("doc2/", tf_idf, query)
	threads = []
	if(len(file) >= 100):
		for i in range(1, 101):
			t = threading.Thread(target = compute_relevance_distance, args = (tf_idf, query, tf_idf_query, file, distance, i))
			threads.append(t)
	else:
		for i in range(1, len(file) + 1):
			t = threading.Thread(target = compute_relevance_distance, args = (tf_idf, query, tf_idf_query, file, distance, i))
			threads.append(t)
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	distance = dict(collections.OrderedDict(sorted(distance.items(), key = lambda kv: kv[1])))
	keys = list(islice(distance, 20))
	sorted_distance= {}
	for key in keys:
		sorted_distance[key] = distance[key]
	return sorted_distance

def compute_relevance_distance(tf_idf, query, tf_idf_query, file, distance, currentThread):
	if(len(file) >= 100):
		begin = int(len(file) / 100 *(currentThread - 1))
		end = int((len(file) / 100)*currentThread - 1)
	else:
		begin = int(currentThread - 1)
		end = int(currentThread - 1)
	for filename in range(begin,end + 1):
		dis = 0.0
		distance[file[filename]] = []
		for item in tf_idf:
			if(file[filename] in tf_idf[item]):
				if(item in tf_idf_query):
					dis += (tf_idf[item][file[filename]] - tf_idf_query[item])**2
				else:
					dis += tf_idf[item][file[filename]]**2
			else:
				if(item in tf_idf_query):
					dis += tf_idf_query[item]**2
		distance[file[filename]].append(math.sqrt(dis))

def build_inverted_tf():
	stopwords = stopword("vietnamese-stopwords.txt")

	build_inverted_index("doc2/", stopwords,'title','inverted_index1.txt')
	file = codecs.open('inverted_index1.txt', 'r', 'utf-8')
	iv_title = json.load(file)
	file.close()
	print("success" + 'inverted_index1.txt')
	build_inverted_index("doc2/", stopwords,'content','inverted_index2.txt')
	file = codecs.open('inverted_index2.txt', 'r', 'utf-8')
	iv_content = json.load(file)
	file.close()
	print("success" + 'inverted_index2.txt')
	compute_tf_idf("doc2/", iv_title,'tf_idf1.txt')
	print("success" + 'tf_idf1.txt')
	compute_tf_idf("doc2/", iv_content,'tf_idf2.txt')
	print("success" + 'tf_idf2.txt')

