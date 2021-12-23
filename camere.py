from flask import Blueprint,render_template, request, jsonify, redirect, url_for
from . import db
from .models import Camere, TipologiaCamere, Tariffe, Periodi
from flask_login import login_required, current_user
import datetime
from .form import AggiungiTipologia, AggiungiCamera, ModificaTipologia

camere = Blueprint('camere_', __name__) #DICHIARO IL BLUEPRINT

@camere.context_processor 
def global_variable():
    return dict(nome=current_user.name)

# @route -> /cemere
# 

@camere.route('/camere', methods=['POST']) 
@login_required
def tipologiaPost():
    form = AggiungiTipologia()
    if form.validate_on_submit():
        nuova_Tipologia = TipologiaCamere(form)
        nuoveTariffe = list ()
        periodi = Periodi.query.filter_by (account_id = current_user.get_id()).all()
        for periodo in periodi :
            nuovaTariffa = Tariffe(
                    bedBreakfast = 0, bedBreakfastSettimana = 0, 
                    mezzaPensione= 0, mezzaPensioneSettimana= 0,
                    pensioneCompleta= 0, pensioneCompletaSettimana= 0)
            nuovaTariffa.periodo = periodo
            nuovaTariffa.tipologia = nuova_Tipologia
            nuoveTariffe.append (nuovaTariffa)

        db.session.add(nuova_Tipologia, nuoveTariffe)
        db.session.commit()
    
    return redirect (url_for('camere_.camereView'))

@camere.route('/camere')
@login_required
def camereView():
    form, formCamere, formModificaTipologia = AggiungiTipologia() , AggiungiCamera(), ModificaTipologia ()
    tipologiaCamere = TipologiaCamere.query.filter_by(account_id=current_user.get_id()).all()
    return render_template('camere.html', tipologiaCamere = tipologiaCamere, form = form, formCamere = formCamere, formModificaTipologia = formModificaTipologia)

@camere.route('/apiTipologia/', methods=['post'])
@login_required
def apiTipologia():
    form = AggiungiCamera() #dichiaro il form su cui farò i controlli
    if form.validate_on_submit(): #Controllo la validazione del form
        tipologiaCamera = TipologiaCamere.query.filter_by(account_id=current_user.get_id()).filter_by(id=request.form['dataTipologia']).first() #Faccio un controllo server side per verificare che non ci siano stati cambi di dati
        if not tipologiaCamera : #Verifico che esista
            return jsonify(data={'status' : 'errore', 'message': 'Nessuna tipologia corrispondente al tuo account'}) #Responso per il client
        else :
            nuovaCamera = Camere(numeroCamera = request.form['numero_camera']) #Creo l'oggetto camera
            nuovaCamera.tipologia_id = tipologiaCamera.id #Aggiungo la FK
            db.session.add(nuovaCamera) #Aggiungo l'oggetto alla session 
            db.session.commit() #Invio 
            return jsonify(data={'status' : 'success', 'message': 'Inserito correttamente', 'numeroPosti' : tipologiaCamera.numeri_posti, 'data_camera' : nuovaCamera.id}) #Responso per il client
    else :
        return jsonify(data={'status' : 'errore', 'message': 'Compila correttamente il form'}) #Responso per il client

@camere.route('/apiModificaCamera/', methods=['post'])
@login_required
def modificaCamera():
    if Camere.query.filter_by(id=request.form['dataTipologia']).first().tipologia.account_id == int(current_user.get_id()) :
        Camere.query.filter_by(id=request.form['dataTipologia']).first().numeroCamera = int(request.form['nuovoNumero'])
        db.session.commit() #Invio 
        return jsonify(data={'status' : 'success', 'message': 'Inserito correttamente'}) #Responso per il client
    else :
        return jsonify(data={'status' : 'errore', 'message': 'Nessuna tipologia corrispondente al tuo account'}) #Responso per il client

@camere.route('/apiEliminaCamera/', methods=['post'])
@login_required
def eliminaCamera():
    if Camere.query.filter_by(id=request.form['dataTipologia']).first().tipologia.account_id == int(current_user.get_id()) :
        db.session.delete (Camere.query.filter_by(id=request.form['dataTipologia']).first())
        db.session.commit() #Invio 
        return jsonify(data={'status' : 'success', 'message': 'Inserito correttamente'}) #Responso per il client
    else :
        return jsonify(data={'status' : 'errore', 'message': 'Nessuna tipologia corrispondente al tuo account'}) #Responso per il client

@camere.route('/modificaTipologia/', methods=['post'])
@login_required
def modificaTipologia():
    formModificaTipologia = ModificaTipologia ()
    if formModificaTipologia.validate_on_submit():   
        if TipologiaCamere.query.filter_by(id=formModificaTipologia.id_tipologia.data).first().account_id == int(current_user.get_id())  :
            tipologiaDaModificare = TipologiaCamere.query.filter_by(id=formModificaTipologia.id_tipologia.data).first()
            tipologiaDaModificare.numeri_posti =formModificaTipologia.numero_persone.data
            tipologiaDaModificare.tipologia = formModificaTipologia.tipologia.data
            tipologiaDaModificare.tipo = formModificaTipologia.tipo.data
            db.session.commit()
    else :
        print (formModificaTipologia.errors)
    
    return redirect(url_for('camere_.camereView'))

@camere.route('/getTipologia/', methods=['post'])
@login_required
def getTipologia():
    tipologiaCamere = TipologiaCamere.query.filter_by(account_id=current_user.get_id()).all()
    id_tipologia = {'id' : []}
    for tipologia in tipologiaCamere :
        id_tipologia ['id'].append (tipologia.id)
    return jsonify(data={'status':'success', 'data': id_tipologia})

@camere.route('/eliminaTipologia/', methods=['post'])
@login_required
def eliminaTipologia():
    if TipologiaCamere.query.filter_by(id=request.form['id']).first().account_id == int(current_user.get_id()) :
       db.session.delete(TipologiaCamere.query.filter_by (id=request.form ['id']).first())    
       db.session.commit()
       return jsonify(data={'status' : 'success'})
    else :
        return jsonify(data={'status' : 'error'})
    

