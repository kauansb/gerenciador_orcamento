# 🚀 Guia Oficial de Deploy - Gerenciador de Orçamento (CloudPanel + Ubuntu)

Este guia descreve o processo **correto e testado** para implantar a aplicação Flask "Gerenciador de Orçamento" em um servidor VPS Hostinger rodando Ubuntu 22.04/24.04 com CloudPanel.

## 📋 Pré-requisitos
1.  VPS com CloudPanel instalado e acessível.
2.  Subdomínio (ex: `apppython.versatilti.com.br`) apontado para o IP da VPS.
3.  Acesso SSH `root` ou usuário sudo.

> 💡 **Por que usar subdomínio?** Se o domínio principal (`www.versatilti.com.br`) já está em uso em outro plano (ex: Hostinger Business com PHP), usar um subdomínio permite manter ambos funcionando independentemente.

### 🌐 Configurar DNS do Subdomínio (hPanel Hostinger)
1. Acesse o **hPanel da Hostinger** → **Domínios** → `versatilti.com.br` → **DNS Zone**.
2. Adicione um novo registro **A**:
   - **Tipo**: A
   - **Nome**: `apppython` (isso criará `apppython.versatilti.com.br`)
   - **Aponta para**: IP da sua VPS CloudPanel (ex: `123.456.789.0`)
   - **TTL**: 14400 (ou padrão)
3. Clique em **Adicionar Registro**.
4. Aguarde a propagação DNS (geralmente 5-15 minutos, máximo 24h).
5. Verifique com: `ping apppython.versatilti.com.br`

---

## 🏗️ Passo 1: Criar o Site no CloudPanel

Isso criará automaticamente o usuário do sistema, diretórios e certificados SSL.

1.  Acesse o painel administrativo do CloudPanel (ex: `https://seu-ip:8443`).
2.  Vá em **Sites** → **Add Site**.
3.  Escolha **Create Python Site** (ou *Node.js Site* se Python não estiver listado; o importante é criar o contêiner do site).
4.  Preencha:
    *   **Domain Name**: `apppython.versatilti.com.br`
    *   **Node.js/Python Version**: Selecione a versão mais recente (ex: Python 3.10+).
    *   **App Port**: `5000` (Isso é importante! O CloudPanel já vai preparar o proxy reverso para esta porta).
5.  **Create User**: Anote o usuário criado (ex: `apppython`) e a senha.
6.  **Site User Password**: Defina uma senha.
7.  Clique em **Create**.

### 🔐 Passo 1.1: Ativar SSL (Let's Encrypt)
*Imediatamente após criar o site:*
1.  No CloudPanel, clique no domínio criado (`apppython.versatilti.com.br`).
2.  Vá na aba **SSL/TLS**.
3.  Clique em **Actions** → **New Let's Encrypt Certificate**.
4.  Clique em **Create and Install**.
    *   *Nota: Isso garante que os certificados existam antes de qualquer alteração manual no Nginx.*

---

## 💻 Passo 2: Configurar a Aplicação via SSH

Acesse o servidor via SSH com o usuário criado pelo CloudPanel (ou root e troque para o usuário).

```bash
# Se estiver como root:
su - versatilti
```

### 2.1 Clonar o Repositório
O CloudPanel cria a pasta raiz em `/home/versatilti/htdocs/gerenciador_orcamento`.

```bash
cd /home/versatilti/htdocs/gerenciador_orcamento
# Remova arquivos padrões se houver
rm -rf * 

# Clone seu projeto (use . para clonar na pasta atual)
git clone https://github.com/SEU_USUARIO/gerenciador_orcamento.git .
```

### 2.2 Configurar Ambiente Virtual
```bash
# Criar venv
python3 -m venv venv

# Ativar e instalar dependências
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn  # Garantir que gunicorn está instalado
```

### 2.3 Configurar Variáveis de Ambiente
Crie o arquivo `.env`:
```bash
nano .env
```
Conteúdo recomendado (usando SQLite para maior estabilidade):
```env
# Gere uma chave segura: python3 -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=SuaChaveSuperSecretaAqui
FLASK_ENV=production
FLASK_DEBUG=False
# DATABASE_URL omitida para usar SQLite padrão (instance/orcamento.db)
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
```

