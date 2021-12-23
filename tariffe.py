from flask import Blueprint,render_template, request, jsonify, redirect, url_for
from . import db
from .models import TipologiaCamere, Periodi, Tariffe
from flask_login import login_required, current_user
import datetime
from .form import AggiungiPeriodo
#from form import 

tariffe = Blueprint('tariffe_', __name__)

@tariffe.context_processor
def global_variable():
    return dict(nome=current_user.name)

### VIEW PRINCIPALE ###

@tariffe.route('/tariffe')
@login_required
def tariffeView():
    form = AggiungiPeriodo ()
    tipologiaCamere = TipologiaCamere.query.filter_by(account_id=current_user.get_id()).all()
    periodi = Periodi.query.filter_by(account_id=current_user.get_id()).all()
    tipiSoggiorno = ['B&B', 'Mezza pensione', 'Pensione completa']
    return render_template('tariffe.html',tipologiaCamere = tipologiaCamere, tipiSoggiorno = tipiSoggiorno, periodi = periodi, form = form)

### PERIODI REQUEST ###

@tariffe.route('/tariffePost', methods=['post'])
@login_required
def tariffePost():
    form = AggiungiPeriodo ()
    if form.validate_on_submit () :

        nuovoPeriodo = Periodi (
            inizio = form.dataInizio.data,
            fine = form.dataFine.data,
            account_id = current_user.get_id()
        )

        tipologie =  TipologiaCamere.query.filter_by (account_id = current_user.get_id())
        nuoveTariffe = list ()
        for tipologia in tipologie :
            nuovaTariffa = Tariffe (
                bedBreakfast = 0,
                bedBreakfastSettimana = 0,
                mezzaPensione = 0,
                mezzaPensioneSettimana = 0,
                pensioneCompleta = 0,
                pensioneCompletaSettimana = 0
            )

            nuovaTariffa.periodo = nuovoPeriodo
            nuovaTariffa.tipologia = tipologia
            nuoveTariffe.append (nuovaTariffa)

        db.session.add (nuovoPeriodo, nuoveTariffe)
        db.session.commit()
        
    else :
        print ('ERROR', form.errors)
    
    return redirect (url_for('tariffe_.tariffeView'))

@tariffe.route ('/getPeriodi/', methods=['post'])
@login_required
def getPeriodi():
    periodi = Periodi.query.filter_by(account_id=current_user.get_id()).all()
    id_periodo = {'id' : []}
    for periodo in periodi :
        id_periodo ['id'].append (periodo.id)
    return jsonify(data={'status':'success', 'data': id_periodo})

@tariffe.route ('/eliminaPeriodo/', methods=['post'])
@login_required
def eliminaPeriodo():
    if Periodi.query.filter_by(id=request.form['id']).first().account_id == int(current_user.get_id()) :
       db.session.delete(Periodi.query.filter_by (id=request.form ['id']).first())    
       db.session.commit()
       return jsonify(data={'status' : 'success'})
    else :
        return jsonify(data={'status' : 'error'})

@tariffe.route ('/cambiaPeriodo/', methods=['post'])
@login_required
def cambiaPeriodo():
    form = AggiungiPeriodo ()
    if form.validate_on_submit ():
        if Periodi.query.filter_by(id = request.form['id']).first().account_id == int(current_user.get_id()) :
            Periodi.query.filter_by(id = request.form['id']).first().inizio = form.dataInizio.data
            Periodi.query.filter_by(id = request.form['id']).first().fine = form.dataFine.data 
            db.session.commit()
            return jsonify(data={'status' : 'success'})
        else :
            return jsonify(data={'status' : 'error'})

### TARIFFE REQUEST ###

@tariffe.route('/modificaTariffe/', methods=['post'])
@login_required
def modificaTariffe():
    if Tariffe.query.filter_by(id=request.form['dataTariffa']).first().tipologia.account_id == int(current_user.get_id()) :
        if int(request.form['tipologia']) == 0 :
            Tariffe.query.filter_by(id=request.form['dataTariffa']).first().bedBreakfast = int(request.form['prezzoNotte'])
            Tariffe.query.filter_by(id=request.form['dataTariffa']).first().bedBreakfastSettimana = int(request.form['prezzoSettimana'])
        if int(request.form['tipologia']) == 1 :
            Tariffe.query.filter_by(id=request.form['dataTariffa']).first().mezzaPensione = int(request.form['prezzoNotte'])
            Tariffe.query.filter_by(id=request.form['dataTariffa']).first().mezzaPensioneSettimana = int(request.form['prezzoSettimana'])
        if int(request.form['tipologia']) == 2 :
            Tariffe.query.filter_by(id=request.form['dataTariffa']).first().pensioneCompleta = int(request.form['prezzoNotte'])
            Tariffe.query.filter_by(id=request.form['dataTariffa']).first().pensioneCompletaSettimana = int(request.form['prezzoSettimana'])
        db.session.commit() #Invio 
        return jsonify(data={'status' : 'success', 'message': 'Inserito correttamente'}) #Responso per il client
    else :
        return jsonify(data={'status' : 'errore', 'message': 'Nessuna tipologia corrispondente al tuo account'}) #Responso per il client

@tariffe.route('/resetTariffe/', methods=['post'])
@login_required
def resetTariffe():
    if Tariffe.query.filter_by(id=request.form['dataTariffa']).first().tipologia.account_id == int(current_user.get_id()) :
        if int(request.form['tipologia']) == 0 :
            Tariffe.query.filter_by(id=request.form['dataTariffa']).first().bedBreakfast = 0
            Tariffe.query.filter_by(id=request.form['dataTariffa']).first().bedBreakfastSettimana = 0
        if int(request.form['tipologia']) == 1 :
            Tariffe.query.filter_by(id=request.form['dataTariffa']).first().mezzaPensione = 0
            Tariffe.query.filter_by(id=request.form['dataTariffa']).first().mezzaPensioneSettimana = 0
        if int(request.form['tipologia']) == 2 :
            Tariffe.query.filter_by(id=request.form['dataTariffa']).first().pensioneCompleta = 0
            Tariffe.query.filter_by(id=request.form['dataTariffa']).first().pensioneCompletaSettimana = 0
        db.session.commit() #Invio 
        return jsonify(data={'status' : 'success', 'message': 'Inserito correttamente'}) #Responso per il client
    else :
        return jsonify(data={'status' : 'errore', 'message': 'Nessuna tipologia corrispondente al tuo account'}) #Responso per il client

