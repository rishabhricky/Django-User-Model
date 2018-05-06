from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator

from .utils import code_generator

USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'

"""
    If you want to customize your user model do it in the beginning before making the
    initial makemigrations

    Below is how we extend abstract base user

    Below code example from https://docs.djangoproject.com/en/1.10/topics/auth/customizing/#a-full-example
    - Extend User Model
    - Customize User Model
    - Extend Customized user model

"""
class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            # date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
            # date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex = USERNAME_REGEX,
                message = 'Username must be alphanumeric or contain any of the following:". @ + -"',
                code = 'invalid_username',
            )],
        unique = True,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # date_of_birth = models.DateField()
    zipcode = models.CharField(max_length=120, default="440114",)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    # Email is by default here is your username field
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['date_of_birth']
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin


class ActivationProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    key = models.CharField(max_length=120)
    expired = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.key = code_generator()
        super(ActivationProfile, self).save(*args, **kwargs)

def post_save_activation_receiver(sender, instance, created, *args, **kwargs):
    if created:
        #send_email
        print("activation created")
        # url = "http<>/activate" + instance.key

# Hook the signal
post_save.connect(post_save_activation_receiver, sender=ActivationProfile)

"""
    Associate a signal here so whenever a user is created a profile is associated with it

    Below is now you extend the USER MODEL
"""

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    city = models.CharField(max_length=120, null=True, blank=True)

    # For python2
    def __str__(self):
        return str(self.user.username)

    # For python3
    def __unicode__(self):
        return str(self.user.username)


# This will be for the user model not for the profile
def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
            ActivationProfile.create(user=instance)
        except:
            pass

# Hook the signal
post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)

