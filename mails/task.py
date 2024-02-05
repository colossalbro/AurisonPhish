#NOTE (TO FUTURE SELF): I ABANDONED CELERY FOR APSCHEDULER. THIS IS IRRELEVANT.



from management.models import AurisonUser, Campaign
from management.utils import genCampaignAnalytics
from django.utils import timezone
from .postmark import Postmark


from datetime import datetime, timedelta
from os import path as osPath, getcwd
from celery import shared_task
from time import time



@shared_task
def sendEmails(campaignID: str):
    postmark = Postmark()

    campaign = Campaign.objects.get(pk = campaignID)

    campaign.sentEmails = True 
    campaign.active = True

    campaign.endDate = campaign.endDate.replace(    #So there's a uniform date? :) 
        hour=campaign.created.hour,
        minute=campaign.created.minute,
        second=campaign.created.second,
        microsecond=campaign.created.microsecond,
    )

    campaign.save()

    now = timezone.now()
    timeDiff = campaign.endDate - now
    
    # eta = now + timedelta(minutes=1)
    eta = now + timeDiff

    users = AurisonUser.objects.filter(campaign = campaign)
    postmark.sendEmails(users)
    
    # sendAnalytics.delay(campaignID)
    sendAnalytics.apply_async(args=[campaignID], eta=eta)   #queue campaign to close and send analytics






@shared_task
def sendAnalytics(campaignID: str):
    campaign = Campaign.objects.get(pk = campaignID)
    campaign.closed = True  #close the campiagn
    campaign.active = False
    campaign.save()
    
    allUsers = AurisonUser.objects.filter(campaign = campaign)

    #Users who submitted their passwords
    phished = AurisonUser.objects.filter(campaign = campaign, submittedPass = True)

    #Users who clicked the link but didn't submit their passwords.
    clicked = AurisonUser.objects.filter(campaign = campaign, clickedLink = True, submittedPass = False)

    #Users who opened the email and ignored it.
    ignored = AurisonUser.objects.filter(campaign = campaign, openedEmail = True, clickedLink = False, submittedPass = False)

    fileName = f'{ int(time()) }-{campaign.name}.xlsx'  #unique excel file
    excelFile = osPath.join( getcwd(), 'management', 'static', 'files', fileName)  #path to excel

    try:
        genCampaignAnalytics(excelFile, allUsers, clicked, phished, ignored)
    except Exception as e:
        print(e)
        return False
    
    Postmark.sendAnalytics(excelFile, campaign)

