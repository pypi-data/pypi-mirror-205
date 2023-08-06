# generated by datamodel-codegen:
#   filename:  tests/testDefinition.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from ..entity.data import table
from ..type import basic, entityHistory, entityReference


class TestPlatform(Enum):
    OpenMetadata = 'OpenMetadata'
    GreatExpectations = 'GreatExpectations'
    DBT = 'DBT'
    Deequ = 'Deequ'
    Soda = 'Soda'
    Other = 'Other'


class TestDataType(Enum):
    NUMBER = 'NUMBER'
    INT = 'INT'
    FLOAT = 'FLOAT'
    DOUBLE = 'DOUBLE'
    DECIMAL = 'DECIMAL'
    TIMESTAMP = 'TIMESTAMP'
    TIME = 'TIME'
    DATE = 'DATE'
    DATETIME = 'DATETIME'
    ARRAY = 'ARRAY'
    MAP = 'MAP'
    SET = 'SET'
    STRING = 'STRING'
    BOOLEAN = 'BOOLEAN'


class EntityType(Enum):
    TABLE = 'TABLE'
    COLUMN = 'COLUMN'


class TestCaseParameterDefinition(BaseModel):
    name: Optional[str] = Field(None, description='name of the parameter.')
    displayName: Optional[str] = Field(
        None, description='Display Name that identifies this parameter name.'
    )
    dataType: Optional[TestDataType] = Field(
        None, description='Data type of the parameter (int, date etc.).'
    )
    description: Optional[basic.Markdown] = Field(
        None, description='Description of the parameter.'
    )
    required: Optional[bool] = Field(False, description='Is this parameter required.')


class TestDefinition(BaseModel):
    class Config:
        extra = Extra.forbid

    id: Optional[basic.Uuid] = Field(
        None, description='Unique identifier of this test case definition instance.'
    )
    name: basic.EntityName = Field(
        ..., description='Name that identifies this test case.'
    )
    displayName: Optional[str] = Field(
        None, description='Display Name that identifies this test case.'
    )
    fullyQualifiedName: Optional[basic.FullyQualifiedEntityName] = Field(
        None, description='FullyQualifiedName same as `name`.'
    )
    description: basic.Markdown = Field(..., description='Description of the testcase.')
    entityType: Optional[EntityType] = None
    testPlatforms: List[TestPlatform]
    supportedDataTypes: Optional[List[table.DataType]] = None
    parameterDefinition: Optional[List[TestCaseParameterDefinition]] = None
    owner: Optional[entityReference.EntityReference] = Field(
        None, description='Owner of this TestCase definition.'
    )
    version: Optional[entityHistory.EntityVersion] = Field(
        None, description='Metadata version of the entity.'
    )
    updatedAt: Optional[basic.Timestamp] = Field(
        None,
        description='Last update time corresponding to the new version of the entity in Unix epoch time milliseconds.',
    )
    updatedBy: Optional[str] = Field(None, description='User who made the update.')
    href: Optional[basic.Href] = Field(
        None, description='Link to the resource corresponding to this entity.'
    )
    changeDescription: Optional[entityHistory.ChangeDescription] = Field(
        None, description='Change that lead to this version of the entity.'
    )
    deleted: Optional[bool] = Field(
        False, description='When `true` indicates the entity has been soft deleted.'
    )
