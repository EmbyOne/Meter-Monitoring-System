from django.http import HttpResponse
import requests
from .models import Meter, Archive, Alert
import json
from django.utils import timezone
from datetime import timedelta
import time

ultraSecretApiKey = '9e70c43d19034a0cbd246eb2444c40d7' #for Azure

#reset the tables
Meter.objects.all().delete()
Archive.objects.all().delete()
Alert.objects.all().delete()

mockapiurl = 'http://localhost:8000/ofc' #not in use

apiurl = 'https://westeurope.api.cognitive.microsoft.com/vision/v3.2/read/analyze/'

#This one big view contains most of the api logic
def bigApiView(request):
    #If this is gonna be the first entry, get the time for later use
    if Archive.objects.exists() == False:
        global starttime
        starttime = timezone.now()

    timeval = timezone.now() # used to that archive and meter match dates

    #1ST REQUEST
    #get the image url from request params
    url = request.GET.get('url')
    data = {'url': url}
    #set custom headers
    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': ultraSecretApiKey}
    requrl = apiurl
    #send json request to azure api
    r = requests.post(requrl, json=data, headers=headers)
    #get the link that we need to see results in json data
    enigma = r.headers
    print(enigma)
    enigmalink = enigma['Operation-Location']

    time.sleep(5) #ensure that azure has time to process, since ratelimiting and slow connection

    #SECOND REQUEST
    headers = {'Ocp-Apim-Subscription-Key': ultraSecretApiKey}
    r = requests.get(enigmalink, headers=headers)

    #debugging info
    print(r.json())
    print(r.json()['analyzeResult']['readResults'][0]['lines'][0]['text'])

    #get digit from json data response
    number = int(r.json()['analyzeResult']['readResults'][0]['lines'][0]['text'])

    if Meter.objects.exists():
        oldnum = Meter.objects.latest('time').value

        #find difference
        delta = number - oldnum
        print(delta) 

        value = delta
    else:
        value = number
    
    #save digit to database along with time of creation
    water = Meter.objects.create(value=value, time=timeval)
    #archive it as well
    archive = Archive.objects.create(value=value, time=timeval)
    water.save
    archive.save


    #get all the meter values
    values = Meter.objects.values_list('value')

    #Hacky fix for tuple issue in database entries
    realvals = []
    for i in values:
        realvals.append(i[0])
    
    print(realvals)

    #if it has been over 24 hours since the first entry and delta hasnt been 0 in the last 24 hours, trigger alarm
    if (0 not in realvals) & (timezone.now() - starttime >= timedelta(hours=24)) :
        Alert.objects.create(tragedy=archive.id)
    #Show current alerts since uptime in HttpResponse
    if Alert.objects.exists():
        badlist = ''
        for record in Alert.objects.all():
            epicid = record.tragedy
            badlist = badlist + Archive.objects.get(pk=epicid).time.strftime('%c') + ' '
        
        #response based on cases of leaks
        resptext = 'Leaks have been noted on the following dates: ' + badlist
    else:
        resptext = 'No leaks have been detected during system uptime.'
    return HttpResponse(resptext)