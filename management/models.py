from django.db import models

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
    campaign = models.ForeignKey('campaign', on_delete=models.CASCADE, default=1)
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
    