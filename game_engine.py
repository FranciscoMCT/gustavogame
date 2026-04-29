"""
FracaoQuest — Motor de Perguntas
Gera perguntas dinâmicas para todos os tópicos de frações do 7º ano.
Sem banco de dados: tudo gerado em tempo real com random.
"""
import random
import math
from fractions import Fraction


# ══════════════════════════════════════════════════════════════════════════════
# DEFINIÇÃO DAS FASES / CHEFÕES
# ══════════════════════════════════════════════════════════════════════════════

FASES = [
    {
        "id": 1,
        "nome": "A Reta Numérica Sombria",
        "topico": "reta_numerica",
        "chefao": "Espectro do Zero",
        "emoji_chefao": "👻",
        "descricao": "O Espectro do Zero assombra a reta numérica! Mostre que domina frações positivas e negativas para vencê-lo.",
        "cor": "#6c63ff",
        "dificuldade": 1,
        "xp_recompensa": 150,
        "vida_chefao": 5,
    },
    {
        "id": 2,
        "nome": "O Coliseu da Comparação",
        "topico": "comparacao",
        "chefao": "Gladiador Fracionário",
        "emoji_chefao": "⚔️",
        "descricao": "O Gladiador desafia você a comparar frações em batalha! Prove quem é maior.",
        "cor": "#f59e0b",
        "dificuldade": 2,
        "xp_recompensa": 200,
        "vida_chefao": 6,
    },
    {
        "id": 3,
        "nome": "Torres da Adição e Subtração",
        "topico": "adicao_subtracao",
        "chefao": "Arquimago Somador",
        "emoji_chefao": "🧙",
        "descricao": "O Arquimago lança feitiços de adição e subtração! Calcule rápido para sobreviver.",
        "cor": "#10b981",
        "dificuldade": 2,
        "xp_recompensa": 250,
        "vida_chefao": 7,
    },
    {
        "id": 4,
        "nome": "O Santuário Inverso",
        "topico": "fracao_inversa",
        "chefao": "Oráculo Invertido",
        "emoji_chefao": "🔮",
        "descricao": "O Oráculo gira o mundo de cabeça para baixo! Domina frações inversas para restaurar a ordem.",
        "cor": "#ec4899",
        "dificuldade": 3,
        "xp_recompensa": 300,
        "vida_chefao": 7,
    },
    {
        "id": 5,
        "nome": "Fábrica da Multiplicação e Divisão",
        "topico": "multiplicacao_divisao",
        "chefao": "Engenheiro Caótico",
        "emoji_chefao": "⚙️",
        "descricao": "O Engenheiro multiplicou o caos! Resolve as equações para desligar as máquinas.",
        "cor": "#f97316",
        "dificuldade": 3,
        "xp_recompensa": 350,
        "vida_chefao": 8,
    },
    {
        "id": 6,
        "nome": "A Torre da Potenciação",
        "topico": "potenciacao",
        "chefao": "Dragão Exponencial",
        "emoji_chefao": "🐉",
        "descricao": "O Dragão cospe potências de frações! Enfrente as chamas dos expoentes.",
        "cor": "#ef4444",
        "dificuldade": 4,
        "xp_recompensa": 400,
        "vida_chefao": 8,
    },
    {
        "id": 7,
        "nome": "O Templo dos Ângulos",
        "topico": "angulos",
        "chefao": "Guardião Geométrico",
        "emoji_chefao": "📐",
        "descricao": "O Guardião Geométrico protege os segredos dos ângulos fracionários. Derrote-o para completar a jornada!",
        "cor": "#8b5cf6",
        "dificuldade": 4,
        "xp_recompensa": 500,
        "vida_chefao": 10,
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# GERADORES DE PERGUNTAS POR TÓPICO
# ══════════════════════════════════════════════════════════════════════════════

def _opcoes_embaralhadas(correto, erradas):
    """Monta lista de 4 opções embaralhadas."""
    ops = [str(correto)] + [str(e) for e in erradas[:3]]
    random.shuffle(ops)
    return ops, str(correto)


def _frac_str(num, den):
    """Formata fração como string legível."""
    if den == 1:
        return str(num)
    return f"{num}/{den}"


def gerar_reta_numerica():
    """Frações positivas e negativas na reta numérica."""
    tipo = random.choice(["posicao", "sinal", "ordem"])

    if tipo == "posicao":
        den = random.randint(2, 8)
        num = random.randint(-den + 1, den - 1)
        while num == 0:
            num = random.randint(-den + 1, den - 1)
        pergunta = f"A fração {_frac_str(num, den)} está à _____ do zero na reta numérica."
        correto = "esquerda" if num < 0 else "direita"
        erradas = ["esquerda", "direita", "sobre o zero", "não está na reta"]
        erradas = [e for e in erradas if e != correto][:3]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"Frações negativas ficam à esquerda do zero; positivas à direita. {_frac_str(num, den)} é {'negativa' if num < 0 else 'positiva'}."}

    elif tipo == "sinal":
        den = random.randint(2, 6)
        num = random.randint(1, den - 1)
        sinal_num = random.choice([-1, 1])
        sinal_den = random.choice([-1, 1])
        n, d = sinal_num * num, sinal_den * den
        f = Fraction(n, d)
        correto = "positiva" if f > 0 else "negativa"
        pergunta = f"A fração {n}/{d} é:"
        erradas = ["positiva", "negativa", "nula", "indefinida"]
        erradas = [e for e in erradas if e != correto][:3]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"Sinais iguais = positivo; sinais diferentes = negativo. {n}/{d} = {f} que é {correto}."}

    else:  # ordem
        den = random.randint(2, 6)
        nums = random.sample(range(-den + 1, den), 4)
        fracs = sorted([Fraction(n, den) for n in nums])
        correto = f"{fracs[0].numerator}/{fracs[0].denominator}" if fracs[0].denominator != 1 else str(fracs[0].numerator)
        pergunta = f"Qual dessas frações é a MENOR? (denominador {den})\n{', '.join([_frac_str(n, den) for n in nums])}"
        erradas = [_frac_str(f.numerator, f.denominator) for f in fracs[1:]]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"Na reta numérica, números mais à esquerda são menores. A menor é {correto}."}


