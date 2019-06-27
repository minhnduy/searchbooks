from bs4 import BeautifulSoup
import requests
import codecs
import os
import json



def createDocFile(responseText,fileName):
	
		dataArray = json.loads(responseText)

		currentFileName = fileName

		for item in dataArray:

			
			title = item['title']
			author = BeautifulSoup(item['authorValue'],'html.parser').getText()
			description = BeautifulSoup(item['description'],'html.parser').getText()
			content = author  + ' '+ title + ' ' + description


		

			jsonObject = {}

			jsonObject["title"] = title
			jsonObject["content"] = title +" "+content

			if 'link' in item:
				jsonObject["detailLink"] = item['link']
			if 'detaillink' in item:
				jsonObject["detailLink"] = item['detaillink']
			if 'readlink' in item:
				jsonObject["detailLink"] = item['readlink']
			
			jsonObject["thumpnail"] = item['thumb']

			fileContent = json.dumps(jsonObject,  ensure_ascii=False)
	

			file = codecs.open("doc2/" + str(currentFileName) + ".json", "w", "utf-8")
			file.write(fileContent)
			file.close()	
			currentFileName = currentFileName + 1
		
		return currentFileName 
def bookCrawler():

	fileName = 100000
	categoryList = [69,35,176,79,73,138,71,92,141,144,45]

	for categoryId in categoryList:

		init = True
		pageNum = 1
		
		while(init):

			url = 'https://waka.vn/data/book-in-category?id='+str(categoryId)+'&limit=50&cid=0&page='+str(pageNum)+'&is_paginate=0'
			response = requests.get(url)

			print(url)
			print(str(fileName))
			if(response.status_code == 200):
				if(response.text != '[]'):
					currentFileName = createDocFile(response.text,fileName)
					pageNum = pageNum + 1
					fileName = currentFileName
					
				else:
					init = False
			
			



