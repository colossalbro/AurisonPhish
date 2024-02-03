from celery import shared_task
from os import remove
    
    
@shared_task
def deleteFile(path: str):
    try:
        remove(path)
    except OSError as e:
        print(e)        #Honestly should consider adding a log file.




