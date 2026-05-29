from django import forms
from django.contrib.auth import authenticate
from .models import CustomUser


class SignUpForm(forms.ModelForm):
    """회원가입 폼"""
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': '8자 이상의 비밀번호'
        })
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': '비밀번호를 다시 입력하세요'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'nickname')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': '이메일 주소'
            }),
            'username': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': '사용자명'
            }),
            'nickname': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': '닉네임'
            }),
        }

    def clean_password2(self):
        """비밀번호 일치 확인"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
            if len(password1) < 8:
                raise forms.ValidationError('비밀번호는 8자 이상이어야 합니다.')

        return password2

    def clean_email(self):
        """이메일 중복 확인"""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 사용 중인 이메일입니다.')
        return email

    def clean_nickname(self):
        """닉네임 중복 확인"""
        nickname = self.cleaned_data.get('nickname')
        if CustomUser.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError('이미 사용 중인 닉네임입니다.')
        return nickname

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """로그인 폼"""
    email = forms.EmailField(
        label='이메일',
        widget=forms.EmailInput(attrs={
            'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': '이메일 주소'
        })
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': '비밀번호'
        })
    )

    def clean(self):
        """로그인 검증"""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = CustomUser.objects.get(email=email)

                # 계정 잠금 확인
                if user.is_account_locked():
                    raise forms.ValidationError(
                        f'계정이 잠겼습니다. 30분 후 다시 시도해주세요.'
                    )

                # 비밀번호 검증
                if not user.check_password(password):
                    user.increment_login_fail()
                    remaining = 5 - user.login_fail_count
                    if remaining > 0:
                        raise forms.ValidationError(
                            f'비밀번호가 일치하지 않습니다. ({remaining}회 남음)'
                        )
                    else:
                        raise forms.ValidationError(
                            '로그인 시도 횟수를 초과했습니다. 계정이 30분간 잠겼습니다.'
                        )

            except CustomUser.DoesNotExist:
                raise forms.ValidationError('등록되지 않은 이메일입니다.')

        return cleaned_data


class ProfileForm(forms.ModelForm):
    """프로필 수정 폼"""
    class Meta:
        model = CustomUser
        fields = ('nickname', 'bio', 'profile_image')
        widgets = {
            'nickname': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': '닉네임'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': '한 줄 소개',
                'rows': 4
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
            }),
        }
