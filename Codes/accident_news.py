import requests
from bs4 import BeautifulSoup
import csv

soup_objects = []

for d in range(20200817,20200818):
    for p in range(1,31):
        list_url = f'https://news.naver.com/main/list.nhn?mode=LS2D&sid2=249&mid=shm&sid1=102&date={d}&page={p}'

        response = requests.get(list_url)
        # # print(response.text)

        soup_objects.append(BeautifulSoup(response.text, 'html.parser'))

        # if BeautifulSoup(response.text, 'html.parser') not in soup_objects:
        #     soup_objects.append(BeautifulSoup(response.text, 'html.parser'))

# print(soup_objects)
# print(len(soup_objects))

news_data = []

for soup in soup_objects:
    page_news = soup.select('#main_content .list_body.newsflash_body a')
    # print(each_news)

    news_data_schema = {'news_title':'', 'news_content':''}

    for news in page_news:
        if news.string == None:
            continue
        # print('title : ' + str.strip(news.string))
        news_data_schema['news_title'] = str.strip(news.string)
        # print(news.attrs)
        # print('link : ' + news.attrs['href'] + '\n')
        
        each_news = requests.get(news.attrs['href'])
        soup_content = BeautifulSoup(each_news.text, 'html.parser')
        content = soup_content.select_one('#articleBodyContents')
        # print('content : ' + content.text)
        news_data_schema['news_content'] = content.text
        print(news_data_schema, '\n')

        # with open('./naver_accident_news.csv', 'a') as csvfile:
        #     fieldnames = ['news_title', 'news_content']
        #     csv_writer = csv.DicWriter(csvfile, fieldnames=fieldnames)
        #     csv_writer.writerow(news_data_schema)

        #     print(news_data_schema, '\n')