from fastapi import APIRouter
from api.v1.repositories.create_url_repository import CreateUrlRepository
from models.url_model import UrlIn


router = APIRouter()


@router.post("/")
async def create_url(urlin: UrlIn):
    """
    Endpoint para criar uma nova URL de produto/oferta.

    Args:
        urlin (UrlIn): Objeto contendo as informações da URL a ser criada.

    Returns:
        Um dicionário com a mensagem de sucesso em caso de cadastro bem-sucedido.

    Raises:
        HTTPException: Exceção lançada quando ocorre um erro durante o cadastro da URL.
    """
    create_url_repository = CreateUrlRepository()
    return await create_url_repository.add_url(urlin.link)
