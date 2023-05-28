class Settings():
    """
    Classe que representa as configurações do aplicativo.
    """
    
    # DB 
    MONGODB_USERNAME = ''
    MONGODB_PASSWORD = ''
    MONGODB_HOST = ''
    MONGODB_LOCALHOST = ''
    MONGODB_DB = ''
    

    # API
    DESCRIPTION = 'Este documento apresenta o protótipo desenvolvido como parte do Trabalho de Conclusão de Curso (TCC) do curso de Ciência da Computação da IESGF, referente ao ano letivo de 2022-2023. O objetivo do protótipo é demonstrar a solução proposta, que consiste em uma API para coleta de dados produtos/ofertas do site Mercado Livre.'
    TITLE='TCC - Jonas Hamerski'

    # SECURITY
    ROUTER_LOGIN = ''
    ROUTER_PWD = ''

    # VERSION PREFIX
    API_V1_STR: str = '/api/v1'

settings: Settings = Settings()
