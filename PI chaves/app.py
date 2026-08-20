from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from tabelas import engine, Base, Chave, Usuario, Perfil, Ambiente, Movimentacao, Reserva, Devolucao


#cria a sesao
Session = sessionmaker(bind=engine)
sessao  = Session()


app = Flask(__name__)
app.secret_key="123456"

#home
@app.route("/")
def home():
    return render_template('index.html')


#chave #feito e #verificado
@app.route("/chave", methods=["GET", "POST"])
def chave():

    #lista de todas chaves
    todos_ambiente = sessao.query(Ambiente).all()

    if request.method == "POST":
        # Aqui você pode processar os dados do formulário, por exemplo, salvando em um banco de dados
        identificador = request.form.get("identificador")
        observacao = request.form.get("observacao")
        disponivel = request.form.get("disponivel")
        nome_chave = request.form.get("nome_chave")
        id_ambiente = request.form.get("ambiente")
        
        # Validação do nome
        if nome_chave == "":
            flash("Nome da Chave é obrigatório!", "danger")
            return render_template("chave.html")

        #inserir chave
        c = Chave(identificador=identificador, observacao=observacao, disponivel=disponivel, nome_chave=nome_chave, id_ambiente=id_ambiente)
        sessao.add(c)
        sessao.commit()
        flash("Chave salva com sucesso!", "success")

        # Redireciona para a página inicial após o envio do formulário
        return redirect(url_for("chave"))
    return render_template('chave.html', ambientes=todos_ambiente)


#alterar chave #falta ver
@app.route("/chave/alterar/<int:id_chave>", methods=["GET", "POST"])
def alterar_chave(id_chave):
    
    #buscar os dados o id_chave
    chave = sessao.query(Chave).get(id_chave)
    
    #valida se existe a chave com a id_chave informada
    if chave is None:
        flash("Chave não encontrada","danger")
        return redirect(url_for("chave"))
    
    #pegar os dados e atualizar a chave
    if request.method == "POST":
        chave.nome_chave = request.form.get("nome_chave")
        chave.observacao = request.form.get("observacao")
        chave.disponivel = request.form.get("disponivel")
        chave.identificador = request.form.get("identificador")
        
        #validade chave
        if chave.nome_chave == "":
            flash("Nome da Chave é obrigatório!","danger")
            return render_template("alterar.chave.html", chave=chave)
        
        #salvar as alterações
        sessao.commit()
        flash("Alterado com sucesso!","sucess")
        return redirect(url_for("chave"))
    
    return render_template("alterar.chave.html", chave=chave)

#chave excluir #falta ver
@app.route("/chave/excluir/<int:id_chave>", methods=["POST"])
def excluir_chave(id_chave):
    #buscar os dados o id_chave
    chave = sessao.query(Chave).get(id_chave)
    
    #realizar a exclusao do cliente
    if chave:
        sessao.delete(chave)
        sessao.commit()
        flash("Excluído com sucesso!","sucess")
    else:
        flash("Chave não encontrada!","danger")
    
    #retornar a tela principal do cliente
    return redirect(url_for("chave"))

#chave consultar #feito e #verificado
@app.route("/chave/consultar", methods=["GET", "POST"])
def consultar_chave():
    #Pegar a chave foi informada
    chave_nome = request.args.get("nome_chave","")
    #consultar chave
    chaves = sessao.query(Chave).filter(Chave.nome_chave.like(f"%{chave_nome}%")).all()
    #chamar cahve.html para mostrar dados
    return render_template('chave.html', chaves=chaves)


