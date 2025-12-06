# 🚀 Deploy Render - Essencial# Guia de Deploy - Gerenciador de Orçamento



Seu app está **pronto para deploy** em 5 minutos!## Checklist de Pre-Deploy



---- [ ] Atualizar `SECRET_KEY` em `.env`

- [ ] Definir `FLASK_DEBUG=False`

## ⚡ 3 Passos Rápidos- [ ] Testar localmente com `FLASK_ENV=production`

- [ ] Verificar se database está configurado (SQLite ou PostgreSQL)

### 1️⃣ Gerar SECRET_KEY- [ ] Revisar todas as secrets no arquivo `.env`

```powershell- [ ] Adicionar repositório remoto do seu host de deploy

python setup_deploy.py- [ ] Confirmar que `requirements.txt` tem todas as dependências

```

## Gerar SECRET_KEY Segura

### 2️⃣ Testar Localmente

```powershell```powershell

.\venv\Scripts\Activate.ps1python -c "import secrets; print(secrets.token_urlsafe(32))"

pip install -r requirements.txt```

$env:SECRET_KEY = "sua-chave-do-.env"

waitress-serve --port=8000 wsgi:appCopie a saída e adicione ao seu `.env`:

``````

SECRET_KEY=sua_chave_gerada_aqui

Acesse: http://127.0.0.1:8000```



### 3️⃣ Deploy no Render## Deploy Local com Gunicorn (teste antes de fazer push)

```bash

git add .```powershell

git commit -m "Deploy ready for Render"# 1. Ativar ambiente virtual

git push.\venv\Scripts\Activate.ps1

```

# 2. Instalar gunicorn (já deve estar em requirements.txt)

Depois:pip install gunicorn

1. Ir para https://render.com

2. Conectar com GitHub# 3. Testar com Gunicorn

3. Criar novo **Web Service**$env:FLASK_ENV = "production"

4. Deploy automático! ✅$env:SECRET_KEY = "test-key-123456789"

gunicorn --bind 127.0.0.1:5000 --workers 1 wsgi:app

---

# Acesse http://127.0.0.1:5000

## 🔑 Variáveis de Ambiente```



`render.yaml` cria `SECRET_KEY` automaticamente.## Deploy no Heroku (recomendado para iniciantes)



Se precisar customizar, adicione em **Environment** no Render.### Pré-requisitos

- Conta Heroku (gratuita em https://heroku.com)

---- Heroku CLI instalado: https://devcenter.heroku.com/articles/heroku-cli



## ✅ Checklist### Passos



- [ ] Rodou `python setup_deploy.py`1. **Login no Heroku**

- [ ] Testou com `waitress-serve --port=8000 wsgi:app`   ```bash

- [ ] Fez push para GitHub   heroku login

- [ ] Criou Web Service no Render   ```

- [ ] Deploy ✅

2. **Criar aplicação**

---   ```bash

   heroku create seu-app-orcamento

## 🆘 Problemas?   ```



**Erro: "SECRET_KEY not set"**3. **Configurar variáveis de ambiente**

```powershell   ```bash

python setup_deploy.py   # Gerar SECRET_KEY segura

```   python -c "import secrets; print(secrets.token_urlsafe(32))"

   

**Erro ao testar?**   # Configurar no Heroku

```powershell   heroku config:set SECRET_KEY="sua-chave-aqui"

pip install -r requirements.txt   heroku config:set FLASK_ENV=production

```   heroku config:set FLASK_DEBUG=False

   ```

**App não inicia no Render?**

- Verifique logs no dashboard do Render4. **Fazer push do código**

- Certifique-se que `render.yaml` está na raiz   ```bash

   git push heroku develop

---   ```

   (Se estiver na branch `main`, use `git push heroku main`)

**Status:** ✅ PRONTO PARA RENDER

5. **Ver logs**
   ```bash
   heroku logs --tail
   ```

6. **Acessar aplicação**
   ```bash
   heroku open
   ```

## Deploy no Railway (alternativa moderna)

1. Ir para https://railway.app
2. Conectar com GitHub
3. Selecionar repositório
4. Railway detectará automaticamente o `Procfile`
5. Adicionar variáveis de ambiente no painel do Railway
6. Deploy automático ao fazer push no repositório

## Deploy no PythonAnywhere (sem conta bancária)

1. Criar conta em https://www.pythonanywhere.com
2. Fazer upload do código via Git
3. Criar Web App → Python 3.11 → Flask
4. Apontar para `wsgi:app`
5. Configurar variáveis de ambiente em configurações
6. Reiniciar Web App

## Database em Produção

### Usar PostgreSQL em vez de SQLite

**Opção 1: PostgreSQL no Heroku (banco padrão)**
```bash
# Heroku já fornece DATABASE_URL automaticamente
heroku config
# Procure por DATABASE_URL - já estará configurado
```

**Opção 2: Configurar PostgreSQL manualmente**
```bash
# Instalar driver PostgreSQL
pip install psycopg2-binary
```

Atualizar `.env`:
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

## Troubleshooting

### Erro: "SECRET_KEY not set"
```bash
# Configurar SECRET_KEY
export SECRET_KEY="sua-chave"
# ou em PowerShell:
$env:SECRET_KEY = "sua-chave"
```

### Erro: "ModuleNotFoundError: No module named 'app'"
- Confirmar que está usando `wsgi.py` como entry point
- Confirmar que `app/` está no mesmo diretório de `wsgi.py`

### Erro: "Database is locked"
- Significa que SQLite está sendo usado em produção (não recomendado)
- Migrar para PostgreSQL usando DATABASE_URL

### Porta não especificada
- Heroku/Railway fornece a porta via variável `$PORT`
- Procfile já usa `$PORT` automaticamente

## Monitoramento Pós-Deploy

```bash
# Heroku: ver logs em tempo real
heroku logs --tail

# Heroku: verificar status da aplicação
heroku status

# Heroku: escalar dynos (aumentar poder)
heroku dyno:resize standard-1x
```

## Próximas Melhorias

- [ ] Adicionar migrations com Alembic/Flask-Migrate
- [ ] Configurar email para recuperação de senha
- [ ] Adicionar autenticação de usuários
- [ ] Implementar CI/CD com GitHub Actions
- [ ] Adicionar logging estruturado
- [ ] Backup automático do banco de dados
