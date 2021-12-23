from flask import Blueprint,render_template, request, jsonify, redirect, url_for
from . import db
from .models import Preventivo, Periodi, TipologiaCamere, Camere, Arrivi, Extra, Contatti, ArriviSupplementi
from flask_login import login_required, current_user
from datetime import timedelta, date, datetime
from .form import AggiungiPreventivo, AggiungiPrenotazione, RegistraCliente, AggiungiExtraPrenotazione, AggiungiPagamentoPrenotazione
from sqlalchemy import and_
import json
from datetime import datetime

prenotazioni = Blueprint('prenotazioni_', __name__)

@prenotazioni.context_processor
def global_variable():
    return dict(nome=current_user.name)

@prenotazioni.route('/aggiungiPrenotazione')
@login_required
def aggiungiPrenotazioniView(formData = '', idCamera = '', trattamento = '', prezzo = '', idPreventivo = '', idExtra = '', prezzoSupplementi = ''):
    preventivo, camera =  '', ''
    extra = Extra.query.filter_by (account_id = current_user.get_id()).all()
    extraJson = {}
    for i in Extra.query.filter_by (account_id = current_user.get_id()).all() : 
        extraJson [i.getId] = i.toJson 
    if formData != '' : 
        form = formData
        camera = Camere.query.filter_by (id = idCamera).first()
        tariffe = camera.tipologia.tariffe
        prezzo = prezzo
        if trattamento == 'bb' : trattamento = 'Bed&Breakfast'
        if trattamento == 'mp' : trattamento = 'Mezza pensione'
        if trattamento == 'pc' : trattamento = 'Pensione completa'
        
        trattamento = trattamento
        ciao = 3
    else : 
        form = AggiungiPrenotazione ()
        ciao = 1

    return render_template('prenotazione.html', form = form, ciao = ciao, preventivo = preventivo, camera = camera, trattamento = trattamento, prezzo=prezzo, extra = extra, extraJson = extraJson, idCamera = idCamera, idPreventivo = idPreventivo, idExtra = idExtra, prezzoSupplementi = prezzoSupplementi)

@prenotazioni.route('/createPrenotazione', methods=['get', 'post'])
@login_required
def createPrenotazione():
    idCamera, trattamento, idExtra, idPreventivo, prezzo, prezzoSupplementi = request.args.get('idCamera'), request.args.get('trattamento'), request.args.getlist('idExtra'), request.args.get('idPreventivo'), request.args.get('prezzo'), request.args.get('prezzoSupplementi')
    idExtraDict = {}
    for extraId in idExtra : idExtraDict [extraId] = idExtra.count (extraId)
    idExtra = idExtraDict
    form = AggiungiPrenotazione (request.form, trattamento = trattamento)
    return aggiungiPrenotazioniView(form,  idCamera, trattamento, prezzo, idPreventivo, idExtra, prezzoSupplementi)

def getPrenotazioneAggiornata (idPrenotazione) :
    dictAggiornato = {}
    prenotazione = Arrivi.query.filter (Arrivi.preventivo.has(and_(Preventivo.account_id == current_user.get_id(), Arrivi.id == idPrenotazione))).first()
    dictAggiornato ['prezzoSupplementi'] = prenotazione.calcolaPrezziSupplementi()
    dictAggiornato ['prezzoExtra'] = prenotazione.calcolaPrezziExtra()
    dictAggiornato ['tassaSoggiorno'] = prenotazione.calcolaTassaSoggiorno()
    dictAggiornato ['totale'] = prenotazione.calcolaTotale()
    dictAggiornato ['pagato'] = prenotazione.getPagamenti()
    return dictAggiornato

@prenotazioni.route ('/inserisciPrenotazione', methods = ['post'])
@login_required
def inserisciPrenotazione () :
    listCamere = request.get_json()
    for camera in listCamere['camere'] :
        if camera ['numeroStanza'] != '000000' : 
            preventivo = Preventivo.query.filter_by (id = camera ['idPreventivo']).first()
            camera_ = Camere.query.filter_by (id = camera ['idCamera']).first()
            if preventivo.account_id == int(current_user.get_id()) :
                if camera_.tipologia.account_id == int(current_user.get_id()) :
                    arrivo = Arrivi (
                        trattamento = camera ['trattamento'],
                        prezzoCamera = camera ['prezzo'],
                    )
                    arrivo.aggiungiSupplemento(Extra.query.filter(Extra.id.in_(list(camera['extra'].keys()))).all(), list(camera['extra'].values()))
                    arrivo.prezzoSupplementi = sum(a.prezzoExtra * int(b) for a, b in zip(Extra.query.filter(Extra.id.in_(list(camera['extra'].keys()))).all(), list(camera['extra'].values())))
                    arrivo.camera = camera_
                    arrivo.preventivo = preventivo
                    db.session.add (arrivo)
                    db.session.commit ()
                    i = Arrivi.query.filter_by (id = arrivo.id).first()
    return jsonify({'data':'ciao'})

