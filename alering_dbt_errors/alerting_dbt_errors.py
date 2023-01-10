'''
get dbt logs as parameter
'''

dbutils.widgets.text("dbt_results", "","")
dbt_log = dbutils.widgets.get("dbt_results")


'''
extract number of errors from logs
'''

import re
regex = re.compile('ERROR=(\d+)')
search_result = re.search(regex, dbt_log)

if search_result:
    error_count = int(search_result.group(1))
  
#print(error_count)


'''
if errors found, send email
'''

if error_count > 0:
  
    email_sender='sender_example@domain.com'
    email_sender_password='mypassword123'
    email_receiver='data_engineer_example@domain.com'


    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    s = smtplib.SMTP(host='smtp-mail.domain.com', port=587)
    s.starttls()
    s.login(email_sender, email_sender_password)

    msg = MIMEMultipart() 

    msg['From']=email_sender

    msg['To']=email_receiver

    msg['Subject']="Yikes! DBT got some error"

    msg.attach(MIMEText(dbt_log, 'plain'))

    s.send_message(msg)

    s.quit()
