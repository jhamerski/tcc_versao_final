from bson import ObjectId
from fastapi import HTTPException, status
from core.db_connection import DatabaseConnection


class ProductUnavailableRepository:
    """
    Classe que representa um repositório para buscar produtos indisponíveis no banco de dados.
    """
    async def search_products(self, qtd_error):
        try:
            connection = DatabaseConnection()
            db = connection.get_database()
            urls_collection = db['url']
            cursor = urls_collection.find(
                {"error_monitoramento": {"$gt": qtd_error}},
                projection={"_id": False}
            )

            urls = []
            cont = 0
            async for url_dict in cursor:
                cont = cont + 1
                print(cont)
                for key, value in url_dict.items():
                    if isinstance(value, ObjectId):
                        url_dict[key] = str(value)
                        cont = cont + 1
                urls.append(url_dict)

            return urls, f"total_indisponiveis: " f"{cont}"
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f'Error {e}')
        finally:
            connection.close()