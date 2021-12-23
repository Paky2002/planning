from flask import Blueprint,render_template, request, jsonify, make_response, send_file
from io import BytesIO  
from . import db
from flask_login import login_required, current_user
import datetime
from imap_tools import MailBox, AND
from .models import *
import datetime
from sqlalchemy import and_
from .form import RegistraCliente, AggiungiPreventivo
import imaplib
import email
from imap_tools import MailBox, AND, OR, NOT, A, H, U
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid
from email.mime.base import MIMEBase
from email import encoders


main = Blueprint('main', __name__)
mailbox = MailBox('imap.gmail.com').login('garagncontrol@gmail.com', 'gargano2020')

@main.context_processor
def global_variable():
    return dict(nome=current_user.name)

@main.route('/home')
@login_required
def home():
    arriviDict = {}
    arriviDict ['arrivi'] = Arrivi.query.filter (Arrivi.preventivo.has(Preventivo.account_id == current_user.get_id())).order_by(Arrivi.id.desc()).all()
    arriviDict ['arriviOggi'] = Arrivi.query.filter (Arrivi.preventivo.has(and_(Preventivo.account_id == current_user.get_id(), Preventivo.checkIn == datetime.date.today()))).all()
    arriviDict ['partenzeOggi'] = Arrivi.query.filter (Arrivi.preventivo.has(and_(Preventivo.account_id == current_user.get_id(), Preventivo.checkOut == datetime.date.today()))).all()
    preventivi = Preventivo.query.filter_by (account_id = current_user.get_id()).order_by(Preventivo.id.desc()).all()
    return render_template('dashboard.html', arriviDict = arriviDict, preventivi = preventivi)

@main.route('/')
def index():
    return 'Index'

@main.route('/profile')
@login_required
def example():
    return render_template('user-profile.html')


#PAGINA PRINCIPALE DELLA MAIL

@main.route('/mail')
@login_required
def mail():
    formPreventivo = AggiungiPreventivo ()
    mailBoxInformation = {'folder' : []}
    for f in mailbox.folder.list():
        if str(f.name) != '[Gmail]' :
            mailBoxInformation ['folder'].append ({'name' : str(f.name), 'messaggiNumero' : mailbox.folder.status(str(f.name)) ['MESSAGES']})
    msg =  [msg for msg in mailbox.fetch(limit=10,bulk=True, reverse=True, headers_only = True)]
    return render_template('emailbox.html', msg = msg, mailBoxInformation = mailBoxInformation, formPreventivo = formPreventivo)

#API SMTP

#INVIO DI UN MESSAGGIO 
  
@main.route('/sendMessage', methods = ['post'])
@login_required
def sendMessage():
    message = EmailMessage()
    message['Subject'] = request.form['oggetto']
    message['From'] = "garagncontrol@gmail.com"
    message['To'] = request.form['to']

    if request.form['reply'] == True : 
        message.add_header('reply-to', "garagncontrol@gmail.com")
        message.add_alternative(request.form['msg'], subtype='html')
    
    if 'preventivo' in request.form : 
        setHtml(message)
    
    if 'files[]' in request.files :
        files = request.files.getlist("files[]")
        for file_ in files :
            message.add_attachment(file_.read(), maintype='application', subtype=file_.content_type, filename=file_.filename)

    try:
        smtp_server = None
        smtp_server = smtplib.SMTP("mail.tophost.it", 587)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login("selezionimadeinpuglia.it", 'gargano2020.')
        smtp_server.send_message(message)
        return jsonify(data={'status' : 'success', 'msg': 'Messaggio inviato correttamente'}) #Responso per il client
    except Exception as e:
        print("Error: ", str(e))
    finally:
        if smtp_server is not None:
            smtp_server.quit()

#INSERISCE I MESSAGGI HTML PREFATTI IN EMAIL

