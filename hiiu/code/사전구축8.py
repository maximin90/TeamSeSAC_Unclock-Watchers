import os
import pandas as pd

# 파일 경로 설정
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_name = 'chunk_1.csv'
file_path = os.path.join(desktop_path, file_name)
ngram_df = pd.read_csv(file_path)
print(ngram_df)
# 상승과 하락 데이터 필터링
positive_df = ngram_df[ngram_df['label'] == '상승']
negative_df = ngram_df[ngram_df['label'] == '하락']

# 각 단어의 출현 횟수 계산
positive_counts = positive_df['ngram'].str.split(',').explode().value_counts()
negative_counts = negative_df['ngram'].str.split(',').explode().value_counts()

# 총 n-gram 수
total_positive_ngrams = positive_counts.sum()
total_negative_ngrams = negative_counts.sum()

# 상승과 하락 라벨에 대한 n-gram 사전 구성
positive_dictionary = set()
negative_dictionary = set()

for word in ngram_df['ngram'].str.split(',').explode().unique():
    positive_word_count = positive_counts.get(word, 0)
    negative_word_count = negative_counts.get(word, 0)
    
    positive_word_ratio = positive_word_count / total_positive_ngrams if total_positive_ngrams > 0 else 0
    negative_word_ratio = negative_word_count / total_negative_ngrams if total_negative_ngrams > 0 else 0
    
    ratio_of_word_ratios = positive_word_ratio / negative_word_ratio if negative_word_ratio > 0 else 0
    
    if ratio_of_word_ratios >= 1.3:
        positive_dictionary.add(word)
    if ratio_of_word_ratios <= 0.76:  
        negative_dictionary.add(word)



positive_dictionary_df = pd.DataFrame(list(positive_dictionary), columns=['positive_word'])
negative_dictionary_df = pd.DataFrame(list(negative_dictionary), columns=['negative_word'])

# positive_dictionary_df를 CSV 파일로 저장
positive_dictionary_df.to_csv(os.path.join(desktop_path, 'final_positive.csv'), index=False)

# negative_dictionary_df를 CSV 파일로 저장
negative_dictionary_df.to_csv(os.path.join(desktop_path, 'final_negative.csv'), index=False)

### 작은 부분으로 나누어 읽기### 그냥 하면 메모리 에러 뜹니다ㅜㅜ#########################
chunk_size = int(len(ngram_df) / 10)
chunks = pd.read_csv(file_path, chunksize=chunk_size)

# 저장할 파일 이름 및 경로 설정
output_path = os.path.join(desktop_path, 'chunked_data2')

# 디렉토리가 없다면 생성
if not os.path.exists(output_path):
    os.makedirs(output_path)

# 각 부분을 파일로 저장
for i, chunk in enumerate(chunks):
    chunk.to_csv(os.path.join(output_path, f'chunk_{i + 1}.csv'), index=False)
    print(f'Chunk {i + 1} saved.')

print("Data split and saved successfully.")
