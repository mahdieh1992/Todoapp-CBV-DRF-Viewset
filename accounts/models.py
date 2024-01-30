from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver

date_now = date.today()
date_add = date_now.year + 2
date_current = date_now.replace(year=date_add)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email"), unique=True)
    Isdeleted = models.BooleanField(default=False)
    ExpireDate = models.DateField(default=date_current)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} "


class UserDetail(models.Model):
    User_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="UserDetail"
    )
    FirstName = models.CharField(_("First_name"), max_length=250)
    LastName = models.CharField(_("Last_name"), max_length=250)
    Gender = models.BooleanField(default=False)
    NationalCode = models.CharField(max_length=10)
    Mobile = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.User_id}"


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        UserDetail.objects.create(User_id=instance)
