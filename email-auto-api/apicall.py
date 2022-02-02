import requests
import datetime
import pytz

response = requests.get(url='http://127.0.0.1:8000/sendmail');

if(response.status_code == 200):
    print("Mail sent Successfully ");
else:
    print("Server Not working");
