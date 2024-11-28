def article_image_path(instance, filename):
    return f'article_images/{instance.author.username}/{instance.id}/{filename}'