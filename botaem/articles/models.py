from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from user.models import CustomUser
from articles.utils import article_image_path
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from myprofile.validators import validate_image_size
from django.db.utils import IntegrityError


class Article(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='articles')
    tittle = models.CharField(max_length=40, unique=True, verbose_name='Title', validators=[MinLengthValidator(5), MaxLengthValidator(40)])
    content = models.TextField(max_length=4000, validators=[MinLengthValidator(5), MaxLengthValidator(4000)])
    image = models.ImageField(
        upload_to=article_image_path,
        blank=True,
        null=True,
        default='default_images/article_jaba.jpg',
        validators=[
            validate_image_size,
            FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg']),
        ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=45, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.tittle
    
    def save(self, *args, **kwargs):
        if not self.slug:
            try:
                self.slug = slugify(self.tittle)
            except IntegrityError:
                self.slug = slugify(self.tittle + str(self.id))
        super(Article, self).save(*args, **kwargs)


class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Article_Params(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='params')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='articles')
    complexity = models.IntegerField(choices=[(1, 'Easy'), (2, 'Medium'), (3, 'Hard')], default=1)
    views = models.IntegerField(default=0)

#TODO make tests for this
class Article_read_later(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='read_later')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='read_later_articles')

class Article_likes(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liked_articles')
