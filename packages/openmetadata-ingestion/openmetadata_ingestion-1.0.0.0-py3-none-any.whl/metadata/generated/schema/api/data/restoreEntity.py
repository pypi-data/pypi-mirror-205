# generated by datamodel-codegen:
#   filename:  api/data/restoreEntity.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from pydantic import BaseModel, Extra, Field

from ...type import basic


class RestoreEntity(BaseModel):
    class Config:
        extra = Extra.forbid

    id: basic.Uuid = Field(
        ..., description='Unique identifier that identifies an entity instance.'
    )
