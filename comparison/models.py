from django.core.exceptions import ValidationError
from django.db import models
import os
def truncate_filename(filename, max_length=150):
    """
    Truncate filename to fit within the max_length limit.
    """
    root, ext = os.path.splitext(filename)
    if len(root) > max_length:
        root = root[:max_length]
    return root + ext

def custom_upload_path(instance, filename):
    """
    Custom upload path function that truncates the filename.
    """
    filename = truncate_filename(filename)
    return f'images/{filename}'

class CustomImageField(models.ImageField):
    def validate_image_file_extension(self, file):
        super().validate_image_file_extension(file)
        max_filename_length = 150  # Adjust this to your desired maximum filename length
        if len(file.name) > max_filename_length:
            raise ValidationError(
                f'This filename has more than {max_filename_length} characters.'
            )

    def formfield(self, **kwargs):
        defaults = {'max_length': 150}  # Adjust this to match the maximum filename length
        defaults.update(kwargs)
        return super().formfield(**defaults)

class Image(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = CustomImageField(upload_to=custom_upload_path)
    elo_rating = models.FloatField(default=1000)  # Initial ELO rating

    def __str__(self):
        return self.title or str(self.pk)

class Vote(models.Model):
    image1 = models.ForeignKey(Image, related_name='vote_image1', on_delete=models.CASCADE)
    image2 = models.ForeignKey(Image, related_name='vote_image2', on_delete=models.CASCADE)
    winner = models.ForeignKey(Image, related_name='vote_winner', on_delete=models.CASCADE)
    vote_time = models.DateTimeField(auto_now_add=True)




class Visitor(models.Model):
    ip_address = models.CharField(max_length=39)  # IPv6 maximum length
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Visitor {self.ip_address}'

class VisitorCounter(models.Model):
    total_visitors = models.IntegerField(default=0)

    def __str__(self):
        return f'Total Visitors: {self.total_visitors}'