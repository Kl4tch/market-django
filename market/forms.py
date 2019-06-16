from django import forms


class SearchAllForm(forms.Form):
    search = forms.CharField(label="", max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Введите название'}))


class SearchForm(forms.Form):
    search = forms.CharField(required=False, label="", max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Введите название'}))
