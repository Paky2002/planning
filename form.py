from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, SelectField,HiddenField, PasswordField, DateField
from wtforms.validators import Email, Length, ValidationError,  InputRequired


def validate_numero_persone (form, field):
    if field.data < 1:
        raise ValidationError('Inserisci almeno una perasona')

class Login(FlaskForm):
    email = StringField(
      'Email',
      render_kw={'class':'form-control radius-30', 'type':'email'}, 
      validators=[InputRequired(), Length(1, 64), Email()])

    password = PasswordField(
      'Password', 
      render_kw={'class':'form-control radius-30', 'type':'password'}, 
      validators=[InputRequired()])

#FORM NELLA PAGINA CAMERE

class AggiungiTipologia (FlaskForm):

    numero_persone = IntegerField(
      'Numero persone', 
      render_kw={'class':'form-control radius-30','type':'number', 'value':'1', 'data-tipologia': 'NameModel'}, 
      validators=[InputRequired()])

    tipologia = StringField(
      'Nome tipologia', 
      render_kw={'class':'form-control radius-30', 'type':'text'}, 
      validators=[InputRequired(), Length(min=4, message='Inserisci un nome completo')])

    tipo = SelectField(
        'Tipo',
        choices = [('camera', 'Camera'), ('appartamento', 'Appartamento'), ('bungalow','Bungalow')],
        render_kw={'class':'form-control radius-30'}, 
        validators=[InputRequired()])

class ModificaTipologia (AggiungiTipologia):
    
    id_tipologia = IntegerField(
      'ID', 
      render_kw={'class':'form-control radius-30','type':'number', 'value':'1', 'data-tipologia': 'NameModel', 'readonly': True}, 
      validators=[InputRequired()])
    
class AggiungiCamera (FlaskForm):

    numero_camera = IntegerField(
      'Numero camera', 
      render_kw={'class':'form-control radius-30', 'id':'numero_camera','type':'number', 'value':'1', 'data-tipologia' : '0'}, 
      validators=[InputRequired()])

#FINE FORM NELLA PAGINA CAMERA

#FORM NELLA PAGINA TARIFFE

class AggiungiPeriodo (FlaskForm) :

  dataInizio = DateField(
      'Inizio periodo', 
      render_kw={'class':'form-control radius-30','type':'date'}, 
      validators=[InputRequired()])

  dataFine = DateField(
      'Fine periodo', 
      render_kw={'class':'form-control radius-30','type':'date'}, 
      validators=[InputRequired()])

#FORM NELLA PAGINA EXTRA

class AggiungiExtra (FlaskForm) :

  nomeExtra = StringField (
    'Nome extra',
    render_kw={'class':'form-control radius-30','type':'text'}, 
    validators=[InputRequired()])

  prezzoExtra = IntegerField (
    'Prezzo extra',
    render_kw={'class':'form-control radius-30','type':'number'}, 
    validators=[InputRequired()])

  tipoExtra = SelectField (
    'tipo extra',
    choices = [('per_camera', 'Per camera'), ('per_persona', 'A persona')],
    render_kw={'class':'form-control radius-30'}, 
    validators=[InputRequired()])

#FORM NELLA PAGINA PREVENTIVO

class AggiungiPreventivo (FlaskForm) :

  cognome = StringField (
    'Cognome',
    render_kw={'class':'form-control radius-30 clean','type':'text'}, 
    validators = [InputRequired()]
  )

  checkIn = DateField (
    'check-In',
    render_kw={'class':'form-control radius-30','type':'date'}, 
    validators = [InputRequired()]
  )

  checkOut = DateField (
    'check-oUT',
    render_kw={'class':'form-control radius-30','type':'date'}, 
    validators = [InputRequired()]
  )

  adulti = IntegerField (
    'Adulti',
    render_kw={'class':'form-control radius-30 clean','type':'number'}, 
    validators=[InputRequired()])

  ridotti = IntegerField (
    'Ridotti',
    render_kw={'class':'form-control radius-30 clean','type':'number'}, 
    validators=[InputRequired()])

  infant = IntegerField (
    'Infant',
    render_kw={'class':'form-control radius-30 clean','type':'number'}, 
    validators=[InputRequired()])

  telefono = StringField (
    'Telefono',
    render_kw={'class':'form-control radius-30 clean','type':'number'}, 
    validators=[InputRequired()])

  email = StringField (
    'Email',
    render_kw={'class':'form-control radius-30 clean','type':'text'}, 
    validators=[InputRequired()])

