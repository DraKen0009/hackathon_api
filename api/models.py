from django.contrib.auth.models import User
from django.db import models


class Hackathon(models.Model):
    SUBMISSION_CHOICES = (
        ('image', 'Image'),
        ('file', 'File'),
        ('link', 'Link'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    background_image = models.ImageField(upload_to='hackathon_images/')
    hackathon_image = models.ImageField(upload_to='hackathon_images/')
    submission_type = models.CharField(max_length=10, choices=SUBMISSION_CHOICES)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reward_prize = models.DecimalField(max_digits=10, decimal_places=2)
    enrolled_users = models.ManyToManyField(User, through='HackathonRegistration', related_name='enrolled_hackathons')

    def __str__(self):
        return self.title


class Submission(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    summary = models.TextField()

    # Add specific fields for each submission type (image, file, link)
    image_submission = models.ImageField(upload_to='submission_images/', blank=True, null=True)
    file_submission = models.FileField(upload_to='submission_files/', blank=True, null=True)
    link_submission = models.URLField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ['user', 'hackathon']

    def __str__(self):
        return self.name


# submissions/models.py

class HackathonRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'hackathon']


    def __str__(self):
        return f"{self.user.username} registered for {self.hackathon.title}"
