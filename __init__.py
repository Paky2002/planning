#IMPORTO LE LIBRERIE

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

def page_not_found(e):
  return render_template('error/errors-404-error.html'), 404

def server_error(e):
  return render_template('error/errors-500-error.html'), 500

db = SQLAlchemy() # CREO OGGETTO PER I DB

def create_app():

    #flask db stamp head - flask db migrate - flask db upgrade

    app = Flask(__name__) #Creo app principale
    migrate = Migrate(app, db)
    app.config['SECRET_KEY'] = 'secret-key-goes-here' #ASSEGNO UNA SECRET KEY ALLA MIA APP 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' #ASSEGNO URL PER I DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #SETTO IL MODIFICATORE SU FALSO
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False # Disabilita le pre-request CSRF

    from .auth import auth as auth_blueprint #DOPO AVER CREATO L'APP IMPORTO I BLUEPRINT DEL FILE AUTH (LOGIN E REGISTRAZIONE)
    app.register_blueprint(auth_blueprint) #REGISTRO IL BLUEPRINT NELL 'APP

    from .main import main as main_blueprint #DOPO AVER CREATO L'APP IMPORTO I BLUEPRINT DEL FILE MAIN (LOGIN E REGISTRAZIONE)
    app.register_blueprint(main_blueprint) #REGISTRO IL BLUEPRINT

    from .camere import camere as camere_blueprint #DOPO AVER CREATO L'APP IMPORTO I BLUEPRINT DEL FILE MAIN (LOGIN E REGISTRAZIONE)
    app.register_blueprint(camere_blueprint) #REGISTRO IL BLUEPRINT

    from .tariffe import tariffe as tariffe_blueprint #DOPO AVER CREATO L'APP IMPORTO I BLUEPRINT DEL FILE MAIN (LOGIN E REGISTRAZIONE)
    app.register_blueprint(tariffe_blueprint) #REGISTRO IL BLUEPRINT

    from .extra import extra as extra_blueprint #DOPO AVER CREATO L'APP IMPORTO I BLUEPRINT DEL FILE MAIN (LOGIN E REGISTRAZIONE)
    app.register_blueprint(extra_blueprint) #REGISTRO IL BLUEPRINT

    from .preventivi import preventivi as preventivi_blueprint #DOPO AVER CREATO L'APP IMPORTO I BLUEPRINT DEL FILE MAIN (LOGIN E REGISTRAZIONE)
    app.register_blueprint(preventivi_blueprint) #REGISTRO IL BLUEPRINT

    from .prenotazioni import prenotazioni as prenotazioni_blueprint #DOPO AVER CREATO L'APP IMPORTO I BLUEPRINT DEL FILE MAIN (LOGIN E REGISTRAZIONE)
    app.register_blueprint(prenotazioni_blueprint) #REGISTRO IL BLUEPRINT

    app.register_error_handler(404, page_not_found) #SETTO IL TEMPLATE PER ERRORE 404 (not found)
    app.register_error_handler(500, server_error) #SETTO IL TEMPLATE PER ERRORE 500 (server error)

    db.init_app(app) #DO ALL'OGGETTO DB I PARAMETRI PRINCIPALI DELLA MIA APPP
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    csrf = CSRFProtect() #CREO L'OGGETTO PER LA PROTEZIONE ALLE RICHIESTE ESTERNE
    csrf.init_app(app) #INIZIALIZZO 

    from .models import User, Preventivo, TipologiaCamere, Camere, Tariffe, Periodi, Extra, Arrivi, ArriviSupplementi, ArriviExtra, ArriviPagamenti, Contatti #IMPORTO IL MODELLO DEGLI USER

    admin = Admin (app) #CREO IL MIO PANNELLO ADMIN BACKEND
    
    admin.add_view (ModelView(User, db.session)) #AGGIUNGO DI VEDERE IL DB USER
    admin.add_view (ModelView(Preventivo, db.session)) #AGGIUNGO DI VEDERE IL DB RICHIESTA
    admin.add_view (ModelView(TipologiaCamere, db.session)) #AGGIUNGO DI VEDERE IL DB TIPOLOGIA CAMERE
    admin.add_view (ModelView(Camere, db.session)) #AGGIUNGO DI VEDERE IL DB CAMERE
    admin.add_view (ModelView(Tariffe, db.session)) #AGGIUNGO DI VEDERE IL DB TARIFFE 
    admin.add_view (ModelView(Periodi, db.session)) #AGGIUNGO DI VEDERE IL DB PERIODI
    admin.add_view (ModelView(Extra, db.session)) #AGGIUNGO DI VEDERE IL DB PERIODI
    admin.add_view (ModelView(Arrivi, db.session)) #AGGIUNGO DI VEDERE IL DB PERIODI
    admin.add_view (ModelView(ArriviSupplementi, db.session)) #AGGIUNGO DI VEDERE IL DB PERIODI
    admin.add_view (ModelView(ArriviExtra, db.session)) #AGGIUNGO DI VEDERE IL DB PERIODI
    admin.add_view (ModelView(ArriviPagamenti, db.session)) #AGGIUNGO DI VEDERE IL DB PERIODI
    admin.add_view (ModelView(Contatti, db.session)) #AGGIUNGO DI VEDERE IL DB PERIODI
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app #DOPO AVER INIZIALIZATO TUTTO RITORNO L'APP