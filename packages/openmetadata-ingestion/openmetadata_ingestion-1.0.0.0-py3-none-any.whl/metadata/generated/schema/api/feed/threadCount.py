# generated by datamodel-codegen:
#   filename:  api/feed/threadCount.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Extra, Field, conint

from ...type import basic


class EntityLinkThreadCount(BaseModel):
    class Config:
        extra = Extra.forbid

    count: conint(ge=0) = Field(
        ..., description='Count of threads for the given entity link.'
    )
    entityLink: basic.EntityLink


class CountOfThreadsRelatedToAnEntity(BaseModel):
    class Config:
        extra = Extra.forbid

    totalCount: conint(ge=0) = Field(..., description='Total count of all the threads.')
    counts: List[EntityLinkThreadCount] = Field(..., description='')
