from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from IPython import embed
from django.contrib import messages # message framwork
from django.contrib.auth.decorators import login_required
from .models import Article, Comment, HashTag
from .forms import ArticleForm, CommentForm


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


# 1. Form을 주는 과정 (GET)
# 2. DB에 저장하는 동작 (POST)
# 두개의 동작을 하나의 URL로 관리할 수 있다.
@login_required
def create(request):
    # POST 요청 -> 검증 및 저장
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES) # request.POST 사용자가 입력한 내용
        # embed()
        # 검증에 성공하면 저장하고,
        if article_form.is_valid(): # 중요한 로직!
            # title = article_form.cleaned_data.get('title')
            # content = article_form.cleaned_data.get('content')
            # article = Article(title=title, content=content)
            # article.save()
            article = article_form.save(commit=False)
            article.user = request.user 
            article.save()
            # 해시태그 저장 및 연결 작업 => 여기서 하는 이유 article의 pk를 알아야하기 때문!
            for word in article.content.split():
                if word.startswith('#'): # if word[0] == '#':
                    # 해시태그에 있으면 해당 pk값을
                    # if tag in article.hashtags.all():
                    hashtag, created = HashTag.objects.get_or_create(content=word)
                    article.hashtags.add(hashtag)
            # redirect
            return redirect('articles:detail', article.pk)
        # else:
        #   다시 폼으로 돌아가 -> 중복되서 제거!
        #   검증 실패시,
        #   사용자가 입력한 값(request.POST)를 article_form으로 넘겨준다.
        #   만약 넘겨주지 않으면, 검증실패시 작성했던 내용이 사라진다.
    # GET 요청이면
    else:
        # GET 요청 -> Form
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
    # pk값이 없어서 뜨는 error는 404에러이다.
    comments = article.comment_set.all()
    comment_form = CommentForm()
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'image': article.image
    }
    return render(request, 'articles/detail.html', context)

from django.core.exceptions import PermissionDenied

@require_POST
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.user == request.user:
        article.delete()    
        return redirect('articles:index')
    else:
        raise PermissionDenied

def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.user == request.user:
        if request.method == 'POST': # 수정한 내용 저장할 때 POST
            article_form = ArticleForm(request.POST, instance=article) # 수정하려는 인스턴스 - article 넣어주기!
            if article_form.is_valid():
                article = article_form.save()
                # 해시태그 수정
                article.hashtags.clear() # M:N 관계에서 해당하는 값 지울 때
                # create와 동일한 부분
                for word in article.content.split():
                    if word.startswith('#'): # if word[0] == '#':
                        # 해시태그에 있으면 해당 pk값을
                        # if tag in article.hashtags.all():
                        hashtag, created = HashTag.objects.get_or_create(content=word)
                        article.hashtags.add(hashtag)
                return redirect('articles:detail', article.pk)
        else: # 수정버튼 눌렀을 때 수정화면으로 가는 것 GET
            article_form = ArticleForm(instance=article) # 수정하려는 인스턴스 넣어주기!
        context = {
            'article_form': article_form
        }
        return render(request, 'articles/form.html', context)
    else:
        raise PermissionDenied

from django.http import HttpResponseForbidden, HttpResponse
@require_POST # POST로 넘어왔을 때만 실행!, import해주기 
def comment_create(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        # 1. modelform에 사용자 입력값 넣고
        comment_form = CommentForm(request.POST)
        # 2. 검증하고,
        if comment_form.is_valid():
        # 3. 맞으면 저장!
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
        # 4. return redirect
        else:
            messages.success(request, '댓글이 형식에 맞지 않습니다.')
        return redirect('articles:detail', article_pk)
    else:
        return HttpResponse('Unauthored', status=401)
    # comment = Comment() => import 주의!
    # comment.content = request.POST.get('content')
    # comment.article = article => 안하면 error
    # or comment.article_id = article_pk
    # comment.save()
    # return redirect('articles:detail', article_pk)

from django.http import HttpResponseForbidden
@require_POST 
# 인자 3개 일 때 : (request, comment_pk, article_pk)
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user == request.user:
        article_pk = comment.article_id
        comment.delete()
        # 길게
        # messages.add_message(request, messages.INFO, '댓글이 삭제되었습니다.')
        # 짧게
        messages.info(request, '댓글이 삭제되었습니다.')
        return redirect('articles:detail', article_pk)    
    else:
        return HttpResponseForbidden()
        # raise PermissionDenied과 같음

# 주의! @required_POST하면 안된다. 
# 로그인 안한 상태에서 좋아요 누르면 -> 로그인 화면이 뜬다. -> 로그인하는 순간 login 실행 후 redirect하게 되는데
# get 요청으로 해당하는 url로 가기 때문에 HTTP ERROR 405에러가 뜬다. 
# post로 redirect할 수 없다!
@login_required
# 로그인이 되어있지 않다면 객체가 아니다. => 로그인 하지 않은채로 좋아요 누르면 오류발생
# 로그인이 되어있다면 user 객체
def like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user in article.like_users.all():
    # if article.like_users.filter(id=request.user.id).exist():  # => get은 오류를 발생시킴
    # 좋아요를 누른적이 있다면?
        request.user.like_articles.remove(article)
        # article.like_users.remove(request.user)
        # 좋아요 취소 로직
    # 아니면
    else:
        request.user.like_articles.add(article)
        # 좋아요 로직
    return redirect('articles:detail', article_pk)

def hashtag(request, hashtag_pk):
    hashtag = get_object_or_404(HashTag, pk=hashtag_pk)
    context = {
        'hashtag': hashtag
    }
    return render(request, 'articles/hashtag.html', context)

from itertools import chain
def explore(request):
    followings = request.user.followings.all()
    followings = chain(followings, [request.user])
    articles = Article.objects.filter(user__in=followings).order_by('-id')
    context = {
        'articles': articles
    }
    return render(request, 'articles/test.html', context)