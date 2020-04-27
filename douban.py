import requests
from bs4 import BeautifulSoup
import re
import jieba
import pandas as pd
import numpy as np
from PIL import Image
from wordcloud import WordCloud,ImageColorGenerator

#Crawl the movie review
def get_Comment():
	##The big list to store every page of data
	commentList = []
	headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
	for i in range(10):
		url = 'https://movie.douban.com/subject/26794435/comments?start='+ str(i*20) + '&limit=20&sort=new_score&status=P'

		resp = requests.get(url,headers=headers)
		html = resp.text
		#print(html)
		soup = BeautifulSoup(html,'html.parser')

		comment_div = soup.find_all('div',class_='comment')
		comment_list = []
		f = open('test1.txt','a',encoding='UTF-8')
		for item in comment_div:
			if item.find_all('p')[0].text is not None:
				comment_list.append(item.find_all('p')[0].text)
				f.write(item.find_all('p')[0].text)
		f.close()
		commentList.append(comment_list)
		#print(comment_list)
	return commentList

commentList = get_Comment()
comments = ''
# 将列表中的数据转换为字符串
for k in range(len(commentList)):
	comments = comments+(str(commentList[k])).strip()

# 使用正则表达式去除标点符号(Only Chinese)
pattern = re.compile(r'[\u4e00-\u9fa5]+')
filterdata = re.findall(pattern,comments)
#将字符串数组逐个拼接成一个纯文本
cleaned_comments = ''.join(filterdata)
segment = jieba.lcut(cleaned_comments)
#print(segment)

word_df = pd.DataFrame({'segment':segment})
#去掉停用词
stopwords = pd.read_csv("cn_stopwords.txt",index_col=False,quoting=3,sep='t',names=['stopwords'],encoding='utf-8')
word_df = word_df[~word_df.segment.isin(stopwords.stopwords)]

#统计词频
words_stst = word_df.groupby(by=['segment'])['segment'].agg({'Count':np.size})
#将统计好的词频降序排列
words_stst = words_stst.reset_index().sort_values(by=['Count'],ascending=False)

#通过图片处理背景
mask = np.array(Image.open('./sponge.jpeg'))

#配置词云参数
word_cloud = WordCloud(font_path='Arial Unicode.ttf',mask=mask,background_color='white',max_font_size=80,random_state=30)

#把词频转变为字典
word_fre = {x[0]:x[1] for x in words_stst.values}
print(word_fre)

#加载词云字典
word_cloud = word_cloud.fit_words(word_fre)
#基于图像颜色调整目标颜色
image_color = ImageColorGenerator(mask)
word_cloud.recolor(color_func=image_color)

#形成图片
image_result = word_cloud.to_image()
#展示图片
image_result.show()































