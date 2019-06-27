import os
import codecs
import chardet


def changeEncoding(filename, newFilename, encoding_from, encoding_to='UTF-8'):
    with open(filename, 'r', encoding = encoding_from) as fr:
        with open(newFilename, 'w', encoding = encoding_to) as fw:
            for line in fr:
                fw.write(line[:-1]+'\r\n')

path = "./news_dataset/"
result_path = "./result/"
files = os.listdir(path)

for file in files:
	file1 = open(path + file, "rb")
	content = file1.read()
	file1.close()
	a = chardet.detect(content)
	start = a["encoding"]
	begin = path + file
	result = result_path + file
	changeEncoding(begin, result, start)