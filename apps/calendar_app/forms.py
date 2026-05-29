from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'location']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-500 '
                         'focus:border-transparent text-gray-900 placeholder-gray-400',
                'placeholder': '일정 제목을 입력하세요',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-500 '
                         'focus:border-transparent text-gray-900 placeholder-gray-400',
                'placeholder': '일정 설명을 입력하세요 (선택사항)',
                'rows': 4,
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-500 '
                         'focus:border-transparent text-gray-900',
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-500 '
                         'focus:border-transparent text-gray-900',
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-500 '
                         'focus:border-transparent text-gray-900 placeholder-gray-400',
                'placeholder': '장소를 입력하세요 (선택사항)',
            }),
        }
        labels = {
            'title': '제목',
            'description': '설명',
            'start_date': '시작일',
            'end_date': '종료일',
            'location': '장소',
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError('종료일은 시작일 이후여야 합니다.')

        return cleaned_data

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 2:
            raise forms.ValidationError('제목은 2자 이상이어야 합니다.')
        return title
