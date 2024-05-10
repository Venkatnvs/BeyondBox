from django.db import models
import uuid

class AdsSize(models.Model):
    width = models.CharField(max_length=100,null=True,blank=True)
    height = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return f"{self.width}x{self.height}"

class AdsBase(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=240,null=True,blank=True)
    url = models.URLField(null=True,blank=True)
    size = models.ForeignKey(AdsSize,on_delete=models.CASCADE)
    forward_url = models.URLField(null=True,blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.title} - {self.size}"