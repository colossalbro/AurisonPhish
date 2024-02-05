from django.utils import timezone


from os import getcwd, listdir, path as ospath, remove
from management.utils import genCampaignAnalytics
from mails.postmark import Postmark
from datetime import datetime, timedelta
from management.models import *
from time import time



def deleteXlsx():
    #This task periodically checks two directories for xlsx files to delete.
    #management/static/files and management/static/uploads are the directories checked.
    #Deleted files are determined by the timestamp used in creating them.
    #E.g, given a file '1706993227-test.xlsx', the timestamp would be 1706993227
    dir1 = ospath.join( getcwd(), 'management', 'static', 'files' )
    dir2 = ospath.join( getcwd(), 'management', 'uploads' )

    deleteStaleFiles(dir1)
    deleteStaleFiles(dir2)



def deleteStaleFiles(path: str) -> None:
    now = int(time())   #UTC

    for file in listdir(path):          #Example of file stored in dir: 1706993227-test.xlsx
        if file == 'sample.xlsx':
            continue

        timestamp = int(file.split('-')[0])

        if now > timestamp:
            fullPath = ospath.join(path, file)

            remove(fullPath)



def sendEmail():
    postmark = Postmark()

    for task in SendEmailTask.objects.all():
        try:
            postmark.sendEmail(task.user)
            task.delete()
        except Exception as e:
            print(e)
        


def sendAnalytics():
    now = timezone.now()    #Dateobject returns considers the timezone in settings.py

    for task in SendAnalyticsTask.objects.all():
        if now > task.campaign.endDate:     #send the analytics.
            task.campaign.active = False
            task.campaign.closed = True
            task.campaign.save()

            allUsers = AurisonUser.objects.filter(campaign = task.campaign)

            #Users who submitted their passwords
            phished = AurisonUser.objects.filter(campaign = task.campaign, submittedPass = True)

            #Users who clicked the link but didn't submit their passwords.
            clicked = AurisonUser.objects.filter(campaign = task.campaign, clickedLink = True, submittedPass = False)

            #Users who opened the email and ignored it.
            ignored = AurisonUser.objects.filter(campaign = task.campaign, openedEmail = True, clickedLink = False, submittedPass = False)

            #5 Minutes from now. This should be enough time for the file to get emailed before the scheduler deletes it.
            timestamp = datetime.now() + timedelta(minutes=5)
            timestamp = int(timestamp.timestamp()) #convert to epoch.

            fileName = f'{timestamp}-{task.campaign.name}.xlsx'  #unique excel file
    
            excelFile = ospath.join( getcwd(), 'management', 'static', 'files', fileName)  #path to excel

            try:
                genCampaignAnalytics(excelFile, allUsers, clicked, phished, ignored)
            except Exception as e:
                print(e)
                return False
            
            Postmark.sendAnalytics(excelFile, task.campaign)

            task.delete()   #Delete the task
