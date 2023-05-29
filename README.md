# <h1 align="center">TCC 2022/2023 - Web scraping para detecção das oportunidades de compra em e-commerce</h1>

![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=CONCLUIDO&color=GREEN&style=for-the-badge)

Este projeto consiste na implementação de um web scraping voltado para a detecção de oportunidades de compra em e-commerce. O objetivo principal é coletar dados do Mercado Livre de forma automatizada e disponibilizar informações relevantes sobre estes produtos/ofertas. Essas informações podem ser usadas de diferentes maneiras, permitindo aos usuários encontrar oportunidades de compra.

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
2. Acesse os endpoints da API através do endereço:
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
├── indisponiveis.py
├── install_scrapy.txt
├── main.py
├── requirements.txt
└── ws_tcc.py
```
---
# :hammer: Funcionalidades do projeto

- `Funcionalidade 1`: Consultar quantidades de monitoramentos realizados pelo Web Scraping.
- `Funcionalidade 2`: Adicionar novo produto/oferta.
- `Funcionalidade 3`: Histórico referente variações de valores dos produtos/ofertas.
- `Funcionalidade 4`: Verificar último valor do produto/oferta e quando ocorreu a última consulta realizada.
- `Funcionalidade 5`: Consultar produtos/ofertas indisponíveis.

---
## ✔️ Tecnologias utilizadas

- ``Virtual Private Server (VPS) - Linux``
- ``Python``
- ``MongoDB``
- ``FastAPI``
- ``Framework Scrapy``

---
## 📁 Acesso ao projeto
Você pode acessar os endpoints clicando [aqui](https://tcc.devja.com.br/docs).

---
### Autor

<a href="https://jonas.devja.com.br/">
 <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/43897983?v=4" width="100px;" alt=""/>
 <br />
<sub><b>Jonas Hamerski</b></sub></a> 🚀

[![Linkedin Badge](https://img.shields.io/badge/-Jonas-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/jonas-hamerski-975552184/)](https://www.linkedin.com/in/jonas-hamerski-975552184/) 
[![Gmail Badge](https://img.shields.io/badge/-jonashamerski87@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:jonashamerski87@gmail.com)](mailto:jonashamerski87@gmail.com)
