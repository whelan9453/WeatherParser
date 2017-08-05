import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display
import os


def send_mail(content):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    gmailUser = os.environ['sender']
    gmailPassword = = os.environ['sender_pwd']
    recipient = os.environ['recipient']

    msg = MIMEMultipart('alternative')
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = 'Today\'s weather briefing'
    msg.attach(MIMEText(content, 'plain'))

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)
    mailServer.sendmail(gmailUser, recipient, msg.as_string())
    mailServer.close()


#Remote VMs do not have displays
display = Display(visible=0, size=(800, 600))
display.start()

url = 'http://www.cwb.gov.tw/V7/forecast/taiwan/Taipei_City.htm'
#Prepare soup
r = requests.get(url)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')

#Get the city list
# for city in soup.findAll('option'):
#     print(city['value'])

#Prepare web driver and scrape weather information
driver = webdriver.Firefox()
driver.get(url)
html = driver.execute_script("return document.documentElement.outerHTML")
sel_soup = BeautifulSoup(html, 'html.parser')
res = sel_soup.find('div', {'id': 'ftext'})
driver.close()

#send email
send_mail(res.text)

