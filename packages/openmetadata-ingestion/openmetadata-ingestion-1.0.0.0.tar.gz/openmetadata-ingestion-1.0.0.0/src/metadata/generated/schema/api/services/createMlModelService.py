# generated by datamodel-codegen:
#   filename:  api/services/createMlModelService.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from ...entity.services import mlmodelService
from ...type import basic, entityReference, tagLabel


class CreateMlModelServiceRequest(BaseModel):
    class Config:
        extra = Extra.forbid

    name: basic.EntityName = Field(
        ..., description='Name that identifies the this entity instance uniquely'
    )
    displayName: Optional[str] = Field(
        None, description='Display Name that identifies this mlModel service.'
    )
    description: Optional[basic.Markdown] = Field(
        None, description='Description of mlModel service entity.'
    )
    serviceType: mlmodelService.MlModelServiceType
    connection: mlmodelService.MlModelConnection
    tags: Optional[List[tagLabel.TagLabel]] = Field(
        None, description='Tags for this MlModel Service.'
    )
    owner: Optional[entityReference.EntityReference] = Field(
        None, description='Owner of this mlModel service.'
    )
