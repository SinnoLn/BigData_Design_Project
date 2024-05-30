import pandas as pd
import pymongo
from datetime import datetime

# CSV 파일 읽기
broken_info_csv = pd.read_csv('data/broken_info_2311-12.csv', encoding='cp949')

# MongoDB 연결 설정
client = pymongo.MongoClient("mongodb://localhost:27018/")
db_conn = client['cycle']

# 데이터를 저장할 리스트 초기화
broken_info = []

# 데이터 프레임 크기 계산
size = len(broken_info_csv)

# 데이터 파싱 및 리스트에 추가
for i in range(size):
    broken_info.append(
        {
            "bike_no": str(broken_info_csv['자전거번호'][i]),
            "reg_date": pd.to_datetime(broken_info_csv['등록일시'][i]),
            "breakdown_type": str(broken_info_csv['고장구분'][i])
        }
    )

# MongoDB에 데이터 삽입
db_conn.get_collection("broken_info").insert_many(broken_info)
