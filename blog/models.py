from django.db import models
from utils.models import CreationMixin


class Blog(CreationMixin):
    title = models.CharField(max_length=50)
    post = models.TextField(blank=True, null=True)
    author = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
