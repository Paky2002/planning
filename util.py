from flask import Blueprint,render_template, request, jsonify, redirect, url_for
from .models import Preventivo, Periodi, TipologiaCamere, Camere, Arrivi, Extra, Contatti, ArriviSupplementi
from form import AggiungiPreventivo, AggiungiPrenotazione, RegistraCliente
from sqlalchemy import and_
import json
from datetime import datetime
from util import *

def aggiungiSupplementi (arrivo, dictSupplementi) : 
    arrivo.aggiungiSupplemento(Extra.query.filter(Extra.id.in_(list(dictSupplementi.keys()))).all(), list(dictSupplementi.values()))
    arrivo.prezzoSupplementi = sum(a.prezzoExtra * int(b) for a, b in zip(Extra.query.filter(Extra.id.in_(list(dictSupplementi.keys()))).all(), list(dictSupplementi.values())))