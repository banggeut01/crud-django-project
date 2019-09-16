from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
# from IPython import embed

from .models import Article, Comment

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
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        article = Article.objects.create(title=title, content=content)
        # article = Article.objects.create(title=title, content=content).id
        # context = {
        #     'article': article
        # }
        # return render(request, 'articles/create.html', context)
        # embed()
        return redirect('articles:detail', article.pk)
    else:
        return render(request, 'articles/new.html')

def detail(request, article_pk):
    # 단일 데이터 조회
    article = Article.objects.get(id=article_pk)
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comments': comments
    }
    return render(request, 'articles/detail.html', context)

from django.views.decorators.http import require_POST

@require_POST
def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    # if request.method == 'POST':
    article.delete()    
    return redirect('articles:index')
    # else:
        # return redirect('articles:detail', article.pk)

# def edit(request, article_pk):
#     article = Article.objects.get(pk=article_pk)
#     context = {
#         'article': article
#     }
#     return render(request, 'articles/edit.html', context)

def update(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        article.title = title
        article.content = content
        article.save()
        return redirect('articles:detail', article.pk)
    else:
        context = {
        'article': article
        }
        return render(request, 'articles/edit.html', context)

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
    return redirect('articles:detail', article_pk)    