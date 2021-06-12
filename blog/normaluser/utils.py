# ngamtwxuitmnbyif
import smtplib, ssl

sender_email = "sarkar741127@gmail.com"
password = "ngamtwxuitmnbyif"

def send_mail(receiver_email,message):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_email, password)
    final_message = "Subject : Mail From DevHunt Blog \n\n"+message
    s.sendmail(sender_email, receiver_email, final_message)
    s.quit()