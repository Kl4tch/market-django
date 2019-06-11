from django import forms


class Form(forms.Form):
    url = forms.URLField(label='Ссылка на товары', max_length=150)
    category = forms.CharField(label='Название категории', max_length=50)
    startPage = forms.IntegerField(label='Начать со страницы:')
    endPage = forms.IntegerField(label='Закончить на странице:')
