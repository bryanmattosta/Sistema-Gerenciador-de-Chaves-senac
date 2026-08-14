from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from tabelas import engine, Base, Chave, Usuario, Perfil, Ambiente, Movimentacao, Reserva, Movimentacao_devolucao


#cria a sesao
Session = sessionmaker(bind=engine)
sessao  = Session()


app = Flask(__name__)
app.secret_key="123456"

#home
@app.route("/")
def home():
    return render_template('index.html')


#chave
@app.route("/chave")
def chave():
    return render_template('chave.html')


#ambiente
@app.route("/ambiente")
def ambiente():
    return render_template('ambiente.html')

#perfil
@app.route("/perfil")
def perfil():
    return render_template('perfil.html')

#movimentacao
@app.route("/movimentacao")
def movimentacao():
    return render_template('movimentacao.html')

#reserva
@app.route("/reserva")
def reserva():
    return render_template('reserva.html')

#historico
@app.route("/historico")
def historico():
    return render_template('historico.html')


app.run(debug=True)