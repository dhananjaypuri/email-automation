from urllib import response
import requests
import datetime
import pytz

cust = datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata')).date();

todaydate = datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata')).date();

newdate = datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata')).date().strftime('%Y-%m-%d');
print(newdate);
response = requests.get(url=f'http://127.0.0.1:8000/sendmail2/{newdate}');

if(cust == todaydate):
    print("Dates are eqaul");
else:
    print("Dates are not equal");