def gerar_comparacao():
    """Comparação de frações."""
    tipo = random.choice(["maior_menor", "equivalente", "ordem_lista"])

    if tipo == "maior_menor":
        den1 = random.randint(2, 8)
        den2 = random.randint(2, 8)
        num1 = random.randint(1, den1 * 2)
        num2 = random.randint(1, den2 * 2)
        f1, f2 = Fraction(num1, den1), Fraction(num2, den2)
        if f1 == f2:
            num2 += 1
            f2 = Fraction(num2, den2)
        correto = ">" if f1 > f2 else "<"
        pergunta = f"Complete com > ou <:\n{num1}/{den1}  ___  {num2}/{den2}"
        ops, resp = _opcoes_embaralhadas(correto, ["<", ">", "=", "≠"])
        return {"pergunta": pergunta, "opcoes": [">", "<", "=", "≠"], "resposta": correto,
                "explicacao": f"MMC({den1},{den2}) = {math.lcm(den1,den2)}. Convertendo: {f1} e {f2}. Logo {num1}/{den1} {correto} {num2}/{den2}."}

    elif tipo == "equivalente":
        den = random.randint(2, 6)
        num = random.randint(1, den - 1)
        mult = random.randint(2, 5)
        n2, d2 = num * mult, den * mult
        pergunta = f"Qual fração é EQUIVALENTE a {num}/{den}?"
        correto = f"{n2}/{d2}"
        erradas = [f"{num*mult+1}/{d2}", f"{n2}/{d2+1}", f"{num}/{den+1}"]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"Multiplicando numerador e denominador por {mult}: {num}×{mult}/{den}×{mult} = {n2}/{d2}."}

    else:
        den = random.randint(2, 6)
        nums = random.sample(range(1, den * 2), 4)
        fracs = [Fraction(n, den) for n in nums]
        ordem = sorted(fracs)
        correto = " < ".join([f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator) for f in ordem])
        pergunta = f"Ordene do menor ao maior (denominador {den}):\n{', '.join([str(n)+'/'+str(den) for n in nums])}"
        # Gera opções erradas trocando posições
        errada1 = " < ".join([f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator) for f in reversed(ordem)])
        errada2 = " < ".join([f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator) for f in [ordem[1], ordem[0], ordem[2], ordem[3]]])
        errada3 = " < ".join([f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator) for f in [ordem[0], ordem[2], ordem[1], ordem[3]]])
        ops, resp = _opcoes_embaralhadas(correto, [errada1, errada2, errada3])
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"Com mesmo denominador, compara-se os numeradores. Ordem correta: {correto}."}


