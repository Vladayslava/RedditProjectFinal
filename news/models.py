from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class Post(models.Model):
    title = models.CharField(max_length=255)  
    content = models.TextField()  
    created_at = models.DateTimeField(default=timezone.now)  
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)  

    def __str__(self):
        return self.title  

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments") 
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    content = models.TextField() 
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f'{self.author} on {self.post}' 
    
class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="votes") 
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    value = models.IntegerField()  

    def __str__(self):
        return f'{self.user} voted {self.value} on {self.post}'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatars/default_avatar.jpg', upload_to='avatars/')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def compress_image(self, image):
        img = Image.open(image)
        img = img.convert("RGB")
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=80)  
        return ContentFile(img_io.getvalue(), name=image.name)

    def resize_image(self, image):
        img = Image.open(image)
        img.thumbnail((150, 150))  
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=80)  
        return ContentFile(img_io.getvalue(), name=image.name)