#FORM NELLA PAGINA PRENOTAZIONE 

class AggiungiPrenotazione (AggiungiPreventivo) :

  trattamento = SelectField (
    'Trattamento',
    choices = [('Bed&Breakfast', 'Bed&Breakfast'), ('Mezza pensione', 'Mezza pensione'), ('Pensione completa','Pensione completa')],
    render_kw={'class':'form-control radius-30'}, 
  )

#FORM REGISTRA CLIENTE

class RegistraCliente (FlaskForm) :

  nome = StringField (
    'Nome',
    render_kw={'class':'form-control radius-30','type':'text'}, 
    validators = [InputRequired()]
  )

  cognome = StringField (
    'Cognome',
    render_kw={'class':'form-control radius-30','type':'text'}, 
    validators = [InputRequired()]
  )

  cittadinanza = StringField (
    'Cittadinanza',
    render_kw={'class':'form-control radius-30','type':'text'}, 
    validators = [InputRequired()]
  )

  sesso = SelectField (
    'Sesso',
    choices = [('Maschio', 'Maschio'), ('Donna', 'Donna'), ('Non specificato','Non specificato')],
    render_kw={'class':'form-control radius-30','type':'number'}, 
    validators=[InputRequired()])

  telefono = StringField (
    'Telefono',
    render_kw={'class':'form-control radius-30','type':'number'}, 
    validators=[InputRequired()])

  email = StringField (
    'Email',
    render_kw={'class':'form-control radius-30','type':'email'}, 
    validators=[InputRequired()])

  dataDiNascita = DateField (
    'Data di nascita',
    render_kw={'class':'form-control radius-30','type':'date'}, 
    validators=[InputRequired()])

  paeseNascita = StringField (
    'Paese Nascita',
    render_kw={'class':'form-control radius-30','type':'text', 'list':"paesi"}, 
    validators=[InputRequired()])

  paeseResidenza = StringField (
    'Paese Residenza',
    render_kw={'class':'form-control radius-30','type':'text', 'list':"paesi"}, 
    validators=[InputRequired()])

  comuneNascita = StringField (
    'Comune Nascita',
    render_kw={'class':'form-control radius-30','type':'text', 'list':"comuni"}, 
    validators=[InputRequired()])

  comuneResidenza = StringField (
    'Comune Residenza',
    render_kw={'class':'form-control radius-30','type':'text', 'list':"comuni"}, 
    validators=[InputRequired()])

  cap = StringField (
    'Cap',
    render_kw={'class':'form-control radius-30','type':'number'}, 
    validators=[InputRequired()])

  indirizzo = StringField (
    'Indirizzo',
    render_kw={'class':'form-control radius-30','type':'text'}, 
    validators=[InputRequired()])

  documento = StringField (
    'Documento',
    render_kw={'class':'form-control radius-30','type':'text'}, 
    validators=[InputRequired()])

  paeseImmissione = StringField (
    'Paese di immissione',
    render_kw={'class':'form-control radius-30','type':'text'}, 
    validators=[InputRequired()])

  numeroDocumento = StringField (
    'Numero documento',
    render_kw={'class':'form-control radius-30','type':'number'}, 
    validators=[InputRequired()])

  emessoDa = StringField (
    'Emesso da',
    render_kw={'class':'form-control radius-30','type':'text'}, 
    validators=[InputRequired()])

  dataEmissione = DateField (
    'Data Di Emissione',
    render_kw={'class':'form-control radius-30','type':'date'}, 
    validators=[InputRequired()])

  dataScadenza = DateField (
    'Data Di Scadenza',
    render_kw={'class':'form-control radius-30','type':'date'}, 
    validators=[InputRequired()])

class AggiungiExtraPrenotazione (FlaskForm) :

  nome = StringField (
    'Nome',
    render_kw={'class':'form-control radius-30','type':'text'}, 
    validators = [InputRequired()]
  )

  quantita = StringField (
    'Quantita',
    render_kw={'class':'form-control radius-30','type':'number'}, 
    validators = [InputRequired()]
  )

  prezzo = StringField (
    'Prezzo per uno',
    render_kw={'class':'form-control radius-30','type':'number', 'step':"0.01"}, 
    validators = [InputRequired()]
  )


class AggiungiPagamentoPrenotazione (FlaskForm) :

  pagamento = StringField (
    'Pagamento',
    render_kw={'class':'form-control radius-30','type':'number', 'step':"0.01"}, 
    validators = [InputRequired()]
  )


