from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from IPython import embed
from django.contrib import messages # message framwork
from .models import Article, Comment
from .forms import ArticleForm

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-id') # 최신글 위로 오도록
    context = {
        'articles': articles
    }
    # embed()
    return render(request, 'articles/index.html', context)

# def new(request):
#     return render(request, 'articles/new.html')

def create(request):
    # POST 요청 -> 검증 및 저장
    if request.method == 'POST':
        article_form = ArticleForm(request.POST) # request.POST 사용자가 입력한 내용
        # embed()
        # 검증에 성공하면 저장하고,
        if article_form.is_valid(): # 중요한 로직!
            # title = article_form.cleaned_data.get('title')
            # content = article_form.cleaned_data.get('content')
            # article = Article(title=title, content=content)
            # article.save()
            article = article_form.save()
            # redirect
            return redirect('articles:detail', article.pk)
        # else:
        #   다시 폼으로 돌아가 -> 중복되서 제거!
    # GET 요청이면
    else:
        # Form으로 돌아가기
        article_form = ArticleForm()
    # GET -> 비어있는 Form context
    # POST -> 검증 실패시 에러메시지와 입력값 채워진 context
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)

def detail(request, article_pk):
    # 단일 데이터 조회
    article = get_object_or_404(Article, pk=article_pk) # 없으면 404 에러, 안해주면 500error가 뜬다.
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comments': comments
    }
    return render(request, 'articles/detail.html', context)

@require_POST
def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    article.delete()    
    return redirect('articles:index')

def update(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'POST': # 수정한 내용 저장할 때 POST
        article_form = ArticleForm(request.POST, instance=article) # 수정하려는 인스턴스 - article 넣어주기!
        if article_form.is_valid():
            article = article_form.save()
            return redirect('articles:detail', article.pk)
    else: # 수정버튼 눌렀을 때 수정화면으로 가는 것 GET
        article_form = ArticleForm(instance=article) # 수정하려는 인스턴스 넣어주기!
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)

@require_POST # POST로 넘어왔을 때만 실행!, import해주기 
def comment_create(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    # comment = Comment() => import 주의!
    # comment.content = request.POST.get('content')

    # comment.article = article => 안하면 error
    # or comment.article_id = article_pk

    # comment.save()
    content = request.POST.get('content')
    Comment.objects.create(content=content, article_id=article_pk)
    return redirect('articles:detail', article_pk)

@require_POST 
# 인자 3개 일 때 : (request, comment_pk, article_pk)
def comment_delete(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    article_pk = comment.article_id
    comment.delete()
    # 길게
    # messages.add_message(request, messages.INFO, '댓글이 삭제되었습니다.')
    # 짧게
    messages.info(request, '댓글이 삭제되었습니다.')
    return redirect('articles:detail', article_pk)    