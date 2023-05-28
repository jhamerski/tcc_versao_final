# TCC 2022-2023 IESGF

Este documento apresenta o protótipo desenvolvido como parte do Trabalho de Conclusão de Curso (TCC) do curso de Ciência da Computação da IESGF, referente ao ano letivo de 2022-2023. O objetivo do protótipo é demonstrar a solução proposta, que consiste em uma API para coleta de dados produtos/ofertas do site Mercado Livre.

## Requisitos
Python versão 3.10.6

## Instalação
1. Clone o repositório para o seu ambiente local:
```shell
git clone https://github.com/jhamerski/tcc_versao_final
```
2. Crie um ambiente virtual usando o virtualenv. No diretório raiz do projeto, execute o seguinte comando no terminal:
```shell
virtualenv venv
```
3. Ative o ambiente virtual. No Linux ou macOS, utilize o comando:
```shell
source venv/bin/activate
```
No Windows, utilize o comando:
```shell
venv\Scripts\activate
```
4. Instale as dependências do projeto. No diretório raiz do projeto, execute o seguinte comando:
```shell
pip install -r requirements.txt
```
---
## Configuração
Antes de executar o projeto, é necessário preencher as variáveis de configuração no arquivo `core/config.py`. Esse arquivo contém as configurações necessárias para o funcionamento do projeto.

---
## Utilização
1.Execute o projeto:
```shell
python main.py
```
2. Acesse os endpoints da API através do endpoint:
```shell
http://localhost:8000/docs
```
---
## Estrutura do Projeto
```shell
project/
├── api/
│   └── v1/
│       ├── repository/
│       │   ├── create_url_repository.py
│       │   └── ...
│       ├── routers/
│       │   ├── create_url.py
│       │   └── ...
│       └── api.py
├── core/
│   ├── config.py
│   ├── db_connection.py
│   └── security.py
├── mercadolivre/
│   └── mercadolivre/
│       └── spiders/
│           └── ml.py
├── models/
│   └── url_model.py
├── configs_ws.txt
├── indisponiveis.py
├── install_scrapy.txt
├── main.py
├── requirements.txt
└── ws_tcc.py
```