def testHtml (message) : 
    asparagus_cid = make_msgid()
    message.add_alternative
    message.add_alternative("""
    <!DOCTYPE html>
<html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">
  <head>
    <title></title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css">
    <meta charset="utf-8"/>
    <meta content="width=device-width,initial-scale=1" name="viewport" />
    <style>
      * {
        box-sizing: border-box
      }

      th.column {
        padding: 0
      }

      a[x-apple-data-detectors] {
        color: inherit !important;
        text-decoration: inherit !important
      }

      #MessageViewBody a {
        color: inherit;
        text-decoration: none
      }

      p {
        line-height: inherit
      }

      @media (max-width:720px) {
        .icons-inner {
          text-align: center
        }

        .icons-inner td {
          margin: 0 auto
        }

        .row-content {
          width: 100% !important
        }

        .stack .column {
          width: 100%;
          display: block
        }
      }
    </style>
  </head>
  <body>
    <input type="hidden" id="gContact" data-idPreventivo="1" />
    <p>NOME</p>
    </body>
    </html>
    """, subtype='html')


def setHtml (message) : 
    asparagus_cid = make_msgid()
    message.add_alternative
    message.add_alternative("""
    <!DOCTYPE html>
<html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">
  <head>
    <title></title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css">
    <meta charset="utf-8"/>
    <meta content="width=device-width,initial-scale=1" name="viewport" />
    <style>
      * {
        box-sizing: border-box
      }

      th.column {
        padding: 0
      }

      a[x-apple-data-detectors] {
        color: inherit !important;
        text-decoration: inherit !important
      }

      #MessageViewBody a {
        color: inherit;
        text-decoration: none
      }

      p {
        line-height: inherit
      }

      @media (max-width:720px) {
        .icons-inner {
          text-align: center
        }

        .icons-inner td {
          margin: 0 auto
        }

        .row-content {
          width: 100% !important
        }

        .stack .column {
          width: 100%;
          display: block
        }
      }
    </style>
  </head>

  <body style="background-color:#f9f9f9;margin:0;padding:0;-webkit-text-size-adjust:none;text-size-adjust:none">
    <table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation" style="background-color:#f9f9f9" width="100%">
      <tbody>
        <tr>
          <td>
            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1" role="presentation"  width="100%">
              <tbody>
                <tr>
                  <td>
                      <!-- TABLE HEADER -->
                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content" role="presentation"  width="700">
                      <tbody>
                        <tr>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="50%">
                            <table border="0" cellpadding="0" cellspacing="0" class="image_block" role="presentation"  width="100%">
                              <tr>
                                <td style="padding-left:25px;width:100%;padding-right:0;padding-top:5px;padding-bottom:5px">
                                  <div style="line-height:10px">
                                    <p>HOTEL ALBANO</p>
                                  </div>
                                </td>
                              </tr>
                            </table>
                          </th>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="50%">
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:15px;padding-left:10px;padding-right:10px;padding-top:15px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;color:#555;line-height:1.2;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif">
                                      <strong><p style="margin:0;text-align:right">ID PREVENTIVO : </p></strong>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                          </th>
                        </tr>
                      </tbody>
                    </table>

                    <!-- END TABLE HEADER -->

                  </td>
                </tr>
              </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2" role="presentation"  width="100%">
              <tbody>
                <tr>
                  <td>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="background-color:#fff" width="700">
                      <tbody>
                        <tr>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="100%">
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:20px;padding-left:10px;padding-right:10px;padding-top:30px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif;color:#0b1560;line-height:1.2">
                                      <p style="margin:0;font-size:16px;text-align:center">
                                        <span style="font-size:42px">
                                          <strong>CIAO JAMES</strong>
                                        </span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:25px;padding-left:30px;padding-right:30px;padding-top:10px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif;color:#555;line-height:1.5">
                                      <p style="margin:0;font-size:14px;text-align:center;">
                                        <span style="font-size:15px"> Abbiamo ricevuto la sua richiesta di preventivo con check-in il 21/21/2021 check-out il 23/23/2021, 3 adulti, 1 bambini, 1 infant.</span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:30px;padding-left:10px;padding-right:10px;padding-top:10px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;color:#0b1560;line-height:1.2;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif">
                                      <p style="margin:0;font-size:14px;text-align:center">
                                        <span style="font-size:24px">
                                          <strong>ABBIAMO SCELTO PER TE LE SEGUENTI SOLUZIONI</strong>
                                        </span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                          </th>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-3" role="presentation"  width="100%">
              <tbody>
                <tr>
                  <td>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="background-color:#ebedff" width="700">
                      <tbody>
                        <tr>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="100%">
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-left:10px;padding-right:10px;padding-top:50px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;color:#0b1560;line-height:1.2;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif">
                                      <p style="margin:0;font-size:14px;text-align:center">
                                        <span style="font-size:24px">
                                          <strong>MATRIMONIALE</strong>
                                        </span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:60px;padding-left:30px;padding-right:30px;padding-top:10px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif;color:#555;line-height:1.5">
                                      <p style="margin:0;font-size:14px;text-align:center;">
                                        <span style="font-size:15px">Camera composta da 2 letti singoli e un matrimoniale, super confortevole</span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                          </th>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-4" role="presentation"  width="100%">
              <tbody>
                <tr>
                  <td>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content" role="presentation" style="background-color:#ebedff" width="700">
                      <tbody>
                        <tr>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="33.333333333333336%">
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-left:10px;padding-right:10px;padding-top:15px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;color:#555;line-height:1.2;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif">
                                      <p style="margin:0;font-size:14px;text-align:center">
                                        <span style="font-size:16px">dal</span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-left:10px;padding-right:10px;padding-top:5px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;color:#555;line-height:1.2;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif">
                                      <p style="margin:0;font-size:14px;text-align:center">
                                        <span style="color:#000">
                                          <strong>
                                            <span style="font-size:18px">04.01.20</span>
                                          </strong>
                                        </span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                          </th>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="33.333333333333336%">
                            <table border="0" cellpadding="0" cellspacing="0" class="image_block" role="presentation"  width="100%">
                              <tr>
                                <td style="width:100%;padding-right:0;padding-left:0;padding-top:35px;padding-bottom:40px">
                                  <div align="center" style="line-height:10px">
                                    <--------->
                                  </div>
                                </td>
                              </tr>
                            </table>
                          </th>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="33.333333333333336%">
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-left:10px;padding-right:10px;padding-top:15px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;color:#555;line-height:1.2;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif">
                                      <p style="margin:0;font-size:14px;text-align:center">
                                        <span style="font-size:16px">al</span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-left:10px;padding-right:10px;padding-top:5px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;color:#555;line-height:1.2;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif">
                                      <p style="margin:0;font-size:14px;text-align:center">
                                        <span style="color:#000">
                                          <strong>
                                            <span style="font-size:18px">04.01.20</span>
                                          </strong>
                                        </span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                          </th>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-5" role="presentation"  width="100%">
              <tbody>
                <tr>
                  <td>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="background-color:#ebedff" width="700">
                      <tbody>
                        <tr>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="100%">
                            <hr>
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-left:30px;padding-right:30px;padding-top:15px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif;color:#555;line-height:1.5">
                                      <p style="margin:0;font-size:14px;text-align:center;">
                                        <center><span style="font-size:15px">Trattamento : B&amp;B</span></center>
                                        <center><p><del>800€</del> solo per te <strong style="font-size:25px;color:green"> 650€</strong></center>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <hr>
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-left:30px;padding-right:30px;padding-top:15px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif;color:#555;line-height:1.5">
                                      <p style="margin:0;font-size:14px;text-align:center;">
                                        <span style="font-size:15px">Trattamento : B&amp;B</span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <hr>
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-left:30px;padding-right:30px;padding-top:15px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif;color:#555;line-height:1.5">
                                      <p style="margin:0;font-size:14px;text-align:center;">
                                        <span style="font-size:15px">Trattamento : B&amp;B</span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <hr style="margin-bottom : 0px">
                          </th>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-6" role="presentation"  width="100%">
              <tbody>
                <tr>
                  <td>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="background-color:#fff" width="700">
                      <tbody>
                        <tr>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="100%">
                            <table border="0" cellpadding="0" cellspacing="0" class="divider_block" role="presentation"  width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-left:10px;padding-right:10px;padding-top:15px">
                                  <div align="center">
                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"  width="95%">
                                      <tr>
                                        <td class="divider_inner" style="font-size:1px;line-height:1px;border-top:1px solid #dde3e8">
                                          <span></span>
                                        </td>
                                      </tr>
                                    </table>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:30px;padding-left:10px;padding-right:10px;padding-top:25px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;color:#0b1560;line-height:1.2;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif">
                                      <p style="margin:0;font-size:14px;text-align:center">
                                        <span style="font-size:24px">
                                          <strong>SUPPLEMENTI RICHIESTI</strong>
                                        </span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                          </th>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-7" role="presentation"  width="100%">
              <tbody>
                <tr>
                  <td>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="background-color:#fff" width="700">
                      <tbody>
                        <tr>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="33.333333333333336%">
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-left:25px;padding-right:10px;padding-top:20px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;color:#555;line-height:1.2;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif">
                                      <p style="margin:0;font-size:14px;text-align:left">
                                        <span style="color:#000">
                                          <strong>
                                            <span style="font-size:18px">1 Condizionatore</span>
                                          </strong>
                                        </span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                          </th>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="66.66666666666667%">
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:15px;padding-left:30px;padding-right:30px;padding-top:15px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif;color:#555;line-height:1.8">
                                      <p style="margin:0;font-size:14px;text-align:left;">
                                        <span style="font-size:15px">Maximum weight of hand luggage: 8 kg Maximum dimensions: 56 cm x 45 cm x 25 cm</span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                          </th>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-8" role="presentation"  width="100%">
              <tbody>
                <tr>
                  <td>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="background-color:#fff" width="700">
                      <tbody>
                        <tr>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="100%">
                            <table border="0" cellpadding="0" cellspacing="0" class="divider_block" role="presentation"  width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-left:10px;padding-right:10px;padding-top:15px">
                                  <div align="center">
                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"  width="95%">
                                      <tr>
                                        <td class="divider_inner" style="font-size:1px;line-height:1px;border-top:1px solid #dde3e8">
                                          <span></span>
                                        </td>
                                      </tr>
                                    </table>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:25px;padding-left:10px;padding-right:10px;padding-top:25px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;color:#0b1560;line-height:1.2;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif">
                                      <p style="margin:0;font-size:14px;text-align:center">
                                        <span style="font-size:20px">
                                          <strong>COS'E' INCLUSO NEL PREZZO ?</strong>
                                        </span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-left:30px;padding-right:30px;padding-top:10px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif;color:#555;line-height:1.8">
                                      <p style="margin:0;font-size:14px;text-align:left;">
                                        <span style="font-size:15px">Nel prezzo è incluso ingresso in piscina, tessera club, alloggio, mangiare</span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <table border="0" cellpadding="10" cellspacing="0" class="divider_block" role="presentation"  width="100%">
                              <tr>
                                <td>
                                  <div align="center">
                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"  width="95%">
                                      <tr>
                                        <td class="divider_inner" style="font-size:1px;line-height:1px;border-top:1px solid #dde3e8">
                                          <span></span>
                                        </td>
                                      </tr>
                                    </table>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:25px;padding-left:10px;padding-right:10px;padding-top:25px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;color:#0b1560;line-height:1.2;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif">
                                      <p style="margin:0;font-size:14px;text-align:center">
                                        <span style="font-size:20px">
                                          <strong>COSA FARE SUL GARGANO ?</strong>
                                        </span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:15px;padding-left:30px;padding-right:30px;padding-top:10px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif;color:#555;line-height:1.8">
                                      <p style="margin:0;font-size:14px;text-align:left;">
                                        <span style="font-size:15px">Il Gargano offre mille escursioni, tra le più importanti troviamo Costa&amp;Grotte e Tremiti prenotabili da qui. Oltre a queste ci sono...</span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                          </th>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-9" role="presentation"  width="100%">
              <tbody>
                <tr>
                  <td>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="background-color:#fff" width="700">
                      <tbody>
                        <tr>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="100%">
                            <table border="0" cellpadding="0" cellspacing="0" class="divider_block" role="presentation"  width="100%">
                              <tr>
                                <td style="padding-bottom:15px;padding-left:10px;padding-right:10px;padding-top:15px">
                                  <div align="center">
                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"  width="100%">
                                      <tr>
                                        <td class="divider_inner" height="5" style="font-size:1px;line-height:1px;border-top:0 solid transparent">
                                          <span></span>
                                        </td>
                                      </tr>
                                    </table>
                                  </div>
                                </td>
                              </tr>
                            </table>
                          </th>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-10" role="presentation"  width="100%">
              <tbody>
                <tr>
                  <td>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="background-color:#0b1560" width="700">
                      <tbody>
                        <tr>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="100%">
                            <table border="0" cellpadding="0" cellspacing="0" class="divider_block" role="presentation"  width="100%">
                              <tr>
                                <td style="padding-bottom:15px;padding-left:10px;padding-right:10px;padding-top:15px">
                                  <div align="center">
                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"  width="100%">
                                      <tr>
                                        <td class="divider_inner" height="5" style="font-size:1px;line-height:1px;border-top:0 solid transparent">
                                          <span></span>
                                        </td>
                                      </tr>
                                    </table>
                                  </div>
                                </td>
                              </tr>
                            </table>
                          </th>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-11" role="presentation"  width="100%">
              <tbody>
                <tr>
                  <td>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="background-color:#0b1560" width="700">
                      <tbody>
                        <tr>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="50%">
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-left:25px;padding-right:10px;padding-top:10px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif;color:#fff;line-height:1.2">
                                      <p style="margin:0;font-size:18px;text-align:left">
                                        <strong>
                                          <span style="color:#fff">Info</span>
                                        </strong>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-left:25px;padding-right:10px;padding-top:10px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif;color:silver;line-height:1.2">
                                      <p style="margin:0">
                                        <span></span>
                                      </p>
                                      <p style="margin:0;font-size:14px;text-align:left">
                                        <span style="color:silver;font-size:12px"> Stay up-to-date with current activities and future events by following us on your favorite social media channels.</span>
                                      </p>
                                      <p style="margin:0;">
                                        <br />
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <table border="0" cellpadding="0" cellspacing="0" class="html_block" role="presentation"  width="100%">
                              <tr>
                                <td>
                                  <div align="center" style="font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif">
                                    <div style="height:20px;"></div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <table border="0" cellpadding="0" cellspacing="0" class="social_block" role="presentation"  width="100%">
                              <tr>
                                <td style="padding-left:20px;text-align:left;padding-right:0">
                                  <table align="left" border="0" cellpadding="0" cellspacing="0" class="social-table" role="presentation"  width="188px">
                                    <tr>
                                      <td style="padding:0 15px 0 0">
                                        <a href="https://www.facebook.com/" target="_blank">
                                          <img alt="Facebook" height="32" src="images/facebook2x.png" style="display:block;height:auto;border:0" title="Facebook" width="32" />
                                        </a>
                                      </td>
                                      <td style="padding:0 15px 0 0">
                                        <a href="https://twitter.com/" target="_blank">
                                          <img alt="Twitter" height="32" src="images/twitter2x.png" style="display:block;height:auto;border:0" title="Twitter" width="32" />
                                        </a>
                                      </td>
                                      <td style="padding:0 15px 0 0">
                                        <a href="https://plus.google.com/" target="_blank">
                                          <img alt="Google+" height="32" src="images/googleplus2x.png" style="display:block;height:auto;border:0" title="Google+" width="32" />
                                        </a>
                                      </td>
                                      <td style="padding:0 15px 0 0">
                                        <a href="https://instagram.com/" target="_blank">
                                          <img alt="Instagram" height="32" src="images/instagram2x.png" style="display:block;height:auto;border:0" title="Instagram" width="32" />
                                        </a>
                                      </td>
                                    </tr>
                                  </table>
                                </td>
                              </tr>
                            </table>
                          </th>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="50%">
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-left:25px;padding-right:10px;padding-top:10px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif;color:#fff;line-height:1.2">
                                      <p style="margin:0;font-size:18px;text-align:left">
                                        <strong>
                                          <span style="color:#fff">Contact Us</span>
                                        </strong>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-left:25px;padding-right:10px;padding-top:10px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;color:silver;line-height:1.5;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif">
                                      <p style="margin:0;">
                                        <span style="color:silver;font-size:12px">www.company.com</span>
                                      </p>
                                      <p style="margin:0;">
                                        <span style="color:silver;font-size:12px"></span>
                                      </p>
                                      <p style="margin:0;">
                                        <span style="color:silver;font-size:12px">Company address here <br />+1 123 123 123 </span>
                                      </p>
                                      <p style="margin:0;">
                                        <br/>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                            <table border="0" cellpadding="0" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-left:25px;padding-right:10px;padding-top:10px">
                                  <div style="font-family:sans-serif">
                                    <div style="font-size:12px;color:silver;line-height:1.2;font-family:Montserrat,Trebuchet MS,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Tahoma,sans-serif">
                                      <p style="margin:0">
                                        <span style="color:silver;font-size:12px">Changed your mind? <a href="{{ unsubscribe_link }}" style="color:#fff" target="_blank"> Unsubscribe</a>
                                        </span>
                                      </p>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            </table>
                          </th>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-12" role="presentation"  width="100%">
              <tbody>
                <tr>
                  <td>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="background-color:#0b1560" width="700">
                      <tbody>
                        <tr>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="100%">
                            <table border="0" cellpadding="0" cellspacing="0" class="divider_block" role="presentation"  width="100%">
                              <tr>
                                <td style="padding-bottom:15px;padding-left:10px;padding-right:10px;padding-top:15px">
                                  <div align="center">
                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"  width="100%">
                                      <tr>
                                        <td class="divider_inner" height="5" style="font-size:1px;line-height:1px;border-top:0 solid transparent">
                                          <span></span>
                                        </td>
                                      </tr>
                                    </table>
                                  </div>
                                </td>
                              </tr>
                            </table>
                          </th>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
            <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-13" role="presentation"  width="100%">
              <tbody>
                <tr>
                  <td>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation"  width="700">
                      <tbody>
                        <tr>
                          <th class="column" style="font-weight:400;text-align:left;vertical-align:top" width="100%">
                            <table border="0" cellpadding="0" cellspacing="0" class="icons_block" role="presentation"  width="100%">
                              <tr>
                                <td style="padding-bottom:10px;padding-top:10px;color:#9d9d9d;font-family:inherit;font-size:15px;text-align:center">
                                  <table cellpadding="0" cellspacing="0" role="presentation"  width="100%">
                                    <tr>
                                      <td style="text-align:center">
                                        <!--[if vml]>
																				<table align="left" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
																					<![endif]-->
                                        <!--[if !vml]>
																					<!-->
                                        
                                </td>
                              </tr>
                            </table>
                          </th>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>
    <!-- End -->
  </body>
</html>""", subtype='html')
        
