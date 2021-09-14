from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email=models.EmailField(unique=True,verbose_name="ایمیل")
    is_author=models.BooleanField(default=False,verbose_name="وضعیت نویسندگی")
    special_user = models.DateTimeField(default= timezone.now,verbose_name="کاربر ویژه تا")
    user_profile_image=models.ImageField(upload_to = "images",verbose_name="عکس پروفایل",blank=True,null=True)
    use_gravatar=models.BooleanField(default=False,verbose_name="استفاده از گراواتار")
    
    def is_special_user(self):
        if(self.special_user > timezone.now()):
            return True
        else:
            return False
    is_special_user.boolean=True
    is_special_user.short_description="وضعیت کاربر ویژه"