def gerar_adicao_subtracao():
    """Adição e subtração entre frações."""
    op = random.choice(["+", "-"])
    tipo = random.choice(["mesmo_den", "den_diferente", "misto"])

    if tipo == "mesmo_den":
        den = random.randint(2, 10)
        n1 = random.randint(1, den * 2)
        n2 = random.randint(1, den * 2)
        if op == "-" and n1 < n2:
            n1, n2 = n2, n1
        f = Fraction(n1, den) + Fraction(n2, den) if op == "+" else Fraction(n1, den) - Fraction(n2, den)
        correto = f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)
        pergunta = f"Calcule: {n1}/{den} {op} {n2}/{den} ="
        erradas = [f"{n1+n2}/{den}", f"{abs(n1-n2)}/{den*2}", f"{n1*n2}/{den}"]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"Mesmo denominador: mantém o denominador, {op} os numeradores. {n1} {op} {n2} = {n1+n2 if op=='+' else n1-n2}. Simplificando: {correto}."}

    elif tipo == "den_diferente":
        den1 = random.randint(2, 6)
        den2 = random.randint(2, 6)
        while den1 == den2:
            den2 = random.randint(2, 6)
        n1 = random.randint(1, den1)
        n2 = random.randint(1, den2)
        f1, f2 = Fraction(n1, den1), Fraction(n2, den2)
        f = f1 + f2 if op == "+" else f1 - f2
        correto = f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)
        mmc = math.lcm(den1, den2)
        pergunta = f"Calcule: {n1}/{den1} {op} {n2}/{den2} ="
        erradas = [f"{n1+n2}/{den1+den2}", f"{n1*den2 + n2*den1}/{mmc+1}", f"{abs(n1-n2)}/{mmc}"]
        erradas = [e for e in erradas if e != correto]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"MMC({den1},{den2}) = {mmc}. Convertendo: {n1*mmc//den1}/{mmc} {op} {n2*mmc//den2}/{mmc} = {correto}."}

    else:  # número misto
        inteiro = random.randint(1, 4)
        den = random.randint(2, 6)
        num = random.randint(1, den - 1)
        f_misto = Fraction(inteiro * den + num, den)
        f2 = Fraction(random.randint(1, den - 1), den)
        f = f_misto + f2 if op == "+" else f_misto - f2
        correto = f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)
        pergunta = f"Calcule: {inteiro} {num}/{den} {op} {f2.numerator}/{f2.denominator} ="
        erradas = [f"{f.numerator+1}/{f.denominator}", f"{f.numerator-1}/{f.denominator}", f"{inteiro}{num+f2.numerator}/{den}"]
        erradas = [e for e in erradas if e != correto]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"Converta {inteiro} {num}/{den} para fração imprópria: {f_misto.numerator}/{den}. Depois {op} normalmente."}


def gerar_fracao_inversa():
    """Fração inversa (recíproca)."""
    tipo = random.choice(["inversa_simples", "inversa_negativa", "produto_inverso"])

    if tipo == "inversa_simples":
        den = random.randint(2, 9)
        num = random.randint(1, den * 2)
        correto = f"{den}/{num}"
        pergunta = f"Qual é a fração inversa (recíproca) de {num}/{den}?"
        erradas = [f"{num}/{den+1}", f"{-num}/{den}", f"{den+1}/{num}"]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"A inversa troca numerador e denominador: inversa de {num}/{den} = {den}/{num}."}

    elif tipo == "inversa_negativa":
        den = random.randint(2, 8)
        num = random.randint(1, den - 1)
        correto = f"{-den}/{num}"
        pergunta = f"Qual é a fração inversa de -{num}/{den}?"
        erradas = [f"{den}/{num}", f"{-num}/{den}", f"{num}/{den}"]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"Troca-se numerador e denominador, mantendo o sinal: inversa de -{num}/{den} = -{den}/{num}."}

    else:
        den = random.randint(2, 6)
        num = random.randint(1, den - 1)
        produto = Fraction(num, den) * Fraction(den, num)
        pergunta = f"Quanto é {num}/{den} × {den}/{num}?"
        correto = "1"
        ops = ["1", "0", f"{num*den}/{den*num}", f"{num**2}/{den**2}"]
        random.shuffle(ops)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": "1",
                "explicacao": f"Uma fração multiplicada pela sua inversa SEMPRE resulta em 1. {num}/{den} × {den}/{num} = {num*den}/{den*num} = 1."}