#usuario inserir feito
@app.route("/usuario", methods=["GET", "POST"])
def usuario():
    
    #pegar os perfils
    todo_perfil = sessao.query(Perfil).all()
    
    if request.method == "POST":
        # Aqui você pode processar os dados do formulário, por exemplo, salvando em um banco de dados
        nome_usuario = request.form.get("nome_usuario")
        senha = request.form.get("senha_usuario")
        email = request.form.get("email_usuario")
        id_perfil    = request.form.get("perfil")
        
        # Validação do nome
        if nome_usuario == "":
            flash("Nome do Usuário é obrigatório!", "danger")
            return render_template("usuario.html")

        #inserir usuário
        p = Usuario(nome_usuario=nome_usuario, email=email, senha=senha, id_perfil=id_perfil)
        sessao.add(p)
        sessao.commit()
        flash("Usuário salvo com sucesso!", "success")

        # Redireciona para a página inicial após o envio do formulário
        return redirect(url_for("usuario"))
    return render_template('usuario.html', perfils=todo_perfil)

#consultar usuário falta ver
@app.route("/usuario/consultar", methods=["GET", "POST"])
def consultar_usuario():
    
    #pegar o usuário que foi informado no formulário
    nome_usuario = request.args.get("usuario","")
    
    #consultar o(s) usuário(s)
    usuarios = sessao.query(Usuario).filter(Usuario.nome_usuario.like(f"%{nome_usuario}%")).all()
    
    #chamar usuario.html para mostrar os dados
    return render_template("usuario.html", usuarios=usuarios)

#alterar usuario falta ver
@app.route("/usuario/alterar/<int:id_usuario>", methods=["GET", "POST"])
def alterar_usuario(id_usuario):
    
    #buscar os dados o id_usuario
    usuario = sessao.query(Usuario).get(id_usuario)
    
    #valida se existe o usuário com a id_usuario informada
    if usuario is None:
        flash("Usuário não encontrado","danger")
        return redirect(url_for("usuario"))
    
    #pegar os dados e atualizar o usuário
    if request.method == "POST":
        usuario.nome_usuario = request.form.get("nome_usuario")
        usuario.email = request.form.get("email")
        usuario.senha = request.form.get("senha")
        
        #validade usuário
        if usuario.nome_usuario == "":
            flash("Nome do Usuário é obrigatório!","danger")
            return render_template("alterar.usuario.html", usuario=usuario)
        
        #salvar as alterações
        sessao.commit()
        flash("Alterado com sucesso!","sucess")
        return redirect(url_for("usuario"))
    
    return render_template("alterar.usuario.html", usuario=usuario)

#usuario excluir falta ver
@app.route("/usuario/excluir/<int:id_usuario>", methods=["POST"])
def excluir_usuario(id_usuario):
    #buscar os dados o id_usuario
    usuario = sessao.query(Usuario).get(id_usuario)

    #realizar a exclusao do usuario
    if usuario:
        sessao.delete(usuario)
        sessao.commit()
        flash("Excluído com sucesso!","sucess")
    else:
        flash("Usuário não encontrado!","danger")

    #retornar a tela principal do usuario
    return redirect(url_for("usuario"))

#ambiente 
@app.route("/ambiente", methods=["GET", "POST"])
def ambiente():
    if request.method == "POST":
        # Aqui você pode processar os dados do formulário, por exemplo, salvando em um banco de dados
        ambiente = request.form.get("nome_ambiente")
        observacao_ambiente = request.form.get("observacao_ambiente")
        disponivel_ambiente = request.form.get("disponivel_ambiente")
        
        # Validação do nome
        if ambiente == "":
            flash("Nome do Ambiente é obrigatório!", "danger")
            return render_template("ambiente.html")

        #inserir ambiente
        a = Ambiente(ambiente=ambiente, observacao_ambiente=observacao_ambiente, disponivel_ambiente=disponivel_ambiente)
        sessao.add(a)
        sessao.commit()
        flash("Ambiente salvo com sucesso!", "success")

        # Redireciona para a página inicial após o envio do formulário
        return redirect(url_for("ambiente"))
    
    return render_template('ambiente.html')


