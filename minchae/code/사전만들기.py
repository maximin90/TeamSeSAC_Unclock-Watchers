import os
import pandas as pd

# 주어진 폴더 경로
csv_file_path = "C:/Users/minch/OneDrive/바탕 화면/n-gram/ngram_merged.csv"

# CSV 파일을 데이터프레임으로 읽어오기
ngram_df = pd.read_csv(csv_file_path)

# 상승과 하락 데이터 필터링
positive_df = ngram_df[ngram_df['label'] == '상승']
negative_df = ngram_df[ngram_df['label'] == '하락']

# 각 단어의 출현 횟수 계산
positive_counts = positive_df['ngram'].str.split(',').explode().value_counts()
negative_counts = negative_df['ngram'].str.split(',').explode().value_counts()

# 총 n-gram 수
total_positive_ngrams = positive_counts.sum()
total_negative_ngrams = negative_counts.sum()

# 상승 라벨에 대한 n-gram 사전 구성
positive_dictionary = set()
negative_dictionary = set()

# 각 단어에 대한 빈도와 비율 계산
for word in ngram_df['ngram'].str.split(',').explode().unique():
    positive_word_count = positive_counts.get(word, 0)
    negative_word_count = negative_counts.get(word, 0)
    
    positive_word_ratio = positive_word_count / total_positive_ngrams if total_positive_ngrams > 0 else 0
    negative_word_ratio = negative_word_count / total_negative_ngrams if total_negative_ngrams > 0 else 0
    
    ratio_of_word_ratios = positive_word_ratio / 1  # 기준값을 1로 설정
    
    # 상승 라벨에 대한 단어 추가
    if ratio_of_word_ratios >= 1.3:
        positive_dictionary.add(word)
    elif ratio_of_word_ratios <= 0.76:
        negative_dictionary.add(word)

# 결과를 DataFrame으로 나타내기
positive_dictionary_df = pd.DataFrame(list(positive_dictionary), columns=['positive_word'])
negative_dictionary_df = pd.DataFrame(list(negative_dictionary), columns=['negative_word'])

# # 두 DataFrame을 하나로 합치기 
# merged_df = pd.concat([positive_dictionary_df, negative_dictionary_df], axis=1)
# merged_df = positive_dictionary_df  

# 결과를 CSV 파일로 저장
positive_dictionary_df.to_csv("C:/Users/minch/OneDrive/바탕 화면/22positive_dictionary_df.csv", index=False)
negative_dictionary_df.to_csv("C:/Users/minch/OneDrive/바탕 화면/22negative_dictionary_df.csv", index=False)

print(positive_dictionary_df)
print(negative_dictionary_df)