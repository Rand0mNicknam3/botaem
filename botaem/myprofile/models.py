import logging
from django.db import models
from myprofile.validators import validate_image_size
from django.core.validators import FileExtensionValidator, MaxLengthValidator
from django.utils.text import slugify
from user.models import CustomUser
from follower.models import Follower
from myprofile.utils import profile_image_path

logger = logging.getLogger(__name__)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(
        blank=True,
        default='FAANG Senior developer 18 y.o.',
        max_length=250,
        validators=[
            MaxLengthValidator(250),
        ])
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(
        upload_to=profile_image_path,
        blank=True,
        null=True,
        default="default_images/profile.jpg",
        validators=[
            validate_image_size,
            FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg']),
        ]
        )
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name='URL')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)
    
    def is_followed(self, target_user):
        logger.info(f'Checking if {target_user} is follower of {self.user}')
        return Follower.objects.filter(follower=target_user, user=self.user).exists()