#alterar ambiente falta ver
@app.route("/ambiente/alterar/<int:id_ambiente>", methods=["GET", "POST"])
def alterar_ambiente(id_ambiente):
    
    #buscar os dados o id_ambiente
    ambiente = sessao.query(Ambiente).get(id_ambiente)
    
    #valida se existe o ambiente com a id_ambiente informada
    if ambiente is None:
        flash("Ambiente não encontrado","danger")
        return redirect(url_for("ambiente"))
    
    #pegar os dados e atualizar o ambiente
    if request.method == "POST":
        ambiente.ambiente = request.form.get("ambiente")
        ambiente.observacao_ambiente = request.form.get("observacao_ambiente")
        ambiente.disponivel_ambiente = request.form.get("disponivel_ambiente")
        
        #validade usuário
        if ambiente.ambiente == "":
            flash("Nome do Ambiente é obrigatório!","danger")
            return render_template("alterar.ambiente.html", ambiente=ambiente)
        
        #salvar as alterações
        sessao.commit()
        flash("Alterado com sucesso!","sucess")
        return redirect(url_for("ambiente"))
    
    return render_template("alterar.ambiente.html", ambiente=ambiente)

#ambiente excluir falta ver
@app.route("/ambiente/excluir/<int:id_ambiente>", methods=["POST"])
def excluir_ambiente(id_ambiente):
    #buscar os dados o id_ambiente
    ambiente = sessao.query(Ambiente).get(id_ambiente)

    #realizar a exclusao do ambiente
    if ambiente:
        sessao.delete(ambiente)
        sessao.commit()
        flash("Excluído com sucesso!","sucess")
    else:
        flash("Ambiente não encontrado!","danger")

    #retornar a tela principal do ambiente
    return redirect(url_for("ambiente"))

#ambiente consultar #feito e #verificado
@app.route("/ambiente/consultar",methods=["GET", "POST"])
def consultar_ambiente():
    #Pegar o ambiente informado
    ambiente_nome = request.args.get("ambiente","")
    
    #consultar chave
    ambientes = sessao.query(Ambiente).filter(Ambiente.ambiente.like(f"%{ambiente_nome}%"))
    
    #chamar p ambiente.html para mostrar dados
    return render_template('ambiente.html', ambientes=ambientes)

#perfil #feito
@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    if request.method == "POST":
        # Aqui você pode processar os dados do formulário, por exemplo, salvando em um banco de dados
        nome_perfil = request.form.get("nome_perfil")
        matricula = request.form.get("matricula_perfil")
        cargo = request.form.get("cargo_perfil")
        
        # Validação do nome
        if nome_perfil == "":
            flash("Nome do Perfil é obrigatório!", "danger")
            return render_template("perfil.html")

        #inserir perfil
        p = Perfil(nome_perfil=nome_perfil, matricula=matricula, cargo=cargo)
        sessao.add(p)
        sessao.commit()
        flash("Perfil salvo com sucesso!", "success")

        # Redireciona para a página inicial após o envio do formulário
        return redirect(url_for("perfil"))
   
    return render_template('perfil.html')

#consultar perfil #feito e #verificado
@app.route("/perfil/consultar", methods=["GET", "POST"])
def consultar_perfil():
    
    #pegar o perfil que foi informado no formulário
    perfil_nome = request.args.get("perfil","")
    
    #consultar o(s) perfil(s)
    perfis = sessao.query(Perfil).filter(Perfil.nome_perfil.like(f"%{perfil_nome}%")).all()
    
    #chamar perfil.html para mostrar os dados
    return render_template("perfil.html", perfis=perfis)


#alterar perfil falta ver
@app.route("/perfil/alterar/<int:id_perfil>", methods=["GET", "POST"])
def alterar_perfil(id_perfil):
    
    #buscar os dados o id_perfil
    perfil = sessao.query(Perfil).get(id_perfil)
    
    #valida se existe o perfil com a id_perfil informada
    if perfil is None:
        flash("Perfil não encontrado","danger")
        return redirect(url_for("perfil"))
    
    #pegar os dados e atualizar o perfil
    if request.method == "POST":
        perfil.nome_perfil = request.form.get("nome")
        perfil.matricula = request.form.get("matricula")
        perfil.cargo = request.form.get("cargo")
        
        #validade perfil
        if perfil.nome_perfil == "":
            flash("Nome do Perfil é obrigatório!","danger")
            return render_template("alterar.perfil.html", perfil=perfil)
        
        #salvar as alterações
        sessao.commit()
        flash("Alterado com sucesso!","sucess")
        return redirect(url_for("perfil"))
    
    return render_template("alterar.perfil.html", perfil=perfil)

