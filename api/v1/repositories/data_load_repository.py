from datetime import datetime
import json
import logging
import os
import tempfile
from fastapi import HTTPException
from pymongo import InsertOne
from core.db_connection import DatabaseConnection


class DataLoadRepository:
    """
    Classe que representa um repositório para carregar dados a partir de um arquivo.
    """
    
    def __init__(self, file):
        """
        Construtor da classe DataLoadRepository.

        Args:
            file (str): O arquivo a ser carregado.
        """
        self.file = file
        self.batch_size = 500


    @staticmethod
    def configure_logger():
        """
        Configura o logger para registrar mensagens de log.
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('data_load.log')  # Nome do arquivo de log
            ]
        )


    @staticmethod
    def write_log(log_message):
        """
        Registra uma mensagem de log.

        Args:
            log_message (str): Mensagem de log a ser registrada.
        """
        logger = logging.getLogger('data_load')
        logger.info(log_message)


    @staticmethod
    async def batch_insert(collection, batch_size, data):
        """
        Insere os documentos em lote na coleção especificada.

        Args:
            collection: Coleção do banco de dados onde os documentos serão inseridos.
            batch_size (int): Tamanho do lote de inserção.
            data: Dados a serem inseridos.
        """
        requests = []
        for doc in data:
            doc['data_cadastro'] = datetime.now()
            requests.append(InsertOne(doc))

        num_docs = len(requests)
        num_batches = (num_docs // batch_size) + 1

        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = (i + 1) * batch_size
            batch_requests = requests[start_idx:end_idx]

            if batch_requests:
                collection.bulk_write(batch_requests)


    async def process_data_load(self):
        """
        Processa o carregamento de dados.

        Returns:
            dict: Dicionário contendo a mensagem de sucesso do carregamento.

        Raises:
            HTTPException: Exceção lançada quando ocorre um erro durante o carregamento de dados.
        """
        if not self.file:
            return {"message": "No file sent"}

        # Verificar se o arquivo tem a extensão .json
        if not self.file.filename.endswith('.json'):
            raise HTTPException(status_code=400, detail='.json required')

        temp_file_path = await self.save_temp_file()
        links = await self.load_json_data(temp_file_path)
        await self.insert_data(links)
        await self.clean_up(temp_file_path)

        return {'detail': 'Data uploaded successfully'}


    async def save_temp_file(self) -> str:
        """
        Salva o arquivo temporário no disco.

        Returns:
            str: Caminho do arquivo temporário salvo.

        Raises:
            HTTPException: Exceção lançada quando ocorre um erro ao salvar o arquivo temporário.
        """
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            temp_file.write(await self.file.read())
            temp_file.close()
            return temp_file.name
        except:
            os.remove(temp_file.name)
            raise


    async def load_json_data(self, file_path: str):
        """
        Carrega os dados do arquivo JSON.

        Args:
            file_path (str): Caminho do arquivo JSON.

        Returns:
            list: Dados carregados do arquivo JSON.

        Raises:
            HTTPException: Exceção lançada quando ocorre um erro ao carregar os dados do arquivo JSON.
        """
        try:
            with open(file_path) as json_file:
                return json.load(json_file)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail='.json required')


    async def insert_data(self, data):
        """
        Insere os dados na coleção do banco de dados.

        Args:
            data (list): Dados a serem inseridos.

        Raises:
            HTTPException: Exceção lançada quando ocorre um erro durante a inserção dos dados.
        """
        connection = DatabaseConnection()
        db = connection.get_database()
        urls_collection = db['url']
        try:
            DataLoadRepository.configure_logger()
            DataLoadRepository.write_log(f"Start of loading: {datetime.now()}")

            await self.batch_insert(urls_collection, self.batch_size, data)

            DataLoadRepository.write_log(f"End of loading: {datetime.now()}")
        except Exception as e:
            self.write_log(f"Error: {str(e)}")
            raise HTTPException(status_code=500, detail='Error')
        finally:
            connection.close()


    async def clean_up(self, file_path: str):
        """
        Realiza a limpeza de recursos após o processamento.

        Args:
            file_path (str): Caminho do arquivo a ser removido.
        """
        if os.path.exists(file_path):
            os.remove(file_path)
