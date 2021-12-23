from flask_login import UserMixin
from . import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.types import (Integer,String,TypeDecorator)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import orm
import uuid
import json
from datetime import datetime, date
from sqlalchemy import inspect
from flask_login import login_required, current_user

#TYPE DECORATOR

class ArrayType(TypeDecorator):

    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

    def copy(self):
        return ArrayType(self.impl.length)

#ASSOCIATIVE TABLE

class ArriviSupplementi (db.Model) :
    __tablename__ = "arrivi_supplementi"
    id = db.Column('id_ArriviSupplementi', db.Integer(), primary_key=True, autoincrement=True, unique=True)
    idSupplemento = db.Column('id_supplemento', db.Integer, db.ForeignKey('arrivi.id_arrivo'))
    idPrenotazione = db.Column('id_prenotazione', db.Integer, db.ForeignKey('extra.id_extra'))
    prenotazione = relationship('Arrivi', back_populates= "supplementi_arrivi")
    supplemento = relationship('Extra', back_populates= "supplementi_arrivi")
    quantita = db.Column(db.Integer)

class ArriviExtra (db.Model) :
    __tablename__ = "arrivi_extra"
    id = db.Column('id_ArriviExtra', db.Integer(), primary_key=True, autoincrement=True, unique=True)
    idPrenotazione = db.Column('id_prenotazione', db.Integer, db.ForeignKey('arrivi.id_arrivo'))
    prenotazione = relationship('Arrivi', back_populates= "extra_arrivi")
    nome = db.Column(db.String(100))
    quantita = db.Column(db.Integer)
    prezzo = db.Column(db.Integer)

class ArriviPagamenti (db.Model) :
    __tablename__ = "arrivi_pagamenti"
    id = db.Column('id_ArriviPagamenti', db.Integer(), primary_key=True, autoincrement=True, unique=True)
    idPrenotazione = db.Column('id_prenotazione', db.Integer, db.ForeignKey('arrivi.id_arrivo'))
    prenotazione = relationship('Arrivi', back_populates= "pagamenti_arrivi")
    pagamento = db.Column(db.Integer)
    dataPagamento = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    
    def __repr__(self):
        return '<User {}>'.format(self.id)    

class TipologiaCamere (db.Model, SerializerMixin) :
    __tablename__ = "tipologiaCamere"
    id = db.Column ('id_tipologiaCamera', db.Integer, primary_key=True)
    numeri_posti = db.Column(db.Integer)
    tipologia = db.Column(db.String(100))
    tipo = db.Column(db.String(100))
    account_id = db.Column(db.Integer)
    camere = db.relationship('Camere', back_populates='tipologia', lazy=True)
    tariffe = db.relationship('Tariffe', back_populates='tipologia', lazy=True, cascade="all, delete")

    def __init__ (self, form) :
        self.numeri_posti = form.numero_persone.data
        self.tipologia = form.tipologia.data
        self.tipo = form.tipo.data
        self.account_id = current_user.get_id()

class Camere (db.Model) :
    __tablename__ = "camere"
    id = db.Column ('id_camera', db.Integer, primary_key=True, autoincrement=True)
    numeroCamera = db.Column(db.Integer)
    tipologia_id = db.Column(db.Integer, db.ForeignKey('tipologiaCamere.id_tipologiaCamera'))
    tipologia = relationship("TipologiaCamere", back_populates="camere")
    arrivi = db.relationship('Arrivi', back_populates='camera', lazy=True, cascade="all, delete")

    def __init__ (self, numeroCamera) :
        self.numeroCamera = numeroCamera

    def __repr__(self):
        return "Numero camera :" + str(self.numeroCamera)

### MODEL PER TARIFFE E PERIODI ###

class Tariffe (db.Model) :
    __tablename__ = "tariffe"
    id = db.Column ('id_tariffa', db.Integer, primary_key=True, autoincrement=True)
    bedBreakfast = db.Column(db.Integer)
    bedBreakfastSettimana = db.Column(db.Integer)
    mezzaPensione = db.Column(db.Integer)
    mezzaPensioneSettimana = db.Column(db.Integer)
    pensioneCompleta = db.Column(db.Integer)
    pensioneCompletaSettimana = db.Column(db.Integer)
    #RELAZIONI
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodi.id_periodo'))
    periodo = relationship("Periodi", back_populates="tariffe")
    tipologia_id = db.Column(db.Integer, db.ForeignKey('tipologiaCamere.id_tipologiaCamera'))
    tipologia = relationship("TipologiaCamere", back_populates="tariffe")

    