#perfil excluir falta ver
@app.route("/perfil/excluir/<int:id_perfil>", methods=["POST"])
def excluir_perfil(id_perfil):
    #buscar os dados o id_perfil
    perfil = sessao.query(Perfil).get(id_perfil)

    #realizar a exclusao do perfil
    if perfil:
        sessao.delete(perfil)
        sessao.commit()
        flash("Excluído com sucesso!","sucess")
    else:
        flash("Perfil não encontrado!","danger")

    #retornar a tela principal do perfil
    return redirect(url_for("perfil"))

#movimentacao #feito
@app.route("/movimentacao", methods=["GET", "POST"])
def movimentacao():
    
    #pegar dados para for
    perfils=sessao.query(Perfil).all()
    chaves=sessao.query(Chave).all()
    ambientes=sessao.query(Ambiente).all()
    
    if request.method == "POST":
        # Aqui você pode processar os dados do formulário, por exemplo, salvando em um banco de dados
        data_movimentacao = request.form.get("data_fim_movimentacao")
        hora_inicio_movimentacao = request.form.get("hora_inicio_movimentacao")
        hora_fim_movimentacao = request.form.get("hora_fim_movimentacao")
        data_movimentacao = request.form.get("data_movimentacao")
        id_perfil= request.form.get("perfil")
        id_ambiente=request.form.get("ambiente")
        id_chave=request.form.get("chave")
        
        # Validação da data de retirada
        if data_movimentacao == "":
            flash("Data de retirada é obrigatória!", "danger")
            return render_template("movimentacao.html")

        #inserir movimentacao
        m = Movimentacao(hora_inicio_movimentacao=hora_inicio_movimentacao, hora_fim_movimentacao=hora_fim_movimentacao, data_movimentacao=data_movimentacao, id_perfil=id_perfil, id_ambiente=id_ambiente, id_chave=id_chave)
        sessao.add(m)
        sessao.commit()
        flash("Movimentação salva com sucesso!", "success")

        # Redireciona para a página inicial após o envio do formulário
        return redirect(url_for("movimentacao"))
    
    return render_template('movimentacao.html', perfils=perfils, chaves=chaves, ambientes=ambientes)

#consultar movimentacao
@app.route("/movimentacao/consultar", methods=["GET", "POST"])
def consultar_movimentacao():
    
    #pegar a movimentacao que foi informada no formulário
    data_retirada = request.args.get("data_retirada","")
    
    #consultar o(s) movimentacao(s)
    movimentacoes = sessao.query(Movimentacao).filter(Movimentacao.data_retirada.like(f"%{data_retirada}%")).all()
    
    #chamar movimentacao.html para mostrar os dados
    return render_template("movimentacao.html", movimentacoes=movimentacoes)


#alterar movimentacao
@app.route("/movimentacao/alterar/<int:id_movimentacao>", methods=["GET", "POST"])
def alterar_movimentacao(id_movimentacao):
    
    #buscar os dados o id_movimentacao
    movimentacao = sessao.query(Movimentacao).get(id_movimentacao)
    
    #valida se existe a movimentacao com a id_movimentacao informada
    if movimentacao is None:
        flash("Movimentação não encontrada","danger")
        return redirect(url_for("movimentacao"))
    
    #pegar os dados e atualizar o perfil
    if request.method == "POST":
        movimentacao.data_retirada = request.form.get("data_retirada")
        movimentacao.horario_inicio = request.form.get("horario_inicio")
        
        #validade movimentacao
        if movimentacao.data_retirada == "":
            flash("Data de retirada é obrigatória!","danger")
            return render_template("alterar.movimentacao.html", movimentacao=movimentacao)
        
        #salvar as alterações
        sessao.commit()
        flash("Alterado com sucesso!","sucess")
        return redirect(url_for("movimentacao"))
    
    return render_template("alterar.movimentacao.html", movimentacao=movimentacao)

