from django.test import TestCase
from articles.forms import ArticleForm, ArticleParamsForm


class TestArticleForm(TestCase):
    
    def test_tittle_placeholder(self):
        form = ArticleForm()
        self.assertEqual(form.fields['tittle'].widget.attrs['placeholder'], 'Title is limited to 40 characters')
    
    def test_tittle_label(self):
        form = ArticleForm()
        self.assertEqual(form.fields['tittle'].label, 'Title')

    def test_content_label(self):
        form = ArticleForm()
        self.assertEqual(form.fields['content'].label, 'Provide content')

    def test_image_label(self):
        form = ArticleForm()
        self.assertEqual(form.fields['image'].label, 'Upload image(optional), default is pretty cool as well :)')