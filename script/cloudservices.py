import json, urllib.request, socket, smtplib
from datetime import datetime

def sendEmail(name, reason, text):
   FROM = 'from@domain.com'
   TO  = 'user@domain.com'
   SUBJECT = name + " is: \"" + reason + "\""
   message = """\From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, TO, SUBJECT, text)
   server = smtplib.SMTP('smtpserver.local', 25)
   server.sendmail(FROM, TO, message)
   server.quit()

def log(name, status):
   now = str(datetime.now()).split('.')[0]
   with open('D:/sites/cloudservices/cslog.txt', "a") as logfile:
      logfile.write(str(now + " - " + name + " - " + status + "\n"))

json_data = json.load(open('D:/sites/cloudservices/csstatus.json'))
urls = json_data["urls"]
       
for url in urls:
   code = url["code"]
   url["lastCode"] = code
   lastCode = url["lastCode"]
   name = url["name"]
   reason = url["reason"]
   protocol = url["protocol"]
   
   try:
      fullURL = protocol + "://" + name
      response = urllib.request.urlopen(fullURL, timeout=10)
      if lastCode != "200":
         sendEmail(name, "GOOD", "It used to be bad.")
         log(name, "GOOD")
      newCode = str(response.getcode())
      newReason = "GOOD"
   except:
      newReason = "BAD"
      if lastCode == "200":
         sendEmail(name, newReason, "It used to be good.")
         log(name, "BAD")
      newCode = "-1"

   url["code"] = newCode
   url["reason"] = newReason

with open('D:/sites/cloudservices/csstatus.json', "w") as outfile:
   json.dump(json_data, outfile)
