from flask import Blueprint,render_template, request, jsonify, redirect, url_for
from . import db
from .models import Preventivo, Periodi, TipologiaCamere, Extra
from flask_login import login_required, current_user
from datetime import timedelta, date, datetime
from .form import AggiungiPreventivo
from sqlalchemy import and_, desc, asc

preventivi = Blueprint('preventivi_', __name__)

@preventivi.context_processor
def global_variable():
    return dict(nome=current_user.name)

@preventivi.route('/preventivo')
@login_required
def preventiviView():
    form = AggiungiPreventivo ()
    extra = Extra.query.filter_by (account_id = current_user.get_id()).all()
    extraJson = {}
    for i in Extra.query.filter_by (account_id = current_user.get_id()).all() : 
        extraJson [i.getId] = i.toJson 
    return render_template('preventivo.html', form = form, extraJson = extraJson, extra = extra)

@preventivi.route('/calcolaPreventivo', methods=['post'])
@login_required
def calcolaPrezzo():
    form = AggiungiPreventivo ()
    tariffeFine = {}
    if form.validate_on_submit () :
        nuovoPreventivo = Preventivo (
            cognome = request.form ['cognome'],
            checkIn = datetime.strptime(request.form ['checkIn'], "%Y-%m-%d").date(),
            checkOut = datetime.strptime(request.form ['checkOut'], "%Y-%m-%d").date(),
            adulti = request.form ['adulti'],
            ridotti = request.form ['ridotti'],
            infant = request.form ['infant'],
            telefono = request.form ['telefono'],
            email = request.form ['email'],
            account_id = current_user.get_id(),
        )
        db.session.add (nuovoPreventivo)
        db.session.commit ()

        periodi = Periodi.query.filter_by (account_id = current_user.get_id()).all()
        tipologie = TipologiaCamere.query.filter (and_(TipologiaCamere.numeri_posti >= int(request.form ['adulti']) + int(request.form['ridotti']), TipologiaCamere.account_id == current_user.get_id())).all()
        for tipologia in tipologie :
            tariffeFine[tipologia.tipologia] = []
            for camera in tipologia.camere :
                bb, mp, pc = 0,0,0
                if controllaDisponibilita(camera, nuovoPreventivo.checkIn, nuovoPreventivo.checkOut) == True:
                    for giorno in daterange(nuovoPreventivo.checkIn, nuovoPreventivo.checkOut): 
                        for tariffa in getPeriodo (giorno, periodi).tariffe :
                            if tariffa.tipologia == tipologia :
                                bb += tariffa.bedBreakfast 
                                mp += tariffa.mezzaPensione
                                pc += tariffa.pensioneCompleta
                    dictCamera = {
                        camera.numeroCamera : {'bb' : bb,'mp' : mp,'pc' : pc, 'tipo' : tipologia.tipo, 'idPreventivo' : nuovoPreventivo.id, 'idCamera' : camera.id}
                    }
                    tariffeFine[tipologia.tipologia].append(dictCamera)
    else : 
        print (form.errors)
    return jsonify(data={'status':'success', 'final' : tariffeFine}) 


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def controllaDisponibilita (camera,start_date, end_date) :
    for arrivo in camera.arrivi :
        if (start_date < arrivo.preventivo.checkOut) and (arrivo.preventivo.checkIn < end_date) :
            return False
    return True
     

def getPeriodo (giorno, periodi) :
    for periodo in periodi : 
        if periodo.inizio <= giorno <= periodo.fine :
            return periodo 


