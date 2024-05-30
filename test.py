from pymongo import MongoClient
import json
from bson.json_util import dumps

# MongoDB 서버에 연결
client = MongoClient('mongodb://localhost:27017/')

# 'test' 데이터베이스 연결
db = client['test']

# 'project' 컬렉션 연결
collection = db['project']

# MongoDB 쿼리 실행
results = collection.find({"주소.시도명": "제주특별자치도", "상권업종": {"$elemMatch": {"분류명": "대분류", "명칭": "음식"}}})

# 결과를 보기 좋게 출력 (bson.json_util.dumps를 사용)
for result in results:
    print(dumps(result, indent=4, ensure_ascii=False))
