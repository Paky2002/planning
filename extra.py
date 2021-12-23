from flask import Blueprint,render_template, request, jsonify, redirect, url_for
from . import db
from .models import Extra, Arrivi, Preventivo
from flask_login import login_required, current_user
import datetime
from .form import AggiungiExtra
from sqlalchemy import and_

extra = Blueprint('extra_', __name__)

@extra.context_processor
def global_variable():
    return dict(nome=current_user.name)

@extra.route('/extra')
@login_required
def extraView():
    form = AggiungiExtra ()
    extras = Extra.query.filter_by(account_id=current_user.get_id()).all()
    return render_template('extra.html', extras = extras, form = form)

@extra.route('/aggiungiExtra/', methods=['post'])
@login_required
def aggiungiExtra():
    form = AggiungiExtra ()
    if form.validate_on_submit () :
        nuovoExtra = Extra (
            nomeExtra = request.form['nomeExtra'],
            prezzoExtra = request.form['prezzoExtra'],
            tipoExtra = request.form['tipoExtra'],
            account_id = current_user.get_id()
        )
        db.session.add(nuovoExtra)
        db.session.commit ()
        return jsonify(data={'status' : 'success', 'nomeExtra' : nuovoExtra.nomeExtra, 'prezzoExtra' : nuovoExtra.prezzoExtra, 'tipoExtra' : request.form['tipoExtra']}) #Responso per il client
    else :
        print (form.errors)

@extra.route('/modificaExtra/', methods=['post'])
@login_required
def modificaExtra():
    if Extra.query.filter_by (id= request.form['id']).first().account_id == int (current_user.get_id()) :
        extraDaModificare = Extra.query.filter_by (id= request.form['id']).first()
        extraDaModificare.nomeExtranomeExtra =  request.form ['nomeExtra']
        extraDaModificare.prezzoExtra =  request.form ['prezzoExtra']
        extraDaModificare.prezzoExtra =  request.form ['prezzoExtra']
        extraDaModificare.tipoExtra =  request.form ['tipoExtra']
        db.session.commit ()
        return jsonify(data={'status':'success', 'message':'Extra modificato correttamente'})
    else :
        return jsonify (data={'status':'error', 'message':'Nessun Extra corrispondente al tuo account'})

@extra.route('/eliminaExtra/', methods=['post'])
@login_required
def eliminaExtra(): #eliminaExtra
    if Extra.query.filter_by (id= request.form['id']).first().account_id == int (current_user.get_id()) :
        extraDaEliminare = Extra.query.filter_by (id= request.form['id']).first()
        db.session.delete(extraDaEliminare)
        db.session.commit ()
        return jsonify(data={'status':'success', 'message':'Extra eliminato correttamente'})
    else :
        return jsonify (data={'status':'error', 'message':'Nessun Extra corrispondente al tuo account'})

    #CONCLUDERE LA MODIFICA, INSERIRE ID EXTRA 

@extra.route('/getExtra/', methods=['post'])
@login_required
def getExtra(): #eliminaExtra
    extras = Extra.query.filter_by(account_id=current_user.get_id()).all()
    extraList = []
    for extra in extras :
        extraDict = {'id': extra.id, 'nomeExtra' : extra.nomeExtra, 'prezzoExtra' : extra.prezzoExtra, 'tipoExtra' : extra.tipoExtra}
        extraList.append(extraDict)
    return jsonify(data={'status':'success', 'data': extraList})

    #CONCLUDERE LA MODIFICA, INSERIRE ID EXTRA 


    #CONCLUDERE LA MODIFICA, INSERIRE ID EXTRA 


        
    

