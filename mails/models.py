from django.db import models
from management.models import Campaign

# Create your models here.
class Email(models.Model):
    mailID = models.CharField(max_length=50)
    email = models.EmailField(max_length=35, default='') #Who this email was sent to
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.campaign.name}: {self.mailID} to {self.email}'


class Token(models.Model):
    tokenID = models.CharField(max_length=30)
    email = models.EmailField(max_length=35, default='') #Who was this token generated for
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.campaign.name}: {self.tokenID} for {self.email}'
    