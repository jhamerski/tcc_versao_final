from datetime import datetime, timedelta
import re
from bson import ObjectId
from fastapi import HTTPException, status
from core.db_connection import DatabaseConnection


class CreateUrlRepository:
    """
    Classe que representa um repositório para criar URLs no banco de dados.
    """
    
    async def add_url(self, link):
        """
        Adiciona um URL ao banco de dados.

        Args:
            link (str): O URL a ser adicionado.

        Returns:
            dict: Um dicionário contendo a mensagem de sucesso.

        Raises:
            HTTPException: Se o link fornecido for inválido ou já estiver registrado.
        """
        try:
            connection = DatabaseConnection()
            db = connection.get_database()
            url_collection = db['url']

            # Valida o link
            if not re.match(r'^https://produto\.mercadolivre\.com\.br/', link):
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid Link.")

            # Verifica se o link já está cadastrado
            existing_url = await url_collection.find_one({"link": link})
            if existing_url:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Link already registered.")

            # Insere o novo registro
            url_dict = {
                "_id": ObjectId(),
                "link": link,
                "data_cadastro": datetime.utcnow() - timedelta(hours=3),
                "titulo": None,
                "valor_atual": None,
                "ultima_consulta_em": None,
                "quantidade_registro": 0,
                "error": None
            }
            await url_collection.insert_one(url_dict)
            return {"detail": "Product successfully registered."}
        finally:
            connection.close()
        