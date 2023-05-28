from core.db_connection import DatabaseConnection

class DisplayGroupedLogsRepository:
    """
    Classe que representa um repositório para exibir logs agrupados.
    """

    async def get_urls(self, search_query):
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
            url_log_collection = db['url_log']
            pipeline = [
                {"$match": {"url": {"$regex": search_query, "$options": "i"}}},
                {"$group": {"_id": "$url", "logs": {"$push": {"valor_atual": "$valor_atual", "data_registro": "$data_registro"}}}}
            ]

            cursor = url_log_collection.aggregate(pipeline)
            results = await cursor.to_list(length=None)

            response = []
            for group in results:
                url = group["_id"]
                logs = group["logs"]

                displayed_values = set()  # Conjunto para armazenar os valores já exibidos

                url_logs = []
                for log in logs:
                    valor_atual = log["valor_atual"]
                    data_registro = log["data_registro"]

                    # Verifica se o valor atual não é nulo e se ainda não foi exibido anteriormente
                    if valor_atual is not None and valor_atual not in displayed_values:
                        url_logs.append({"valor_atual": valor_atual, "data_registro": data_registro})

                        # Adiciona o valor atual ao conjunto de valores exibidos
                        displayed_values.add(valor_atual)

                response.append({"url": url, "logs": url_logs})
        finally:
            connection.close()

        return response