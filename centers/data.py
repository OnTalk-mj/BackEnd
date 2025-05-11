import csv
from .models import CounselingCenter

def import_data():
    with open('teenCenter.csv', encoding='euc-kr') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            CounselingCenter.objects.create(
                region=row['지역'],
                name=row['센터명'],
                category=row['카테고리'] if '카테고리' in row else '',
                address=row['주소'],
                phone=row['전화번호_1'],
                website=row['홈페이지'] if row['홈페이지'] != '' else None,
                latitude=None,
                longitude=None
            )