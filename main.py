from fastapi import  FastAPI
from api.v1.api import api_router
from core.config import settings

# Criação da instância do aplicativo FastAPI
app = FastAPI(description=settings.DESCRIPTION, title=settings.TITLE)


# Inclusão do roteador da API
app.include_router(router=api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    import uvicorn

    # Execução do servidor Uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000,
                log_level='info', reload=True)
