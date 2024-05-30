import pandas as pd
import pymongo

# CSV 파일 읽기
rental_shop_info_csv = pd.read_csv('data/rental_shop_info.csv', encoding='cp949')

# MongoDB 연결 설정
client = pymongo.MongoClient("mongodb://localhost:27018/")
db_conn = client['cycle']

# 데이터를 저장할 리스트 초기화
rental_shop_info = []

# 데이터 프레임 크기 계산
size = len(rental_shop_info_csv)

# 데이터 파싱 및 리스트에 추가
for i in range(size):
    rental_shop_info.append(
        {
            "rental_shop_id": str(rental_shop_info_csv['대여소_ID'][i]),
            "address1": str(rental_shop_info_csv['주소1'][i]),
            "address2": str(rental_shop_info_csv['주소2'][i]),
            "latitude": float(rental_shop_info_csv['위도'][i]),
            "longitude": float(rental_shop_info_csv['경도'][i])
        }
    )

# MongoDB에 데이터 삽입
db_conn.get_collection("rental_shop_info").insert_many(rental_shop_info)
