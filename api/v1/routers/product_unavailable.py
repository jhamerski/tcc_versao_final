from fastapi import APIRouter
from api.v1.repositories.product_unavailable_repository import ProductUnavailableRepository


router = APIRouter()


@router.get("/")
async def product_unavailable(qtd_error: int):
    """
    Endpoint para obter produtos indisponíveis no banco de dados.

    Parâmetros:
    - qtd_error (int): Quantidade mínima de produtos com error_monitoramento.

    Retorna uma lista de produtos indisponíveis.

    Exemplo de uso:
    - GET /?qtd_error=5
    - Retorna uma lista com os produtos indisponíveis cujo "error_monitoramento" é maior que 5.
    """
    product_unavailable_repository = ProductUnavailableRepository()
    return await product_unavailable_repository.search_products(qtd_error)