#movimentacao excluir
@app.route("/movimentacao/excluir/<int:id_movimentacao>", methods=["POST"])
def excluir_movimentacao(id_movimentacao):
    #buscar os dados o id_movimentacao
    movimentacao = sessao.query(Movimentacao).get(id_movimentacao)

    #realizar a exclusao da movimentacao
    if movimentacao:
        sessao.delete(movimentacao)
        sessao.commit()
        flash("Excluído com sucesso!","sucess")
    else:
        flash("Movimentação não encontrada!","danger")

    #retornar a tela principal da movimentacao
    return redirect(url_for("movimentacao"))

#devolucao #feita
@app.route("/devolucao", methods=["GET", "POST"])
def devolucao():
    
    #pegar dados para for
    perfils = sessao.query(Perfil).all()
    reservas = sessao.query(Reserva).all()
    
    if request.method == "POST":
        # Aqui você pode processar os dados do formulário, por exemplo, salvando em um banco de dados
        data_devolucao = request.form.get("data_devolucao")
        hora_inicio_devolucao = request.form.get("hora_inicio_devolucao")
        hora_fim_devolucao = request.form.get("hora_fim_devolucao")
        id_perfil = request.form.get("perfil")
        id_reserva = request.form.get("reserva")
        observacao_devoluca = request.form.get("observacao_devolucao")
        
        # Validação da data de reserva
        if data_devolucao == "":
            flash("Data de reserva é obrigatória!", "danger")
            return render_template("devolucao.html")

        #inserir devolucao
        d = Devolucao(data_devolucao=data_devolucao, hora_fim_devolucao=hora_fim_devolucao, hora_inicio_devolucao=hora_inicio_devolucao, observacao_devoluca=observacao_devoluca, id_perfil=id_perfil, id_reserva=id_reserva)
        sessao.add(d)
        sessao.commit()
        flash("Devolução salva com sucesso!", "success")

        # Redireciona para a página inicial após o envio do formulário
        return redirect(url_for("devolucao"))
    return render_template('devolucao.html', perfils=perfils, reservas=reservas)

#consultar devolucao
@app.route("/devolucao/consultar", methods=["GET", "POST"])
def consultar_devolucao():
    
    #pegar a devolucao que foi informada no formulário
    date_reserva = request.args.get("date_reserva","")
    
    #consultar a(s) devolucao(oes)
    devolucoes = sessao.query(devolucao).filter(devolucao.date_reserva.like(f"%{date_reserva}%")).all()
    
    #chamar devolucao.html para mostrar os dados
    return render_template("devolucao.html", devolucoes=devolucoes)


#alterar devolucao
@app.route("/devolucao/alterar/<int:id_devolucao>", methods=["GET", "POST"])
def alterar_devolucao(id_devolucao):
    
    #buscar os dados o id_devolucao
    devolucao = sessao.query(devolucao).get(id_devolucao)
    
    #valida se existe a devolucao com a id_devolucao informada
    if devolucao is None:
        flash("Devolução não encontrada","danger")
        return redirect(url_for("devolucao"))
    
    #pegar os dados e atualizar o perfil
    if request.method == "POST":
        devolucao.date_reserva = request.form.get("date_reserva")
        devolucao.horario_devolucao = request.form.get("horario_devolucao")
        devolucao.obsevacao_devolucao = request.form.get("obsevacao_devolucao")

        #validade devolucao
        if devolucao.date_reserva == "":
            flash("Data de reserva é obrigatória!","danger")
            return render_template("alterar.devolucao.html", devolucao=devolucao)

        #salvar as alterações
        sessao.commit()
        flash("Alterado com sucesso!","sucess")
        return redirect(url_for("devolucao"))
    
    return render_template("alterar.devolucao.html", devolucao=devolucao)

