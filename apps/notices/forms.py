from django import forms
from .models import Notice


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'is_important']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-500 '
                         'focus:border-transparent text-gray-900 placeholder-gray-400',
                'placeholder': '공지사항 제목을 입력하세요',
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-500 '
                         'focus:border-transparent text-gray-900 placeholder-gray-400',
                'placeholder': '공지사항 내용을 입력하세요',
                'rows': 10,
            }),
            'is_important': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 cursor-pointer',
            }),
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'is_important': '중요 공지로 설정',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 2:
            raise forms.ValidationError('제목은 2자 이상이어야 합니다.')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if len(content) < 5:
            raise forms.ValidationError('내용은 5자 이상이어야 합니다.')
        return content
