from random import random
from django.db import models
from datetime import datetime
import os 
import random
from django.utils import timezone 
from django.utils.html import mark_safe 
from django.contrib.auth.models import AbstractUser, User

now = timezone.now()

def image_path(instance, filename): 
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(10))
    _now = datetime.now() 
    
    return 'book_pic/{year}-{month}-{imageid}-{basename}-{randomstring}{ext}'.format(imageid = instance, basename=basefilename, randomstring=randomstr, ext=file_extension, year=now.strftime('%Y'), month=now.strftime('%m'), day=now.strftime('%d'))

class User(AbstractUser): 
    is_student = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

class Book(models.Model): 
    book_image = models.ImageField(upload_to=image_path, default='book_pic/image.jpg')
    def image_tag(self): 
        return mark_safe('<img src="/books/media/%s" width="50" height="50" />'% (self.book_image))
    book_title = models.CharField(max_length=400, verbose_name='Book Title')
    book_authors = models.CharField(max_length=400, verbose_name='Author/s')
    book_college = models.CharField (max_length=100, verbose_name='College')
    book_course = models.CharField (max_length=100, verbose_name='Course')
    pub_month = models.CharField(max_length=100, verbose_name='Month')
    pub_year = models.CharField(max_length=100, verbose_name='Year')
    book_abstract = models.TextField(max_length=3000, verbose_name='Abstract')
    book_type = models.CharField(max_length=100, verbose_name='Type')
    favorites = models.ManyToManyField(
        User, related_name='favorite', default=None, blank=True)
    
    def __str__(self):
        return self.book_title
    
