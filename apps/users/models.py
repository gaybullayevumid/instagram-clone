from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.shared.models import BaseModel

# Create your models here.

ORDINARY_USER, MANAGER, ADMIN = ("ordinary_user", "manager", "admin")
VIA_EMAIL, VIA_PHONE = ("via_email", "via_phone")
NEW, CODE_VERIFIED, DONE, PHOTO_STEP = ("new", "photo_verified", "done", "photo_step")


class User(AbstractUser, BaseModel):
    USER_ROLES = ((ORDINARY_USER, ORDINARY_USER), (MANAGER, MANAGER), (ADMIN, ADMIN))
    AUTH_TYPE_CHOISES = ((VIA_PHONE, VIA_PHONE), (VIA_EMAIL, VIA_EMAIL))
    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
        (PHOTO_STEP, PHOTO_STEP),
    )
    user_roles = models.CharField(
        max_length=31, choices=USER_ROLES, default=ORDINARY_USER
    )
    AUTH_TYPE = models.CharField(max_length=31, choices=AUTH_TYPE_CHOISES)
    AUTH_STATUS = models.CharField(max_length=31, choices=AUTH_STATUS, default=NEW)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True, unique=True)
    photo = models.ImageField(upload_to="user_photos/", null=True, blank=True)

    def __str__(self):
        return self.username
