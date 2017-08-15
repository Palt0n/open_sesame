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
# test222
# test333
# test444
# test 777
# push it


import sys
import time
from selenium import webdriver
try:
    import httplib
except:
    import http.client as httplib


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

# JAVASCRIPT TO INJECT
JAVASCRIPT_login_fill = 'var username=document.getElementById("LoginUserPassword_auth_username");var password=document.getElementById("LoginUserPassword_auth_password");username.value = '
JAVASCRIPT_login_fill += AUTHCATE_USER
JAVASCRIPT_login_fill += ';password.value = '
JAVASCRIPT_login_fill += AUTHCATE_PASS
JAVASCRIPT_login_fill += ';'
JAVASCRIPT_login_submit = 'oAuthentication.submitActiveForm();'
JAVASCRIPT_logout_submit = 'oAuthentication.submitActiveForm();'
JAVASCRIPT_logout2_regain = 'location="Reset";'

# Web browsing functions
def init_driver():
    driver = webdriver.PhantomJS() # Change if using other webdrivers e.g. Firefox-geckodriver or Chromium-ChromeDriver
def load_page():
    driver.get(URL_WIFI_PORTAL_PAGE)
    time.sleep(TIME_FOR_PAGE_TO_LOAD)
    driver.save_screenshot('open_sesame_login_page.png')
def login_fill():
    driver.execute_script(JAVASCRIPT_login_fill)
    driver.save_screenshot('open_sesame_login_fill.png')
def login_submit():
    driver.execute_script(JAVASCRIPT_login_submit)
    time.sleep(5)
    driver.save_screenshot('open_sesame_login_submit.png')
def save_page():
    driver.save_screenshot('open_sesame_latest.png')
# Internet Testing function
def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False
#


sys.stdout.write('\nStarting: open_sesame.py\n')
#-------#
# SETUP #
#-------#
init_driver()
fail_count = 0

#------#
# LOOP #
#------#
for n in range(0,3):
    internet_state = False
    while(not internet_state):
        # Login page
        # Check if Wi-Fi Portal Page is loaded
        try:
            load_page()
            login_fill()
            login_submit()
            save_page()
        except:
            sys.stdout.write('\nCannot Load Wi-Fi Page! Reconnect after '+str(COUNTDOWN_FAILURETIMEOUT_SECONDS)+' seconds\n')
            time.sleep(COUNTDOWN_FAILURETIMEOUT_SECONDS)
        else:# Check if Internet is up
            internet_state = have_internet()
            if internet_state:
                sys.stdout.write('\nSuccessfully Connected to the internet.')
            else: 
                sys.stdout.write('\nNo Internet! Reconnect after '+str(COUNTDOWN_FAILURETIMEOUT_SECONDS)+' seconds\n')
                time.sleep(COUNTDOWN_FAILURETIMEOUT_SECONDS)
#        
    
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
            if have_internet():
                string_time_left += "PASS"
            else:
                string_time_left += "FAIL"
                fail = True
                fail_count += 1
                seconds_left = 0
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
