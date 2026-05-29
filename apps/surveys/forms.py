from django import forms
from .models import Survey


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description', 'is_anonymous', 'expires_at']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': '설문 제목을 입력하세요',
                'minlength': '5',
                'maxlength': '200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': '설문 설명 (선택사항)',
                'rows': 4
            }),
            'is_anonymous': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-indigo-600'
            }),
            'expires_at': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'title': '설문 제목',
            'description': '설문 설명',
            'is_anonymous': '익명 응답',
            'expires_at': '마감일시',
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title', '')
        expires_at = cleaned_data.get('expires_at')

        if title and len(title) < 5:
            self.add_error('title', '설문 제목은 최소 5자 이상이어야 합니다.')

        from django.utils import timezone
        if expires_at and expires_at <= timezone.now():
            self.add_error('expires_at', '마감일시는 현재 시간보다 이후여야 합니다.')

        return cleaned_data
