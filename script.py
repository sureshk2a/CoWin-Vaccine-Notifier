'''
Script: Covid Vaccine Slot Availability Notifier
By Ayushi Rawat
'''

import requests
from pygame import mixer 
from datetime import datetime, timedelta
import time


age = 25
pincodes = ["627604"]
num_days = 2

print_flag = 'Y'

print("Starting search for Covid vaccine slots!")

actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]

while True:
    counter = 0   

    for pincode in pincodes:   
        for given_date in actual_dates:

            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, given_date)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
            
            result = requests.get(URL, headers=header)

            if result.ok:
                response_json = result.json()
                if len(response_json["centers"]) != 0:
                    if(print_flag.lower() =='y'):
                        for center in response_json["centers"]:
                            for session in center["sessions"]:
                                if (session["min_age_limit"] <= age and session["available_capacity"] > 0 ) :
                                    print('Pincode: ' + pincode)
                                    print("Available on: {}".format(given_date))
                                    print("\t", center["name"])
                                    print("\t", center["block_name"])
                                    print("\t Price: ", center["fee_type"])
                                    print("\t Availablity : ", session["available_capacity"])

                                    if(session["vaccine"] != ''):
                                        print("\t Vaccine type: ", session["vaccine"])
                                    print("\n")
                                    counter = counter + 1
                else:
                    print("No vaccination centres available on: {} for the pincode: {}".format(given_date,pincode))
            else:
                print("No Response!")
                
    if counter:
        print("No Vaccination slot available!")
    else:
        mixer.init()
        mixer.music.load('sound/dingdong.wav')
        mixer.music.play()
        print("Search Completed!")

    dt = datetime.now() + timedelta(minutes=3)

    while datetime.now() < dt:
        time.sleep(1)
