from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


from management.models import AurisonUser
from .models import Email

from json import loads


# Create your views here.
class Webhook(View):
    def post(self, request, *args, **kwargs):
        body = loads(request.body)

        event = body['RecordType']
        messageID = body['MessageID']

        email = Email.objects.get(mailID = messageID)
        user = AurisonUser.objects.get(email = email.email, campaign = email.campaign)

        if event == 'Open':
            user.openedEmail = True 


        elif event == 'Click':
            user.openedEmail = True     #I do this because sometimes postmark doesn't send an Open event.
                                        #You have to open the email to click the link :)
            
            user.clickedLink = True
    

        elif event == 'Delivery':
            user.sentEmail = True
        
        
        else: 
            pass

        user.save()

        return HttpResponse('ok')



