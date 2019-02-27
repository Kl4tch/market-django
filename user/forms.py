from .views import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserForm(UserCreationForm):
    phone = forms.CharField()
    phone.label = 'Телефон'

    class Meta:
        model = User
        fields = ['phone']


class UserAuth(forms.Form):
    your_name = forms.CharField(label='Телефон', max_length=15)
    subject = forms.CharField(max_length=100)
    password = forms.PasswordInput()


class CommentForm(forms.Form):

    comment_area = forms.CharField(
        label="",
        widget=forms.Textarea
    )

