import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendEmail(senderEmail, senderName, recipient, subject, bodyText, bodyHtml):
    # Replace smtp_username with your Amazon SES SMTP user name.
    USERNAME_SMTP = "AKIAWO53MB6FLUDGGDUR"

    # Replace smtp_password with your Amazon SES SMTP password.
    PASSWORD_SMTP = "BM4KPAw6GJhC4lnwl+pIYB7YuOZnJkYKqvIXVP8/xK4h"

    # (Optional) the name of a configuration set to use for this message.
    # If you comment out this line, you also need to remove or comment out
    # the "X-SES-CONFIGURATION-SET:" header below.
    #CONFIGURATION_SET = "ConfigSet"

    # If you're using Amazon SES in an AWS Region other than US West (Oregon),
    # replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP
    # endpoint in the appropriate region.
    HOST = "email-smtp.us-west-2.amazonaws.com"
    PORT = 587


    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email.utils.formataddr((senderName, senderEmail))
    msg['To'] = recipient
    # Comment or delete the next line if you are not using a configuration set
    #msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(bodyText, 'plain')
    part2 = MIMEText(bodyHtml, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Try to send the message.
    try:
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        #stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(senderEmail, recipient, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        print ("Error: ", e)
        return False
    else:
        return True