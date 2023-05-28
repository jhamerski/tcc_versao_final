from fastapi import APIRouter
from api.v1.repositories.sum_search_repository import SumSearchRepository


router = APIRouter()


@router.get("/")
async def sum_search():
    """
    Endpoint para obter o número total de consultas realizadas.

    Returns:
        Um dicionário contendo o número total de consultas realizadas.
    """
    sum_search_repository = SumSearchRepository()
    return await sum_search_repository.sum_search()
