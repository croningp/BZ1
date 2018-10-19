#email alert function
#probably should move from adress to hard code or server and password to input but thats jsut house keeping it works at the moment

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE

def email_alert(efrom,eto,ebody):
    
    #send email to multiple emails require list
    fromaddr = efrom
    # must import COMMASPACE
    toaddr = COMMASPACE.join(eto)
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = COMMASPACE.join(toaddr)
    msg['Subject'] = "BZ Limit alert!"

    body = ebody 
    print("start")
    msg.attach(MIMEText(body, 'plain'))
    print("end")

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    text = msg.as_string()
    server.login(fromaddr, "croninlab")
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    return

#non function code for trouble shooting below

# #send email to multiple emails require list
# addr_list = ["2186149q@student.gla.ac.uk",'andrew.quinn1112@gmail.com']
# fromaddr = "bzboardalert@gmail.com"
# #must import COMMASPACE
# toaddr = COMMASPACE.join(addr_list)
# msg = MIMEMultipart()
# msg['From'] = fromaddr
# msg['To'] = COMMASPACE.join(addr_list)
# msg['Subject'] = "BZ Limit alert!"

# body = 'limit reached for ' + 'volume'+ ' please change and confirm on input' 
# msg.attach(MIMEText(body, 'plain'))

# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()
# text = msg.as_string()
# server.login(fromaddr, "croninlab")
# server.sendmail(fromaddr, toaddr, text)
# server.quit()