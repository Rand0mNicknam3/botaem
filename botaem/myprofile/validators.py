from django.forms import ValidationError


def validate_image_size(image):
    megabytes_limit = 4
    if image.size > 1024 * 1024 * megabytes_limit:
        raise ValidationError(f'Изображение должно быть не более {megabytes_limit}MB')