
# 라이브러리 불러오기
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select # dropdown 선택을 위해 필수!
import time

def popularity_filter_crawling(couple_name, page):

    # Headless 옵션 지정
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome("C:/work_django/django_mldl/postype_search/cp_search/chromedriver.exe", chrome_options=options)
    # url = 'https://www.postype.com/search?page={}&keyword='+ couple_name +'&period=any_time&sort=popularity&options_title=1&options_sub_title=1&options_content=1&options_tags=1&options_nickname=1'
    url = 'https://www.postype.com/search/index?page={}&sort=popularity&paid=&period=&price_min=100&price_max=50000&options_title=1&options_sub_title=1&options_content=&options_tags=1&options_nickname=1&status=&keyword='+couple_name

    # 데이터프레임을 생성하기 위한 리스트 생성
    title_li=[] # 글 제목
    url_li=[] # 글 URL
    writer_li = [] # 작가 이름
    like_li=[] # 좋아요 수


    # 크롤링 함수 만들기
    for i in range(1, page+1): # 1페이지 크롤링 안되는 문제 해결
        link = url.format(i)
        driver.get(link)

        time.sleep(3)

        html=requests.get(link).content
        soup=BeautifulSoup(html, 'html.parser')
        # print(soup)

        res=soup.find_all('h3', {'class': 'pst-title'}) # 제목 텍스트를 담고 있는 a 태그의 부모 h3 태그 전부 꺼내기
        res2=soup.find_all('div', {'class' : 'pst-action'}) # 좋아요 수를 담은 span 태그를 답고 있는 div 태그 전부 꺼내기
        res3=soup.find_all('div', {'class' : 'pst-blog'})

        for l in res:
            title=l.get_text() # 제목 텍스트 추출
            text_url=l.find('a')['href'] # 글 링크 추출
            title_li.append(title) # 제목 리스트에 추가
            url_li.append(text_url) # 링크 리스트에 추가

        print('{} 페이지 작품 제목 리스트는 {}입니다.'.format(i, title_li))

        for w in res3:
            writer_name=w.find('a').get_text() # a 태그를 찾지 않고 텍스트를 추출할 경우 블로그 이름까지 추출된다
            writer_li.append(writer_name)

        for h in res2:
            like_count = h.find('span', {'class' : 'count'})

            if like_count!=None: # 좋아요가 있는 게시물
                like_count=int(like_count.get_text())
                like_li.append(like_count)

            else: # 좋아요가 없는 게시물
                like_li.append(0) # 0을 추가한다


    # 리스트 값들의 좌우 공백 삭제
    title_li = [t.strip() for t in title_li]
    writer_li=[x.strip() for x in writer_li]

    print('크롤링이 완료되었습니다. 데이터로 저장합니다.')
    driver.quit() # 가상 브라우저 종료

        # 데이터 프레임으로 만들기
    df = pd.DataFrame(data={'title' : title_li,
                            'writer' : writer_li,
                            'url' : url_li,
                           'likes' : like_li})

    writer_data = dict(df['writer'].value_counts())
    top_writer = list(writer_data.keys())
    top3 = top_writer[:3]

    df.to_csv('C:/work_django/django_mldl/postype_search/cp_search/table.csv')

    html_table = df.to_html(index=False, justify='center', escape=False, render_links=True) # 참고 : https://stackoverflow.com/questions/54746027/convert-pandas-dataframe-to-html-table/54746098
    # 링크를 걸어주기 위해서는 render_links 옵션에 반드시 True를 써주어야 한다!! 참고 : https://github.com/pandas-dev/pandas/pull/23715/files/8683d560da7668a29c09922821cafb520e9bb964

    return html_table, top3

# PR이 되어있는 작품의 경우 좋아요 수와 상관없이 맨 앞으로 올라온다.

# def show_popular_writer(writer_name):