@prenotazioni.route ('/eliminaExtraPrenotazione', methods = ['post'])
@login_required
def eliminaExtraPrenotazione () :
    idPrenotazione = request.form ['idPrenotazione']
    prenotazione =  Arrivi.query.filter(Arrivi.preventivo.has(and_(Preventivo.account_id == current_user.get_id(), Arrivi.id == idPrenotazione))).first()
    if prenotazione is None :
        return jsonify(data={'status' : 'error', 'msg' : 'Errore'})
    else :
        prenotazione.deleteExtra (request.form ['idExtra'])
        db.session.commit()
        return jsonify(data={'status' : 'success', 'msg' : 'Extra eliminato corretamente', 'dictAggiornato' : getPrenotazioneAggiornata(idPrenotazione), 'id' : request.form ['idExtra']})

@prenotazioni.route ('/activeTassaSoggiorno', methods = ['post'])
@login_required
def activeTassaSoggiorno () :
    idPrenotazione = request.form ['idPrenotazione']
    prenotazione =  Arrivi.query.filter(Arrivi.preventivo.has(and_(Preventivo.account_id == current_user.get_id(), Arrivi.id == idPrenotazione))).first()
    if prenotazione is None :
        return jsonify(data={'status' : 'error', 'msg' : 'Errore'})
    else :
        prenotazione.tassaSoggiorno = int(request.form ['stato'])
        db.session.commit()
        return jsonify(data={'status' : 'success', 'msg' : 'Stato cambiato corretamente', 'dictAggiornato' : getPrenotazioneAggiornata(idPrenotazione)})

@prenotazioni.route('/aggiungiExtraPrenotazione', methods=['post'])
@login_required
def aggiungiExtraPrenotazione():
    form = AggiungiExtraPrenotazione()
    idPrenotazione = request.form['idPrenotazione']
    if form.validate_on_submit () :
        prenotazione = Arrivi.query.filter (Arrivi.preventivo.has(and_(Preventivo.account_id == current_user.get_id(), Arrivi.id == idPrenotazione))).first()
        if prenotazione is None :
            return jsonify(data={'status' : 'error', 'msg' : 'Stato non cambiato'})
        else :
            nuovoExtra = prenotazione.aggiungiExtra(request.form['nome'], request.form['quantita'], request.form['prezzo'])
            db.session.commit()
            newDictExtra = {}
            newDictExtra ['nome'] = nuovoExtra.nome
            newDictExtra ['prezzo'] = nuovoExtra.prezzo
            newDictExtra ['quantita'] = nuovoExtra.quantita
            newDictExtra ['id'] = nuovoExtra.id
            return jsonify(data={'status' : 'success', 'msg' : 'Stato cambiato corretamente','newDictExtra' : newDictExtra, 'dictAggiornato' : getPrenotazioneAggiornata(idPrenotazione)})
    else :
        print ('errore ',form.errors)
        return jsonify(data={'status' : 'error', 'msg' : form.errors})

@prenotazioni.route('/eliminaPagamentoPrenotazione', methods=['post'])
@login_required
def eliminaPagamentoPrenotazione():
    idPrenotazione = request.form ['idPrenotazione']
    prenotazione =  Arrivi.query.filter(Arrivi.preventivo.has(and_(Preventivo.account_id == current_user.get_id(), Arrivi.id == idPrenotazione))).first()
    if prenotazione is None :
        return jsonify(data={'status' : 'error', 'msg' : 'Errore'})
    else :
        prenotazione.deletePagamento (request.form ['idPagamento'])
        db.session.commit()
        return jsonify(data={'status' : 'success', 'msg' : 'Pagamento eliminato corretamente', 'dictAggiornato' : getPrenotazioneAggiornata(idPrenotazione), 'id' : request.form ['idPagamento']})

