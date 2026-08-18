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

#chave consultar
@app.route("/chave/consultar", methods=["GET", "POST"])
def consultar_chave():
    #Pegar a chave foi informada
    chave_nome = request.args.get("nome_chave","")
    #consultar chave
    chaves = sessao.query(Chave).filter(Chave.nome_chave.like(f"%{chave_nome}%")).all()
    #chamar cahve.html para mostrar dados
    return render_template('chave.html', chaves=chaves)


#usuario
@app.route("/usuario")
def usuario():
    return render_template('usuario.html')

#ambiente
@app.route("/ambiente")
def ambiente():
    return render_template('ambiente.html')

#ambiente consultar
@app.route("/ambiente/consultar",methods=["GET", "POST"])
def consultar_ambiente():
    #Pegar o ambiente informado
    ambiente_nome = request.args.get("ambiente","")
    
    #consultar chave
    ambientes = sessao.query(Ambiente).filter(Ambiente.ambiente.like(f"%{ambiente_nome}%"))
    
    #chamar p ambiente.html para mostrar dados
    return render_template('ambiente.html', ambientes=ambientes)

#perfil
@app.route("/perfil")
def perfil():
    return render_template('perfil.html')

#movimentacao
@app.route("/movimentacao")
def movimentacao():
    return render_template('movimentacao.html')

#devolucao
@app.route("/devolucao")
def devolucao():
    return render_template('devolucao.html')


#reserva
@app.route("/reserva")
def reserva():
    return render_template('reserva.html')

#historico
@app.route("/historico")
def historico():
    return render_template('historico.html')


app.run(debug=True)