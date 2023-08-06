from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class GeoFormat(Enum):
    """
    Attributes:
        type:
        fields:
        format:
    """
    json = "json"
    geojson = "geojson"


class CommunesParams(BaseModel):
    """
    Attributes:
        codePostal:
        lon:
        lat:
        nom:
        boost:
        code:
        siren:
        codeEpci:
        codeDepartement:
        codeRegion:
        zone:
        type:
        fields:
        format:
        geometry:
        limit:

    """
    codePostal: Optional[str]
    lon: Optional[float]
    lat: Optional[float]
    nom: Optional[str]
    boost: Optional[str]
    code: Optional[str]
    siren: Optional[str]
    codeEpci: Optional[str]
    codeDepartement: Optional[str]
    codeRegion: Optional[str]
    zone: Optional[str]
    type: Optional[str]
    fields: Optional[List[str]]
    format: Optional[GeoFormat] = GeoFormat.json
    geometry: Optional[str]
    limit: Optional[int]


class CommuneCodeParams(BaseModel):
    """
    Attributes:
        code:
        limit:
        fields:
        format:
        geometry:
    """
    code: Optional[str]
    fields: Optional[list]
    geometry: Optional[str]
    format: Optional[GeoFormat] = GeoFormat.json
    limit: Optional[int]


class EpcisCodeParams(CommuneCodeParams):
    pass


class DepartmentCommuneCodeParams(CommuneCodeParams):
    pass


class CommunesResponse(BaseModel):
    """
    Attributes:
        nom:
        code:
        codePostaux:
        codeEpci:
        codeDepartement:
        codeRegion:
        population:
        _score:
    """
    nom: str
    code: int
    codePostaux: Optional[List[str]]
    codeEpci: Optional[str]
    codeDepartement: Optional[str]
    codeRegion: Optional[str]
    population: Optional[str]
    _score: Optional[float]
