# PrimeBotFramework
Este Pacote foi desenvolvido com o intuito de facilitar e agilizar o desenolvimento de automações com base no _Robot Framework_.
Neste Pacote podese encontrar diversos sistemas e suas implementaçoes.

### Instalação
```ssh
pip install PrimeBotFramework
```

___
## _DeathByCaptcha_

### Usage
```py
from PromeBot.DeathByCaptcha import DeathByCaptcha

token = "MY TOKEN HERE"
h_id  = "H ID FROM WEB PAGE"
url   = "PAGE URL"
dth = DeathByCaptcha(token)
solved = dth.resolveHCaptcha(h_id,url,timeout=30)

print(solved)

```

___
## _Vault_


### Utilização
```py
from PromeBot.Vault import VaultClient

token = "s.WrhdYlmstBXsdNIL2ztsccPF"
vCli = VaultClient(token)
cred = vCli.get_credentials("facebook","secrets")

print(cred)

```
___

## _OData_

### Utilização
#### Conectando ao serviço
```py
from PromeBot.OData import OauthParams,ExchangeGraph

config = OauthParams(
        username      = "<username>",
        password      = "<password>",
        client_id     = "<client_id>",
        client_secret = "<client_secret>",
        tenant_id     = "<tenant_id>",
        user_id       = "<user_id>"
    )
OData = ExchangeGraph(config=config)
```

## CPF CNPJ
```py
set_token(TOKEN))
consulta_cnpj(cnpj) = 
```

#### Enviando email
```py

msg = OData.newMessage()
msg.set_subject("test Subject")
msg.set_body("Text","Esse e um email de teste!")
msg.set_toRecipients(["MyEmail@some.com"])
msg.set_attachments([".../myfile.txt"])
msg.send()
```
#### Pastas
```py
folders = OData.get_folders()
print(folders)
```
#### Lendo Emails de uma pasta
```py
subf  = OData.get_folder_by_path("Teste/subfolder1")
mails = subf.get_mails()
print(mails)
```
#### Lendo Emails nao lidos
```py
#PODE ADCIONAR O PARAMETRO -> top=1 PRA TRAZER SO 1 ITEM
mails  = subf.get_mails(filter="isRead eq true")
print(mails)
```

#### Marcando email como lido
```py
mails[0].set_read(True)
```
___
## _Documents_
### Utilização
#### 
```py
from PrimeBot.Documents import cnpjDigitoVerificador
# ADCIONA OS 2 DIGITOS VERIFICADORES AO FINAL DO CNPJ
cnpj = "XXXXXX0001XX"
cnpj = cnpjDigitoVerificador(cnpj)
print(cnpj)
```
___
## _OData_

___
## _Mongo_

___
## _Elastic_

## _ListenerECS_
# PrimeLogger
Biblioteca que criar um arquivo de log em formato ECS, para sincronização com Filebeat e Elasticsearch, sendo possivel enviar mensagens de logs e KPIS de forma estruturada dentro do Robot Framework.
### Importação e uso com Robot Framework
Exemplo:
```
       *** Settings ***
        Library     Primebot.ListenerECS    elastic_test    C:${/}logs${/}log.json
Uso:
```
Keywords:
    Start Elastic: inicia a conexao com o elastic
        Obs.: Usar keyword após as variáveis de ambiente terem sido carregadas

    Log    Mensagem de Log Customizada    level=INFO
```
## Autores
* Patrick Geovani - patrick.geovani@primecontrol.com.br
* Jones Sabino - jones.sabino@primecontrol.com.br
```



# OracleDB
Biblioteca que conecta a um database Oracle e executa queries.
### Importação e uso com Robot Framework
Exemplo:
```
       *** Settings ***
        Library     Primebot.OracleDB
Uso:
```
Keywords:
    Execute Query: inicia a conexao com o database e realiza a query solicitada
        Parametros: 
                    user
                    password
                    dsn 
                    encoding
                    query:

```
## Autores
* Patrick Geovani - patrick.geovani@primecontrol.com.br
* Fabio Neves -     fabio.neves@primecontrol.com.br
```

# D4Sign
Biblioteca para utilização de endpoints do serviço D4Sign .
### Importação e uso com Robot Framework
Exemplo:
```
       *** Settings ***
        Library     Primebot.D4Sign
Uso:
```
Keywords:
    Set Token: inicia a conexao com o database e realiza a query solicitada
    Consulta Documentos Por Fase:

```
## Autores
* Fabio Neves -     fabio.neves@primecontrol.com.br
```

# B2E
Biblioteca para utilização de endpoints do serviço B2E.
### Importação e uso com Robot Framework
Exemplo:
```
       *** Settings ***
        Library     Primebot.B2E
Uso:
```
Keywords:
    autenticacao: realiza a autentização e retorna o token
    atualizar_parecer_proposta: atualiza o status da proposta
    obter_parecer_proposta: obtem o dicionario de dados da proposta    
```
## Autores
* Fabio Neves -     fabio.neves@primecontrol.com.br
```