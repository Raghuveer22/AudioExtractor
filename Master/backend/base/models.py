from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
# Create your models here.
def upload_path(instance,filename):
    return f'{instance.uploaded_by}/{filename}'

class Audio(models.Model):
    uploaded_by=models.ForeignKey(User, related_name='uploaded_by', on_delete=models.CASCADE)
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    name=models.CharField(default="helo",max_length=100)
    duration=models.DurationField(default=None)
    upload_file = models.FileField(upload_to=upload_path, blank=True)
    uploaded_on=models.DateTimeField(default=timezone.now())
    
class Comment(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    text=models.CharField(max_length=256)
    audio=models.ForeignKey(Audio,related_name='audio',on_delete=models.CASCADE)
    timestamp=models.DurationField()
    added_by=models.ForeignKey(User, related_name='added_by', on_delete=models.CASCADE)
    added_on=models.DateTimeField(default=timezone.now())

class Like(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    comment=models.ForeignKey(Comment,related_name='comment',on_delete=models.CASCADE)
    liked_by=models.ForeignKey(User, related_name='liked_by', on_delete=models.CASCADE)
    liked_on=models.DateTimeField(default=timezone.now())
