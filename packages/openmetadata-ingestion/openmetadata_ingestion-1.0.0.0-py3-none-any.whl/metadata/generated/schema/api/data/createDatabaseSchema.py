# generated by datamodel-codegen:
#   filename:  api/data/createDatabaseSchema.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from ...entity.data import databaseSchema
from ...type import basic, entityReference, tagLabel


class CreateDatabaseSchemaRequest(BaseModel):
    class Config:
        extra = Extra.forbid

    name: databaseSchema.EntityName = Field(
        ..., description='Name that identifies this database schema instance uniquely.'
    )
    displayName: Optional[str] = Field(
        None, description='Display Name that identifies this database schema.'
    )
    description: Optional[basic.Markdown] = Field(
        None,
        description='Description of the schema instance. What it has and how to use it.',
    )
    owner: Optional[entityReference.EntityReference] = Field(
        None, description='Owner of this schema'
    )
    database: basic.FullyQualifiedEntityName = Field(
        ...,
        description='Link to the database fully qualified name where this schema is hosted in',
    )
    tags: Optional[List[tagLabel.TagLabel]] = Field(
        None, description='Tags for this table'
    )
