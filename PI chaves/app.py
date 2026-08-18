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

    if request.method == "POST":
        # Aqui você pode processar os dados do formulário, por exemplo, salvando em um banco de dados
        identificador = request.form.get("identificador")
        observacao = request.form.get("observacao")
        disponivel = request.form.get("disponivel")
        nome_chave = request.form.get("nome_chave")
        
        # Validação do nome
        if nome_chave == "":
            flash("Nome da Chave é obrigatório!", "danger")
            return render_template("chave.html")

        #inserir chave
        c = Chave(identificador=identificador, observacao=observacao, disponivel=disponivel, nome_chave=nome_chave)
        sessao.add(c)
        sessao.commit()
        flash("Chave salva com sucesso!", "success")

        # Redireciona para a página inicial após o envio do formulário
        return redirect(url_for("chave"))
    return render_template('chave.html')

#consultar chave
@app.route("/chave/consultar", methods=["GET", "POST"])
def consultar_chave():
    
    #pegar a chave que foi informada no formulário
    nome_chave = request.args.get("chave","")
    
    #consultar o(s) chave(s)
    chaves = sessao.query(Chave).filter(Chave.nome_chave.like(f"%{nome_chave}%")).all()
    
    #chamar chave.html para mostrar os dados
    return render_template("chave.html", chaves=chaves)

#alterar chave
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

#chave excluir
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

#usuario
@app.route("/usuario")
def usuario():
    if request.method == "POST":
        # Aqui você pode processar os dados do formulário, por exemplo, salvando em um banco de dados
        nome_usuario = request.form.get("identificador")
        email = request.form.get("observacao")
        senha = request.form.get("disponivel")
        
        # Validação do nome
        if nome_usuario == "":
            flash("Nome do Usuário é obrigatório!", "danger")
            return render_template("usuario.html")

        #inserir usuário
        u = Usuario(nome_usuario=nome_usuario, email=email, senha=senha)
        sessao.add(u)
        sessao.commit()
        flash("Usuário salvo com sucesso!", "success")

        # Redireciona para a página inicial após o envio do formulário
        return redirect(url_for("usuario"))
    return render_template('usuario.html')

#consultar usuário
@app.route("/usuario/consultar", methods=["GET", "POST"])
def consultar_usuario():
    
    #pegar o usuário que foi informado no formulário
    nome_usuario = request.args.get("usuario","")
    
    #consultar o(s) usuário(s)
    usuarios = sessao.query(Usuario).filter(Usuario.nome_usuario.like(f"%{nome_usuario}%")).all()
    
    #chamar usuario.html para mostrar os dados
    return render_template("usuario.html", usuarios=usuarios)

#alterar usuario
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

#usuario excluir
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
@app.route("/ambiente")
def ambiente():
    if request.method == "POST":
        # Aqui você pode processar os dados do formulário, por exemplo, salvando em um banco de dados
        ambiente = request.form.get("ambiente")
        observacao_ambiente = request.form.get("observacao_ambiente")
        disponivel_ambiente = request.form.get("disponivel_ambiente")
        
        # Validação do nome
        if ambiente == "":
            flash("Nome do Ambiente é obrigatório!", "danger")
            return render_template("ambiente.html")

        #inserir ambiente
        a = Ambiente(ambiente=ambiente, observacao=observacao_ambiente, disponivel=disponivel_ambiente)
        sessao.add(a)
        sessao.commit()
        flash("Ambiente salvo com sucesso!", "success")

        # Redireciona para a página inicial após o envio do formulário
        return redirect(url_for("ambiente"))
    return render_template('ambiente.html')


#alterar ambiente
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

#ambiente excluir
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

#perfil
@app.route("/perfil")
def perfil():
    if request.method == "POST":
        # Aqui você pode processar os dados do formulário, por exemplo, salvando em um banco de dados
        nome_perfil = request.form.get("ambiente")
        matricula = request.form.get("matricula")
        cargo = request.form.get("cargo")
        
        # Validação do nome
        if nome_perfil == "":
            flash("Nome do Perfil é obrigatório!", "danger")
            return render_template("perfil.html")

        #inserir perfil
        p = Perfil(nome=nome_perfil, matricula=matricula, cargo=cargo)
        sessao.add(p)
        sessao.commit()
        flash("Perfil salvo com sucesso!", "success")

        # Redireciona para a página inicial após o envio do formulário
        return redirect(url_for("perfil"))
    return render_template('perfil.html')

