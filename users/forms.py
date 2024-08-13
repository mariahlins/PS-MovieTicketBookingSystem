# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError
from django.utils import timezone

class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'})
    )
    username = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})
    )
    birth_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email', 'birth_date')

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > timezone.now().date():
            raise ValidationError("Data de nascimento inválida")
        return birth_date
    
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            profile = Profile(user=user, birth_date=self.cleaned_data['birth_date'])
            profile.save()
        return user
    

class SignUpFormStaff(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    birth_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    is_staff = forms.BooleanField(required=False, initial=False, label='Is Staff')
    is_superuser = forms.BooleanField(required=False, initial=False, label='Is Superuser')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email', 'birth_date', 'is_staff', 'is_superuser')

    def save(self, commit=True):
        user = super(SignUpFormStaff, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_staff = self.cleaned_data['is_staff']
        user.is_superuser = self.cleaned_data['is_superuser']

        if commit:
            user.save()
            profile = Profile(user=user, birth_date=self.cleaned_data['birth_date'])
            profile.save()
        return user
