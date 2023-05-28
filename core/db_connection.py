from urllib.parse import quote_plus
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

class DatabaseConnection:
    """
    Classe que representa uma conexão com o banco de dados MongoDB.
    """

    def __init__(self):
        self.db = None
        self.client = None

    def connect(self):
        """
        Estabelece a conexão com o banco de dados MongoDB.
        """

        # Formata as credenciais para serem adicionadas no URI
        formatted_username = quote_plus(settings.MONGODB_USERNAME)
        formatted_password = quote_plus(settings.MONGODB_PASSWORD)
        formatted_host = quote_plus(settings.MONGODB_HOST)

        # Define o URI de conexão com autenticação
        uri = f"mongodb://{formatted_username}:{formatted_password}@{formatted_host}/{settings.MONGODB_DB}"

        client = AsyncIOMotorClient(uri)
        self.db = client.get_database(f'{settings.MONGODB_DB}')

    def get_database(self):
        """
        Obtém o objeto de banco de dados.

        Returns:
            Database: O objeto de banco de dados.
        """
        if not self.db:
            self.connect()
        return self.db
    
    def close(self):
        """
        Fecha a conexão com o banco de dados.
        """
        if self.client:
            self.client.close()
