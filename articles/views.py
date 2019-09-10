from django.shortcuts import render, redirect
from .models import Article

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-id') # 최신글 위로 오도록
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

def new(request):
    return render(request, 'articles/new.html')

def create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    article = Article.objects.create(title=title, content=content)
    # article = Article.objects.create(title=title, content=content).id
    # context = {
    #     'article': article
    # }
    # return render(request, 'articles/create.html', context)
    return redirect('articles:detail', article.pk)

def detail(request, article_pk):
    # 단일 데이터 조회
    article = Article.objects.get(id=article_pk)
    context = {
        'article': article
    }
    return render(request, 'articles/detail.html', context)

def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    article.delete()

    return redirect('articles:index')

def edit(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    context = {
        'article': article
    }
    return render(request, 'articles/edit.html', context)

def update(request, article_pk):
    title = request.POST.get('title')
    content = request.POST.get('content')
    article = Article.objects.get(pk=article_pk)
    article.title = title
    article.content = content
    article.save()
    return redirect('articles:detail', article.pk)