#devolucao excluir
@app.route("/devolucao/excluir/<int:id_devolucao>", methods=["POST"])
def excluir_devolucao(id_devolucao):
    #buscar os dados o id_devolucao
    devolucao = sessao.query(devolucao).get(id_devolucao)

    #realizar a exclusao da devolucao
    if devolucao:
        sessao.delete(devolucao)
        sessao.commit()
        flash("Excluído com sucesso!","sucess")
    else:
        flash("Devolução não encontrada!","danger")

    #retornar a tela principal da devolucao
    return redirect(url_for("devolucao"))


#reserva
@app.route("/reserva",  methods=["GET", "POST"])
def reserva():
    
    #pegar dados para for
    perfils=sessao.query(Perfil).all()
    chaves=sessao.query(Chave).all()
    ambientes=sessao.query(Ambiente).all()
    
    
    if request.method == "POST":
        # Aqui você pode processar os dados do formulário, por exemplo, salvando em um banco de dados
        data_reserva = request.form.get("data_reserva")
        hora_inicio_reserva= request.form.get("horario_reserva")
        hora_fim_reserva = request.form.get("horario_reserva_fim")
        id_perfil= request.form.get("perfil")
        id_ambiente=request.form.get("ambiente")
        id_chave=request.form.get("chave")
        
        
        # Validação da data de reserva
        if data_reserva == "":
            flash("Data de reserva é obrigatória!", "danger")
            return render_template("devolucao.html")

        #inserir reserva
        r = Reserva(data_reserva=data_reserva, hora_inicio_reserva=hora_inicio_reserva, hora_fim_reserva=hora_fim_reserva, id_ambiente=id_ambiente, id_chave=id_chave, id_perfil=id_perfil)
        sessao.add(r)
        sessao.commit()
        flash("Reserva salva com sucesso!", "success")

        # Redireciona para a página inicial após o envio do formulário
        return redirect(url_for("reserva"))
    
    return render_template('reserva.html', perfils=perfils, chaves=chaves, ambientes=ambientes)

#consultar reserva
@app.route("/reserva/consultar", methods=["GET", "POST"])
def consultar_reserva():
    
    #pegar a reserva que foi informada no formulário
    data_reserva = request.args.get("data_reserva","")
    
    #consultar a(s) reserva(s)
    reservas = sessao.query(Reserva).filter(Reserva.data_reserva.like(f"%{data_reserva}%")).all()
    
    #chamar reserva.html para mostrar os dados
    return render_template("reserva.html", reservas=reservas)


#alterar reserva
@app.route("/reserva/alterar/<int:id_reserva>", methods=["GET", "POST"])
def alterar_reserva(id_reserva):
    
    #buscar os dados o id_reserva
    reserva = sessao.query(Reserva).get(id_reserva)
    
    #valida se existe a reserva com a id_reserva informada
    if reserva is None:
        flash("Reserva não encontrada","danger")
        return redirect(url_for("reserva"))
    
    #pegar os dados e atualizar o perfil
    if request.method == "POST":
        reserva.data_reserva = request.form.get("data_reserva")
        reserva.horario_reserva = request.form.get("horario_reserva")
        reserva.horario_reserva_fim = request.form.get("horario_reserva_fim")

        #validade reserva
        if reserva.data_reserva == "":
            flash("Data de reserva é obrigatória!","danger")
            return render_template("alterar.reserva.html", reserva=reserva)

        #salvar as alterações
        sessao.commit()
        flash("Alterado com sucesso!","sucess")
        return redirect(url_for("reserva"))
    
    return render_template("alterar.reserva.html", reserva=reserva)

#reserva excluir
@app.route("/reserva/excluir/<int:id_reserva>", methods=["POST"])
def excluir_reserva(id_reserva):
    #buscar os dados o id_reserva
    reserva = sessao.query(Reserva).get(id_reserva)

    #realizar a exclusao da reserva
    if reserva:
        sessao.delete(reserva)
        sessao.commit()
        flash("Excluído com sucesso!","sucess")
    else:
        flash("Reserva não encontrada!","danger")

    #retornar a tela principal da reserva
    return redirect(url_for("reserva"))

#historico
@app.route("/historico")
def historico():
    return render_template('historico.html')


app.run(debug=True)