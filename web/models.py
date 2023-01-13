from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from web.enums import Role


# User = get_user_model()
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'password' and isinstance(self, User):
                if value:
                    self.set_password(value)
            else:
                if value:
                    setattr(self, key, value)
        self.save()
        return self

    class Meta:
        abstract = True


class UserManager(DjangoUserManager):
    def _create_user(self, email, password, commit=True, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, role=Role.admin, **extra_fields)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(unique=True)
    role = models.CharField(
        choices=Role.choices,
        max_length=15,
        default=Role.user
    )
    name = models.CharField(max_length=255, null=True, blank=True)

    @property
    def is_staff(self):
        return self.role in (Role.admin, Role.staff)

    @property
    def is_superuser(self):
        return self.role == Role.admin

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Car(BaseModel):
    name = models.CharField(max_length=255)
    engine = models.CharField(max_length=255)
    power = models.IntegerField()
    transmission = models.CharField(max_length=255)
    drive = models.CharField(max_length=255)
    body_type = models.CharField(max_length=255)
    wheel_type = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)


class Advert(BaseModel):
    # characteristics
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
    car_name = models.CharField(max_length=255, null=True, blank=True)

    mileage = models.IntegerField()
    generation = models.CharField(max_length=255)
    equipment = models.CharField(max_length=255)

    price = models.FloatField(
        validators=[MinValueValidator(0.0)]
    )
    description = models.TextField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    color = models.CharField(max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Favorite(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)


# class Feedback(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     car = models.ForeignKey(Car, on_delete=models.CASCADE)
#     content = models.TextField()
