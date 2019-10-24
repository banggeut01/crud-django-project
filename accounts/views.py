from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
# AuthenticationForm 인증과 관련된 폼
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# 아래 두개는 같다.
# from accounts.models import User
# from django.contrib.auth import get_user_model

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = { # 검증 실패 => 사용자가 입력한 내용 그대로, GET 요청 => 입력 form
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('articles:index')

@login_required
def update(request):
    if request.method == 'POST':
        # 1. 사용자가 보낸 내용 담아서
        form = CustomUserChangeForm(request.POST, instance=request.user)
        # 2. 검증
        if form.is_valid():
            form.save()
            return redirect('articles:index')
        # 3. 반영
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

# 비밀번호 수정
@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('articles:index')
    else: form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)


from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
def profile(request, account_pk):
    # user = User.objects.get(pk=account_pk)
    User = get_user_model() # 클래스 반환
    user = get_object_or_404(User, pk=account_pk) # 객체 반환
    context = {
        'user_profile': user,
    }
    return render(request, 'accounts/profile.html', context)

def follow(request, account_pk):
    User = get_user_model()
    obama = get_object_or_404(User, pk=account_pk)
    if obama != request.user:
        # obama를 팔로우 한적이 있다면
        if request.user in obama.followers.all():
        # if obama in request.user.followings.all():
            obama.followers.remove(request.user)
            # 취소
        # 아니면
        else:
            # 팔로우
            obama.followers.add(request.user)
    return redirect('accounts:profile', account_pk)