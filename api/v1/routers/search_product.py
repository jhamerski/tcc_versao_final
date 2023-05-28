from fastapi import APIRouter
from api.v1.repositories.search_product_repository import SearchProductRepository


router = APIRouter()


@router.get("/{text}")
async def search_product(text: str, page: int = 1, page_size: int = 10):
    """
    Endpoint para buscar produtos com base no termo de pesquisa.

    Args:
        text (str): Termo de pesquisa.
        page (int, opcional): Número da página de resultados. O padrão é 1.
        page_size (int, opcional): Tamanho da página de resultados. O padrão é 10.

    Returns:
        dict: Resultados da pesquisa em formato de dicionário.
    """
    search_product_repository = SearchProductRepository()
    return await search_product_repository.search_product(text, page, page_size)
