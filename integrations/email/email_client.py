from __future__ import annotations
import asyncio,smtplib
from email.message import EmailMessage
from uuid import uuid4
from integrations.email.delivery_receipt import DeliveryReceipt
class EmailClient:
    def __init__(self,host: str,port: int=587,username: str='',password: str='',sender: str='',use_tls: bool=True)->None:self.host=host;self.port=port;self.username=username;self.password=password;self.sender=sender;self.use_tls=use_tls
    async def send(self,recipient: str,subject: str,body: str,*,dry_run: bool=True)->DeliveryReceipt:
        message_id=str(uuid4())
        if dry_run:return DeliveryReceipt.create(message_id,recipient,'simulated')
        def deliver():
            msg=EmailMessage();msg['From']=self.sender;msg['To']=recipient;msg['Subject']=subject;msg['Message-ID']=message_id;msg.set_content(body)
            with smtplib.SMTP(self.host,self.port,timeout=30) as smtp:
                if self.use_tls:smtp.starttls()
                if self.username:smtp.login(self.username,self.password)
                smtp.send_message(msg)
        await asyncio.to_thread(deliver);return DeliveryReceipt.create(message_id,recipient,'sent')
