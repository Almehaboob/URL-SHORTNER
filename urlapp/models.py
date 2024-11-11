from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import hashlib

class URL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_url = models.URLField()
    shortened_url = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.shortened_url:
            self.shortened_url = self.generate_shortened_url()
        super().save(*args, **kwargs)

    def generate_shortened_url(self):
        hash_object = hashlib.md5(self.original_url.encode())
        return hash_object.hexdigest()[:6]  # Shorten to first 6 characters

    def __str__(self):
        return self.title


# Create your models here.
