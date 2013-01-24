#!/usr/bin/env python
#coding: utf-8

from optparse import OptionParser
import os,pwd
import sys

from email import Encoders
from email.Utils import formatdate
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import smtplib

def parse_option():
    parser=OptionParser()
    parser.add_option('-H', '--host', dest='host',
                    help='smtp host', default='localhost')
    parser.add_option('-P', '--port', dest='port',
                    help='smtp port', default=25, type='int')
    parser.add_option('-s', '--subject', dest='mail_subject',
                    help='mail subject', default='mail from mail.py')
    parser.add_option('-r', dest='mail_from',
                    help='mail from', default=pwd.getpwuid(os.getuid()).pw_name)
    parser.add_option('-a', '--attachment', dest='attachment',
                    help='attachment')
    (options, options.mail_to)=parser.parse_args()
    return options

if __name__=='__main__':
    options=parse_option()
    body=''
    for line in sys.stdin:
        body=body+line
    message = MIMEMultipart()
    message['Subject']=options.mail_subject
    message['From']=options.mail_from
    message['To']=','.join(options.mail_to)
    message['Date']=formatdate()

    body=MIMEText(body,'plain','utf-8')
    message.attach(body)

    if options.attachment:
        message_attachment=MIMEBase('application','octet-stream')

        attachment_file=open(options.attachment)
        message_attachment.set_payload(attachment_file.read())
        attachment_file.close()

        Encoders.encode_base64(message_attachment)
        message_attachment.add_header("Content-Disposition","attachment",filename=options.attachment)
        message.attach(message_attachment)

    smtp=smtplib.SMTP(options.host,options.port)
    smtp.sendmail(options.mail_from,options.mail_to,message.as_string())
    smtp.close()



