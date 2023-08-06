from pydantic import BaseModel
from typing import Optional


class RegionsParams(BaseModel):
    """
    Attributes:
        nom:
        code:
        limit:
    """
    nom: Optional[str]
    code: Optional[str]
    limit: Optional[int]


class RegionCodeParams(BaseModel):
    """
    Attributes:
        code:
        limit:
    """
    code: Optional[str]
    limit: Optional[int]


class RegionsResponse(BaseModel):
    """
    Attributes:
        nom:
        code:
        _score:
    """
    nom: str
    code: int
    _score: Optional[float]
