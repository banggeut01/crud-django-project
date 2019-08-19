# Crud Django Project

* 가상환경 생성/실행

* `.gitignore`

* git init

* django 설치

* requirments.txt 설청

```bash
$ pip freeze > requirements.txt
```

지금 상태 `requirements.txt`에 저장

```
Django==2.2.4
pytz==2019.2
sqlparse==0.3.0
```

다른 가상환경에서 패키지를 깔아줌

버전 기록

협업시 활용!



추후 pip install -r requirements.txt설치

```bash
$ pip install -r requirments.txt
```

`requirements.txt`에 있는 내용 설치해줌

======================================================================

```bash
$ django-admin startproject crud .
```

* model 정의

  1. models.py(스키마)

     [소스보기 models.py](./articles/models.py)

```python
from django.db import models

# Create your models here.
# 1. 모델(스키마) 정의
# db 테이블을 정의하고,
# 각각의 컬럼(필드) 정의
class Article(models.Model):
    # CharField - 필수인자로 max_lengh 지정
    title = models.CharField(max_length=10)
    content = models.TextField()
    # DateTimeField
    #   auto_now_add : 생성시 자동으로 입력
    #   auto_not : 수정시마다 자동으로 저장
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

2. makemigrations(마이그레이션 파일 생성)

```bash
$ python manage.py makemigrations
```

3. migrate(db반영)

```bash
$ python manage.py migrate
```



* ipython 설치

  ```bash
  # django 명령어 쳐볼수있음
  $ pip install ipython
  $ python manage.py shell
  ```

  ```shell
  In [1]: from articles.models import Article
  
  # 인스턴스 만들기
  In [2]: article = Article()
  
  # object 만들기
  In [3]: article
  Out[3]: <Article: Article object (None)>
  ```

  ```shell
  # 객체 조작만으로 DB에 데이터 삽입하기
  # 첫번째 방법
  In [5]: article.title = '1번 글'
  
  In [6]: article.content = '1번 내용'
  
  In [7]: article.save()
  
  # a2
  In [8]: a2 = Article()
  
  In [9]: a2.title = '2번 글'
  
  In [10]: a2.content = '2번 내용'
  
  In [11]: a2.save()
  
  # 두번째방법
  # a3
  In [12]: article.content = '1번 내용'
  
  In [13]: article.save()
  
  In [14]: a3 = Article(title='제목', content='내용')
  
  # db에 저장전이기 때문에 id값이 None이다.
  In [15]: a3
  Out[15]: <Article: Article object (None)>
  
  In [16]: a3.save()
  
  # db에 저장 후, id 값이 3으로 바뀌었다.
  In [17]: a3
  Out[17]: <Article: Article object (3)>
  
  # 레코드 하나하나 객체로 가져오기
  In [18]: Article.objects.all()
  Out[18]: <QuerySet [<Article: Article object (1)>, <Article: Article object (2)>, <Article: Article object (3)>]>
  
  # 레코드 가져오기
  In [22]: articles = Article.objects.all()
  
  In [23]: for article in articles:
      ...:     print(article.title)
      ...: 
  1번 글
  2번 글
  제목
  
  # 세번째 방법
  # save() 없이 바로 만들어 저장
  In [24]: Article.objects.create(title='제목4', content='내용4')
  Out[24]: <Article: Article object (4)>
  ```

  ```shell
  # 데이터 변경하기
  
  In [25]: Article.objects.all()
  Out[25]: <QuerySet [<Article: Article object (1)>, <Article: Article object (2)>, <Article: Article object (3)>, <Article: Article object (4)>]>
  
  # 값 1개만 가져오기
  In [26]: Article.objects.all()[0]
  Out[26]: <Article: Article object (1)>
  
  # id(key)로 가져오기
  In [27]: Article.objects.get(pk=1)
  Out[27]: <Article: Article object (1)>
  
  In [28]: article = Article.objects.get(pk=3)
  
  In [29]: article.id
  Out[29]: 3
  
  In [30]: article.title
  Out[30]: '제목'
  
  In [31]: article.created_at
  Out[31]: datetime.datetime(2019, 8, 19, 1, 40, 49, 364595, tzinfo=<UTC>)
  
  In [32]: article.pk
  Out[32]: 3
  
  # 값 변경
  In [33]: article.title = '제목3'
  
  In [34]: article.title
  Out[34]: '제목3'
  
  In [35]: article.content
  Out[35]: '내용'
  
  In [36]: article.content = '내용3'
  
  In [37]: article.content
  Out[37]: '내용3'
  
  # db에 저장하기
  In [38]: article.save()
  ```

  ```shell
  # db에서 삭제하기
  In [40]: article = Article.objects.get(pk=4)
  
  In [41]: article
  Out[41]: <Article: Article object (4)>
  
  In [43]: article.delete()
  Out[43]: (1, {'articles.Article': 1})
  
  # id값이 None으로 바뀌었다.
  In [44]: article
  Out[44]: <Article: Article object (None)>
  
  # save()하지 않아도 바로 db에 반영됨!
  ```

  ```bash
  In [46]: Article.objects.create(title='test', content='text')
  Out[46]: <Article: Article object (5)>
  
  In [47]: Article.objects.create(title='test', content='text')
  Out[47]: <Article: Article object (6)>
  ```

  ```shell
  # filter
  In [49]: articles = Article.objects.filter(title='test')
  
  # QuerySet 형태로 가져옴
  In [50]: articles
  Out[50]: <QuerySet [<Article: Article object (5)>, <Article: Article object (6)>]>
  ```

  ```shell
  # filter vs get
  # filter : 일치하는 것이 하나더라도 QuerySet라는 리스트 리턴
  In [52]: Article.objects.filter(id=3)
  Out[52]: <QuerySet [<Article: Article object (3)>]>
  
  # 결과가 없을 때, 빈 리스트 리턴
  In [54]: Article.objects.get(title='test')
  
  
  # get : 무조건 object 리턴, 반드시 고유한 값이여야함!
  In [53]: Article.objects.get(id=3)
  Out[53]: <Article: Article object (3)>
  
  # 결과가 여러가지 레코드 일 때!
  In [54]: Article.objects.get(title='test')
  MultipleObjectsReturned: get() returned more than one Article -- it returned 2!
  ```

  ```shell
  # 인덱스로 레코드 가져오기
  In [56]: Article.objects.all()[0]
  Out[56]: <Article: Article object (1)>
  
  # first(), last()
  In [57]: Article.objects.all().first()
  Out[57]: <Article: Article object (1)>
  
  In [58]: Article.objects.all().last()
  Out[58]: <Article: Article object (6)>
  
  In [60]: Article.objects.all()[3]
  Out[60]: <Article: Article object (5)>
  
  # list slicing 처럼
  In [61]: Article.objects.all()[:3]
  Out[61]: <QuerySet [<Article: Article object (1)>, <Article: Article object (2)>, <Article: Article object (3)>]>
  
  
  ```

  ```shell
  # query
  In [62]: Article.objects.all()[:3].query
  Out[62]: <django.db.models.sql.query.Query at 0x2b3d1e6c048>
  
  In [63]: print(Article.objects.all()[:3].query)
  SELECT "articles_article"."id", "articles_article"."title", "articles_article"."content", "articles_article"."created_at", "articles_article"."updated_at" FROM "articles_article"  LIMIT 3
  
  # title에 제목이 포함된 레코드 검색 쿼리
  In [64]: a = Article.objects.filter(title__contains='제목')
  
  In [65]: print(a.query)
  SELECT "articles_article"."id", "articles_article"."title", "articles_article"."content", "articles_article"."created_at", "articles_article"."updated_at" FROM "articles_article" WHERE "articles_article"."title" LIKE %제목% ESCAPE '\'
  ```

  ```shell
  # ~ 포함
  In [75]: a = Article.objects.filter(content__contains='내용')
  
  In [76]: a
  Out[76]: <QuerySet [<Article: Article object (1)>, <Article: Article object (2)>, <Article: Article object (3)>]>
  
  # ~로 시작하는,
  In [77]: a = Article.objects.filter(content__startswith='내용')
  
  In [78]: a
  Out[78]: <QuerySet [<Article: Article object (3)>]>
  
  # ~로 끝나는,
  In [79]: a = Article.objects.filter(content__endswith='내용')
  
  In [80]: a
  Out[80]: <QuerySet [<Article: Article object (1)>, <Article: Article object (2)>]>
  
  # type은 query
  In [81]: print(type(a.query))
  <class 'django.db.models.sql.query.Query'>
  ```

  ```shell
  # shell 종료
  Ctrl + D
  ```

  ```bash
  # models.py
  #...(중략)
  username = models.CharField(max_length=10)
  #...
  ```

  `username` 스키마에 추가해주었다.

  ```bash
  # 설계도 
  $ python manage.py makemigrations
  You are trying to add a non-nullable field 'username' to article without a default; we can't do that (the database needs something to populate existing rows).
  Please select a fix:
   1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
   2) Quit, and let me add a default in models.py
  Select an option: 1
  Please enter the default value now, as valid Python
  The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
  Type 'exit' to exit this prompt
  >>> '홍길동'
  Migrations for 'articles':
    articles\migrations\0002_article_username.py
      - Add field username to article
  (venv)
  ```

  ```bash
  # 설계도 반영
  $ python manage.py migrate
  Operations to perform:
    Apply all migrations: admin, articles, auth, contenttypes, sessions
  Running migrations:
    Applying articles.0002_article_username... OK
  (venv)
  student@DESKTOP MINGW64 ~/Desktop/지니짱/web/crud-django-project (master)
  
  # migration 보기
  $ python manage.py showmigrations
  admin
   [X] 0001_initial
   [X] 0002_logentry_remove_auto_add
   [X] 0003_logentry_add_action_flag_choices
  articles
   [X] 0001_initial
   [X] 0002_article_username
  auth
   [X] 0001_initial
   [X] 0002_alter_permission_name_max_length
   [X] 0003_alter_user_email_max_length
   [X] 0004_alter_user_username_opts
   [X] 0005_alter_user_last_login_null
   [X] 0006_require_contenttypes_0002
   [X] 0007_alter_validators_add_error_messages
   [X] 0008_alter_user_username_max_length
   [X] 0009_alter_user_last_name_max_length
   [X] 0010_alter_group_name_max_length
   [X] 0011_update_proxy_permissions
  contenttypes
   [X] 0001_initial
   [X] 0002_remove_content_type_name
  sessions
   [X] 0001_initial
  (venv)
  student@DESKTOP MINGW64 ~/Desktop/지니짱/web/crud-django-project (master)
  $
  ```



* superuser 만들어 관리하기

  ```bash
  $ python manage.py makemigrations
  $ python manage.py migrate
  $ python manage.py createsuperuser
  ```

  ```python
  # admin.py
  from django.contrib import admin
  
  # Register your models here.
  from .models import Article
  
  admin.site.register(Article)
  ```

  ```bash
  $ python manage.py runserver
  ```

  ```
  browser에서
  http://127.0.0.1:8000/admin/ 접속
  ```

  

## 데이터베이스

* RDBMS(관계형데이터베이스 관리 시스템)
  * 컬럼(속성)과 데이터값(레코트)으로 구조화
  * SQLite: 가벼운 데이터베이스
    * 임베디드에서 많이 쓰임

* 구성요소
  * 개체
  * 속성
  * 개체 사이의 관계
* 스키마
  * 데이터베이스의 구조와 제약조건(자료의 구조, 표현 방법, 관계 등) 정의
* **Key**
  * PK(Primary Key)
* **ORM(Object-Relational Mapper)**
  * 객체 지향 프로그래밍 언어를 사용해 호환되지 않는 유형의 시스템(django-sqlite)간 데이터 변환