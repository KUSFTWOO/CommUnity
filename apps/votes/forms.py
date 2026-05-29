from django import forms
from .models import Poll, PollOption


class PollForm(forms.ModelForm):
    options = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'rows': 8,
            'placeholder': '각 선택지를 줄바꿈으로 구분해주세요.\n(최소 2개, 최대 10개)\n예:\n선택지1\n선택지2\n선택지3'
        }),
        help_text='각 선택지를 줄바꿈으로 구분하세요. 최소 2개, 최대 10개.'
    )

    class Meta:
        model = Poll
        fields = ['question', 'expires_at']
        widgets = {
            'question': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': '투표 질문을 입력하세요',
                'minlength': '5',
                'maxlength': '300'
            }),
            'expires_at': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'question': '투표 질문',
            'expires_at': '마감일시',
        }

    def clean(self):
        cleaned_data = super().clean()
        options_text = self.cleaned_data.get('options', '')

        if options_text:
            options_list = [opt.strip() for opt in options_text.split('\n') if opt.strip()]

            if len(options_list) < 2:
                self.add_error('options', '최소 2개 이상의 선택지가 필요합니다.')
            elif len(options_list) > 10:
                self.add_error('options', '최대 10개까지의 선택지만 허용됩니다.')

            for i, option in enumerate(options_list):
                if len(option) < 2:
                    self.add_error('options', f'{i+1}번째 선택지는 최소 2자 이상이어야 합니다.')
                elif len(option) > 200:
                    self.add_error('options', f'{i+1}번째 선택지는 최대 200자까지만 입력 가능합니다.')

        question = self.cleaned_data.get('question', '')
        if question and len(question) < 5:
            self.add_error('question', '투표 질문은 최소 5자 이상이어야 합니다.')

        expires_at = self.cleaned_data.get('expires_at')
        from django.utils import timezone
        if expires_at and expires_at <= timezone.now():
            self.add_error('expires_at', '마감일시는 현재 시간보다 이후여야 합니다.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

            options_text = self.cleaned_data.get('options', '')
            options_list = [opt.strip() for opt in options_text.split('\n') if opt.strip()]

            for option_text in options_list:
                PollOption.objects.create(
                    poll=instance,
                    text=option_text,
                    votes_count=0
                )

        return instance
