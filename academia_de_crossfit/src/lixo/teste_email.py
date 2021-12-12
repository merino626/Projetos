import httplib2
import os
import oauth2client
from oauth2client import client, tools, file
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from src import envia_email as E


def SendMessage(service, sender, to, subject, msgHtml, msgPlain, attachmentFile=None):
    if attachmentFile:
        message1 = createMessageWithAttachment(sender, to, subject, msgHtml, msgPlain, attachmentFile)
    result = message1
    return result


def createMessageWithAttachment(
    sender, to, subject, msgHtml, msgPlain, attachmentFile):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      msgHtml: Html message to be sent
      msgPlain: Alternative plain text message for older email clients          
      attachmentFile: The path to the file to be attached.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEMultipart('mixed')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    messageA = MIMEMultipart('alternative')
    messageR = MIMEMultipart('related')

    messageR.attach(MIMEText(msgHtml, 'html'))
    messageA.attach(MIMEText(msgPlain, 'plain'))
    messageA.attach(messageR)

    message.attach(messageA)

    print("create_message_with_attachment: file: %s" % attachmentFile)
    content_type, encoding = mimetypes.guess_type(attachmentFile)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(attachmentFile, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(attachmentFile, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(attachmentFile, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(attachmentFile, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(attachmentFile)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def main():
    CLIENT_SECRET_FILE = 'src\\credentials.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']
    servico = E.Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    if os.path.isfile("token_gmail_v1.pickle"):
        os.remove("token_gmail_v1.pickle")

    if os.path.isfile('token.json'):
        os.remove('token.json')

    usuario = servico.users().getProfile(userId='me').execute()
    print(usuario)
    
    to = "dudu_luis@hotmail.com.br"
    sender = "me"
    subject = "Assunto"
    msgHtml = "Hi<br/>Html Email"
    msgPlain = "Hi\nPlain Email"

    # Send message with attachment: 
    mensagem = SendMessage(servico, sender, to, subject, msgHtml, msgPlain, 'dados_matriculas.png')
    E.send_message(servico, 'me', mensagem)

if __name__ == '__main__':
    main()