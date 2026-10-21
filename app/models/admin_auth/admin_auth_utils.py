# # You can put this in utils.py or admin_auth.py


# import os
# from dotenv import load_dotenv

# from config import EMAIL_PASS, EMAIL_USER

# load_dotenv()



# import smtplib

# def send_email(recipient, subject, message):
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login('your_email@gmail.com', 'your_app_password')  # Use env vars
#         email_body = f"Subject: {subject}\n\n{message}"
#         server.sendmail('your_email@gmail.com', recipient, email_body)
#         server.quit()
#         return True
#     except Exception as e:
#         print("Email error:", e)
#         return False



# def send_email(recipient, subject, message):
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(EMAIL_USER, EMAIL_PASS)
#         email_body = f"Subject: {subject}\n\n{message}"
#         server.sendmail(EMAIL_USER, recipient, email_body)
#         server.quit()
#         return True
#     except Exception as e:
#         print("Email error:", e)
#         return False
