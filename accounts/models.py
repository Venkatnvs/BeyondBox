from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager,Permission
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save

class UserType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_completed', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_completed = models.BooleanField(default=False)
    is_socialaccount = models.BooleanField(default=False)
    user_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            ("change_userpassword", "Can Change User Password"),
        ]

    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def mobile_number(self):
        return f'{self.userprofile.mobile_no}' if self.userprofile else ''
    
    @property
    def gender(self):
        return f'{self.userprofile.gender}' if self.userprofile else ''

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255, null=True, blank=True)
    mobile_no = models.CharField(max_length=15, null=True, blank=True)
    usn = models.CharField(max_length=100, null=True, blank=True)
    college = models.CharField(max_length=255, blank=True, null=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    course = models.CharField(max_length=255, null=True, blank=True)
    preferred_college = models.TextField(null=True,blank=True)
    abroad_year = models.IntegerField(null=True, blank=True)
    abroad_season = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    @property
    def preferred_college_list(self):
        out = self.preferred_college
        if self.preferred_college is not None:
            out = [item for item in self.preferred_college.split('\r\n') if item]
        return out

    def __str__(self):
        return self.user.email
    
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        profile.save()