#API IMAP

#RITORNA I MESSAGGI DI UNA CARTELLA SPECIFICA

@main.route('/changeFolderList', methods = ['post'])
@login_required
def changeFolderList():
    mailbox.folder.set(request.form['folderName'])
    msg = [{'uid' : msg.uid, 'subject' : msg.subject, 'from' : msg.from_, 'date' : msg.date} for msg in mailbox.fetch(limit=10,bulk=True, reverse=True, headers_only = True)]
    print (msg)
    return jsonify(data={'msgg' : msg})

#RITORNA I MESSAGGI DI UNA PAGINA SUCCESSIVA

@main.route('/getNewMessage', methods = ['post'])
@login_required
def getNewMessage():
    print (request.form ['uid'])
    msg = [{'uid' : msg.uid, 'subject' : msg.subject, 'from' : msg.from_, 'date' : msg.date} for msg in mailbox.fetch(A(uid=U(str(int(request.form['uid'])-10), request.form ['uid'])), headers_only = True, bulk=True)]
    print (msg)
    return jsonify(data={'status' : 'success', 'message': 'Inserito correttamente', 'msgg' : msg}) #Responso per il client

#RITORNA I MESSAGGI DI UNA PAGINA PRECEDENTE

@main.route('/getOldMessage', methods = ['post'])
@login_required
def getOldMessage():
    msg = [{'uid' : msg.uid, 'subject' : msg.subject, 'from' : msg.from_, 'date' : msg.date} for msg in mailbox.fetch(A(uid=U(str(int(request.form['uid'])+10), str(int(request.form['uid'])+20))), headers_only = True, bulk=True)]
    print (msg)
    return jsonify(data={'status' : 'success', 'message': 'Inserito correttamente', 'msgg' : msg}) #Responso per il client

