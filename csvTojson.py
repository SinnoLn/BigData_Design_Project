import pandas as pd
import os

def convert_csv_to_json():
    # 파일 번호 범위 설정 (1부터 17까지)
    for i in range(1, 18):
        # CSV 파일 경로 구성
        csv_file_path = f'./file/202403({i}).csv'

        # CSV 파일 읽기
        data = pd.read_csv(csv_file_path, encoding='utf-8')

        # 주소 데이터를 배열과 임베디드 형식으로 구조화
        data['주소'] = data.apply(lambda x: {
            "시도명": x['시도명'],
            "시군구명": x['시군구명'],
            "세부정보": [
                {"법정동명": x['법정동명']},
                {"행정동명": x['행정동명']},
                {"지번주소": x['지번주소']}
            ],
            "도로명": x['도로명'],
            "도로명주소": x['도로명주소']
        }, axis=1)

        # 건물 정보를 배열로 구조화
        data['건물'] = data.apply(lambda x: [
            {"건물명": x['건물명']},
            {"건물본번지": x['건물본번지']},
            {"건물부번지": x['건물부번지']},
            {"건물관리번호": x['건물관리번호']}
        ], axis=1)

        # 상권업종 정보를 배열로 구조화
        data['상권업종'] = data.apply(lambda x: [
            {"분류명": "대분류", "명칭": x['상권업종대분류명'], "코드": x['상권업종대분류코드']},
            {"분류명": "중분류", "명칭": x['상권업종중분류명'], "코드": x['상권업종중분류코드']},
            {"분류명": "소분류", "명칭": x['상권업종소분류명'], "코드": x['상권업종소분류코드']}
        ], axis=1)

        # 위치 정보 구조화
        data['위치'] = data.apply(lambda x: {
            "경도": x['경도'],
            "위도": x['위도']
        }, axis=1)

        # 불필요한 컬럼 제거
        data = data.drop(columns=['시도명', '시군구명', '법정동명', '행정동명', '지번주소', '도로명', '도로명주소',
                                  '건물명', '건물본번지', '건물부번지', '건물관리번호',
                                  '상권업종대분류명', '상권업종중분류명', '상권업종소분류명', '상권업종대분류코드', '상권업종중분류코드', '상권업종소분류코드',
                                  '경도', '위도'])

        # JSON 파일 경로 구성
        json_file_path = f'./file/202403({i}).json'

        # JSON 형식으로 파일에 저장
        data.to_json(json_file_path, orient='records', force_ascii=False)

        # 변환된 파일 확인 메시지
        print(f'Converted {csv_file_path} to {json_file_path}')


if __name__ == "__main__":
    convert_csv_to_json()

# import pandas as pd
# import os
#
# def convert_csv_to_json():
#     # 파일 번호 범위 설정 (1부터 17까지)
#     for i in range(1, 18):
#         # CSV 파일 경로 구성
#         csv_file_path = f'./file/202403({i}).csv'
#
#         # CSV 파일 읽기
#         data = pd.read_csv(csv_file_path, encoding='utf-8')
#
#         # 데이터 구조화
#         data['주소'] = data.apply(lambda x: {
#             "시도명": x['시도명'],
#             "시군구명": x['시군구명'],
#             "행정동명": x['행정동명'],
#             "법정동명": x['법정동명'],
#             "지번주소": x['지번주소'],
#             "도로명": x['도로명'],
#             "도로명주소": x['도로명주소']
#         }, axis=1)
#
#         data['건물'] = data.apply(lambda x: {
#             "건물명": x['건물명'],
#             "건물본번지": x['건물본번지'],
#             "건물부번지": x['건물부번지'],
#             "건물관리번호": x['건물관리번호']
#         }, axis=1)
#
#         data['상권업종'] = data.apply(lambda x: {
#             "대분류명": x['상권업종대분류명'],
#             "중분류명": x['상권업종중분류명'],
#             "소분류명": x['상권업종소분류명'],
#             "대분류코드": x['상권업종대분류코드'],
#             "중분류코드": x['상권업종중분류코드'],
#             "소분류코드": x['상권업종소분류코드']
#         }, axis=1)
#
#         data['위치'] = data.apply(lambda x: {
#             "경도": x['경도'],
#             "위도": x['위도']
#         }, axis=1)
#
#         # 불필요한 컬럼 제거
#         data = data.drop(columns=['시도명', '시군구명', '행정동명', '법정동명', '지번주소', '도로명', '도로명주소',
#                                   '건물명', '건물본번지', '건물부번지', '건물관리번호',
#                                   '상권업종대분류명', '상권업종중분류명', '상권업종소분류명', '상권업종대분류코드', '상권업종중분류코드', '상권업종소분류코드',
#                                   '경도', '위도'])
#
#         # JSON 파일 경로 구성
#         json_file_path = f'./file/202403({i}).json'
#
#         # JSON 형식으로 파일에 저장
#         data.to_json(json_file_path, orient='records', force_ascii=False)
#
#         # 변환된 파일 확인 메시지
#         print(f'Converted {csv_file_path} to {json_file_path}')
#
#
# if __name__ == "__main__":
#     convert_csv_to_json()