def gerar_multiplicacao_divisao():
    """Multiplicação e divisão com frações."""
    op = random.choice(["×", "÷"])
    tipo = random.choice(["frac_frac", "inteiro_frac", "simplifica"])

    if tipo == "frac_frac":
        d1, d2 = random.randint(2, 6), random.randint(2, 6)
        n1, n2 = random.randint(1, d1), random.randint(1, d2)
        if op == "×":
            f = Fraction(n1, d1) * Fraction(n2, d2)
            correto = f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)
            pergunta = f"Calcule: {n1}/{d1} × {n2}/{d2} ="
            erradas = [f"{n1*n2}/{d1+d2}", f"{n1+n2}/{d1*d2}", f"{n1}/{d2}"]
        else:
            f = Fraction(n1, d1) / Fraction(n2, d2)
            correto = f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)
            pergunta = f"Calcule: {n1}/{d1} ÷ {n2}/{d2} ="
            erradas = [f"{n1*n2}/{d1*d2}", f"{n1}/{d1*d2}", f"{d1*n2}/{n1*d2}"]
        erradas = [e for e in erradas if e != correto]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        explicacao = (f"Multiplicação: multiplica numerador com numerador e denominador com denominador."
                      if op == "×" else
                      f"Divisão: multiplica pela inversa. {n1}/{d1} ÷ {n2}/{d2} = {n1}/{d1} × {d2}/{n2}.")
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp, "explicacao": explicacao}

    elif tipo == "inteiro_frac":
        inteiro = random.randint(2, 8)
        den = random.randint(2, 6)
        num = random.randint(1, den - 1)
        if op == "×":
            f = Fraction(inteiro) * Fraction(num, den)
            correto = f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)
            pergunta = f"Calcule: {inteiro} × {num}/{den} ="
            erradas = [f"{inteiro+num}/{den}", f"{inteiro}/{num*den}", f"{inteiro*den}/{num}"]
        else:
            f = Fraction(inteiro) / Fraction(num, den)
            correto = f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)
            pergunta = f"Calcule: {inteiro} ÷ {num}/{den} ="
            erradas = [f"{inteiro*num}/{den}", f"{num}/{inteiro*den}", f"{inteiro+den}/{num}"]
        erradas = [e for e in erradas if e != correto]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"Número inteiro = {inteiro}/1. Depois aplica a operação normalmente. Resultado: {correto}."}

    else:  # simplifica antes
        d = random.randint(2, 6)
        n1 = random.randint(1, d)
        n2 = random.randint(1, d)
        mdc = math.gcd(n1 * d, d * n2) if op == "×" else 1
        f = Fraction(n1, d) * Fraction(d, n2)
        correto = f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)
        pergunta = f"Simplifique e calcule: {n1}/{d} × {d}/{n2} ="
        erradas = [f"{n1*d}/{d*n2}", f"{n1+d}/{d+n2}", f"{n1}/{n2+1}"]
        erradas = [e for e in erradas if e != correto]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"Pode-se cancelar o {d} antes de multiplicar: {n1}/1 × 1/{n2} = {correto}."}


def gerar_potenciacao():
    """Frações e potenciação."""
    tipo = random.choice(["expoente_positivo", "expoente_negativo", "base_negativa"])

    if tipo == "expoente_positivo":
        den = random.randint(2, 5)
        num = random.randint(1, den - 1)
        exp = random.randint(2, 3)
        f = Fraction(num, den) ** exp
        correto = f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)
        pergunta = f"Calcule: ({num}/{den})^{exp} ="
        erradas = [f"{num*exp}/{den*exp}", f"{num}/{den**exp}", f"{num**exp}/{den+exp}"]
        erradas = [e for e in erradas if e != correto]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"({num}/{den})^{exp} = {num}^{exp}/{den}^{exp} = {num**exp}/{den**exp}. Simplificando: {correto}."}

    elif tipo == "expoente_negativo":
        den = random.randint(2, 4)
        num = random.randint(1, den - 1)
        exp = random.randint(1, 2)
        # (num/den)^(-exp) = (den/num)^exp
        f = Fraction(den, num) ** exp
        correto = f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)
        pergunta = f"Calcule: ({num}/{den})^(-{exp}) ="
        erradas = [f"-{num**exp}/{den**exp}", f"{num**exp}/{den**exp}", f"{den}/{num*exp}"]
        erradas = [e for e in erradas if e != correto]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"Expoente negativo = inverte a fração. ({num}/{den})^(-{exp}) = ({den}/{num})^{exp} = {correto}."}

    else:
        den = random.randint(2, 5)
        num = random.randint(1, den - 1)
        exp = random.randint(2, 4)
        base_neg = Fraction(-num, den)
        f = base_neg ** exp
        correto = f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)
        sinal = "positivo" if exp % 2 == 0 else "negativo"
        pergunta = f"Calcule: (-{num}/{den})^{exp} ="
        erradas = [f"-{abs(f.numerator)}/{f.denominator}", f"{abs(f.numerator)}/{f.denominator+1}", f"-{f.numerator+1}/{f.denominator}"]
        erradas = [e for e in erradas if e != correto]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"Base negativa com expoente {exp} ({'par' if exp%2==0 else 'ímpar'}) = resultado {sinal}. (-{num}/{den})^{exp} = {correto}."}


