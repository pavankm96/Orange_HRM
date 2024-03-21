from playwright.sync_api import Page, expect,sync_playwright
import time
import pandas as pd
from bs4 import BeautifulSoup

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(sender_email, sender_password, receiver_emails, subject, message, attachment_paths):
    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_emails)
    msg['Subject'] = subject

    # Attach message
    msg.attach(MIMEText(message, 'plain'))

    # Attach files
    for attachment_path in attachment_paths:
        filename = attachment_path.split('/')[-1]
        attachment = open(attachment_path, "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}",)
        msg.attach(part)

    # Connect to the SMTP server
    server = smtplib.SMTP('your.mail.smtp', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send email
    text = msg.as_string()
    server.sendmail(sender_email, receiver_emails, text)
    server.quit()

def test_orange_login():
    with sync_playwright() as page:
        browser = page.chromium.launch()
        page = browser.new_page()
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        time.sleep(10)
        page.type('input[name="username"]', 'Admin')
        page.type('input[name="password"]', 'admin123')
        page.keyboard.press('Enter')
        time.sleep(3)
        page.click('//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[1]')
        time.sleep(2)
        admin=page.inner_html('//*[@id="app"]/div[1]/div[2]/div[2]/div/div[2]/div[3]/div/div[2]')
        #admin=pd.read_html(admin)
        #print(admin)
        bs=BeautifulSoup(admin,'html.parser')
        emp_list=len(bs.find_all(class_="oxd-table-row oxd-table-row--with-border")[0])
        username=[]
        userrole=[]
        ename=[]
        status=[]
        admin_report={'Username':username,'User Role':userrole,'Employee':ename,'Status':status}
        #root_html=bs.find_all(class_="oxd-table-row oxd-table-row--with-border")[0].find_all('div',class_="oxd-table-cell oxd-padding-cell")[1].get_text()
        for i in range(emp_list):
            username.append(bs.find_all(class_="oxd-table-row oxd-table-row--with-border")[i].find_all('div',class_="oxd-table-cell oxd-padding-cell")[1].get_text())
            userrole.append(bs.find_all(class_="oxd-table-row oxd-table-row--with-border")[i].find_all('div',class_="oxd-table-cell oxd-padding-cell")[2].get_text())
            ename.append(bs.find_all(class_="oxd-table-row oxd-table-row--with-border")[i].find_all('div',class_="oxd-table-cell oxd-padding-cell")[3].get_text())
            status.append(bs.find_all(class_="oxd-table-row oxd-table-row--with-border")[i].find_all('div',class_="oxd-table-cell oxd-padding-cell")[4].get_text())
        admin_report={'Username':username,'User Role':userrole,'Employee':ename,'Status':status} 
        page.click('//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[2]/a/span')
        pim=page.inner_html('//*[@id="app"]/div[1]/div[2]/div[2]/div/div[2]/div[3]/div/div[2]')
        print(pim)
        bsp=BeautifulSoup(pim,'html.parser')
        root_pim=bsp.find_all(class_="oxd-table-row oxd-table-row--with-border oxd-table-row--clickable")[0].find_all('div',class_="oxd-table-cell oxd-padding-cell")[1].get_text()
        emp_list_pim=len(bsp.find_all(class_="oxd-table-row oxd-table-row--with-border oxd-table-row--clickable"))
        id=[]
        fname=[]
        lname=[]
        pim_report={'ID':id,'First Name':fname,'Last Name':lname}
        for i in range(emp_list_pim):
            id.append(bsp.find_all(class_="oxd-table-row oxd-table-row--with-border oxd-table-row--clickable")[i].find_all('div',class_="oxd-table-cell oxd-padding-cell")[1].get_text())
            fname.append(bsp.find_all(class_="oxd-table-row oxd-table-row--with-border oxd-table-row--clickable")[i].find_all('div',class_="oxd-table-cell oxd-padding-cell")[2].get_text())
            lname.append(bsp.find_all(class_="oxd-table-row oxd-table-row--with-border oxd-table-row--clickable")[i].find_all('div',class_="oxd-table-cell oxd-padding-cell")[3].get_text())
        pim_report={'ID':id,'First Name':fname,'Last Name':lname}
        print(pim_report)  
        admin_report=pd.DataFrame(admin_report)
        pim_report=pd.DataFrame(pim_report)
        admin_report.to_csv('admin_report.csv',index=False)
        pim_report.to_csv('pim_report.csv',index=False) 

        # Example usage
        sender_email = 'xyz@abc.com'
        sender_password = 'your password'
        receiver_emails = ['xyz@abc.com','xyz@abc.com']
        subject = 'Test HR Reports'
        message = 'This is a HR Report PFA report.'
        attachment_paths = ['admin_report.csv','pim_report.csv']
        send_email(sender_email, sender_password, receiver_emails, subject, message, attachment_paths)
        browser.close()
    #playwright.stop()
    
