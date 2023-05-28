from fastapi import APIRouter
from api.v1.routers import data_load, sum_search, create_url, display_grouped_logs, search_product, product_unavailable

api_router = APIRouter()
"""
Roteador principal da API que agrupa os roteadores das diferentes funcionalidades.
"""

api_router.include_router(
    data_load.router, prefix='/data_load', tags=['Carga Inicial'])

api_router.include_router(
    sum_search.router, prefix='/sum_search', tags=['Solicitações Realizadas'])

api_router.include_router(
    create_url.router, prefix='/create_url', tags=['Adicionar Novo Produto/Oferta'])

api_router.include_router(
    display_grouped_logs.router, prefix='/display_grouped_logs', tags=['Histórico Agrupado de Alterações'])

api_router.include_router(
    search_product.router, prefix='/search_product', tags=['Procurar Produto/Oferta'])

api_router.include_router(
    product_unavailable.router, prefix='/product_unavailable', tags=['Produtos/Ofertas Indisponíveis'])
