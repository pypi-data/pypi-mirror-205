from pydantic import BaseModel
from typing import Optional, List


class DepartmentsParams(BaseModel):
    """
    Attributes:
        nom:
        codeRegion:
        code:
        limit:
        fields:

    """
    nom: Optional[str]
    codeRegion: Optional[str]
    code: Optional[str]
    limit: Optional[int]
    fields: Optional[List[str]]


class DepartmentCodeParams(BaseModel):
    """
    Attributes:
        code:
        limit:
        fields:
    """
    code: Optional[str]
    fields: Optional[list]
    limit: Optional[int]


class RegionDepartmentCodeParams(BaseModel):
    """
    Attributes:
        regioncode:
        limit:
    """
    code: Optional[str]
    limit: Optional[int]


class DepartmentsResponse(BaseModel):
    """
    Attributes:
        nom:
        code:
        codeRegion: int
        fields:
        _score:
    """
    nom: str
    code: int
    codeRegion: int
    fields: Optional[list]
    _score: Optional[float]
