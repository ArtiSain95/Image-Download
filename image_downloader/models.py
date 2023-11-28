import os

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_image_extension(value):
    """
    Custom validator to ensure that an uploaded image has a valid file extension.
    """
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    _, file_extension = os.path.splitext(value.name)
    if file_extension.lower() not in valid_extensions:
        raise ValidationError('Invalid file extension. Supported formats: JPG, JPEG, PNG, GIF.')

class Image(models.Model):
    """Model representing an image entity."""
    local_file_path = models.CharField(max_length=250, null=True, blank= True)
    file_name = models.CharField(max_length=150, unique=True)
    source_url = models.URLField(max_length=150, unique=True)
    image = models.ImageField(upload_to='images/', validators=[validate_image_extension], null=True, blank= True)
    is_valid = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.file_name
