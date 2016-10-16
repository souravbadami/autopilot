#!usr/bin/env python
from __future__ import print_function
from bs4 import BeautifulSoup
from gi.repository import Notify
import re
from mechanize import Browser
import time
import urllib
import urllib2

changed = 0

def started():
    Notify.init("Status Check Initiated")
    Notify.Notification.new("\nAutoPilot"," Passport Status Bot Activated.").show()

def start_bot():
    while changed!= 1:
        started()
        main()
        if changed == 1:
            notify()
        time.sleep(3600) # change the checking frequency here (in sec).
 
def notify():
    Notify.init("Status Changed")
    Notify.Notification.new("\nAutoPilot"," Passport Status Changed.").show()

def main():
    global changed
    target = 'https://portal1.passportindia.gov.in/AppOnlineProject/statusTracker/trackStatusInpNew'
    fileNo = '' # file number
    applDob = '' # dd/mm/yyyy
    currentStatus = '' # copy & paste current application status
    nav = Browser()
    nav.set_handle_robots( False )
    nav.addheaders = [('User-agent', 'Firefox')]
    nav.open(target)
    nav.select_form( 'trackStatus' )
    nav.form[nav.controls[0].name] = ['Application_Status']
    nav.form[nav.controls[1].name] = fileNo
    nav.form[nav.controls[2].name] = applDob
    response = BeautifulSoup(nav.submit())
    tableClass = response.find("div", attrs={"class":"block_right_inner"})
    table = tableClass.find("table", attrs={"role":"presentation"})
    tdVal = table.find("td", attrs={"":""}).get_text()
    if currentStatus not in tdVal:
    	changed = 1

if __name__ == '__main__':
	start_bot()