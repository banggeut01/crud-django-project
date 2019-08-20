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
    title = request.GET.get('title')
    content = request.GET.get('content')
    article = Article.objects.create(title=title, content=content)
    # article = Article.objects.create(title=title, content=content).id
    context = {
        'article': article
    }
    # return render(request, 'articles/create.html', context)
    return redirect(f'/articles/{article.pk}/')

def detail(request, article_pk):
    # 단일 데이터 조회
    article = Article.objects.get(id=article_pk)
    context = {
        'article': article
    }
    return render(request, 'articles/detail.html', context)