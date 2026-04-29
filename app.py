"""
FracaoQuest — Aplicação Flask
Jogo de aventura com fases e chefões para aprender frações no 7º ano.
Sem banco de dados: estado 100% em sessão Flask.
"""
from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import json
import os
from game_engine import FASES, gerar_pergunta, get_fase

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fracaoquest-azure-2025-xk9")

# ── Configurações do jogo ────────────────────────────────────────────────────
VIDA_INICIAL   = 5      # corações do jogador
DANO_ERRO      = 1      # vida perdida por erro
CURA_ACERTO    = 0      # vida recuperada por acerto (0 = sem cura)
XP_POR_ACERTO  = 30
XP_BONUS_RAPIDO = 15    # bônus se responder em < 10s
PERGUNTAS_POR_FASE = 5  # quantas perguntas para enfrentar o chefão


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS DE SESSÃO
# ══════════════════════════════════════════════════════════════════════════════

def init_session():
    """Inicializa o estado do jogo na sessão."""
    session.permanent = True
    session.setdefault("jogador_nome", "Herói")
    session.setdefault("xp", 0)
    session.setdefault("nivel", 1)
    session.setdefault("vida", VIDA_INICIAL)
    session.setdefault("fases_completas", [])
    session.setdefault("fase_atual", None)
    session.setdefault("acertos_fase", 0)
    session.setdefault("erros_fase", 0)
    session.setdefault("pergunta_atual", None)
    session.setdefault("batalha_fase", "normal")  # normal | chefao


def xp_para_proximo_nivel(nivel):
    return nivel * 200


def calcular_nivel(xp):
    nivel = 1
    while xp >= xp_para_proximo_nivel(nivel):
        xp -= xp_para_proximo_nivel(nivel)
        nivel += 1
    return nivel, xp


# ══════════════════════════════════════════════════════════════════════════════
# ROTAS
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    init_session()
    return render_template("index.html",
                           fases=FASES,
                           session=session,
                           fases_completas=session.get("fases_completas", []))


@app.route("/set_nome", methods=["POST"])
def set_nome():
    nome = request.form.get("nome", "").strip()[:20]
    if nome:
        session["jogador_nome"] = nome
    return redirect(url_for("index"))


@app.route("/fase/<int:fase_id>")
def fase(fase_id):
    init_session()
    f = get_fase(fase_id)
    if not f:
        return redirect(url_for("index"))

    # Só libera a fase se a anterior estiver completa (exceto fase 1)
    if fase_id > 1 and (fase_id - 1) not in session.get("fases_completas", []):
        return redirect(url_for("index"))

    session["fase_atual"] = fase_id
    session["acertos_fase"] = 0
    session["erros_fase"] = 0
    session["batalha_fase"] = "normal"

    # Vida do chefão separada
    session["vida_chefao"] = f["vida_chefao"]
    return render_template("fase.html", fase=f, session=session)


@app.route("/batalha/<int:fase_id>")
def batalha(fase_id):
    init_session()
    f = get_fase(fase_id)
    if not f or session.get("fase_atual") != fase_id:
        return redirect(url_for("index"))

    # Gera nova pergunta
    q = gerar_pergunta(f["topico"])
    session["pergunta_atual"] = q

    nivel_atual, xp_nivel = calcular_nivel(session["xp"])
    session["nivel"] = nivel_atual

    acertos = session.get("acertos_fase", 0)
    vida_chefao = session.get("vida_chefao", f["vida_chefao"])

    # Determina se é batalha do chefão
    is_chefao = acertos >= PERGUNTAS_POR_FASE

    return render_template("batalha.html",
                           fase=f,
                           pergunta=q,
                           session=session,
                           is_chefao=is_chefao,
                           acertos=acertos,
                           total_perguntas=PERGUNTAS_POR_FASE,
                           vida_chefao=vida_chefao,
                           xp_nivel=xp_nivel,
                           xp_next=xp_para_proximo_nivel(nivel_atual))


@app.route("/responder/<int:fase_id>", methods=["POST"])
def responder(fase_id):
    init_session()
    f = get_fase(fase_id)
    if not f:
        return redirect(url_for("index"))

    q = session.get("pergunta_atual")
    if not q:
        return redirect(url_for("batalha", fase_id=fase_id))

    resposta_usuario = request.form.get("resposta", "").strip()
    tempo_resposta   = int(request.form.get("tempo", 99))
    correto          = resposta_usuario == q["resposta"]

    # Atualiza XP e vida
    xp_ganho = 0
    if correto:
        xp_ganho = XP_POR_ACERTO
        if tempo_resposta < 10:
            xp_ganho += XP_BONUS_RAPIDO
        session["xp"] = session.get("xp", 0) + xp_ganho
        session["acertos_fase"] = session.get("acertos_fase", 0) + 1
        session["vida_chefao"]  = session.get("vida_chefao", f["vida_chefao"]) - 1
    else:
        session["erros_fase"] = session.get("erros_fase", 0) + 1
        session["vida"] = max(0, session.get("vida", VIDA_INICIAL) - DANO_ERRO)

    nivel_atual, xp_nivel = calcular_nivel(session["xp"])
    session["nivel"] = nivel_atual

    # Verifica game over
    if session["vida"] <= 0:
        return redirect(url_for("game_over"))

    # Verifica vitória: chefão derrotado (vida_chefao <= 0)
    vida_chefao = session.get("vida_chefao", f["vida_chefao"])
    fase_vencida = vida_chefao <= 0

    if fase_vencida:
        if fase_id not in session.get("fases_completas", []):
            fases = session.get("fases_completas", [])
            fases.append(fase_id)
            session["fases_completas"] = fases
            session["xp"] = session.get("xp", 0) + f["xp_recompensa"]
        return render_template("resultado_fase.html",
                               fase=f,
                               vitoria=True,
                               session=session,
                               xp_ganho=f["xp_recompensa"],
                               acertos=session.get("acertos_fase", 0),
                               erros=session.get("erros_fase", 0))

    return render_template("feedback.html",
                           fase=f,
                           pergunta=q,
                           correto=correto,
                           resposta_usuario=resposta_usuario,
                           xp_ganho=xp_ganho,
                           session=session,
                           tempo=tempo_resposta,
                           vida_chefao=vida_chefao,
                           xp_nivel=xp_nivel,
                           xp_next=xp_para_proximo_nivel(nivel_atual))


@app.route("/game_over")
def game_over():
    init_session()
    fase_id = session.get("fase_atual", 1)
    f = get_fase(fase_id)
    # Restaura vida
    session["vida"] = VIDA_INICIAL
    session["acertos_fase"] = 0
    session["erros_fase"] = 0
    if f:
        session["vida_chefao"] = f["vida_chefao"]
    return render_template("game_over.html", fase=f, session=session)


@app.route("/reiniciar")
def reiniciar():
    session.clear()
    return redirect(url_for("index"))


@app.route("/status")
def status():
    """Health check para Azure."""
    return jsonify({"status": "ok", "app": "FracaoQuest"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
