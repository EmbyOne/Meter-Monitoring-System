# Meter-Monitoring-System

takes an image url (picture of water meter) input from server.host/api?url=<urlfield> and proccesses it with azure's ocr to recognize digits in the image. Saves the delta (change of flowthrough) to a database with a timestamp and outputs an alarm if delta doesn't hit 0 even once in 24 hours, indicating a leak 
