import pandas as pd
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.util import ngrams
import time

# 바탕화면에 있는 CSV 파일 경로
csv_file_path = "C:/Users/minch/OneDrive/바탕 화면/라벨링/인터뷰_data_df.csv"



# CSV 파일을 데이터프레임으로 읽어오기
data_df = pd.read_csv(csv_file_path)


# # 'Unnamed' 컬럼 삭제
# data_df = data_df.drop(columns=['Unnamed: 0'])

# # 'label'이 "동결"제외
# filtered_df = data_df[data_df['label'] != '동결']

# 'Text' 열의 각 행에 대해 1부터 5까지의 n-gram 생성
ngram_list = []
for idx, row in data_df.iterrows():
    text_tokens = eval(row['Text'])
    n_grams = text_tokens.copy()
    for n in range(2, 6):  # 2부터 3까지의 n-gram 생성
        n_grams += [':'.join(i) for i in list(ngrams(text_tokens, n))]
    ngram_list.append({'index': idx, 'ngram': ','.join(n_grams)})

# 생성된 n-gram 데이터프레임 만들기
ngram_df = pd.DataFrame(ngram_list)

# 파일 저장하기
ngram_df.to_csv('C:/Users/minch/OneDrive/바탕 화면/n-gram/인터뷰_n_gram.csv')

print(ngram_df)