import pandas as pd

# CSV 파일 읽기
broken_info_csv = pd.read_csv('data/broken_info_2311-12.csv', encoding='cp949')

# CSV 파일의 열 이름 출력
print(broken_info_csv.columns)
