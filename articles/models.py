from django.db import models
# Crud 구성요소 (1) model: 데이터베이스 모델링 할 수 있는 공간



# Create your models here.
# 1. 모델(스키마) 정의
# db 테이블을 정의하고,
# 각각의 컬럼(필드) 정의
class Article(models.Model):
    # id : integer 자동으로 정의(Primary Key)
    # id = models.AutoField(primary_key=True) -> Integer 값이 자동으로 하나씩 증가(AUTOINCREMENT)
    # CharField - 필수인자로 max_lengh 지정
    title = models.CharField(max_length=10)
    content = models.TextField()
    # DateTimeField
    #   auto_now_add : 생성시 자동으로 입력
    #   auto_not : 수정시마다 자동으로 저장
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'<{self.id}> {self.title}'

# models.py : python 클래스 정의
#           : 모델 설계도
# makemigrations : migration 파일 생성
#                : DB 설계도
# migrate : migration 파일 DB 반영

class Comment(models.Model):
    content = models.CharField(max_length=140)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

