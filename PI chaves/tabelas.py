from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, Boolean, Time
from sqlalchemy.orm import declarative_base, sessionmaker
from flask_sqlalchemy import SQLAlchemy

#Criando conexao com o banco de dados
engine = create_engine(
    "mysql+pymysql://root:@localhost:3306/db_chave",
    echo=True
)

#Criando tabela banco de dados chave
Base=declarative_base()
class Chave(Base):
    __tablename__ = "tb_chave"
    id_chave      = Column(Integer, primary_key=True)
    identificador = Column(String(250))
    id_ambiente   = Column(Integer)
    observacao    = Column(String(250))
    disponivel    = Column(String(45))
    nome_chave     = Column(String(250))
Base.metadata.create_all(engine)


#Criando tabela banco de dados usuarios
class Usuario(Base):
    __tablename__ = "tb_usuario"
    id_usuario    = Column(Integer, primary_key=True)
    nome_usuario  = Column(String(250))
    email         = Column(String(250))
    senha         = Column(Numeric(15,0))
    id_perfil     = Column(Integer)
Base.metadata.create_all(engine)

#Criando tabela banco de dados perfil
class Perfil(Base):
    __tablename__ = "tb_perfil"
    id_perfil     = Column(Integer, primary_key=True)
    nome_perfil   = Column(String(200), nullable=True)
    matricula     = Column(Numeric(12,0), nullable=True)
    cargo         = Column(String(250), nullable=True)
Base.metadata.create_all(engine)

#Criando tabela banco de dados ambiente
class Ambiente(Base):
    __tablename__       = "tb_ambiente"
    id_ambiente         = Column(Integer, primary_key=True)
    ambiente            = Column(String(150))
    disponivel_ambiente = Column(String(45))
    observacao_ambiente = Column(String(250))
Base.metadata.create_all(engine)


#Criando tabela banco de dados movimentacao
class Movimentacao(Base):
    __tablename__      = "tb_movimentacao"
    id_movimentacao    = Column(Integer, primary_key=True)
    id_chave           = Column(Integer)
    id_perfil          = Column(Integer)
    id_ambiente        = Column(Integer)
    data_movimentacao  = Column(Date)
    id_reserva         = Column(Integer)
    hora_inicio_movimentacao = Column(Time)
    hora_fim_movimentacao = Column(Time)
Base.metadata.create_all(engine)


#Criando tabela banco de dados reserva
class Reserva(Base):
    __tablename__       = "tb_reserva"
    id_reserva          = Column(Integer, primary_key=True)
    id_chave            = Column(Integer)
    id_ambiente         = Column(Integer)
    id_perfil           = Column(Integer)
    data_reserva        = Column(Date)
    hora_inicio_reserva = Column(Time)
    hora_fim_reserva    = Column(Time)
Base.metadata.create_all(engine)


#Criando tabela banco de dados movimentacao_devolucao
class Devolucao(Base):
    __tablename__       = "tb_devolucao"
    id_devolucao        = Column(Integer, primary_key=True)
    id_reserva          = Column(Integer)
    id_perfil            = Column(Integer)
    data_devolucao       = Column(Date)
    hora_fim_devolucao   = Column(Time)
    hora_inicio_devolucao   = Column(Time)
    observacao_devoluca = Column(String(250))
Base.metadata.create_all(engine)

