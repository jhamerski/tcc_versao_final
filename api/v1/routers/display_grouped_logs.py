from fastapi import APIRouter
from api.v1.repositories.display_grouped_logs_repository import DisplayGroupedLogsRepository


router = APIRouter()


@router.get("/")
async def display_grouped_logs(search_query: str = ""):
    """
    Endpoint para exibir logs agrupados.

    Args:
        search_query (str): A consulta de pesquisa para filtrar os logs.

    Returns:
        list: Uma lista contendo os logs agrupados de acordo com o critério especificado.
    """
    display_grouped_logs_repository = DisplayGroupedLogsRepository()
    return await display_grouped_logs_repository.get_urls(search_query)
