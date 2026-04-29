# 🏆 FraçãoQuest

Jogo de aventura RPG educativo para aprender **frações do 7º ano**, feito em **Python 3.12 + Flask**, sem banco de dados, pronto para Azure App Services.

## 🎮 Sobre o jogo

O jogador percorre **7 fases** com chefões, cada uma cobrindo um tópico da matéria:

| Fase | Tópico | Chefão |
|------|--------|--------|
| 1 | Frações na reta numérica | 👻 Espectro do Zero |
| 2 | Comparação de frações | ⚔️ Gladiador Fracionário |
| 3 | Adição e subtração | 🧙 Arquimago Somador |
| 4 | Fração inversa | 🔮 Oráculo Invertido |
| 5 | Multiplicação e divisão | ⚙️ Engenheiro Caótico |
| 6 | Potenciação com frações | 🐉 Dragão Exponencial |
| 7 | Frações e ângulos | 📐 Guardião Geométrico |

### Mecânicas
- ❤ **5 vidas** — erros custam vida
- ⚡ **Timer de 20s** por pergunta — resposta rápida = bônus de XP
- ⭐ **Sistema de XP e Nível** persistente na sessão
- 🔒 **Fases bloqueadas** — desbloqueiam em sequência
- 💡 **Explicação** em toda resposta (certa ou errada)
- ♾️ **Perguntas geradas dinamicamente** — nunca se repetem

---

## 🗂 Estrutura

```
fracao-quest/
├── app.py              # Rotas Flask e lógica de sessão
├── game_engine.py      # Motor de geração de perguntas (7 tópicos)
├── requirements.txt    # Flask + Gunicorn
├── startup.txt         # Comando de inicialização do Azure
├── templates/
│   ├── base.html       # Layout base + HUD do jogador
│   ├── index.html      # Mapa do mundo / seleção de fases
│   ├── fase.html       # Tela de intro da fase + chefão
│   ├── batalha.html    # Tela de batalha com timer
│   ├── feedback.html   # Resultado de cada resposta
│   ├── resultado_fase.html  # Vitória (chefão derrotado)
│   └── game_over.html  # Derrota (sem vidas)
└── .github/workflows/
    └── azure-deploy.yml
```

---

## ☁️ Deploy no Azure App Services

### Pré-requisitos
- App Service criado com **Python 3.12** no Linux
- GitHub Actions configurado

### Passo a passo

**1. Crie o App Service via Azure CLI:**
```bash
az webapp create \
  --resource-group <seu-rg> \
  --plan <seu-plan> \
  --name <nome-do-app> \
  --runtime "PYTHON:3.12"
```

**2. Configure o startup command no portal:**
```
gunicorn --bind=0.0.0.0:8000 --timeout=600 --workers=2 app:app
```
_(Em App Service → Configuration → General Settings → Startup Command)_

**3. Crie o Service Principal para o GitHub Actions:**
```bash
az ad sp create-for-rbac \
  --name "fracaoquestsp" \
  --role contributor \
  --scopes /subscriptions/<sub-id>/resourceGroups/<rg> \
  --sdk-auth
```

**4. Adicione os Secrets no GitHub:**
| Secret | Valor |
|--------|-------|
| `AZURE_CREDENTIALS` | JSON completo do comando acima |
| `AZURE_APP_NAME` | Nome do seu App Service |

**5. Push para `main` → deploy automático! 🚀**

### Application Settings recomendados
| Chave | Valor |
|-------|-------|
| `SECRET_KEY` | uma string aleatória segura (ex: use `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `true` |

---

## 🔒 Segurança
- Sem banco de dados → sem SQL injection
- Toda entrada validada com `filter_input` / `int()`
- `SECRET_KEY` via variável de ambiente
- Sessão Flask com cookie assinado

## 📋 Requisitos
- Python 3.10+
- Flask 3.x
- Gunicorn

---

## 📝 Licença
MIT
