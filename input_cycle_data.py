import pandas as pd
import pymongo
import time

# MongoDB 연결
client = pymongo.MongoClient("mongodb://localhost:27018")
print(client)

# 데이터베이스 목록 출력
for db in client.list_databases():
    print(db)

# 'cycle' 데이터베이스 연결
db_conn = client.get_database("cycle")
print(db_conn)

# CSV 파일 읽기
csv_file = pd.read_csv('data/cycle_2312.csv', encoding='cp949')

# 행렬 크기 출력
col_size = csv_file.columns.size
print("success")
row_size = len(csv_file)
print("row_size: {}".format(row_size))
print(csv_file.head(10))

# 데이터 수집
cycle_info = []

start_time = time.time()
for i in range(row_size):
    try:
        bike_se_cd = str(csv_file['자전거구분'][i]) if '자전거구분' in csv_file else ""
        rental_info = pd.to_datetime(csv_file['대여일시'][i])
        cycle_info.append(
            {
                "cycle_num": str(csv_file['자전거번호'][i]),
                "rental_date": rental_info,
                "rental_place_num": int(csv_file['대여 대여소번호'][i]),
                "rental_place": str(csv_file['대여 대여소명'][i]),
                "rental_holder": int(csv_file['대여거치대'][i]),
                "return_date": pd.to_datetime(csv_file['반납일시'][i]),
                "return_place_num": str(csv_file['반납대여소번호'][i]),
                "return_place": str(csv_file['반납대여소명'][i]),  # rental -> return
                "return_holder": str(csv_file['반납거치대'][i]),
                "use_time_minute": int(csv_file['이용시간(분)'][i]),
                "use_distance_m": float(csv_file['이용거리(M)'][i]),
                "rental_station_id": str(csv_file['대여대여소ID'][i]),
                "return_station_id": str(csv_file['반납대여소ID'][i]),
                "bike_se_cd": bike_se_cd,
                "user": {
                    "birth_day": str(csv_file['생년'][i]),
                    "sex_cd": str(csv_file['성별'][i]),
                    "usr_cls_cd": str(csv_file['이용자종류'][i]),
                }
            }
        )
    except KeyError as e:
        print(f"KeyError at index {i}: {e}")
    except ValueError as e:
        print(f"ValueError at index {i}: {e}")

# MongoDB에 데이터 삽입
try:
    db_conn.get_collection("rental_info").insert_many(cycle_info)
    print("Data inserted successfully")
except pymongo.errors.BulkWriteError as e:
    print(f"BulkWriteError: {e.details}")

end_time = time.time()
duration = (end_time - start_time) / 60
print("success")
print("row size: {}".format(row_size))
print("{}분".format(duration))


# count = 0
# for i in range(row_size):
#     rental_info = str(csv_file['대여일시'][i]).startswith("2323")
#     if rental_info:
#         count += 1
#         print(i)
# print(count)

# print(csv_file['대여일시'][4151127])
# csv_file['대여일시'][4151127] = '2023-06-23 21:27:01'
# print(csv_file['대여일시'][4151127])
