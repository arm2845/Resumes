from django.db import models
from .validators import validate_file_extension


class Resume(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    keywords = models.TextField()
    resume_file = models.FileField(upload_to='doc', validators=[validate_file_extension])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
