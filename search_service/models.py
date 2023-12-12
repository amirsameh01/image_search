from django.db import models

def image_path(instance, filename):
    return f'images/{instance.id}_{filename}'

class FinalImages(models.Model):
    file = models.ImageField(upload_to=image_path)