class Periodi (db.Model) :
    __tablename__ = "periodi"
    id = db.Column ('id_periodo', db.Integer, primary_key=True, autoincrement=True)
    inizio = db.Column(db.Date)
    fine = db.Column(db.Date)
    account_id = db.Column(db.Integer)
    tariffe = db.relationship('Tariffe', back_populates='periodo', lazy=True, cascade="all, delete")

### MODEL PER EXTRA ###

class Extra (db.Model) :
    __tablename__ = "extra"
    id = db.Column ('id_extra', db.Integer, primary_key=True, autoincrement=True)
    nomeExtra = db.Column (db.String(100))
    prezzoExtra = db.Column (db.Integer)
    tipoExtra = db.Column (db.String(100))
    account_id = db.Column(db.Integer)
    supplementi_arrivi = db.relationship("ArriviSupplementi", back_populates = 'supplemento', lazy=True)

    @property
    def toJson (self) :
        return  {
                'nomeExtra' : self.nomeExtra,
                'prezzoExtra' : self.prezzoExtra,
                'tipoExtra' : self.tipoExtra,
                }

    @property
    def getId (self) :
        return str(self.id)
        
### MODEL PER PREVENTIVI ###

class Preventivo (db.Model) :
    __tablename__ = "preventivi"
    id = db.Column ('id_preventivo', db.Integer, primary_key=True, autoincrement=True)
    cognome = db.Column (db.String(100))
    checkIn = db.Column(db.Date)
    checkOut = db.Column(db.Date)
    adulti = db.Column(db.Integer)
    ridotti = db.Column(db.Integer, default = 0)
    infant = db.Column(db.Integer, default = 0)
    telefono = db.Column (db.String(100))
    email = db.Column (db.String(100))
    account_id = db.Column (db.Integer)
    arrivi = db.relationship('Arrivi', back_populates='preventivo', lazy=True)

### MODEL PER ARRIVI ###

