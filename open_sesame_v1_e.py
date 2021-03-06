"""
Monash Sunway Wi-Fi auto login page
"""
# Written by Chin Er Win 15 Aug 2017 last updated 6/9/2017
# Latest update: Testing woeking with Raspbian Stretch
#
# This script requires use of:
# 1. Selenium (sudo pip install selenium)
# For Rpi3 Users:
# 2. phantomJS (https://github.com/fg2it/phantomjs-on-raspberry/tree/master/rpi-2-3/wheezy-jessie/v2.1.1)
# For Ubuntu Users:
# 2. phantomJS (https://gist.github.com/julionc/7476620)
# WARNING! DO NOT sudo apt-get install phantomJS it is a non working version
# Notes:
#
# This script accesses the url and uses JavaScript injection to load, login and submit the pages
# Screenshots of the browser are saved for easier debugging 
# 
#
# Addition Reading:
# Accessing the url https://wifi.monash.edu.my/, will always load LOGIN page
# Timeouts are needed to let the page to load (web pages dont load instantly!)
# WARNING! Only one instance of the script must be running else it may cause 'session expired' login failures!
# use 'dir' command to view contents of objects
# instead of phantomJS, other browsers have webdrivers that support selenium can be used

AUTHCATE_USER = '**user**'
AUTHCATE_PASS = '**password**'
EMAIL_FROM = '@gmail.com'
EMAIL_FROM_PASS = 'emailpassword'
EMAIL_TO = '@gmail.com'
rpi3 = 1 # 1 for rpi 0 for no rpi
IP_interface = 'wlan0' #eth0 for ethernet

try:
    import requests
    import sys
    import time
    import smtplib
    from email.mime.text import MIMEText
    # To get IP address
    import socket,fcntl,struct
    if rpi3:
        import os
except:
    print('One or More libaries are not found!')
    exit()

try:
    from selenium import webdriver
except:
    print('Selenium not found!')
    exit()

# NUMBER_OF_RESTARTS               - Number of times script will restart before exiting
# NUMBER_OF_MAXFAILS               - Number of times it will try to reconnect before waiting COUNTDOWN_WAIT_SECONDS 
# COUNTDOWN_RECONNECT_SECONDS      - Time before it relogs to avoid 12 hours timeout
# COUNTDOWN_CHECK_SECONDS          - Time before it runs the Connection Checker (checks its connection to https://www.google.com)
# COUNTDOWN_TIMEOUT_SECONDS - Time it waits before reconnecting if it fails Connection Checker
# COUNTDOWN_WAIT_SECONDS    - Time it waits before reconnecting if it fail counter reaches NUMBER_OF_MAXFAILS
# TIME_FOR_PAGE_TO_LOAD            - Time it waits for page to load (might be too short if Wi-Fi/Server is slow)
# URL_WIFI_PORTAL_PAGE             - Wi-Fi url page
# URL_INTERNET_PAGE                - For checking internet connection
NUMBER_OF_RESTARTS = 1000 # Number of restarts before exiting
NUMBER_OF_MAXFAILS = 5 # Number of login faills before sleeping
COUNTDOWN_RECONNECT_SECONDS = 11*60*60 # Recommended 11 hours
COUNTDOWN_CHECK_SECONDS = 10*60 # Recommended 10 minutes
COUNTDOWN_TIMEOUT_SECONDS = 10 # Recommended 10 seconds
COUNTDOWN_WAIT_SECONDS = 5*60 # Recommended 5 minutes
TIME_FOR_PAGE_TO_LOAD = 2 # Recommended 2 Seconds
URL_WIFI_PORTAL_PAGE = 'https://wifi.monash.edu.my'
URL_INTERNET_PAGE = 'https://www.google.com/'

# JAVASCRIPT TO INJECT
JAVASCRIPT_login_fill = 'var username=document.getElementById("LoginUserPassword_auth_username");var password=document.getElementById("LoginUserPassword_auth_password");username.value = "'
JAVASCRIPT_login_fill += AUTHCATE_USER
JAVASCRIPT_login_fill += '";password.value = "'
JAVASCRIPT_login_fill += AUTHCATE_PASS
JAVASCRIPT_login_fill += '";'
JAVASCRIPT_login_submit = 'oAuthentication.submitActiveForm();'
JAVASCRIPT_logout_submit = 'oAuthentication.submitActiveForm();'
JAVASCRIPT_logout2_regain = 'location="Reset";'
# HTML ELEMENTS TO INTERACT WITH
HTML_login_LogOut_button = 'UserCheck_Logoff_Button_span'
HTML_login_error_msg = 'LoginUserPassword_error_message'
HTML_login_error_msgtext = 'Username or password incorrect'
# Stores Current IP Address
IP_HOST = ''

