from django.db import models
from accounts.models import User


class Todo(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="todouser"
    )
    Title = models.TextField()
    CreateDate = models.DateField(auto_now_add=True)
    Is_active = models.BooleanField(default=True)
    EditeDate = models.DateField(auto_now=True)
    Completed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.Title}-{self.user}-{self.CreateDate}"
