from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager) :
    
    def create_user(self, nickname, username, password=None): #, birth_date, gender, liked_artist, liked_track
        if not nickname:
            raise ValueError("Users must have an nickname")

        user = self.model(
            nickname = nickname,
            username = username,
            # password = password
            # birth_date = birth_date,
            # gender = gender,
            # liked_artist = liked_artist,
            # liked_track = liked_track
            )
        
        user.set_password(password)
        user.save(using=self._db) 
        return user
        
    def create_superuser(self, nickname, username, password): # , birth_date, gender, liked_artist, liked_track, 
        
        user = self.create_user(
            nickname, 
            username = username, 
            # birth_date = birth_date,
            # gender = gender,
            # liked_artist = liked_artist,
            # liked_track = liked_track,
            password = password
        )
        
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    nickname = models.CharField(
        verbose_name='nickname',
        max_length=255,
        unique=True,
    )
    
    username = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender_choices = (("여자","여자"),("남자","남자"))
    gender = models.CharField( max_length=10, blank=True, null=True, choices=gender_choices)
    liked_artist = models.CharField(max_length=200, blank=True, null=True)
    liked_track = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    #recommended_tracks = models.ManyToManyField('music_rec_app.Track', related_name='recommended_users')
    #recommended_tracks = models.ManyToManyField('Track', related_name='recommended_users') # 음악 추천을 위해 미리 저장

    objects = UserManager()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    class Meta:
        managed = True
        db_table = 'USERS'

    
# class Users(AbstractBaseUser):
    
#     objects = UserManager()

#     # user_id = models.CharField(primary_key=True)
#     nickname = models.CharField(primary_key=True,max_length=30)
#     name = models.CharField( max_length=30, blank=True, null=True)
#     # password = models.CharField(db_column='PASSWORD', max_length=100, blank=True, null=True)
#     # birth_date = models.DateField(blank=True, null=True,default=datetime.date.today)
#     age = models.IntegerField(blank=True, null=True)
#     gender = models.CharField( max_length=10, blank=True, null=True)
#     liked_artist = models.CharField(max_length=200, blank=True, null=True)
#     liked_track = models.CharField(max_length=200, blank=True, null=True)

#     USERNAME_FIELD = 'nickname'
#     REQUIRED_FIELDS = ['name','age', 'gender']
    
           
#     def __str__(self):
#         return self.nickname   



# class CustomUser(AbstractUser):
#     users = models.OneToOneField('Users', on_delete=models.CASCADE)
#     liked_artist = models.CharField(max_length=200)
#     liked_track = models.CharField(max_length=200)

#     class Meta:
#         db_table = 'USERS'  # MySQL의 USERS 테이블과 연결되도록 지정
#         managed = False
        
# class Users(models.Model):
#     users_id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=30)
#     nickname = models.CharField(unique=True, max_length=30)
#     password = models.CharField(max_length=200)
#     birth_date = models.DateField()
#     gender = models.CharField(max_length=10)
#     is_superuser = models.BooleanField()
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.CharField(max_length=30)
#     is_staff = models.BooleanField()
#     is_active = models.BooleanField()

#     USERNAME_FIELD = 'users_id'

#     class Meta:
#         managed = False
#         db_table = 'USERS'     
           
    # def __str__(self):
    #     return self.username    
        
        
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django_resized import ResizedImageField

#  # 프로필 이미지 등록
# class User(AbstractUser):
#    pass
       
# class User(models.Model):
#   user_id=models.CharField(max_length=64, verbose_name='사용자 아이디')
#   password=models.CharField(max_length=64, verbose_name='비밀번호')
#   registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

#   def __str__(self):
#     return self.user_id

        
        
        
        
        
        


        
# from django.db import models
# from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# class User(AbstractBaseUser, models.Model):
#     user_id = models.AutoField(db_column='USER_ID', primary_key=True)
#     username = models.CharField(db_column='USERNAME', max_length=30, blank=True, null=True)
#     nickname = models.CharField(db_column='NICKNAME', unique=True, max_length=30, blank=True, null=True)
#     password = models.CharField(db_column='PASSWORD', max_length=100, blank=True, null=True)
#     age = models.IntegerField(db_column='AGE', blank=True, null=True)
#     gender = models.CharField(db_column='GENDER', max_length=10, blank=True, null=True)
#     liked_artist = models.CharField(db_column='LIKED_ARTIST', max_length=200, blank=True, null=True)
#     liked_track = models.CharField(db_column='LIKED_TRACK', max_length=200, blank=True, null=True)

#     USERNAME_FIELD = 'nickname'
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     objects = BaseUserManager()
    
#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True
    
#     def __str__(self):
#         return self.username
    
#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         # Simplest possible answer: All admins are staff
#         return self.is_admin
    
#     class Meta:
#         managed = True
#         db_table = 'USERS'