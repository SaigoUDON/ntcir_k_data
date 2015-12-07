#-*- coding: utf-8 -*-
import os
import re
def get_file_contents(path):
	files = os.listdir(path)
	doc = []
	for i in sorted(files):
		f = open(path+"/"+i,'r')#""でそのフォルダの中を探せでiでファイルを指定
		doc.append(f.read())

	return doc

def get_name_contents(path):
	files = os.listdir(path)
	name = []
	for i in sorted(files):
		name.append(i)
	return name

def get_file_name_contents(path):
	files = os.listdir(path)
	doc = []
	neme = []
	date = []
	dir_name = []
	for i in sorted(files):
		dir_name.append(i)
		doc.append(get_file_contents(path+"/"+i))
		name.append(get_name_contents(path+"/"+i))
		date.append(i)
	return doc,name,date

def remove_none_file(path):
	files = os.listdir(path)
	for i in sorted(files):
		if len(i) == 0:
			os.remove(path+"/"+i)


###################################################################################main文
if __name__=="__main__":
	space_flag = 1 #テキストの空白を消すフラグ
	plus_one_flag = 0 #テキストを1からにするか0からにするか立てるフラグ
	f = open("test.txt","w")

	'スライドがどこまでか書く'
	slide_classify = get_file_contents("/home/seko/ntcir11/data/a1")
	# print slide_classify
	
	'スライドの範囲の取得'
	slide_classify_num = []
	slide_range = []
	for i in range(len(slide_classify)):
		slide_classify_num = slide_classify[i].split("\n")#最後の文も含める
		print len(slide_classify_num)
		print slide_classify_num[0][1]
	# del slide_classify_num[-1わざと最後のリストなしを追加
	for i in range(len(slide_classify_num)):
		slide_range.append(slide_classify_num[i].split(" "))
	# print int(slide_range[35][1]),len(slide_range)
	# for i in range(len(slide_range)):
	# 	print slide_range[i]
	'スライドの内容'
	name = []
	date = []
	slide_sentence, name ,date= get_file_name_contents("/home/seko/ntcir11/data/kaldi_file1")
	# print date[-1]
	# print len(name[0])
	# print len(slide_sentence[0])
	# print slide_sentence[0][413]
	# if re.search('\d{4}',name[0][2]):
	# 	print re.search('\d{4}',name[0][2]).group(0)"真ん中の部分だけをとる"
	# print slide_sentence[0][1]
	print name[0][2],name[0][3],name[0][4]
	# print slide_classify_num[0]

	slide=[]
	punctuation = []#スライドの一文
	pre = 0
	# print "b",len(slide_range)-1,slide_range[35][1]
	print "name",len(name),"name[0]",len(name[0]),"slide_range",len(slide_range),"slide_range[0]",slide_range[0]
	'スライド文書の入力'
	for i in range(len(slide_range)-1):
		for j in range(len(name[0])):
			# print i,j,slide_range[i]
			if i == len(slide_range)-2:
				if j>=pre and j < len(name[0])-1:
					if space_flag == 1:
						punctuation.append(slide_sentence[0][j].replace(" ",""))
						print j,"bab",len(name[0])-1
						continue
					else:
						punctuation.append(slide_sentence[0][j])
						continue
				elif j>=pre and j== len(name[0])-1:
					print j,"non"
					print slide_sentence[0][j]
					punctuation.append(slide_sentence[0][j].replace(" ",""))
					slide.append(punctuation)
					punctuation=[]
					pre=0
					break;
				else:
					# print "j",j,"pre",pre
					continue
			elif slide_range[i+1][1] == re.search('\d{4}',name[0][j]).group(0) or re.search('\+',slide_range[i+1][1]):#この範囲の時に貯めていたものを吐き出す
				slide.append(punctuation)
				punctuation = []
				pre = j
				break;
			elif (slide_range[i+1][1] != re.search('\d{4}',name[0][j]).group(0)) and (j>=pre):#範囲がファイルの名前よりも小さい時に
				if space_flag == 1:
					punctuation.append(slide_sentence[0][j].replace(" ",""))
				else:
					punctuation.append(slide_sentence[0][j])

#保存のところ(一度実行したら二度目はKALDI_DATAを消してからにしてください)
	out_num=plus_one_flag
	for i in range(len(slide)):
		# f.write("{0:03d}".format(out_num))
		for j in range(len(slide[i])):
			if len(slide[i][j]) == 0:
				print i
				break
			else:
				dir_name = "/home/seko/ntcir11/program/kaldi_data/"+'{0:03d}'.format(out_num)
				f = open(dir_name+".txt","aw")
				f.write(slide[i][j])
			# print slide[i][j]
		out_num+=1

#フォルダを削除する
	remove_none_file("/home/seko/ntcir11/program/kaldi_data/")