@prenotazioni.route('/aggiungiPagamentoPrenotazione', methods=['post'])
@login_required
def aggiungiPagamentoPrenotazione():
    form = AggiungiPagamentoPrenotazione()
    idPrenotazione = request.form['idPrenotazione']
    if form.validate_on_submit () :
        prenotazione = Arrivi.query.filter (Arrivi.preventivo.has(and_(Preventivo.account_id == current_user.get_id(), Arrivi.id == idPrenotazione))).first()
        if prenotazione is None :
            return jsonify(data={'status' : 'error', 'msg' : 'Stato non cambiato'})
        else :
            pagamento = prenotazione.aggiungiPagamento(request.form['pagamento'])
            db.session.commit()
            newDictPagamento={}
            newDictPagamento ['pagamento'] = pagamento.pagamento
            newDictPagamento ['data'] = pagamento.dataPagamento.strftime('%d-%m-%Y %H:%M')
            newDictPagamento ['id'] = pagamento.id
            print (pagamento.id)
            return jsonify(data={'status' : 'success', 'msg' : 'Stato cambiato corretamente', 'dictAggiornato' : getPrenotazioneAggiornata(idPrenotazione), 'newDictPagamento' : newDictPagamento})
    else :
        print ('errore ',form.errors)
        return jsonify(data={'status' : 'error', 'msg' : form.errors})

@prenotazioni.route('/modificaSupplementiPrenotazione', methods=['post'])
@login_required
def modificaSupplementiPrenotazione(): 
    data =  request.get_json(force=True)
    prenotazione = Arrivi.query.filter (Arrivi.preventivo.has(and_(Preventivo.account_id == current_user.get_id(), Arrivi.id == data ['idPrenotazione']))).first()
    if prenotazione is None : 
        return jsonify (data = {'status' : 'error', 'msg' : 'Stato non cambiato'})
    else :
        prenotazione = Arrivi.query.filter_by (id = data ['idPrenotazione']).first()
        for supplemento_arrivo  in prenotazione.supplementi_arrivi :
            db.session.delete(supplemento_arrivo)
        prenotazione.aggiungiSupplemento(Extra.query.filter(Extra.id.in_(list(data ['dictSupplementi'].keys()))).all(), list(data ['dictSupplementi'].values()))
        db.session.commit ()
        return jsonify (data = {'status' : 'success', 'msg' : 'Supplementi modificati correttamente', 'dictAggiornato' : getPrenotazioneAggiornata(data ['idPrenotazione'])})

@prenotazioni.route('/prenotazioneInfo/<int:idPrenotazione>')
@login_required
def prenotazioneInfo(idPrenotazione):
    prenotazione = Arrivi.query.filter (Arrivi.preventivo.has(and_(Preventivo.account_id == current_user.get_id(), Arrivi.id == idPrenotazione))).first()
    supplementi = Extra.query.filter_by (account_id = current_user.get_id()).all()
    form, formExtra, formPagamento = RegistraCliente(), AggiungiExtraPrenotazione (), AggiungiPagamentoPrenotazione()
    valueSupplementi = {}
    for prenotazione_supplementi in prenotazione.supplementi_arrivi :
        valueSupplementi [prenotazione_supplementi.id] = prenotazione_supplementi.quantita 
    with open('static/data/paesi.json') as json_file: dataPaesi = json.load(json_file)
    with open('static/data/comuni.json') as json_file: dataComuni = json.load(json_file)
    return render_template('prenotazioneInfo.html', valueSupplementi=valueSupplementi, prenotazione = prenotazione, supplementi = supplementi ,form = form, formExtra = formExtra,formPagamento = formPagamento, dataPaesi = dataPaesi, dataComuni = dataComuni, idPrenotazione = idPrenotazione)

@prenotazioni.route('/cambiaStatoSoggiorno', methods = ['post'])
@login_required
def cambiaStatoSoggiorno():
    nuovoStato, idPrenotazione = request.form ['nuovoStato'], request.form ['idPrenotazione']
    prenotazione = Arrivi.query.filter (Arrivi.preventivo.has(and_(Preventivo.account_id == current_user.get_id(), Arrivi.id == idPrenotazione))).first()
    if prenotazione is None :
        return jsonify(data={'status' : 'error', 'msg' : 'Stato non cambiato'})
    else :
        prenotazione.statoSoggiorno = nuovoStato
        db.session.commit()
        return jsonify(data={'status' : 'success', 'msg' : 'Stato cambiato corretamente'})

