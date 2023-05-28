from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile
from core.security import user_authorized
from api.v1.repositories.data_load_repository import DataLoadRepository


router = APIRouter()


@router.post("/")
async def data_load(user_authorized: Annotated[str, Depends(user_authorized)], file: UploadFile):
    """
    Endpoint para carregar e processar os dados de um arquivo JSON.

    Args:
        user_authorized (str): Usuário autorizado para acessar a rota.
        file (UploadFile): Arquivo a ser processado.

    Returns:
        dict: Detalhes da operação de upload de dados.
    """
    data_load_repository = DataLoadRepository(file)
    return await data_load_repository.process_data_load()
