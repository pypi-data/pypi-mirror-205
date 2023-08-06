# generated by datamodel-codegen:
#   filename:  dataInsight/type/totalEntitiesByType.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra, Field, confloat

from ...type import basic


class TotalEntitiesByType(BaseModel):
    class Config:
        extra = Extra.forbid

    timestamp: Optional[basic.Timestamp] = Field(None, description='timestamp')
    entityType: Optional[str] = Field(
        None, description='Type of entity. Derived from the entity class.'
    )
    entityCount: Optional[float] = Field(
        None, description='Total count of entity for the given entity type'
    )
    entityCountFraction: Optional[confloat(ge=0.0, le=1.0)] = Field(
        None, description='Total count of entity for the given entity type'
    )
