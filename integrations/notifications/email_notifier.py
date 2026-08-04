from email.message import EmailMessage
import smtplib,ssl
class EmailNotifier:
    def __init__(self,host: str,port: int,username: str,password: str,sender: str) -> None:
        self.host=host; self.port=port; self.username=username; self.password=password; self.sender=sender
    def send(self,recipient: str,subject: str,body: str) -> None:
        msg=EmailMessage(); msg["From"]=self.sender; msg["To"]=recipient; msg["Subject"]=subject; msg.set_content(body)
        with smtplib.SMTP_SSL(self.host,self.port,context=ssl.create_default_context()) as server:
            server.login(self.username,self.password); server.send_message(msg)