#RITORNA LA MAIL IN SE PER SE

@main.route('/getMail', methods = ['post'])
@login_required
def getMail():
    for msg in mailbox.fetch(A(uid=U(str(int(request.form['uid'])))), bulk=True) :
        msg_ = {'uid' : msg.uid, 'subject' : msg.subject, 'from' : msg.from_, 'date' : msg.date, 'html' : msg.html, 'allegato' : []}
        for att in msg.attachments:  # list: imap_tools.MailAttachment+
            msg_ ['allegato'].append({'filename' : att.filename, 'type' : att.content_type, 'size' : att.size, 'att_id' : att.content_id})
    print (msg_)
    return jsonify(data={'status' : 'success', 'message': 'Inserito correttamente', 'msgg' : msg_}) #Responso per il client

#RITORNA GLI ALLEGATI DI UNA MAIL moveToEmail

@main.route ('/getAttachments', methods=['post'])
@login_required
def getAttachments () :
    print (request.form)
    for msg in mailbox.fetch(A(uid=U(request.form['uid'])), bulk=True) :
        for att in msg.attachments: 
            if att.content_id == request.form['att-id'] :
                buffer = BytesIO()
                buffer.write(att.payload)
                buffer.seek(0)
                return send_file(buffer, mimetype=att.content_type)

#SPOSTA UN MESSAGGIO IN UNA FOLDER 

@main.route ('/moveToEmailBox', methods=['post'])
@login_required
def moveToEmailBox () :
    uid, folder = request.form ['uid'], request.form ['folder']
    mailbox.move(uid, folder)
    mailBoxInformation = {'folder' : []}
    for f in mailbox.folder.list():
        if str(f['name']) != '[Gmail]' :
            mailBoxInformation ['folder'].append ({'name' : str(f['name']), 'messaggiNumero' : mailbox.folder.status(str(f['name'])) ['MESSAGES']})
    return jsonify(data={'status' : 'success', 'msg': 'Messaggio spostato correttamente', 'mailBoxInformation' : mailBoxInformation}) #Responso per il client

@main.route('/planning')
@login_required
def planning():
    return render_template('planning.html')

