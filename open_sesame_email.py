"""
Email Ip address
"""

import smtplib
import commands
from email.mime.text import MIMEText

EMAIL1 = '****@gmail.com'
PASS = '******Password****'
EMAIL2 = '****@gmail.com'

from_x = EMAIL1
to_y = EMAIL2

IP = commands.getoutput('hostname -I')
msg = MIMEText('My New IP address is : '+ IP)
msg['Subject'] = 'IP Address Update'
msg['From'] = from_x
msg['To'] = to_y

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.ehlo()
server.login(EMAIL, PASS)
server.sendmail(from_x, to_y, msg.as_string())
server.quit()