# Functions
class MyError2(Exception):
    """
    Exception Class for Custom Exceptions
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

def javascript_test():
    """
    Test javascript
    """
    try:
        browser.execute_script("var test_javascript = 1;")
    except:
        raise MyError2("Cannot execute Javascript!")

def login_fill_and_submit_test():
    """
    Test login process
    """
    try:
        browser.refresh()
        time.sleep(TIME_FOR_PAGE_TO_LOAD)
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
        print('Error Logging In')
        try:
            error = browser.find_element_by_id(HTML_login_error_msg)###WIP
        except:
            print("Unknown Page after Submit")
        else:
            print(error.text)
            if error.text == HTML_login_error_msgtext:
                exit()
        raise MyError2('Login Test failed')

def internet_test():
    """
    Test internet connection
    """
    try:
        response = requests.get(URL_INTERNET_PAGE,timeout=10)
        if response.status_code != requests.codes.ok:
            print('ERROR! Status Code - '+response.status_code)
            raise MyError2("Internet Not Working!(Wrong Status Code)")
    except:
        raise MyError2("Internet Not Working!(Timeout)")
def save_page():
    """
    Saves screenshot of browser
    """
    browser.save_screenshot('open_sesame_latest.png')

def email_IP(email_text):
    """
    Email IP
    """
    msg = MIMEText(email_text)
    msg['Subject'] = 'IP Address Update'
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.ehlo()
    server.login(EMAIL_FROM, EMAIL_FROM_PASS)
    server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    server.quit()
    return text

def get_hw_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

print('\nStarting: open_sesame.py\n')
#-------#
# SETUP #
#-------#
try:
    browser = webdriver.PhantomJS() # Change if using other webdrivers e.g. Firefox-geckodriver or Chromium-ChromeDriver
except:
    print('PhantomJS not found!')
    exit()
fail_count = 0
fail_load = 0

#------#
# LOOP #
#------#
for n in range(0,NUMBER_OF_RESTARTS):
    internet_state = False
    load_state = False
    while(not load_state):
        # Login page
        # Check if Wi-Fi Portal Page is loaded
        try:
            print('Loading Page')
            load_page_test()
            print('Test Javascript')
            javascript_test()
            print('Submit Page')
            login_fill_and_submit_test()
            print('Test login')
            login_test()
            print('Test internet')
            internet_test()
        except MyError2 as problem:
            print("Load,Login,Internet Problem : {0}".format(problem))
            fail_load += 1
            print('\n'+str(fail_load)+': Cannot Load Wi-Fi Page! Reconnect after '+str(COUNTDOWN_TIMEOUT_SECONDS)+' seconds\n')
            time.sleep(COUNTDOWN_TIMEOUT_SECONDS)
            if fail_load > NUMBER_OF_MAXFAILS:
                print('Number of fails exceeded, Reconnect after '+str(COUNTDOWN_WAIT_SECONDS)+' seconds\n')
                time.sleep(COUNTDOWN_WAIT_SECONDS)
                if rpi3:
                    os.system('sudo reboot')
                    exit()
                fail_load = 0
        else:
            load_state = True

    # Countdown Timer Init
    fail = False
    string_restart_number = "\nRestart Counter: " + str(n) + "\n"
    print(string_restart_number)
    seconds_start = time.time()
    seconds_end = seconds_start + COUNTDOWN_RECONNECT_SECONDS
    time_start = time.localtime(seconds_start)
    time_end = time.localtime(seconds_end)
    string_time_start = "Start time: " + time.asctime(time_start)
    string_time_end = "End time: " + time.asctime(time_end)
    print(string_time_start)
    print(string_time_end)
    seconds_now = time.time()
    seconds_left = round(seconds_end - seconds_now)
    
    IP_HOST_new = get_ip_address(IP_interface)
    if IP_HOST != IP_HOST_new:
        IP_HOST = IP_HOST_new
        try:
            text = 'At time : ' + time.asctime(time_start) +'\n'
            text += 'The Raspberry Pi with MAC: ' + get_hw_address(IP_interface) + '\n'
            text += 'Has reconnected with New IP address is : '+ IP_HOST   
            text = email_IP(text)
        except:
            print('Email Failed!')
        else:
            print('Email Sent to :' + EMAIL_TO)
            print(text)
    
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
        string_time_left = "Time to Reconnect: " + h_str+" : "+m_str+" : "+s_str 
        
        # Connection Checker
        seconds_tocheck += 1
        if  seconds_tocheck>COUNTDOWN_CHECK_SECONDS-1:
            save_page()
            string_time_left += " - Last Checked: " + time.asctime(time.localtime(seconds_now)) + " : "
            try:
                internet_test()
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
        print('\nNo Internet! Reconnect after '+str(COUNTDOWN_TIMEOUT_SECONDS)+' seconds\n')
        time.sleep(COUNTDOWN_TIMEOUT_SECONDS)
    else:
        print('\nReconnect Timer Ended. Reconnecting now.\n')

print('\n\nEnding: open_sesame.py\n')

if rpi3:
    os.system('sudo reboot')

exit()
