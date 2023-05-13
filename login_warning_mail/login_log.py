import smtplib #importing the module
import datetime as dt
from email.message import EmailMessage
import platform
import psutil
from dotenv import load_dotenv
import os

load_dotenv()

sender_add=os.getenv('SENDER_ADD') #storing the sender's mail id
receiver_add=os.getenv('RECEIVER_ADD') #storing the receiver's mail id
password=os.getenv('PASSWORD') #storing the password to log in
dtime = dt.datetime.now()
time = dtime.time()
date = dtime.date()
boot_time_timestamp = psutil.boot_time()
bt = dt.datetime.fromtimestamp(boot_time_timestamp)

msg_to_be_sent =f'''
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
>>>>>>>>>>>>>>>>>>>>>>>>>>   NEW ENTRY   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

============================ Boot at: ==========================================
                    DATE ==> {bt.year}/{bt.month}/{bt.day}
                    TIME ==> {bt.hour}:{bt.minute}:{bt.second} {bt.strftime("%p")} 

=========================== Script run at: ====================================
                    DATE ==> {date.year}/{date.month}/{date.day}
                    TIME ==> {time.hour}:{time.minute}:{time.second}



'''

email = EmailMessage()
email['from'] = sender_add
email['to'] = receiver_add
email['subject'] = f'Login in PC {platform.uname().node}.'
email.set_content(msg_to_be_sent)



def send_mail(sender, receiver, password, mail):
    #creating the SMTP server object by giving SMPT server address and port number
    with smtplib.SMTP(host="smtp.gmail.com",port=587) as smtp_server:
        smtp_server.ehlo() #setting the ESMTP protocol
        smtp_server.starttls() #setting up to TLS connection
        smtp_server.ehlo() #calling the ehlo() again as encryption happens on calling startttls()

        smtp_server.login(sender,password) #logging into out email id

        #sending the mail by specifying the from and to address and the message 
        smtp_server.send_message(mail)
        print('Successfully the mail is sent') #priting a message on sending the mail

if __name__=='__main__':
    try:
        send_mail(sender_add, receiver_add, password, email)
    except Exception as e:
        try:
            with open('log.txt', 'a') as log:
                log.write(f'exception {e} created')
        except:
            pass
    with open('log.txt', 'a') as log:
        log.write(msg_to_be_sent)