#consultar perfil
@app.route("/perfil/consultar", methods=["GET", "POST"])
def consultar_perfil():
    
    #pegar o perfil que foi informado no formulário
    nome_perfil = request.args.get("perfil","")
    
    #consultar o(s) perfil(s)
    perfis = sessao.query(Perfil).filter(Perfil.nome.like(f"%{nome_perfil}%")).all()
    
    #chamar perfil.html para mostrar os dados
    return render_template("perfil.html", perfis=perfis)


#alterar perfil
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

#perfil excluir
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

#movimentacao
@app.route("/movimentacao")
def movimentacao():
    if request.method == "POST":
        # Aqui você pode processar os dados do formulário, por exemplo, salvando em um banco de dados
        data_retirada = request.form.get("data_retirada")
        horario_inicio = request.form.get("horario_inicio")
        
        # Validação da data de retirada
        if data_retirada == "":
            flash("Data de retirada é obrigatória!", "danger")
            return render_template("movimentacao.html")

        #inserir movimentacao
        m = Movimentacao(data_retirada=data_retirada, horario_inicio=horario_inicio)
        sessao.add(m)
        sessao.commit()
        flash("Movimentação salva com sucesso!", "success")

        # Redireciona para a página inicial após o envio do formulário
        return redirect(url_for("movimentacao"))
    return render_template('movimentacao.html')

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

#devolucao
@app.route("/devolucao")
def devolucao():
    if request.method == "POST":
        # Aqui você pode processar os dados do formulário, por exemplo, salvando em um banco de dados
        date_reserva = request.form.get("data_reserva")
        horario_devolucao= request.form.get("horario_devolucao")
        obsevacao_devolucao = request.form.get("observacao_devolucao")
        
        # Validação da data de reserva
        if date_reserva == "":
            flash("Data de reserva é obrigatória!", "danger")
            return render_template("devolucao.html")

        #inserir devolucao
        d = Movimentacao_devolucao(date_reserva=date_reserva, horario_devolucao=horario_devolucao, obsevacao_devolucao=obsevacao_devolucao)
        sessao.add(d)
        sessao.commit()
        flash("Devolução salva com sucesso!", "success")

        # Redireciona para a página inicial após o envio do formulário
        return redirect(url_for("devolucao"))
    return render_template('devolucao.html')

#consultar devolucao
@app.route("/devolucao/consultar", methods=["GET", "POST"])
def consultar_devolucao():
    
    #pegar a devolucao que foi informada no formulário
    date_reserva = request.args.get("date_reserva","")
    
    #consultar a(s) devolucao(oes)
    devolucoes = sessao.query(Movimentacao_devolucao).filter(Movimentacao_devolucao.date_reserva.like(f"%{date_reserva}%")).all()
    
    #chamar devolucao.html para mostrar os dados
    return render_template("devolucao.html", devolucoes=devolucoes)


#alterar devolucao
@app.route("/devolucao/alterar/<int:id_devolucao>", methods=["GET", "POST"])
def alterar_devolucao(id_devolucao):
    
    #buscar os dados o id_devolucao
    devolucao = sessao.query(Movimentacao_devolucao).get(id_devolucao)
    
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
    devolucao = sessao.query(Movimentacao_devolucao).get(id_devolucao)

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
@app.route("/reserva")
def reserva():
    if request.method == "POST":
        # Aqui você pode processar os dados do formulário, por exemplo, salvando em um banco de dados
        data_reserva = request.form.get("data_reserva")
        horario_reserva= request.form.get("horario_reserva")
        horario_reserva_fim = request.form.get("horario_reserva_fim")
        
        # Validação da data de reserva
        if data_reserva == "":
            flash("Data de reserva é obrigatória!", "danger")
            return render_template("devolucao.html")

        #inserir reserva
        r = Reserva(date_reserva=data_reserva, horario_reserva=horario_reserva, horario_reserva_fim=horario_reserva_fim)
        sessao.add(r)
        sessao.commit()
        flash("Reserva salva com sucesso!", "success")

        # Redireciona para a página inicial após o envio do formulário
        return redirect(url_for("reserva"))
    return render_template('reserva.html')

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