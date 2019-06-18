from django import forms


class SearchAllForm(forms.Form):
    search = forms.CharField(label="", max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Введите название'}))


class SearchForm(forms.Form):
    search = forms.CharField(required=False, label="", max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Введите название'}))


class FeedBackForm(forms.Form):
    name = forms.CharField(required=True, label="", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя:'}))
    text = forms.TextInput()
    phone = forms.CharField(required=True, label="", max_length=16, widget=forms.TextInput(attrs={'placeholder': 'Ваш мобильный::'}))
