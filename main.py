# -*- coding: utf-8 -*-
import csv
import datetime
import mimetypes
import SETTINGS
import shutil
import smtplib

from email.message import EmailMessage
from email.utils import make_msgid
from getpass import getpass

def install():
    command = "cd ~; cd ./"+SETTINGS.RELATIVE_PATH_TO_MAIN_PY_FOLDER+"; python main.py"
    with open('goto.ps1','w') as file:
        file.writelines(command)

def enter_password():
    string = "Enter password for "+SETTINGS.LOGIN+": "
    secret = getpass(string)
    return secret

def check_if_opened(*args):
    while True:
        try:
            for filename in args:
                csv_file = open(filename+".csv",'a')
                csv_file.close()
            return True
        except:
            print("Close your csv files and click Enter.")
            input()

def create_mailing_list():
    today = datetime.date.today()
    mailing_list = []
    
    with open(SETTINGS.DATABASE_NAME+".csv",'r',newline='\n') as csvfile:
        database = csv.reader(csvfile, delimiter=';', quotechar='|')
        
        print("Looking for possible recipients...")
        for row in database:
            company_name, email_address, date_of_occurence, years_to_remind_after = row
            due_date_year, due_date_month, due_date_day = [int(ymd) for ymd in date_of_occurence.split("-")]
            if due_date_month == 2 and due_date_day == 29:
                due_date_day = 28 #exception for February 29th which is not every year
            due_datetime = datetime.date(due_date_year+int(years_to_remind_after),due_date_month,due_date_day)
            day_difference = due_datetime - today
            
            if day_difference <= datetime.timedelta(days=SETTINGS.SEND_UP_TO_X_DAYS_BEFORE_DUE_DATE) and day_difference >= datetime.timedelta(days=-SETTINGS.SEND_UP_TO_X_DAYS_AFTER_DUE_DATE):
                mailing_list += [row]
                
    if len(mailing_list) > 0:
        print("\nEmails will be send to {number_of_recievers} recipients.".format(number_of_recievers=len(mailing_list)))
    else:
        print("There are no mails to be send.")
        return False
    
    if SETTINGS.CONFIRMATION:
        while True:
            decision_YN = input("Continue? (Y/N) ").upper().strip()

            if decision_YN == "Y":
                print("Please wait...")
                return mailing_list
            elif decision_YN == "N":
                return False
            else:
                print("Answer not recognised. Try again.")

def create_messages(mailing_list):
    with open('theMessagePlainText.txt','r',encoding='utf-8') as f:
        message_template_plain = f.read()
        
    with open('theMessageFullHTML.txt','r',encoding='utf-8') as f:
        message_template_html = f.read()

    messages = []
    for entry in mailing_list:    
        company_name, email_address, date_of_occurence, years_to_remind_after = entry
        msg = EmailMessage()
        msg['Subject'] = SETTINGS.MESSAGE_SUBJECT
        msg['From'] = SETTINGS.LOGIN
        msg.add_header('reply-to', SETTINGS.MAIL_TO_REPLY)
        msg['To'] = email_address
    
        if years_to_remind_after == "1":
            how_many_str = "rok"
        elif years_to_remind_after == "2":
            how_many_str = "dwa lata"
        
        months_pl = ["stycznia","lutego","marca","kwietnia","maja","czerwca","lipca","sierpnia","września","października","listopada","grudnia"]
        date = date_of_occurence.split("-")
        date_string = "{day} {month} {year} r.".format(day=int(date[2]),month=months_pl[int(date[1])-1],year=date[0])
        
        message_text_plain = message_template_plain.format(data=date_string,ile=how_many_str)
        msg.set_content(message_text_plain)
        image_cid = make_msgid()
        msg.add_alternative(message_template_html.format(image_cid=image_cid[1:-1],data=date_string,ile=how_many_str),subtype='html')
        
        with open('logo.png', 'rb') as img:
            maintype, subtype = mimetypes.guess_type(img.name)[0].split('/')
            msg.get_payload()[1].add_related(img.read(), maintype=maintype, subtype=subtype, cid=image_cid)
        
        messages += [msg]
        
    return messages

def start_smtp():
    try:
        s = smtplib.SMTP(SETTINGS.SMTP_HOST,SETTINGS.SMTP_PORT)
        s.ehlo_or_helo_if_needed()
        s.starttls()
        s.login(SETTINGS.LOGIN, enter_password())
        return s
    
    except Exception as e:
        print("Can't setup mail server. " + str(e))
        return False
    
def send_messages(messages,s):
    for msg in messages:
        try:
            s.send_message(msg)
            print("Mail to {reciever} sent successfully!".format(reciever=msg['To']))
            
        except Exception as e:
            print("Can't send email. " + str(e))
            return False

def update_database(mailing_list):
    check_if_opened(SETTINGS.DATABASE_NAME,SETTINGS.SENT_DATABASE_NAME)
        
    today = datetime.date.today()
    date_sent = "{y}-{m}-{d}".format(y=today.year,m=today.month,d=today.day)
    
    database_name = SETTINGS.DATABASE_NAME+".csv"
    database_backup_name = SETTINGS.DATABASE_NAME+"_backup.csv"
    database_sent_mails_name = SETTINGS.SENT_DATABASE_NAME+".csv"
    
    if SETTINGS.CLEAR_SENT_MAILS_DATABASE == True:
        mode = 'w'
    else:
        mode = 'a'
    
    with open(database_sent_mails_name,mode,newline='\n') as csvfile_sent:
        writer_sent = csv.writer(csvfile_sent, delimiter=";", quotechar='|')
        for row in mailing_list:
            company_name, email_address, date_of_occurence, years_to_remind_after = row
            writer_sent.writerow([company_name, email_address, date_of_occurence, years_to_remind_after, date_sent])
    shutil.copyfile(database_name,database_backup_name)
    csvfile_data_backup = open(database_backup_name,'r',newline='\n')
    data = csv.reader(csvfile_data_backup, delimiter=';', quotechar='|')
        
    with open(database_name,'w',newline='\n') as csvfile_data:
        writer_data = csv.writer(csvfile_data, delimiter=";", quotechar='|')
        for row_data in data:
            flag = True
            company_name, email_address, date_of_occurence, years_to_remind_after = row_data
            for row_just_sent in mailing_list:
                if row_data == row_just_sent:
                    flag = False
                    break
            if flag == True:
                writer_data.writerow([company_name, email_address, date_of_occurence, years_to_remind_after])

    csvfile_data_backup.close()
    print("Database updated successfully.")

def main():
    if SETTINGS.INSTALL:
        install()
    mailing_list = create_mailing_list()
    if not mailing_list: 
        return False
    messages = create_messages(mailing_list)
    server = start_smtp()
    if not server: 
        return False
    send_messages(messages,server)
    if not send_messages: 
        return False
    server.quit()
    update_database(mailing_list)

if __name__ == "__main__":
    main()