### 2.4 Inicializar o Banco de Dados
```bash
# A aplicação cria o banco automaticamente na primeira execução,
# mas podemos forçar a criação para testar:
export FLASK_APP=run.py
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```
*Verifique se o arquivo `instance/orcamento.db` foi criado.*

---

## ⚙️ Passo 3: Configurar o Serviço Systemd (Gunicorn)

Precisamos de um processo que mantenha o site rodando. Crie um serviço systemd. **Execute como ROOT ou use sudo.**

```bash
exit # Volte para root se estava logado como usuário do site
sudo nano /etc/systemd/system/orcamento.service
```

Cole o conteúdo abaixo (ajuste o USER e CAMINHOS conforme o nome do seu site/usuário):

```ini
[Unit]
Description=Gunicorn instance directly serving Flask
After=network.target

[Service]
# SUBSTITUA 'versatilti' PELO NOME DO USUÁRIO CRIADO NO CLOUDPANEL
User=versatilti
Group=versatilti

# SUBSTITUA PELO CAMINHO CORRETO
WorkingDirectory=/home/versatilti/htdocs/gerenciador_orcamento
Environment="PATH=/home/versatilti/htdocs/gerenciador_orcamento/venv/bin"
EnvironmentFile=/home/versatilti/htdocs/gerenciador_orcamento/.env

# Comando de execução
ExecStart=/home/versatilti/htdocs/gerenciador_orcamento/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:5000 \
    wsgi:app

Restart=always

[Install]
WantedBy=multi-user.target
```

Ative o serviço:
```bash
sudo systemctl daemon-reload
sudo systemctl enable orcamento
sudo systemctl start orcamento
sudo systemctl status orcamento
```
*Deve aparecer como "active (running)".* 🟢

---

## 🌐 Passo 4: Ajustar Proxy Reverso (Nginx)

Se você selecionou "App Port: 5000" na criação do site Python, o CloudPanel já configurou o básico. No entanto, para garantir que arquivos estáticos e configurações de segurança estejam corretas, vamos verificar.

1.  Volte ao CloudPanel.
2.  Clique no seu site → Aba **VHost**.
3.  Verifique se a configuração `location /` se parece com esta. Se não, edite:

```nginx
server {
    listen 80;
    listen [::]:80;
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    {{ssl_certificate_key}}
    {{ssl_certificate}}
    server_name apppython.versatilti.com.br;
    {{root}}

    {{nginx_access_log}}
    {{nginx_error_log}}

    if ($scheme != "https") {
        rewrite ^ https://$host$uri permanent;
    }

    # Servir arquivos estáticos diretamente (melhor performance)
    location /static/ {
        alias /home/versatilti/htdocs/gerenciador_orcamento/app/static/;
        expires 30d;
    }

    # Proxy reverso para o Gunicorn
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
4.  Clique em **Save**.

*Nota: Se o Nginx falhar ao salvar, verifique se os certificados SSL (passo 1.1) foram gerados corretamente.*

---

## ✅ Passo 5: Verificação Final

1.  Acesse `https://apppython.versatilti.com.br` no navegador.
2.  Você deve ver a tela de login/dashboard do Gerenciador de Orçamento.

### Troubleshooting (Resolução de Problemas)

#### Nginx Erro 502 Bad Gateway
Significa que o Nginx não consegue falar com o Gunicorn.
1.  Verifique se o Gunicorn está rodando:
    `sudo systemctl status orcamento`
2.  Veja os logs do serviço:
    `sudo journalctl -u orcamento -f`
3.  Teste conexão local:
    `curl http://127.0.0.1:5000`

#### Erro de Permissão (403 Forbidden)
Verifique se o usuário `versatilti` é dono dos arquivos:
`chown -R versatilti:versatilti /home/versatilti/htdocs/gerenciador_orcamento`

#### Banco de Dados Read-Only
Se usar SQLite, o arquivo e a pasta `instance` precisam de permissão de escrita:
`chmod 775 /home/versatilti/htdocs/gerenciador_orcamento/instance`
`chown versatilti:versatilti /home/versatilti/htdocs/gerenciador_orcamento/instance/orcamento.db`
