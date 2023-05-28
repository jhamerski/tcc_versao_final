from pydantic import BaseModel, Field


class UrlIn(BaseModel):
    """
    Classe que representa o modelo de entrada para URLs.
    """

    link: str = Field(..., description="Link do produto e oferta a ser monitorado")

    class Config:
        """
        Configurações adicionais para a classe UrlIn.
        """
        schema_extra = {
            "example": {
                "link": ""
            }
        }
        