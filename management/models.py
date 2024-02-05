from django.db import models
from decouple import config

# Create your models here.
class Campaign(models.Model):
    endDate = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    sentEmails = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} campaign created {self.created}"
 


class AurisonUser(models.Model):
    campaign = models.ForeignKey('campaign', on_delete=models.CASCADE)
    email = models.CharField(max_length=35, default='')
    submittedPass = models.BooleanField(default=False)
    openedEmail = models.BooleanField(default=False)
    clickedLink = models.BooleanField(default=False)
    sentEmail = models.BooleanField(default=False)
    organization = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    title = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.title} {self.firstName} -- {self.campaign.name} campaign"
    


class SendEmailTask(models.Model):
    user = models.ForeignKey('aurisonuser', on_delete=models.CASCADE)

    def __str__(self):
        return f'Send email to {self.user.email}'


class SendAnalyticsTask(models.Model):
    campaign = models.ForeignKey('campaign', on_delete=models.CASCADE)

    def __str__(self):
        email = config('ANALYTICS_LIVE_EMAIL') if config('LIVE', cast=bool) else config('ANALYTICS_TEST_EMAIL')
        return f'Email analytics of {self.campaign.name} campaign to {email}'