@prenotazioni.route('/cambiaStatoPagamento', methods = ['post'])
@login_required
def cambiaStatoPagamento():
    nuovoStato, idPrenotazione = request.form ['nuovoStato'], request.form ['idPrenotazione']
    prenotazione = Arrivi.query.filter (Arrivi.preventivo.has(and_(Preventivo.account_id == current_user.get_id(), Arrivi.id == idPrenotazione))).first()
    if prenotazione is None :
        return jsonify(data={'status' : 'error', 'msg' : 'Stato non cambiato'})
    else :
        prenotazione.statoPagamento = nuovoStato
        db.session.commit()
        return jsonify(data={'status' : 'success', 'msg' : 'Stato cambiato corretamente', 'dictAggiornato' : getPrenotazioneAggiornata(idPrenotazione)})

### OPERAZIONE SUI CONTATTI ###

@prenotazioni.route('/registraCliente/<int:idPrenotazione>', methods = ['post'])
@login_required
def registraCliente(idPrenotazione):
    form = RegistraCliente ()
    if form.validate_on_submit () :
        nuovoContatto = Contatti (
            cognome = request.form ['cognome'],
            nome = request.form ['nome'],
            cittadinanza = request.form ['cittadinanza'],
            sesso = request.form ['sesso'],
            telefono = request.form ['telefono'],
            email = request.form ['email'],
            dataDiNascita = datetime.strptime(request.form ['dataDiNascita'], "%Y-%m-%d").date(),
            paeseNascita = request.form ['paeseNascita'],
            comuneNascita = request.form ['comuneNascita'],
            paeseResidenza = request.form ['paeseResidenza'],
            comuneResidenza = request.form ['comuneResidenza'],
            cap = request.form ['cap'],
            indirizzo = request.form ['indirizzo'],
            documento = request.form ['documento'],
            paeseImmissione = request.form ['paeseImmissione'],
            numeroDocumento = request.form ['numeroDocumento'],
            emessoDa = request.form ['emessoDa'],
            dataEmissione = datetime.strptime(request.form ['dataEmissione'], "%Y-%m-%d").date(),
            dataScadenza = datetime.strptime(request.form ['dataScadenza'], "%Y-%m-%d").date(),
        )
        nuovoContatto.prenotazione = Arrivi.query.filter_by (id = idPrenotazione).first()
        db.session.add(nuovoContatto)
        db.session.commit()
        return redirect(url_for('prenotazioni_.prenotazioneInfo', idPrenotazione=idPrenotazione))
    else :
        print (form.errors)

@prenotazioni.route('/eliminaContatto', methods = ['post'])
@login_required
def eliminaContatto():
    idPrenotazione = request.form['idPrenotazione']
    form = RegistraCliente ()
    prenotazione = Arrivi.query.filter (Arrivi.preventivo.has(and_(Preventivo.account_id == current_user.get_id(), Arrivi.id == idPrenotazione))).first()
    if prenotazione is None :
        return jsonify(data={'status' : 'error', 'msg' : 'Stato non cambiato'})
    else :
        prenotazione.eliminaContatto(request.form['idContatto'])
        db.session.commit()
        return jsonify(data={'status' : 'success', 'msg' : 'Cliente eliminato correttamente', 'dictAggiornato' : getPrenotazioneAggiornata(idPrenotazione)})

@prenotazioni.route('/registraCliente/<int:idPrenotazione>/<int:idContatto>', methods = ['post'])
@login_required
def modificaCliente(idPrenotazione, idContatto):
    form = RegistraCliente ()
    if form.validate_on_submit () :
        prenotazione = Arrivi.query.filter (Arrivi.preventivo.has(and_(Preventivo.account_id == current_user.get_id(), Arrivi.id == idPrenotazione))).first()
        prenotazione.modificaContatto(idContatto, request.form)
        db.session.commit()
        return redirect(url_for('prenotazioni_.prenotazioneInfo', idPrenotazione=idPrenotazione))
    else :
        print (form.errors)

@prenotazioni.route('/getContatto', methods = ['post'])
@login_required
def getContatto():
    idPrenotazione = request.form['idPrenotazione']
    prenotazione = Arrivi.query.filter (Arrivi.preventivo.has(and_(Preventivo.account_id == current_user.get_id(), Arrivi.id == idPrenotazione))).first()
    if prenotazione is None :
        return jsonify(data={'status' : 'error', 'msg' : 'Stato non cambiato'})
    else : 
       contatto = Contatti.query.filter (and_(Contatti.id == request.form['idContatto'], Contatti.prenotazione == prenotazione)).first()
       if contatto is None :
           return jsonify(data={'status' : 'error', 'msg' : 'Stato non cambiato'})
       else :
           return jsonify(data={'status' : 'success', 'msg' : 'Stato cambiato corretamente', 'conctat' : contatto.getConctatDict()})


