import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import csv
import os
import pandas as pd


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

# data_list = []

# 625페이지부터 1페이지까지 역순으로 크롤링
for page_number in range(124,200,1):
    print(page_number)
    URL = f'https://thehill.com/page/{page_number}/?s=interest+rate&submit=Search&order=desc&orderby=date'

# URL = 'https://thehill.com/page/619/?s=interest+rate&submit=Search&order=desc&orderby=date'


    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    news = soup.select('div.featured-cards__full__content h1 a')

    data_list = []

    # 2번째부터 8번째 기사까지 크롤링

    for i in range(16,8,-1):

        try:

            current_news_url = news[i].get('href')

            current_news_response = requests.get(current_news_url, headers=headers)
            if current_news_response.status_code == 404:
                print(f"404 에러: {current_news_url}")
                continue
            current_news_response.raise_for_status()
       
            current_news_soup = BeautifulSoup(current_news_response.text, 'html.parser')

            
            # 뉴스 제목 추출
            news_title = current_news_soup.select_one('h1').text.strip()

            # 기사 날짜 추출
            date = current_news_soup.find('section', class_='article__header').find('span').text.strip()
            date_string = date

            # 정규 표현식을 사용하여 월/일/년 부분 추출
            date_pattern = r'(\d{2}/\d{2}/\d{2})'  # MM/DD/YY 형식의 날짜를 추출
            match = re.search(date_pattern, date_string)

            if match:
                extracted_date = match.group(1)  # 첫 번째 그룹을 추출 (날짜 부분)
                formatted_date = datetime.strptime(extracted_date, "%m/%d/%y").strftime("%Y-%m-%d")
                print("Date:", formatted_date)

            # 뉴스 기사 내용 추출
            news_content = current_news_soup.select_one('div.article__text').text.strip()

            # 결과 출력 또는 다른 작업 수행
            print('')
            print(f"날짜: {formatted_date}")
            print(f"제목: {news_title}")
            print(f"내용: {news_content}")
            print("-"*100)
            print('')

            data_list.append([formatted_date, news_title, news_content])

            time.sleep(5)

        except AttributeError as e:
            print(f'에러 발생: {e}')
            print(f"{i}번째 기사를 처리하는 중 오류가 발생했습니다. 다음 기사로 이동합니다.")
            

    # 1분 동안 대기
    print("Sleeping for 1 minutes...")
    time.sleep(1 * 60)



    # 9~16개까지 크롤링
    for i in range(8,0,-1):
        try:

            current_news_url = news[i].get('href')
            current_news_response = requests.get(current_news_url, headers=headers)
            current_news_soup = BeautifulSoup(current_news_response.text, 'html.parser')

            # 뉴스 제목 추출
            news_title = current_news_soup.select_one('h1').text.strip()

            # 기사 날짜 추출
            date = current_news_soup.find('section', class_='article__header').find('span').text.strip()
            date_string = date

            # 정규 표현식을 사용하여 월/일/년 부분 추출
            date_pattern = r'(\d{2}/\d{2}/\d{2})'  # MM/DD/YY 형식의 날짜를 추출
            match = re.search(date_pattern, date_string)

            if match:
                extracted_date = match.group(1)  # 첫 번째 그룹을 추출 (날짜 부분)
                formatted_date = datetime.strptime(extracted_date, "%m/%d/%y").strftime("%Y-%m-%d")
                print("Date:", formatted_date)

            # 뉴스 기사 내용 추출
            news_content = current_news_soup.select_one('div.article__text').text.strip()

            # 결과 출력 또는 다른 작업 수행
            print('')
            print(f"날짜: {formatted_date}")
            print(f"제목: {news_title}")
            print(f"내용: {news_content}")
            print("-"*100)
            print('')

            data_list.append([formatted_date, news_title, news_content])

            time.sleep(5)

        except AttributeError as e:
            print(f'에러 발생: {e}')
            print(f"{i}번째 기사를 처리하는 중 오류가 발생했습니다. 다음 기사로 이동합니다.")


    # 전체 데이터를 DataFrame으로 변환
    df = pd.DataFrame(data_list, columns=['Date', 'Title', 'Contents'])

    # 결과를 CSV 파일로 저장
    csv_file_path = f'./The Hill/news_page_{page_number}.csv'
    df.to_csv(csv_file_path, index=False, encoding='utf-8')

    print(f'페이지 {page_number} 데이터가 {csv_file_path}에 저장되었습니다.')
    print('==============================================저장완료==============================================')

print("Sleeping for 1 minutes...")
time.sleep(1 * 60)
print('----------------end--------------')