class Arrivi (db.Model) :
    __tablename__ = "arrivi"
    id = db.Column ('id_arrivo', db.Integer, primary_key=True, autoincrement=True)
    trattamento = db.Column (db.String(100))
    prezzoCamera = db.Column(db.Integer, default = 0)
    prezzoSupplementi = db.Column(db.Integer, default = 0)
    prezzoExtra = db.Column(db.Integer, default = 0)
    statoPagamento = db.Column(db.Integer(), default = 1)
    statoSoggiorno = db.Column(db.Integer(), default = 1)
    tassaSoggiorno = db.Column(db.Integer(), default = 1)
    extra = db.Column(db.Integer(), default=0)
    #RELAZIONI
    camera_id = db.Column(db.Integer, db.ForeignKey('camere.id_camera'))
    camera = relationship("Camere", back_populates="arrivi")
    preventivo_id = db.Column(db.Integer, db.ForeignKey('preventivi.id_preventivo'))
    preventivo = relationship("Preventivo", back_populates="arrivi")
    #RELAZIONI BACK
    contatti = db.relationship('Contatti', back_populates='prenotazione', lazy=True)
    supplementi_arrivi = db.relationship("ArriviSupplementi", back_populates = 'prenotazione', lazy=True, cascade="all, delete")
    extra_arrivi = db.relationship("ArriviExtra", back_populates = 'prenotazione', lazy=True, cascade="all, delete")
    pagamenti_arrivi = db.relationship("ArriviPagamenti", back_populates = 'prenotazione', lazy=True, cascade="all, delete")

    def calcolaTotale (self) :
        return self.prezzoCamera + self.calcolaPrezziSupplementi() + self.calcolaPrezziExtra() + self.calcolaTassaSoggiorno()

    def aggiungiSupplemento(self, supplementi, quantita):
        for i in range (0,len(supplementi)):
            if quantita != 0 :
                ArriviSupplementi(prenotazione=self, supplemento=supplementi[i], quantita=quantita[i])

    def calcolaPrezziSupplementi (self):
        prezzoSupplementi = 0
        for supplemento in self.supplementi_arrivi:
            prezzoSupplementi += supplemento.supplemento.prezzoExtra * supplemento.quantita
        return prezzoSupplementi

    def calcolaPrezziExtra (self):
        prezzoExtra = 0
        for extra in self.extra_arrivi:
            prezzoExtra += extra.prezzo * extra.quantita
        return prezzoExtra

    def deleteExtra (self, idExtra) :
        for extra in self.extra_arrivi : 
            if int(extra.id) == int(idExtra) :
                db.session.delete(extra)

    def aggiungiExtra(self, nome, quantita, prezzo):
        return ArriviExtra(prenotazione=self, nome=nome, quantita=quantita, prezzo=prezzo)

    def aggiungiPagamento(self, pagamento):
        return ArriviPagamenti(prenotazione=self, pagamento=pagamento)

    def deletePagamento (self, idPagamento) :
        for pagamento in self.pagamenti_arrivi : 
            if int(pagamento.id) == int(idPagamento) :
                db.session.delete(pagamento)

    def calcolaCaparra (self) :
        return round(20 * ((self.prezzoCamera + self.calcolaPrezziSupplementi())/100), 2)

    def getPagamenti (self):
        pagato = 0

        for pagamento in self.pagamenti_arrivi :
            pagato += pagamento.pagamento
        if self.statoPagamento != 1 :
            pagato += self.calcolaCaparra()
        
        return round(pagato, 2)

    def calcolaTassaSoggiorno(self):
        prezzoTassaDiSoggiorno = 0
        if self.tassaSoggiorno == 1 :
            if (self.preventivo.checkOut - self.preventivo.checkIn).days < 10: 
                v = (self.preventivo.checkOut - self.preventivo.checkIn).days
            else : 
                v = 10
            for cliente in self.contatti : 
                if (date.today().year - cliente.dataDiNascita.year) > 10 :
                    for i in range (0, v) : prezzoTassaDiSoggiorno += 2.40
        return round(prezzoTassaDiSoggiorno, 2)

    def eliminaContatto (self, idContatto) :
        print ('idContatto', idContatto)
        for contatto in self.contatti :
            if int(contatto.id) == int(idContatto) : db.session.delete(contatto)

    def modificaContatto (self, idContatto, dictInfo) :
        for contatto in self.contatti :
            if contatto.id == idContatto :
                for dat in dictInfo.keys() :
                    if dat in contatto.__table__.columns:
                        if type(contatto.__table__.columns[str(dat)].type) == type(db.String()) : setattr(contatto, str(dat), dictInfo[str(dat)])
                        elif type(contatto.__table__.columns[str(dat)].type) == type(db.Date()) : setattr(contatto, str(dat), datetime.strptime(dictInfo[str(dat)], "%Y-%m-%d").date())
                        elif type(contatto.__table__.columns[str(dat)].type) == type(db.Integer()) : setattr(contatto, str(dat), int(dictInfo[str(dat)]))

    def __init__ (self, trattamento, prezzoCamera) :
        self.trattamento = trattamento
        self.prezzoCamera = prezzoCamera
        self.prezzoSupplementi = 0
    
class Contatti (db.Model) :
    __tablename__ = "contatti"
    id = db.Column ('id_contatto', db.Integer, primary_key=True, autoincrement=True)
    cognome = db.Column (db.String(100))
    nome = db.Column (db.String(100))
    cittadinanza = db.Column (db.String(100))
    sesso = db.Column (db.String(100))
    telefono = db.Column (db.String(100))
    email = db.Column (db.String(100))
    dataDiNascita = db.Column(db.Date)
    paeseNascita = db.Column (db.String(100))
    paeseResidenza = db.Column (db.String(100))
    comuneNascita = db.Column (db.String(100))
    comuneResidenza = db.Column (db.String(100))
    cap = db.Column(db.Integer())
    indirizzo = db.Column (db.String(100))
    documento = db.Column (db.String(100))
    paeseImmissione = db.Column (db.String(100))
    numeroDocumento = db.Column (db.String(100))
    emessoDa = db.Column (db.String(100))
    dataEmissione = db.Column(db.Date)
    dataScadenza = db.Column(db.Date)
    #RELAZIONI
    prenotazione_id = db.Column(db.Integer, db.ForeignKey('arrivi.id_arrivo'))
    prenotazione = relationship("Arrivi", back_populates="contatti")

    def getConctatDict (self) : 
        return {c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs}