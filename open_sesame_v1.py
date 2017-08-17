"""
Monash Sunway Wi-Fi auto login page
"""
# Written by Chin Er Win 15 Aug 2017
# Latest update: UI Upgrade
# 
# This script requires use of:
# 1. Selenium (sudo pip install selenium)
# 2. phantomJS (https://github.com/fg2it/phantomjs-on-raspberry/tree/master/rpi-2-3/wheezyjessie/v2.1.1)
# 3. speedtest-cli (sudo pip install speedtest-cli)
#
# Notes:
# The Wi-Fi portal page has 3 possible pages: LOGIN,LOGOUT,LOGOUT2
# Accessing the url https://wifi.monash.edu.my/, will always load LOGIN page
#
# Addition Reading:
# For speedtest-cli - https://github.com/sivel/speedtest-cli/wiki
# use 'dir' command to view contents of objects
# instead of phantomJS, other browsers have webdrivers that support selenium can be used


import sys
import time
from selenium import webdriver

AUTHCATE_USER = '"**user**"'
AUTHCATE_PASS = '"**password**"'

# COUNTDOWN_RECONNECT_SECONDS      - Time before it relogs to avoid 12 hours timeout
# COUNTDOWN_CHECK_SECONDS          - Time before it runs the Connection Checker (checks its connection to https://www.google.com)
# COUNTDOWN_FAILURETIMEOUT_SECONDS - Time it waits before reconnecting if it fails Connection Checker
# TIME_FOR_PAGE_TO_LOAD            - Time it waits for page to load (might be too short if Wi-Fi/Server is slow)
# URL_WIFI_PORTAL_PAGE             - Wi-Fi url page
# IP_GOOGLE_DNS                    - For checking internet connection
COUNTDOWN_RECONNECT_SECONDS = 11*60*60 # Recommended 11 hours
COUNTDOWN_CHECK_SECONDS = 10*60 # Recommended 10 minutes
COUNTDOWN_FAILURETIMEOUT_SECONDS = 5*60 # Recommended 5 minutes
TIME_FOR_PAGE_TO_LOAD = 5 # Recommended 5 Seconds
URL_WIFI_PORTAL_PAGE = 'https://wifi.monash.edu.my'
URL_INTERNET_PAGE = 'https://www.google.com/'
STRING_INTERNET_PAGE_TITLE = 'Google'

# JAVASCRIPT TO INJECT
JAVASCRIPT_login_fill = 'var username=document.getElementById("LoginUserPassword_auth_username");var password=document.getElementById("LoginUserPassword_auth_password");username.value = '
JAVASCRIPT_login_fill += AUTHCATE_USER
JAVASCRIPT_login_fill += ';password.value = '
JAVASCRIPT_login_fill += AUTHCATE_PASS
JAVASCRIPT_login_fill += ';'
JAVASCRIPT_login_submit = 'oAuthentication.submitActiveForm();'
JAVASCRIPT_logout_submit = 'oAuthentication.submitActiveForm();'
JAVASCRIPT_logout2_regain = 'location="Reset";'

HTML_login_LogOut_button = 'UserCheck_Logoff_Button_span'
HTML_login_error_msg = 'LoginUserPassword_error_message'
HTML_google_title = 'Google'

# Web browsing functions

class MyError2(Exception):
    """
    Exception Class for Load,Login,Internet Tests
    """
    def __init__(self, mismatch):
        Exception.__init__(self, mismatch)

def load_page_test():
    """
    Test load page
    """
    try:
        browser.get(URL_WIFI_PORTAL_PAGE)
        time.sleep(TIME_FOR_PAGE_TO_LOAD)
        browser.save_screenshot('open_sesame_login_page.png')
    except:
        raise MyError2("Cannot Load Page (Wi-Fi may be down)")

def login_fill_and_submit_test():
    """
    Test login process
    """
    try:
        browser.execute_script(JAVASCRIPT_login_fill)
        browser.save_screenshot('open_sesame_login_fill.png')
        browser.execute_script(JAVASCRIPT_login_submit)
        time.sleep(TIME_FOR_PAGE_TO_LOAD)
        browser.save_screenshot('open_sesame_login_submit.png')
    except:
        raise MyError2("Cannot Input/Submit User and Pass (Page might have changed)")


def login_test():
    """
    Test successful login
    """
    try:
        browser.find_element_by_id(HTML_login_LogOut_button)###WIP
    except:
        try:
            error = browser.find_element_by_id(HTML_login_error_msg)###WIP
        except:
            raise MyError2("Unknown Page after Submit")
        else:
            print(error.text)
            raise MyError2("Wrong User and/or Password")

def internet_test():
    """
    Test internet connection
    """
    try:
        browser.get(URL_INTERNET_PAGE)
        time.sleep(TIME_FOR_PAGE_TO_LOAD)
        title = browser.title###WIP
        if title != STRING_INTERNET_PAGE_TITLE:
            raise MyError2("Imposter! This is not Google!")
    except:
        raise MyError2("Internet Not Working")

def save_page():
    """
    Saves screenshot of browser
    """
    browser.save_screenshot('open_sesame_latest.png')

def print_fail1():
    """
    Set Timeout
    """
    sys.stdout.write('\nCannot Load Wi-Fi Page! Reconnect after '+str(COUNTDOWN_FAILURETIMEOUT_SECONDS)+' seconds\n')
    time.sleep(COUNTDOWN_FAILURETIMEOUT_SECONDS)

sys.stdout.write('\nStarting: open_sesame.py\n')
#-------#
# SETUP #
#-------#
browser = webdriver.PhantomJS() # Change if using other webdrivers e.g. Firefox-geckodriver or Chromium-ChromeDriver
fail_count = 0


#------#
# LOOP #
#------#
for n in range(0,3):
    internet_state = False
    load_state = False
    while(not load_state):
        # Login page
        # Check if Wi-Fi Portal Page is loaded
        try:
            load_page_test()
            login_fill_and_submit_test()
            login_test()
            internet_test()
        except MyError2 as problem:
            print "Load,Login Problem : {0}".format(problem)
        else:
            load_state = True
#        # Check if Internet is up

    # Countdown Timer Init
    fail = False
    string_restart_number = "\nRestart Counter: " + str(n) + "\n"
    sys.stdout.write(string_restart_number)
    seconds_start = time.time()
    seconds_end = seconds_start + COUNTDOWN_RECONNECT_SECONDS
    time_start = time.localtime(seconds_start)
    time_end = time.localtime(seconds_end)
    string_time_start = "Start time:" + time.asctime(time_start)+"\n"
    string_time_end = "End time: " + time.asctime(time_end)+"\n"
    sys.stdout.write(string_time_start)
    sys.stdout.write(string_time_end)
    seconds_now = time.time()
    seconds_left = round(seconds_end - seconds_now)

    # Countdown Timer Run
    seconds_tocheck = 0
    while seconds_left > 0 : 
        seconds_now = time.time()
        seconds_left = round(seconds_end - seconds_now)
        h = int(seconds_left/(60*60))
        m = int((seconds_left%(60*60))/60)
        s = int(seconds_left%60)
        if h<10:
            h_str = "0"+str(h)
        else:
            h_str = str(h)
        if m<10:
            m_str = "0"+str(m)
        else:
            m_str = str(m)
        if s<10:
            s_str = "0"+str(s)
        else:
            s_str = str(s)
        string_time_left = "Time Left Before Reconnect: " + h_str+" : "+m_str+" : "+s_str 
        
        # Connection Checker
        seconds_tocheck += 1
        if  seconds_tocheck>COUNTDOWN_CHECK_SECONDS-1:
            save_page()
            string_time_left += " - Connection Last Checked: " + time.asctime(time.localtime(seconds_now)) + " : "
            try:
                internet_test():
            except:
                string_time_left += "FAIL"
                fail = True
                fail_count += 1
                seconds_left = 0
            else:
                string_time_left += "PASS"
            seconds_tocheck = 0
        sys.stdout.write(string_time_left)
        sys.stdout.write('\r')
        sys.stdout.flush()
        time.sleep(1)
    
    #Connection Failure Timeout 
    if fail:
        sys.stdout.write('\nNo Internet! Reconnect after '+str(COUNTDOWN_FAILURETIMEOUT_SECONDS)+' seconds\n')
        time.sleep(COUNTDOWN_FAILURETIMEOUT_SECONDS)
    else:
        sys.stdout.write('\nReconnect Timer Ended. Reconnecting now.\n')

sys.stdout.write('\n\nEnding: open_sesame.py\n')
