from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.shared.models import BaseModel
from datetime import datetime, timedelta
from django.core.validators import FileExtensionValidator
import random

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
    photo = models.ImageField(
        upload_to="user_photos/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extension=["jpg", "jpeg", "png", "heic", "heif"]
            )
        ],
    )

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name}, {self.last_name}"

    def create_verify_code(self, verify_type):
        code = "".join([str(random.randint((0, 100) % 10)) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id=self.id, verify_type=verify_type, code=code
        )
        return code


PHONE_EXPIRE = 2
EMAIL_EXPIRE = 5


class UserConfirmation(BaseModel):
    TYPE_CHOICES = ((VIA_PHONE, VIA_PHONE), (VIA_EMAIL, VIA_EMAIL))
    code = models.CharField(max_length=4)
    verify_type = models.CharField(max_length=31, choices=TYPE_CHOICES)
    users = models.ForeignKey(
        "apps.users.User", models.CASCADE, related_name="verify_codes"
    )
    expirations_time = models.DateTimeField(null=True)
    is_comfirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.verify_type == VIA_EMAIL:
                self.expirations_time = datetime.now() + timedelta(minutes=EMAIL_EXPIRE)
            else:
                self.expirations_time = datetime.now() + timedelta(minutes=PHONE_EXPIRE)
        super(UserConfirmation, self).save(*args, **kwargs)