def gerar_angulos():
    """Frações e ângulos."""
    tipo = random.choice(["fracao_volta", "angulo_fracao", "soma_angulos"])

    if tipo == "fracao_volta":
        opcoes_frac = [(1, 2, 180), (1, 4, 90), (3, 4, 270), (1, 3, 120), (2, 3, 240), (1, 6, 60), (1, 8, 45)]
        num, den, graus = random.choice(opcoes_frac)
        pergunta = f"Qual é o ângulo correspondente a {num}/{den} de volta completa (360°)?"
        correto = f"{graus}°"
        erradas = [f"{graus+10}°", f"{graus-10}°", f"{360//den}°" if num != 1 else f"{graus+30}°"]
        erradas = [e for e in erradas if e != correto]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"{num}/{den} de 360° = {num} × 360 ÷ {den} = {graus}°."}

    elif tipo == "angulo_fracao":
        angulos = [(90, 1, 4), (180, 1, 2), (60, 1, 6), (120, 1, 3), (270, 3, 4), (45, 1, 8)]
        graus, num, den = random.choice(angulos)
        pergunta = f"O ângulo de {graus}° corresponde a qual fração de uma volta completa (360°)?"
        correto = f"{num}/{den}"
        erradas = [f"{num+1}/{den}", f"{num}/{den+2}", f"{num*2}/{den}"]
        erradas = [e for e in erradas if e != correto]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"{graus} ÷ 360 = {graus//math.gcd(graus,360)}/{360//math.gcd(graus,360)} = {num}/{den} de volta."}

    else:
        den = random.randint(3, 8)
        n1 = random.randint(1, den - 1)
        n2 = random.randint(1, den - 1)
        soma = Fraction(n1, den) + Fraction(n2, den)
        graus_soma = int(soma * 360)
        pergunta = f"Um ângulo é {n1}/{den} de volta e outro é {n2}/{den} de volta. Qual a soma em graus?"
        correto = f"{graus_soma}°"
        erradas = [f"{graus_soma+36}°", f"{graus_soma-36}°", f"{(n1+n2)*360//den + 10}°"]
        erradas = [e for e in erradas if e != correto]
        ops, resp = _opcoes_embaralhadas(correto, erradas)
        return {"pergunta": pergunta, "opcoes": ops, "resposta": resp,
                "explicacao": f"Some as frações: {n1}/{den} + {n2}/{den} = {soma.numerator}/{soma.denominator}. Depois × 360° = {graus_soma}°."}


# ══════════════════════════════════════════════════════════════════════════════
# DISPATCHER
# ══════════════════════════════════════════════════════════════════════════════

GERADORES = {
    "reta_numerica":       gerar_reta_numerica,
    "comparacao":          gerar_comparacao,
    "adicao_subtracao":    gerar_adicao_subtracao,
    "fracao_inversa":      gerar_fracao_inversa,
    "multiplicacao_divisao": gerar_multiplicacao_divisao,
    "potenciacao":         gerar_potenciacao,
    "angulos":             gerar_angulos,
}


def gerar_pergunta(topico: str) -> dict:
    """Gera uma pergunta aleatória para o tópico dado."""
    gerador = GERADORES.get(topico)
    if not gerador:
        raise ValueError(f"Tópico desconhecido: {topico}")
    q = gerador()
    q["topico"] = topico
    return q


def get_fase(fase_id: int) -> dict | None:
    for f in FASES:
        if f["id"] == fase_id:
            return f
    return None
