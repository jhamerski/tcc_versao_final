from core.db_connection import DatabaseConnection


class SumSearchRepository:
    """
    Classe que representa um repositório para realizar somas em pesquisas.
    """
    
    @staticmethod
    async def get_aggregate_result(cursor):
        """
        Obtém os resultados da agregação a partir do cursor.

        Args:
            cursor: Cursor do MongoDB.

        Returns:
            Uma lista contendo os documentos resultantes da agregação.
        """
        results = []
        async for document in cursor:
            results.append(document)
        return results


    async def sum_search(self):
        """
        Realiza a soma das consultas realizadas.

        Returns:
            Um dicionário contendo o número total de consultas realizadas.
        """
        pipeline = [
            {"$group": {"_id": None, "total": {"$sum": "$qtd_consultas"}}}
        ]

        connection = DatabaseConnection()
        db = connection.get_database()
        urls_collection = db['url']

        try:
            cursor = urls_collection.aggregate(pipeline)
            result = await cursor.to_list(length=None)
            consultas_realizadas = result[0]['total'] if result else 0

            return {"consultas_realizadas": consultas_realizadas}
        finally:
            connection.close()
