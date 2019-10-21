from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    # model = Article -> 클래스 변수로 선언되어버림
    
    # 위젯 설정 방법 1
    title = forms.CharField(
        max_length=140, 
        label='제목',
        help_text='140자 이내로 작성바랍니다.',
        widget=forms.TextInput(
            attrs={
                'placeholder': '제목을 입력바랍니다.'
            }
        )
    )
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs={
                'class': 'my-content',
                'placeholder': '내용을 입력바랍니다.',
                'rows': 5,
                'cols': 60
            }
        )
    )
    class Meta: # meta 클래스 정의
        model = Article
        exclude = ('user',) 
        # fields = '__all__' # 모든 필드

        # 위젯 설정 방법 2
        # widgets = {
        #     'title': forms.TextInput(
        #         attrs={
        #             'placeholder': '제목을 입력바랍니다.'
        #         }
        #     )
        # }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', ) # 지정 필드만 보여줌
        # exclude = ('article', ) 지정 필드 제외하고 나머지 보여줌


# class ArticleForm(forms.Form):
#     title = forms.CharField(
#         max_length=140, 
#         label='제목',
#         widget=forms.TextInput(
#             attrs={
#                 'placeholder': '제목을 입력바랍니다.'
#             }
#         )
#     )
#     content = forms.CharField(
#         # label 내용 수정
#         label='내용',
#         # Django form에서 HTML 지정 -> widget
#         widget=forms.Textarea(
#             attrs={
#                 'class': 'my-content',
#                 'placeholder': '내용을 입력바랍니다.',
#                 'rows': 5,
#                 'cols': 60
#             }
#         )
#     )