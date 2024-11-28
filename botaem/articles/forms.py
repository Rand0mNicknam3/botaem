from django import forms
from articles.models import Article, Article_Params, Topic


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('tittle', 'content', 'image')

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['tittle'].widget.attrs.update({
            'placeholder': 'Title is limited to 40 characters',
        })
        self.fields['content'].label ='Provide content'
        self.fields['image'].label = 'Upload image(optional), default is pretty cool as well :)'
        self.fields['tittle'].label = 'Title'


class ArticleParamsForm(forms.ModelForm):
    topic = forms.ModelChoiceField(queryset=Topic.objects.all())
    
    class Meta:
        model = Article_Params
        fields = ('topic', 'complexity')
