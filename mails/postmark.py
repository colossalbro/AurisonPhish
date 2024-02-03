from management.models import AurisonUser
from .models import *


from os import path as osPath, getcwd
from string import ascii_letters
from base64 import b64encode
from decouple import config
from random import choice
from requests import post


class Postmark:
    def __init__(self):
        self.analyticsStream = config('POSTMARK_ANALYTICS_STREAM')
        self.messageStream = config('POSTMARK_PHISHING_STREAM')
        self.endpoint = 'https://api.postmarkapp.com/email'
        self.serverToken = config('POSTMARK_SERVER_TOKEN')
        self.URL = config('DOMAIN_URL')
        self.htmlEmail = ''
        self.txtEmail = ''

        self.loadEmail()




    def sendEmail(self, user: AurisonUser) -> bool:
        #Note (to self): I abandoned django's core send_email, along with anymail application.
        #I did this because I needed to grab the MessageID returned by postmark and store in the DB.
        #It was easier (and faster) to just send an http request.
        personal = self.makePersonal(user)

        try:
            auth = {
                'X-Postmark-Server-Token' : self.serverToken
            }
            
            payload = {
                'From': 'noreply@aurisonn.app',
                'To': user.email,
                'Subject': 'Important Information About Your Account!',
                'HtmlBody': personal['htmlEmail'],
                'TextBody': personal['txtEmail'],
                'MessageStream': self.messageStream
            }


            res = post(self.endpoint, json=payload, headers=auth)

            print(res.status_code)
            print(res.json())
            json = res.json()

            if json['Message'] == 'OK': 
                emailID = json['MessageID']
                
                email = Email(mailID=emailID, email=user.email, campaign=user.campaign)
                token = Token(tokenID=personal['token'], email=user.email, campaign=user.campaign)

                email.save()
                token.save()

                return True
            
            else:
                raise Exception     #Improve this later 
        
        except Exception as e:
            print(e)
            return False
        
    



    def sendEmails(self, users: list[AurisonUser]) -> dict:
        data = {}

        #takes in a list of AurisonUsers, loops through them and sends the phish
        for user in users:
            successful = self.sendEmail(user)
            
            if not successful: 
                data[user] = False    
                continue
            
            data[user.firstName] = True      #Email sent for this user.
            
        return data





    def loadEmail(self):
        htmlFile = 'email.html'
        txtFile = 'email.txt'

        htmlPath = osPath.join( getcwd(), 'mails', 'templates', htmlFile)
        txtPath = osPath.join( getcwd(), 'mails', 'templates', txtFile)

        try:
            self.htmlEmail = open(htmlPath).read()
            self.txtEmail = open(txtPath).read()
        except:
            #Likely a file read error. Too lazy to handle
            pass 





    def makePersonal(self, user: AurisonUser) -> dict:
        phishToken = self.genPhishToken()
        
        link = f'{self.URL}verify/{user.email}/{phishToken}'
        name = user.firstName 
        


        html = self.htmlEmail.replace('PERSON_LINK', link).replace('PERSON_NAME', name)

        txt = self.txtEmail.replace('PERSON_LINK', link).replace('PERSON_NAME', name)


        return {
            'htmlEmail' : html,
            'txtEmail' : txt,
            'token' : phishToken
        }





    def genPhishToken(self) -> str:
        #Generates a random phishing token.
        tempToken = ''.join( choice(ascii_letters) for _ in range(30) )     #RandomID

        startIndex = choice( range(26) )    #range 16 because 700r is 4 charcters long. So 30 - 4
        endIndex = startIndex + 4

        fHalf = tempToken[0:startIndex]     #Get everthing before start index
        sHalf = tempToken[endIndex:-1]      #Get everthing after end index

        phishToken = fHalf + '700r' + sHalf     #Embed phishing identifier inbetween.

        return phishToken
    



    @classmethod
    def sendAnalytics(self, xlsxPath: str, campaign: Campaign):
        try:
            content = open(xlsxPath, 'rb').read()   
            encodedContent = b64encode(content).decode('utf-8')

        except FileNotFoundError:   #There really shouldn't ever occur since we pass in the xlsxPath :)
            return FileNotFoundError('File not found')
        
        endpoint = 'https://api.postmarkapp.com/email'
    
        email = config('ANALYTICS_LIVE_EMAIL') if config('LIVE', cast=bool) else config('ANALYTICS_TEST_EMAIL')

        auth = {
                'X-Postmark-Server-Token' : config('POSTMARK_SERVER_TOKEN')
        }

        
        html = f'<p>Analytics report for {campaign.name} campaign, created {campaign.created} GMT</p>'
        txt = f'Analytics report for {campaign.name} campaign, created {campaign.created} GMT'

        payload = {
            'From': 'noreply@aurisonn.app',
            'To': email,
            'Subject': f'Analytics Report For {campaign.name} Campaign',
            'HtmlBody': html,
            'TextBody': txt,
            'MessageStream': config('POSTMARK_ANALYTICS_STREAM'),
            "Attachments": [
                {
                "Name": "analytics.xlsx",
                "Content": encodedContent,
                "ContentType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "ContentEncoding": "base64"
                },
            ]
        }

        try:
            res = post(endpoint, json=payload, headers=auth)

            # if int(res.status_code) > 300: #something wrong occurred :(
            #     print(res)
            #     print(res.json())
        except Exception as e:
            print(e)

            return False



