from django import forms


class SearchTitleForm(forms.Form):
    title = forms.CharField()


class SearchImdbForm(forms.Form):
    imdb_id = forms.CharField()
