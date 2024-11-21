# Projeto: Chão de Fábrica Metalfino

## Introdução
* **Objetivo:** 
    Realizar controle de produção tendo como ponto chave as embalagens que comportam os produtos durante o processo produtivo.
* **Tecnologias:** 
    * Design - Canvas
    * FrontEnd Web - HTML, CSS, JS, BOOTSTRAP
    * BackEnd Web - Python
    * Comunicação Senior - WebServices SOAP
    * Banco de dados - SQL Server (Desenvolvimento), Oracle (Produção)
* **Data de início:** 
    * Levantamento de requisitos - 21/08/2024
    * Planejamento - 22/08/2024
    * Desenvolvimento - 09/10/2024

## Check-List

## Recursos Úteis
* [Web service de autenticação Senior](https://documentacao.senior.com.br/tecnologia/5.10.1/index.htm#web-services/mcwfusers.htm#AuthenticateJAAS)

## Comandos utilitários
* **Descrição:** Criar models de tabelas existentes em banco de forma automática
    * **Comando:** ``python manage.py inspectdb tabela1, tabela2 > models.py``
* **Descrição:** Criar um novo app na aplicação
    * **Comando:** ``python manage.py startapp app``

## Problemas atuais
* **Problema:** Incluir nome do setor na tela
* **Problema:** Incluir turno de trabalho no histórico da embalagem
* **Problema:** Necessário envolver as requisições no java scprit com try catch e tratar o erro

