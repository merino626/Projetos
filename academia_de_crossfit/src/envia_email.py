import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import mimetypes
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import smtplib


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


def create_message(sender, to, subject, message_text):
  """Criador de mensagens para um email.

  Args:
    sender: Email que enviará a mensagem.
    to: Email que receberá a mensagem.
    subject: O assunto da mensagem.
    message_text: O texto que conterá o email.

  Returns:
    Um objeto contendo um objedo decodificado de email Base64url
  """
  message = MIMEText(message_text, "html")
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
  """Enviar uma mensagem de email.

  Args:
    service: Instancia autorizada da API de serviço do Gmail
    user_id: Endereço de email do usuário. O valor especial "me"
    pode ser usado para indicar o usuario autenticado.
    message: Mensagem a ser enviada.

  Returns:
    Mensagem enviada.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print ('Message Id: %s' % message['id'])
    return message
  except Exception as error:
    print ('An error occurred: %s' % error)

def conecta_user(SCOPES):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('src\\token.json'):
        creds = Credentials.from_authorized_user_file('src\\token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'src\\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('src\\token.json', 'w') as token:
            token.write(creds.to_json())


def createMessageWithAttachment(
    service,sender, to, subject, msgHtml, msgPlain, attachmentFiles):
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

    for attachmentFile in attachmentFiles:
      print("create_message_with_attachment: file: %s" % attachmentFile)
      content_type, encoding = mimetypes.guess_type(attachmentFile)

      if content_type is None or encoding is not None:
          content_type = 'application/octet-stream'

      main_type, sub_type = content_type.split('/', 1)

      if main_type == 'text':
          fp = open(attachmentFile, 'rb')
          msg = MIMEText(fp.read(), _subtype=sub_type, _charset="utf-8")
          fp.close()
      elif main_type == 'image':
          fp = open(attachmentFile, 'rb')
          msg = MIMEImage(fp.read(), _subtype=sub_type)
          fp.close()
      elif main_type == 'audio':
          fp = open(attachmentFile, 'rb')
          msg = MIMEAudio(fp.read(), _subtype=sub_type)
          fp.close()
      elif sub_type == "pdf" or sub_type == "vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        fp = open(attachmentFile, 'rb')
        msg = MIMEApplication(fp.read(), _subtype=sub_type)
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

def SendMessage(service, sender, to, subject, msgHtml, msgPlain, attachmentFile=None):
    if attachmentFile:
        message1 = createMessageWithAttachment(service, sender, to, subject, msgHtml, msgPlain, attachmentFile)
    result = message1
    return result


def advinha_tipo_arquivo(attachmentFile: str) -> str:
  content_type, encoding = mimetypes.guess_type(attachmentFile)
  try:
    file = attachmentFile.split('/')[-1]
    if ".PDF" in file.upper():
      return "pdf"
    if ".XLSX" in file.upper():
      return "excel"
    if ".PY" in file.upper():
      return "python"
  except:
    pass

  if content_type is None or encoding is not None:
      content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
      fp = open(attachmentFile, 'rb')
      msg = "text"
      fp.close()
  elif main_type == 'image':
      fp = open(attachmentFile, 'rb')
      msg = "image"
      fp.close()
  elif main_type == 'audio':
      fp = open(attachmentFile, 'rb')
      msg = "audio"
      fp.close()
  else:
      fp = open(attachmentFile, 'rb')
      msg = "arquivo"
      fp.close()
  return msg

def envia_email_credenciais_mobile(user, password, email):
  msg = MIMEMultipart()
  msg['From'] = "robo.crosslife@gmail.com"
  msg['To'] = email
  msg['Subject'] = 'Credenciais de acesso ao aplicativo Crosslife'
  message = f"""<h1>Bem vindo a academia Crosslife!</h1><br>
               <h2>Segue abaixo seu acesso ao aplicativo</h2><br>
               <p><strong>Usuario:</strong> {user}</p><br>
               <p><strong>Senha:</strong> {password}</p><br>
               <i>Credenciais geradas aleatoriamente. Recomendamos que após o primeiro acesso seja redefinida a senha.</i>""" 
  msg.attach(MIMEText(message, "html"))

  mailserver = smtplib.SMTP('smtp.gmail.com',587)
  # identify ourselves to smtp gmail client
  mailserver.ehlo()
  # secure our email with tls encryption
  mailserver.starttls()
  # re-identify ourselves as an encrypted connection
  mailserver.ehlo()
  mailserver.login("youremail", "youtpass")
  mailserver.sendmail("youreamil",email,msg.as_string())
  mailserver.quit()


if __name__ == "__main__":
  CLIENT_SECRET_FILE = 'src\\credentials.json'
  API_NAME = 'gmail'
  API_VERSION = 'v1'
  SCOPES = ['https://mail.google.com/']
  servico = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

  if os.path.isfile("token_gmail_v1.pickle"):
    os.remove("token_gmail_v1.pickle")

  if os.path.isfile('token.json'):
    os.remove('token.json')

  #conecta_user(SCOPES)
  usuario = servico.users().getProfile(userId='me').execute()
  print(usuario)

  to = "dudu_luis@hotmail.com.br"
  sender = "me"
  subject = "Assunto"
  msgHtml = "Hi<br/>Html Email"
  msgPlain = "Hi\nPlain Email"
  # Send message with attachment: 
  mensagem = SendMessage(servico, sender, to, subject, msgHtml, msgPlain, ['dados_matriculas.png'])
  send_message(servico, 'me', mensagem)
