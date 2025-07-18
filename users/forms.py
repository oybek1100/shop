from django import forms
from .models import CustomUser

from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError("Bu email bilan foydalanuvchi topilmadi.")

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Parol kamida 8 ta belgidan iborat bo‘lishi kerak.")
        return password



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class RegisterModelForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ('email', 'password' , 'confirm_password')
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters')
        return password

    def clean_email(self):
        email = self.data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f'{email.title()} already exist ')
        return email
    

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError('Password did not match')
        
        return confirm_password