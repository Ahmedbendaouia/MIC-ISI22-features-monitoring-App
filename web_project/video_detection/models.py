from django.db import models

# Create your models here.

class Video_feed(models.Model):
    description = models.CharField(max_length=255, blank=True)    
    path = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_in_charge = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.is_in_charge:
            # set is_in_charge to False for all other instances
            Video_feed.objects.exclude(pk=self.pk).update(is_in_charge=False)
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.path.delete()
        super().delete(*args, **kwargs)       
        