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
	slide_classify = get_file_contents("/home/seko/ntcir11/ntcir_k_data/data/a")
	# print slide_classify[1]#slide_classify[a] a:07-01.align,08-21.align
	# print len(slide_classify)
	print "スライド範囲の取得"

	'スライドの範囲の取得'
	slide_classify_num = []
	slide_range = []
	slide_range_tmp=[]
	for i in range(len(slide_classify)):
		slide_classify_num.append(slide_classify[i].split("\n"))#最後の文も含める
	# print len(slide_classify_num[0][1])
	# print slide_classify_num[0][1]#slide_classify_num[a][b] a:07-01.align,08-21.align b:1 0000,2 0004
	# print slide_classify_num[0][0].split(" ")
	# 'スライドの範囲の取得'
	# slide_classify_num = []
	# slide_range = []
	# slide_classify_tmp = []
	# for di in range(len(slide_classify)):
	# 	for i in range(len(slide_classify[di])):
	# 		slide_classify_tmp.append(slide_classify[di][i].split("\n"))
	# 	slide_classify_num.append(slide_classify_tmp)
	# 	slide_classify_tmp=[]
	# print len(slide_classify_num[0]),len(slide_classify_num[0][0]),len(slide_classify_num[0][0][0])
	# del slide_classify_num[-1わざと最後のリストなしを追加
	for di in range(len(slide_classify_num)):
		for i in range(len(slide_classify_num[di])):
			slide_range_tmp.append(slide_classify_num[di][i].split(" "))
		slide_range.append(slide_range_tmp)
		slide_range_tmp = []
	print "スライドに渡す形に範囲を変換"
	print slide_range[0][1][1]#slide_range[a][b][c] a:07-01.align,08-21.align b:1 0000,2 0004,c:0=左、1＝右
	# # print int(slide_range[35][1]),len(slide_range)
	# for i in range(len(slide_range)):
	# 	print slide_range[i]
	# print len(slide_range),len(slide_range[0])
	'スライドの内容'
	name = []
	date = []
	slide_sentence, name ,date= get_file_name_contents("/home/seko/ntcir11/ntcir_k_data/data/kaldi_file")
	# print date[-1]
	# print len(name[0])
	# print len(slide_sentence[0])
	# print slide_sentence[0][413]
	# if re.search('\d{4}',name[0][2]):
	# 	print re.search('\d{4}',name[0][2]).group(0)"真ん中の部分だけをとる"
	# print slide_sentence[0][1]
	# print name[1][2],name[1][3],name[1][4]
	# # print slide_classify_num[0]
	# print slide_sentence[1][0],slide_sentence[1][1],slide_sentence[1][2]
	# print len(slide_sentence)
	print "スライドの内容を取得"

	# print len(name[i])
#主な分類分け
	slide=[]
	slide_tmp=[]
	punctuation = []#スライドの一文
	pre = 0
	# print "b",len(slide_range)-1,slide_range[35][1]
	'スライド文書の入力'
	for di in range(len(slide_range)):#フォルダの最後
		for i in range(len(slide_range[di])-1):#
			for j in range(len(name[di])):
				# print i,j,slide_range[di][i]

				#最後の部分
				if i == len(slide_range[di])-2:
					if j>=pre and j < len(name[di])-1:
						if space_flag == 1:
							punctuation.append(slide_sentence[di][j].replace(" ",""))
							# print j,"bab",len(name[di])-1
							continue
						
						else:
							punctuation.append(slide_sentence[di][j])
							continue
					elif j>=pre and j== len(name[di])-1:
						# print j,"non"
						# print slide_sentence[di][j]
						punctuation.append(slide_sentence[di][j].replace(" ",""))
						slide_tmp.append(punctuation)#重要な文を入れる
						punctuation=[]
						pre=0
						break;
					else:
						# print "j",j,"pre",pre
						continue

				elif slide_range[di][i+1][1] >= re.search('\d{4}',name[di][j]).group(0) or re.search('\+',slide_range[di][i+1][1]):#この範囲の時に貯めていたものを吐き出す
					slide_tmp.append(punctuation)
					punctuation = []
					pre = j
					break;

				elif (slide_range[di][i+1][1] != re.search('\d{4}',name[di][j]).group(0)) and (j>=pre):#範囲がファイルの名前よりも小さい時に
					if space_flag == 1:
						punctuation.append(slide_sentence[di][j].replace(" ",""))
					else:
						punctuation.append(slide_sentence[di][j])

		slide.append(slide_tmp)
		# print "point_slide"
		# print len(slide_tmp),slide_tmp[0]
		slide_tmp=[]
	# print "slide_num",len(slide)

	print "スライド文書の作成終了"
	for i in range(len(slide)):
		print len(slide[i])
	# for i in range(len(slide[-1][-1])):
		# print slide[-1][-2][i]

# 保存のところ(一度実行したら二度目はKALDI_DATAを消してからにしてください)
	out_num=plus_one_flag
	m=0
	# print len(slide)
	# print len(slide[1][28])
	# print len(slide[0]),len(slide[1]),len(slide[2])
	for di in range(len(slide)):#日付文
		print len(slide[di])
		for i in range(len(slide[di])):#スライド文
			# f.write("{0:03d}".format(out_num))
			for j in range(len(slide[di][i])):#一スライドの中の細かい文
				if len(slide[di][i][j]) == 0: #スライドが空だった場合
					# print i
					continue
				else:
					dir_name = "/home/seko/ntcir11/ntcir_k_data/data/kaldi_data/"+date[m]+"_"+'{0:03d}'.format(out_num)
					f = open(dir_name+"kaldi.txt","aw")
					f.write(str(slide[di][i][j]))
					f.write("\n")
				# print slide[i][j]
			out_num+=1
		out_num=plus_one_flag
		m+=1

	#フォルダを削除する
	remove_none_file("/home/seko/ntcir11/ntcir_k_data/data/kaldi_data/")