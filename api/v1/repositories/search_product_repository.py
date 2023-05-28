import re
from bson import ObjectId
from fastapi import HTTPException, status
from core.db_connection import DatabaseConnection


class SearchProductRepository:
    """
    Classe que representa um repositório para buscar produtos no banco de dados.
    """
    
    async def search_product(self, text, page, page_size):
        """
        Realiza a busca por produtos no banco de dados.

        Args:
            text (str): O texto a ser pesquisado.
            page (int): O número da página de resultados.
            page_size (int): O tamanho da página de resultados.

        Returns:
            list: Uma lista de URLs de produtos correspondentes à pesquisa.

        Raises:
            HTTPException: Se ocorrer um erro ao executar a pesquisa.
        """
        connection = DatabaseConnection()
        try:
            db = connection.get_database()
            urls_collection = db['url']
            regex = re.compile(text, re.IGNORECASE)
            skip = (page - 1) * page_size
            cursor = urls_collection.find(
                {
                    "$or": [
                        {"titulo": {"$regex": regex}},
                        {"link": {"$regex": regex}}
                    ]
                },
                projection={"_id": False}
            ).skip(skip).limit(page_size)

            urls = []
            async for url_dict in cursor:
                for key, value in url_dict.items():
                    if isinstance(value, ObjectId):
                        url_dict[key] = str(value)
                urls.append(url_dict)

            return urls
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f'Error {e}')
        finally:
            connection.close()
